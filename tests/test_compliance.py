from mcp_docs_compliance.compliance import check_user_config_compliance
from mcp_docs_compliance.models import SupportedUserConfig


def test_compliance_secret_matches():
    actual = "username netops secret 9 $9$example"
    supported = SupportedUserConfig("cisco", "IOS-XE 17", "5", "9", None, None)
    result = check_user_config_compliance(actual, supported)
    assert result["secret_comply"] is True
    assert result["comply"] is True


def test_compliance_password_mismatch():
    actual = "username netops password 7 000000"
    supported = SupportedUserConfig("cisco", "IOS-XE 17", "5", "9", None, None)
    result = check_user_config_compliance(actual, supported)
    assert result["password_comply"] is False
    assert result["comply"] is False
