"""Market signal repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.market_signal import MarketSignal
from app.domain.value_objects import SignalId


class MarketSignalRepository(ABC):
    """
    Market Signal repository interface (port)
    
    Following Interface Segregation Principle
    """
    
    @abstractmethod
    def find_by_id(self, signal_id: SignalId) -> Optional[MarketSignal]:
        """Find signal by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[MarketSignal]:
        """Find all signals"""
        pass
    
    @abstractmethod
    def find_recent(self, limit: int = 10) -> List[MarketSignal]:
        """Find recent signals"""
        pass
    
    @abstractmethod
    def find_high_relevance(self, threshold: float = 0.7) -> List[MarketSignal]:
        """Find high relevance signals"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[MarketSignal]:
        """Find signals by category"""
        pass
    
    @abstractmethod
    def save(self, signal: MarketSignal) -> MarketSignal:
        """Save signal (create or update)"""
        pass
    
    @abstractmethod
    def delete(self, signal_id: SignalId) -> bool:
        """Delete signal"""
        pass
