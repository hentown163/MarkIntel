"""Signal ID value object"""
from dataclasses import dataclass
from app.core.exceptions import ValidationError


@dataclass(frozen=True)
class SignalId:
    """Immutable signal identifier"""
    value: str
    
    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValidationError("Signal ID must be a non-empty string")
        
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, SignalId):
            return False
        return self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
