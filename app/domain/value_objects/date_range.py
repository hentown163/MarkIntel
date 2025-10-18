"""Date Range value object"""
from dataclasses import dataclass
from datetime import date, datetime
from app.core.exceptions import ValidationError


@dataclass(frozen=True)
class DateRange:
    """Immutable date range"""
    start_date: date
    end_date: date
    
    def __post_init__(self):
        if not isinstance(self.start_date, date):
            raise ValidationError("start_date must be a date object")
        if not isinstance(self.end_date, date):
            raise ValidationError("end_date must be a date object")
        if self.end_date < self.start_date:
            raise ValidationError("end_date must be after start_date")
        
    @property
    def duration_days(self) -> int:
        """Get duration in days"""
        return (self.end_date - self.start_date).days
    
    def contains(self, check_date: date) -> bool:
        """Check if date is within range"""
        return self.start_date <= check_date <= self.end_date
    
    def __str__(self) -> str:
        return f"{self.start_date} to {self.end_date}"
