"""Assemble deterministic, allowlist-only DemoProxy release archives."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import re
import stat
import struct
import tarfile
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Callable, Iterable


_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[.-][A-Za-z0-9]+)*$")
_TARGETS = {
    "windows-x64": ("windows", "x64", ".zip", "mitmdump.exe"),
    "macos-arm64": ("macos", "arm64", ".tar.gz", "mitmdump"),
    "macos-x64": ("macos", "x64", ".tar.gz", "mitmdump"),
}


@dataclass(frozen=True)
class ReleaseTarget:
    name: str
    platform: str
    architecture: str
    archive_suffix: str
    runtime_name: str

    @classmethod
    def from_name(cls, name: str) -> "ReleaseTarget":
        try:
            platform_name, architecture, suffix, runtime_name = _TARGETS[name]
        except KeyError as exc:
            raise ValueError(f"unsupported release target: {name}") from exc
        return cls(name, platform_name, architecture, suffix, runtime_name)


@dataclass(frozen=True)
class _PackageFile:
    path: PurePosixPath
    content: bytes
    mode: int


def validate_runtime_binary(runtime_path: Path, target: ReleaseTarget) -> None:
    """Reject an executable whose binary header does not match its target."""

    try:
        content = runtime_path.read_bytes()
    except OSError as exc:
        raise ValueError(f"runtime is unreadable: {runtime_path}") from exc
    if target.platform == "windows":
        valid = _is_pe_x64(content)
    else:
        cpu_types = _macho_cpu_types(content)
        expected = 0x0100000C if target.architecture == "arm64" else 0x01000007
        valid = expected in cpu_types
    if not valid:
        raise ValueError(
            f"runtime architecture does not match target {target.name}: {runtime_path}"
        )


def assemble_release(
    *,
    source_root: Path,
    target: ReleaseTarget,
    runtime_path: Path,
    licenses_dir: Path,
    output_dir: Path,
    version: str,
    source_date_epoch: int | None = None,
) -> Path:
    """Build one deterministic archive from an explicit safe-file allowlist."""

    if not _VERSION_PATTERN.fullmatch(version):
        raise ValueError(f"unsafe or invalid version: {version!r}")
    source_root = source_root.resolve()
    runtime_path = runtime_path.resolve()
    licenses_dir = licenses_dir.resolve()
    validate_runtime_binary(runtime_path, target)
    if not licenses_dir.is_dir() or not any(licenses_dir.iterdir()):
        raise ValueError("licenses directory must contain release notices")
    epoch = source_date_epoch
    if epoch is None:
        epoch = int(os.environ.get("SOURCE_DATE_EPOCH", "0"))
    if epoch < 0:
        raise ValueError("SOURCE_DATE_EPOCH must not be negative")

    release_name = f"DemoResponseProxy-{version}-{target.name}"
    files = _collect_files(
        source_root=source_root,
        target=target,
        runtime_path=runtime_path,
        licenses_dir=licenses_dir,
        version=version,
    )
    files.append(_manifest_file(files, target=target, version=version))
    files.sort(key=lambda item: item.path.as_posix())
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact = output_dir / f"{release_name}{target.archive_suffix}"
    if target.platform == "windows":
        _write_zip(artifact, release_name, files, epoch)
    else:
        _write_tar_gz(artifact, release_name, files, epoch)
    return artifact


def write_checksums(output_dir: Path) -> Path:
    """Write sorted SHA-256 entries for release archives in output_dir."""

    artifacts = sorted(
        (
            path
            for path in output_dir.iterdir()
            if path.is_file()
            and (path.name.endswith(".zip") or path.name.endswith(".tar.gz"))
        ),
        key=lambda path: path.name,
    )
    if not artifacts:
        raise ValueError(f"no release archives found in {output_dir}")
    lines = [f"{_sha256(path.read_bytes())}  {path.name}" for path in artifacts]
    checksum_path = output_dir / "SHA256SUMS.txt"
    checksum_path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
    return checksum_path


def _collect_files(
    *,
    source_root: Path,
    target: ReleaseTarget,
    runtime_path: Path,
    licenses_dir: Path,
    version: str,
) -> list[_PackageFile]:
    files: list[_PackageFile] = []

    def add_file(source: Path, destination: str, mode: int = 0o644) -> None:
        if not source.is_file() or source.is_symlink():
            raise ValueError(f"required package file is missing or unsafe: {source}")
        files.append(_PackageFile(PurePosixPath(destination), source.read_bytes(), mode))

    def add_tree(
        source: Path,
        destination: str,
        *,
        include: Callable[[Path], bool],
        executable: Callable[[Path], bool] = lambda path: False,
    ) -> None:
        if not source.is_dir() or source.is_symlink():
            raise ValueError(f"required package directory is missing or unsafe: {source}")
        for path in sorted(source.rglob("*")):
            if path.is_symlink() or not path.is_file() or not include(path):
                continue
            relative = path.relative_to(source).as_posix()
            add_file(
                path,
                f"{destination}/{relative}",
                0o755 if executable(path) else 0o644,
            )

    files.append(
        _PackageFile(
            PurePosixPath(f"bin/{target.runtime_name}"),
            runtime_path.read_bytes(),
            0o755,
        )
    )
    sanitized_config = source_root / "config" / "proxy.example.yaml"
    sanitized_lock = source_root / "config" / "demo-lock.example.json"
    add_file(sanitized_config, "config/proxy.yaml")
    add_file(sanitized_config, "config/proxy.example.yaml")
    add_file(sanitized_lock, "config/demo-lock.json")
    add_file(sanitized_lock, "config/demo-lock.example.json")
    add_tree(
        source_root / "proxy",
        "proxy",
        include=lambda path: path.suffix == ".py" and "__pycache__" not in path.parts,
    )
    add_file(source_root / "pac" / "demo-proxy.pac", "pac/demo-proxy.pac")
    add_tree(
        source_root / "scripts" / "common",
        "scripts/common",
        include=lambda path: path.suffix == ".py",
        executable=lambda path: path.name == "verify_config.py",
    )
    add_tree(
        source_root / "scripts" / target.platform,
        f"scripts/{target.platform}",
        include=lambda path: path.suffix in {".sh", ".ps1"},
        executable=lambda path: path.suffix == ".sh",
    )
    add_tree(
        source_root / "startup" / target.platform,
        f"startup/{target.platform}",
        include=lambda path: path.suffix in {".plist", ".xml"},
    )
    add_file(source_root / "README.md", "README.md")
    add_file(source_root / "DEMO_RUNBOOK.md", "DEMO_RUNBOOK.md")
    files.append(_PackageFile(PurePosixPath("VERSION"), f"{version}\n".encode(), 0o644))
    add_tree(
        licenses_dir,
        "LICENSES",
        include=lambda path: True,
    )
    return files


def _manifest_file(
    files: Iterable[_PackageFile], *, target: ReleaseTarget, version: str
) -> _PackageFile:
    manifest = {
        "files": {
            item.path.as_posix(): _sha256(item.content)
            for item in sorted(files, key=lambda item: item.path.as_posix())
        },
        "formatVersion": 1,
        "target": target.name,
        "version": version,
    }
    content = json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    return _PackageFile(PurePosixPath("MANIFEST.json"), content, 0o644)


def _write_zip(
    artifact: Path,
    release_name: str,
    files: list[_PackageFile],
    epoch: int,
) -> None:
    timestamp = max(epoch, 315532800)  # ZIP timestamps cannot predate 1980.
    date_time = time.gmtime(timestamp)[:6]
    with zipfile.ZipFile(
        artifact, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for directory in _directories(files):
            info = zipfile.ZipInfo(f"{release_name}/{directory}/", date_time)
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = (stat.S_IFDIR | 0o755) << 16
            archive.writestr(info, b"")
        for item in files:
            info = zipfile.ZipInfo(
                f"{release_name}/{item.path.as_posix()}", date_time
            )
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | item.mode) << 16
            archive.writestr(info, item.content)


def _write_tar_gz(
    artifact: Path,
    release_name: str,
    files: list[_PackageFile],
    epoch: int,
) -> None:
    with artifact.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=epoch) as compressed:
            with tarfile.open(
                fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT
            ) as archive:
                for directory in _directories(files):
                    info = _tar_info(f"{release_name}/{directory}", 0o755, epoch)
                    info.type = tarfile.DIRTYPE
                    archive.addfile(info)
                for item in files:
                    info = _tar_info(
                        f"{release_name}/{item.path.as_posix()}", item.mode, epoch
                    )
                    info.size = len(item.content)
                    archive.addfile(info, fileobj=_BytesReader(item.content))


def _directories(files: Iterable[_PackageFile]) -> list[str]:
    directories: set[str] = set()
    for item in files:
        parent = item.path.parent
        while parent != PurePosixPath("."):
            directories.add(parent.as_posix())
            parent = parent.parent
    return sorted(directories)


def _tar_info(name: str, mode: int, epoch: int) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.mode = mode
    info.mtime = epoch
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    return info


class _BytesReader:
    def __init__(self, content: bytes) -> None:
        self._content = content
        self._offset = 0

    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = len(self._content) - self._offset
        result = self._content[self._offset : self._offset + size]
        self._offset += len(result)
        return result


def _is_pe_x64(content: bytes) -> bool:
    if len(content) < 0x40 or content[:2] != b"MZ":
        return False
    pe_offset = struct.unpack_from("<I", content, 0x3C)[0]
    return (
        pe_offset + 6 <= len(content)
        and content[pe_offset : pe_offset + 4] == b"PE\0\0"
        and struct.unpack_from("<H", content, pe_offset + 4)[0] == 0x8664
    )


def _macho_cpu_types(content: bytes) -> set[int]:
    if len(content) < 8:
        return set()
    magic = content[:4]
    if magic == b"\xcf\xfa\xed\xfe":
        return {struct.unpack_from("<I", content, 4)[0]}
    if magic == b"\xfe\xed\xfa\xcf":
        return {struct.unpack_from(">I", content, 4)[0]}
    if magic not in {b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf"}:
        return set()
    is_64 = magic == b"\xca\xfe\xba\xbf"
    count = struct.unpack_from(">I", content, 4)[0]
    entry_size = 32 if is_64 else 20
    result: set[int] = set()
    for index in range(count):
        offset = 8 + index * entry_size
        if offset + 4 > len(content):
            return set()
        result.add(struct.unpack_from(">I", content, offset)[0])
    return result


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=sorted(_TARGETS), required=True)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--licenses", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--source-root", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--version", default=(Path(__file__).parents[1] / "VERSION").read_text().strip())
    args = parser.parse_args()
    artifact = assemble_release(
        source_root=args.source_root,
        target=ReleaseTarget.from_name(args.target),
        runtime_path=args.runtime,
        licenses_dir=args.licenses,
        output_dir=args.output_dir,
        version=args.version,
    )
    checksum = write_checksums(args.output_dir)
    print(json.dumps({"artifact": str(artifact), "checksums": str(checksum)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
