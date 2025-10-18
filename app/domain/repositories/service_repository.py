"""Service repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.service import Service
from app.domain.value_objects import ServiceId


class ServiceRepository(ABC):
    """
    Service repository interface (port)
    
    Following Interface Segregation Principle
    """
    
    @abstractmethod
    def find_by_id(self, service_id: ServiceId) -> Optional[Service]:
        """Find service by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Service]:
        """Find all services"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[Service]:
        """Find services by category"""
        pass
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Service]:
        """Find service by name (exact or partial match)"""
        pass
    
    @abstractmethod
    def save(self, service: Service) -> Service:
        """Save service (create or update)"""
        pass
    
    @abstractmethod
    def delete(self, service_id: ServiceId) -> bool:
        """Delete service"""
        pass
