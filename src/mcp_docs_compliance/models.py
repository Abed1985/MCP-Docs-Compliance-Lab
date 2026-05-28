from dataclasses import dataclass


@dataclass(frozen=True)
class SupportedUserConfig:
    vendor: str
    version: str
    password_type: str | None
    secret_type: str | None
    supported_password_line: str | None
    supported_secret_line: str | None
    source_url: str | None = None

    def to_dict(self):
        return {
            "vendor": self.vendor,
            "version": self.version,
            "password_type": self.password_type,
            "secret_type": self.secret_type,
            "supported_password_line": self.supported_password_line,
            "supported_secret_line": self.supported_secret_line,
            "source_url": self.source_url,
        }
