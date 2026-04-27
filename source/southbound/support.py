"""
southbound/support.py

All logic for reading remote data files and preparing rows for publishing.
Nothing in this file publishes — it only fetches, decodes, and transforms.

Public API:
    get_files_by_url(url)                          → list[str]
    url_read_content(url, line, is_german)         → dict | list[dict] | None
    calculate_timestamp(row_id, off_set, ...)      → str
"""

import ast
import csv
import datetime
import io
import json
import re
import zoneinfo

import requests
from bs4 import BeautifulSoup


# ─────────────────────────────────────────────
# Internal constants
# ─────────────────────────────────────────────

_TIMESTAMP_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}):\s*(.*)")
_TIMESTAMP_FMT_OUT = "%Y-%m-%dT%H:%M:%S.%fZ"
_TIMESTAMP_FMT_IN  = "%Y-%m-%dT%H:%M:%S.%fZ"


# ─────────────────────────────────────────────
# Directory listing
# ─────────────────────────────────────────────

def get_files_by_url(url: str) -> list[str]:
    """
    Return the list of .csv / .json files available under a directory URL.
    Equivalent to `ls` against the URL.

    :args:
        url:str - base directory URL to scan
    :return:
        list of filenames (not full URLs)
    """
    try:
        response = requests.get(url, timeout=120)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to list files at {url} (Error: {error})")

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a")]
    except Exception as error:
        raise Exception(f"Failed to parse directory listing at {url} (Error: {error})")

    return [link for link in links if link and link.rsplit(".", 1)[-1] in ("csv", "json")]


# ─────────────────────────────────────────────
# Raw line fetch
# ─────────────────────────────────────────────

def _get_file_line(url: str, line_num: int, is_german: bool = False, timeout: float = 120):
    """
    Stream a remote file and return the content of a specific 1-based line.
    Returns None if the line does not exist (file exhausted).

    :args:
        url:str      - full URL of the file
        line_num:int - 1-based line number to fetch
        is_german:bool - use UTF-8-sig encoding (BOM-aware) for German CSV files
        timeout:float  - HTTP timeout in seconds
    :return:
        raw line content (str for JSON lines, dict for CSV rows) or None
    """
    encoding   = "utf-8-sig" if is_german else "utf-8"
    is_csv     = url.endswith(".csv")
    header_row = None

    try:
        with requests.get(url, timeout=timeout, stream=True) as response:
            response.raise_for_status()
            for current_line, raw in enumerate(response.iter_lines(), start=1):
                if is_csv and current_line == 1:
                    header_row = next(csv.reader(io.StringIO(raw.decode(encoding))))

                if current_line == line_num:
                    decoded = raw.decode(encoding)
                    if is_csv:
                        values = next(csv.reader(io.StringIO(decoded)))
                        return dict(zip(header_row, values)) if header_row else decoded
                    return decoded

    except Exception as error:
        raise Exception(f"Failed to fetch line {line_num} from {url} (Error: {error})")

    return None  # line_num beyond end of file


# ─────────────────────────────────────────────
# Format decoders
# ─────────────────────────────────────────────

def _decode_vessel_format(match: re.Match) -> dict:
    """
    Decode lines in the vessel timestamp-prefixed format:
        2026-01-01 00:00:00: '{"key": value, ...}'

    :args:
        match:re.Match - result of _TIMESTAMP_RE.match(line)
    :return:
        dict with all fields plus "timestamp"
    """
    timestamp = match.group(1)
    json_part = match.group(2)

    try:
        content = json.loads(json_part) if not isinstance(json_part, dict) else json_part
        content["timestamp"] = timestamp
        return content
    except Exception as error:
        raise Exception(
            f"Invalid vessel-format content — {timestamp}: {json_part} (Error: {error})"
        )


