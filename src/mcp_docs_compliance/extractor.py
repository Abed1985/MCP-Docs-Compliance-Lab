import re

from .models import SupportedUserConfig


PASSWORD_PATTERN = re.compile(r"username\s+\S+\s+password(?:\s+(?P<type>\d+))?\s+\S+", re.IGNORECASE)
SECRET_PATTERN = re.compile(r"username\s+\S+\s+secret(?:\s+(?P<type>\d+))?\s+\S+", re.IGNORECASE)


def _clean_line(line):
    return " ".join(line.strip().split())


def _first_match(text, pattern):
    for line in text.splitlines():
        cleaned = _clean_line(line)
        match = pattern.search(cleaned)
        if match:
            return cleaned, match.group("type") or "0"
    return None, None


def extract_supported_user_config(text, vendor, version, source_url=None):
    password_line, password_type = _first_match(text, PASSWORD_PATTERN)
    secret_line, secret_type = _first_match(text, SECRET_PATTERN)
    return SupportedUserConfig(
        vendor=vendor,
        version=version,
        password_type=password_type,
        secret_type=secret_type,
        supported_password_line=password_line,
        supported_secret_line=secret_line,
        source_url=source_url,
    )
