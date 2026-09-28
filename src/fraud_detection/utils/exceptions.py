class FraudPlatformError(Exception):
    """Base domain exception."""

class DataContractError(FraudPlatformError):
    """Raised when source data violates the required contract."""

class ModelArtifactError(FraudPlatformError):
    """Raised when a model artifact is missing or invalid."""
