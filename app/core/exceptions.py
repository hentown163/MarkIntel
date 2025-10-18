"""Domain and Application exceptions"""

class DomainException(Exception):
    """Base exception for domain layer"""
    pass


class ValidationError(DomainException):
    """Validation failed"""
    pass


class EntityNotFoundError(DomainException):
    """Entity not found in repository"""
    def __init__(self, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id '{entity_id}' not found")


class ApplicationError(Exception):
    """Base exception for application layer"""
    pass


class UseCaseError(ApplicationError):
    """Use case execution failed"""
    pass


class InfrastructureError(Exception):
    """Base exception for infrastructure layer"""
    pass


class RepositoryError(InfrastructureError):
    """Repository operation failed"""
    pass


class ExternalServiceError(InfrastructureError):
    """External service call failed"""
    pass
