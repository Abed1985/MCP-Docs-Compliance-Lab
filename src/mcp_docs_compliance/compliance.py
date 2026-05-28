import re


ACTUAL_PASSWORD_PATTERN = re.compile(r"username\s+\S+\s+password(?:\s+(?P<type>\d+))?\s+\S+", re.IGNORECASE)
ACTUAL_SECRET_PATTERN = re.compile(r"username\s+\S+\s+secret(?:\s+(?P<type>\d+))?\s+\S+", re.IGNORECASE)


def _extract_actual(text, pattern):
    for line in text.splitlines():
        cleaned = " ".join(line.strip().split())
        match = pattern.search(cleaned)
        if match:
            return cleaned, match.group("type") or "0"
    return None, None


def check_user_config_compliance(actual_config, supported):
    supported_dict = supported.to_dict() if hasattr(supported, "to_dict") else dict(supported)
    password_line, password_type = _extract_actual(actual_config, ACTUAL_PASSWORD_PATTERN)
    secret_line, secret_type = _extract_actual(actual_config, ACTUAL_SECRET_PATTERN)

    password_expected = supported_dict.get("password_type")
    secret_expected = supported_dict.get("secret_type")
    password_comply = bool(password_type and password_expected and password_type == password_expected)
    secret_comply = bool(secret_type and secret_expected and secret_type == secret_expected)

    return {
        "vendor": supported_dict.get("vendor"),
        "version": supported_dict.get("version"),
        "actual_password_line": password_line,
        "actual_password_type": password_type,
        "actual_secret_line": secret_line,
        "actual_secret_type": secret_type,
        "supported_password_type": password_expected,
        "supported_secret_type": secret_expected,
        "supported_password_line": supported_dict.get("supported_password_line"),
        "supported_secret_line": supported_dict.get("supported_secret_line"),
        "password_comply": password_comply,
        "secret_comply": secret_comply,
        "comply": password_comply or secret_comply,
    }
