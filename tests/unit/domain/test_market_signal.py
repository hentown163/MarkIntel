import pytest
from datetime import datetime

from app.domain.entities.market_signal import MarketSignal, ImpactLevel
from app.domain.value_objects.signal_id import SignalId
from app.core.exceptions import ValidationError


@pytest.mark.unit
class TestMarketSignal:
    def test_create_market_signal_success(self, mock_signal_id):
        signal = MarketSignal(
            id=mock_signal_id,
            source="Twitter",
            content="New AI trends emerging in the market",
            timestamp=datetime.now(),
            relevance_score=0.85,
            category="AI/ML",
            impact=ImpactLevel.HIGH
        )
        assert signal.source == "Twitter"
        assert signal.relevance_score == 0.85
        assert signal.impact == ImpactLevel.HIGH
        assert signal.category == "AI/ML"
    
    def test_create_market_signal_no_source_fails(self, mock_signal_id):
        with pytest.raises(ValidationError, match="must have a source"):
            MarketSignal(
                id=mock_signal_id,
                source="",
                content="Content",
                timestamp=datetime.now(),
                relevance_score=0.85,
                category="AI/ML",
                impact=ImpactLevel.HIGH
            )
    
    def test_create_market_signal_no_content_fails(self, mock_signal_id):
        with pytest.raises(ValidationError, match="must have content"):
            MarketSignal(
                id=mock_signal_id,
                source="Twitter",
                content="",
                timestamp=datetime.now(),
                relevance_score=0.85,
                category="AI/ML",
                impact=ImpactLevel.HIGH
            )
    
    def test_create_market_signal_invalid_relevance_score_fails(self, mock_signal_id):
        with pytest.raises(ValidationError, match="must be between 0 and 1"):
            MarketSignal(
                id=mock_signal_id,
                source="Twitter",
                content="Content",
                timestamp=datetime.now(),
                relevance_score=1.5,
                category="AI/ML",
                impact=ImpactLevel.HIGH
            )
    
    def test_create_market_signal_no_category_fails(self, mock_signal_id):
        with pytest.raises(ValidationError, match="must have a category"):
            MarketSignal(
                id=mock_signal_id,
                source="Twitter",
                content="Content",
                timestamp=datetime.now(),
                relevance_score=0.85,
                category="",
                impact=ImpactLevel.HIGH
            )
    
    def test_is_highly_relevant_true(self, mock_market_signal):
        mock_market_signal.relevance_score = 0.85
        assert mock_market_signal.is_highly_relevant() is True
    
    def test_is_highly_relevant_false(self, mock_market_signal):
        mock_market_signal.relevance_score = 0.65
        assert mock_market_signal.is_highly_relevant() is False
    
    def test_is_highly_relevant_at_threshold(self, mock_market_signal):
        mock_market_signal.relevance_score = 0.7
        assert mock_market_signal.is_highly_relevant() is True
    
    def test_is_high_impact_true(self, mock_market_signal):
        mock_market_signal.impact = ImpactLevel.HIGH
        assert mock_market_signal.is_high_impact() is True
    
    def test_is_high_impact_false(self, mock_market_signal):
        mock_market_signal.impact = ImpactLevel.MEDIUM
        assert mock_market_signal.is_high_impact() is False