def _parse_german_number(value):
    """
    Convert a German-locale numeric string to int or float.
    Examples:
        "1.234,56"  → 1234.56
        "42"        → 42
        "text"      → "text"   (unchanged)

    :args:
        value - any value; non-strings are returned as-is
    :return:
        int | float | str
    """
    if not isinstance(value, str):
        return value

    value = value.strip()

    if "," in value and "." in value:
        value = value.replace(".", "").replace(",", ".")
    elif "," in value:
        value = value.replace(",", ".")

    try:
        return ast.literal_eval(value)
    except Exception:
        return value


def _decode_german_content(content) -> dict:
    """
    Parse a German-format JSON row and convert all numeric strings.

    :args:
        content:str|dict - raw content from a German-locale data file
    :return:
        dict with cleaned numeric values
    """
    if isinstance(content, str):
        content = json.loads(content.strip())
    return {key.strip(): _parse_german_number(value) for key, value in content.items()}


def _decode_row(row, url: str = "", is_german: bool = False):
    """
    Route a raw row through the appropriate decoder.

    Handles three formats:
        - Vessel timestamp prefix:  "2026-01-01 00:00:00: '{...}'"
        - German locale CSV/JSON:   comma-decimal numerics
        - Standard JSON string

    :args:
        row        - raw content (str or dict already parsed by CSV reader)
        url:str    - source URL, used only in error messages
        is_german:bool - apply German number parsing
    :return:
        dict | list[dict]
    """
    if isinstance(row, dict):
        # Already parsed by the CSV reader — apply German conversion if needed
        return _decode_german_content(row) if is_german else row

    if isinstance(row, str):
        match = _TIMESTAMP_RE.match(row)
        if match:
            return _decode_vessel_format(match)
        if is_german:
            return _decode_german_content(row)
        try:
            parsed = json.loads(row)
        except Exception as error:
            raise Exception(f"Failed to parse JSON content from {url} (Error: {error})")

        # Recurse to handle lists of rows
        if isinstance(parsed, list):
            return [_decode_row(item, url=url, is_german=is_german) for item in parsed]
        return parsed

    return row


# ─────────────────────────────────────────────
# Public fetch + decode
# ─────────────────────────────────────────────

def url_read_content(url:str, line:int=0, is_german: bool = False):
    """
    Fetch a specific row from a remote file and return it as a decoded dict.

    :args:
        url:str      - full URL of the data file (.csv or .json)
        line:int     - 0-based row index (internally converted to 1-based)
        is_german:bool - apply German locale number parsing
    :return:
        dict | list[dict] | None (None means the file has no more rows)
    """
    raw = _get_file_line(url=url, line_num=line + 1, is_german=is_german)
    if raw is None:
        return None
    return _decode_row(raw, url=url, is_german=is_german)


# ─────────────────────────────────────────────
# Timestamp generation
# ─────────────────────────────────────────────

def calculate_timestamp(
    row_id: int,
    off_set: float,
    current_timestamp: str | datetime.datetime | None = None,
    timezone: datetime.timezone | zoneinfo.ZoneInfo = datetime.timezone.utc,
) -> str:
    """
    Generate a publish timestamp for a data row.

    If current_timestamp is provided, the timestamp is calculated by
    advancing it by (off_set * row_id) seconds, preserving the original
    time series spacing. If not provided, the current wall-clock time is
    used (first row of a new cycle).

    :args:
        row_id:int               - position of this row within the current cycle
        off_set:float            - seconds between consecutive rows
        current_timestamp        - anchor timestamp for the cycle (str or datetime)
        timezone                 - timezone to apply when generating wall-clock time
    :return:
        ISO-8601 timestamp string: "YYYY-MM-DDTHH:MM:SS.ffffffZ"
    """
    if current_timestamp:
        if isinstance(current_timestamp, str):
            current_timestamp = datetime.datetime.strptime(current_timestamp, _TIMESTAMP_FMT_IN)
        timestamp = current_timestamp + datetime.timedelta(seconds=off_set * row_id)
    else:
        timestamp = datetime.datetime.now(tz=timezone)

    return timestamp.strftime(_TIMESTAMP_FMT_OUT)