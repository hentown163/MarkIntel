"""Money value object"""
from dataclasses import dataclass
from decimal import Decimal
from app.core.exceptions import ValidationError


@dataclass(frozen=True)
class Money:
    """Immutable money value"""
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if not isinstance(self.amount, (int, float, Decimal)):
            raise ValidationError("Money amount must be numeric")
        if self.amount < 0:
            raise ValidationError("Money amount cannot be negative")
        object.__setattr__(self, 'amount', Decimal(str(self.amount)))
        
    def __str__(self) -> str:
        return f"{self.currency} {self.amount:,.2f}"
    
    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise ValidationError("Can only add Money to Money")
        if self.currency != other.currency:
            raise ValidationError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    def __hash__(self) -> int:
        return hash((self.amount, self.currency))
