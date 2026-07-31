"""Deterministic, platform-neutral response presentation transforms."""

from __future__ import annotations

import copy
import re
from typing import Any


# Inline style for h3 headers
_H3_STYLE = 'style="font-size: 1.17em; font-weight: bold; margin-top: 1em; margin-bottom: 0.5em; line-height: 1.2;"'
# Inline style for h4 headers  
_H4_STYLE = 'style="font-size: 1em; font-weight: bold; margin-top: 0.75em; margin-bottom: 0.5em; line-height: 1.2;"'
# Inline style for h2 headers
_H2_STYLE = 'style="font-size: 1.5em; font-weight: bold; margin-top: 1.2em; margin-bottom: 0.6em; line-height: 1.2;"'

# Inline styles for table elements
_TABLE_STYLE = 'style="border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 0.9em;"'
_TH_STYLE = 'style="border: 1px solid #ddd; padding: 8px; text-align: left; background-color: #f2f2f2; font-weight: bold;"'
_TD_STYLE = 'style="border: 1px solid #ddd; padding: 8px; text-align: left;"'

# Patterns to match markdown headers
_H3_PATTERN = re.compile(r'^### (.+)$', re.MULTILINE)
_H4_PATTERN = re.compile(r'^#### (.+)$', re.MULTILINE)
_H2_PATTERN = re.compile(r'^## (.+)$', re.MULTILINE)

# Pattern to match markdown tables (header row + separator + data rows)
_TABLE_PATTERN = re.compile(
    r'^\|.+\|[ ]*\n'  # Header row (starts with |, ends with |)
    r'\|[-:\s|]+\|[ ]*\n'  # Separator row (|---|---|)
    r'(?:\|.+\|[ ]*\n?)+',  # One or more data rows
    re.MULTILINE
)

# Pattern to match markdown bold text (**text**)
_BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*')

# Pattern to match markdown horizontal rules (--- on its own line)
_HR_PATTERN = re.compile(r'^---[ ]*$', re.MULTILINE)

# Inline style for horizontal rules
_HR_STYLE = 'style="border: 0; border-top: 1px solid #aaa; margin: 1em 0;"'

# Marker to detect if already transformed (hidden in HTML)
_TRANSFORM_MARKER = '<span style="display:none;" data-transformed="true"></span>'


def _convert_table_to_html(match: re.Match) -> str:
    """Convert a markdown table match to HTML with inline styles."""
    table_text = match.group(0).strip()
    lines = [line.strip() for line in table_text.split('\n') if line.strip()]
    
    if len(lines) < 3:  # Need at least header, separator, and one data row
        return match.group(0)  # Return unchanged if malformed
    
    # Parse header row
    header_row = lines[0]
    headers = [cell.strip() for cell in header_row.split('|')[1:-1]]  # Skip first and last empty elements
    
    # Skip separator row (lines[1])
    
    # Parse data rows (lines[2:])
    data_rows = []
    for line in lines[2:]:
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        data_rows.append(cells)
    
    # Build HTML table
    html_parts = [f'<table {_TABLE_STYLE}>']
    
    # Header
    html_parts.append('<thead><tr>')
    for header in headers:
        html_parts.append(f'<th {_TH_STYLE}>{header}</th>')
    html_parts.append('</tr></thead>')
    
    # Body
    html_parts.append('<tbody>')
    for row_cells in data_rows:
        html_parts.append('<tr>')
        for cell in row_cells:
            html_parts.append(f'<td {_TD_STYLE}>{cell}</td>')
        html_parts.append('</tr>')
    html_parts.append('</tbody>')
    
    html_parts.append('</table>')
    
    return ''.join(html_parts)


def transform_content(content: str) -> str:
    """Convert markdown headers, tables, bold text, and horizontal rules to HTML with inline styles.

    Replaces markdown elements with HTML equivalents that have inline styles,
    ensuring proper rendering even if the Vue app strips style blocks:
    - Headers (##, ###, ####) -> <h2>, <h3>, <h4> with inline styles
    - Tables -> <table> with inline styles
    - Bold text (**text**) -> <strong>
    - Horizontal rules (---) -> <hr> with inline styles
    
    This function is idempotent: if the transformation marker is present,
    content is returned unchanged.
    """

    if not isinstance(content, str):
        raise TypeError("content must be a string")
    
    # Check if already transformed (idempotency)
    if _TRANSFORM_MARKER in content:
        return content
    
    # Convert markdown tables to HTML tables
    result = _TABLE_PATTERN.sub(_convert_table_to_html, content)
    
    # Convert markdown horizontal rules (---) to HTML hr tags
    result = _HR_PATTERN.sub(f'<hr {_HR_STYLE}>', result)
    
    # Replace markdown headers with HTML headers with inline styles
    # Do in reverse order (h4, h3, h2) to avoid partial matches
    result = _H4_PATTERN.sub(rf'<h4 {_H4_STYLE}>\1</h4>', result)
    result = _H3_PATTERN.sub(rf'<h3 {_H3_STYLE}>\1</h3>', result)
    result = _H2_PATTERN.sub(rf'<h2 {_H2_STYLE}>\1</h2>', result)
    
    # Convert markdown bold (**text**) to HTML strong tags
    result = _BOLD_PATTERN.sub(r'<strong>\1</strong>', result)
    
    # Add invisible marker for idempotency (at the end to not interfere with rendering)
    return result + _TRANSFORM_MARKER


def transform_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a transformed deep copy while preserving all non-content data."""

    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    transformed = copy.deepcopy(payload)
    content = transformed.get("content")
    if isinstance(content, str):
        transformed["content"] = transform_content(content)
    return transformed
