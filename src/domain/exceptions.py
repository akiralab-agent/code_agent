class DomainException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class EntityNotFoundException(DomainException):
    def __init__(self, entity: str, identifier: str) -> None:
        super().__init__(f"{entity} with identifier '{identifier}' not found.")


class EntityAlreadyExistsException(DomainException):
    def __init__(self, entity: str, identifier: str) -> None:
        super().__init__(f"{entity} with identifier '{identifier}' already exists.")


class InvalidEntityException(DomainException):
    pass
