"""Export helper utilities for CSV and JSON exports"""
import csv
import io
import json
from typing import List, Dict, Any
from datetime import datetime


def dict_to_csv(data: List[Dict[str, Any]], filename: str = "export") -> tuple[str, str]:
    """Convert list of dicts to CSV string"""
    if not data:
        return "", "text/csv"
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    
    return output.getvalue(), "text/csv"


def dict_to_json(data: Any) -> tuple[str, str]:
    """Convert data to JSON string"""
    return json.dumps(data, indent=2, default=str), "application/json"


def flatten_campaign_for_export(campaign: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten campaign structure for CSV export"""
    flat = {
        "id": campaign.get("id"),
        "name": campaign.get("name"),
        "theme": campaign.get("theme"),
        "status": campaign.get("status"),
        "start_date": campaign.get("start_date"),
        "end_date": campaign.get("end_date"),
        "created_at": campaign.get("created_at"),
        "ideas": "; ".join([idea.get("description", "") for idea in campaign.get("ideas", [])]),
        "channels": "; ".join([ch.get("channel", "") for ch in campaign.get("channel_mix", [])]),
        "budget_allocated": campaign.get("metrics", {}).get("budget_allocated"),
        "engagement": campaign.get("metrics", {}).get("engagement"),
        "leads": campaign.get("metrics", {}).get("leads"),
        "conversions": campaign.get("metrics", {}).get("conversions"),
    }
    return flat


def flatten_signal_for_export(signal: Dict[str, Any]) -> Dict[str, Any]:
    """Flatten market signal structure for CSV export"""
    return {
        "id": signal.get("id"),
        "source": signal.get("source"),
        "content": signal.get("content"),
        "timestamp": signal.get("timestamp"),
        "relevance_score": signal.get("relevance_score"),
        "category": signal.get("category"),
        "impact": signal.get("impact"),
    }
