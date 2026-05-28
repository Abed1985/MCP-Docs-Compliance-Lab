from mcp_docs_compliance.extractor import extract_supported_user_config


def test_extract_supported_user_config():
    text = """
    username admin password 5 <hashed-password>
    username admin secret 9 <hashed-secret>
    """
    result = extract_supported_user_config(text, "cisco", "IOS-XE 17")
    assert result.password_type == "5"
    assert result.secret_type == "9"
    assert result.supported_password_line == "username admin password 5 <hashed-password>"
