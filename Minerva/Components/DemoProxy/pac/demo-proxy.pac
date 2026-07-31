function FindProxyForURL(url, host) {
    var normalizedHost = (host || "").toLowerCase();

    if (normalizedHost === "__TARGET_HOST__") {
        return "PROXY __PROXY_ENDPOINT__; DIRECT";
    }

    return "DIRECT";
}
