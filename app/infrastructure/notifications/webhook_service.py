"""Webhook Notification Service"""
import requests
from typing import Optional, Dict, Any
import json


class WebhookService:
    """Service for sending webhook notifications"""
    
    @staticmethod
    def send_webhook(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> bool:
        """Send webhook notification to a URL"""
        try:
            default_headers = {"Content-Type": "application/json"}
            if headers:
                default_headers.update(headers)
            
            response = requests.post(url, json=payload, headers=default_headers, timeout=10)
            return response.status_code < 400
        except Exception as e:
            print(f"Webhook error: {e}")
            return False
    
    @staticmethod
    def notify_high_impact_signal(signal: Dict[str, Any], webhook_url: str) -> bool:
        """Send notification for high-impact market signal"""
        payload = {
            "event": "high_impact_signal",
            "data": signal,
            "message": f"High-impact market signal detected: {signal.get('content', '')[:100]}"
        }
        return WebhookService.send_webhook(webhook_url, payload)
    
    @staticmethod
    def notify_campaign_status(campaign: Dict[str, Any], webhook_url: str) -> bool:
        """Send notification for campaign status change"""
        payload = {
            "event": "campaign_status_change",
            "data": campaign,
            "message": f"Campaign '{campaign.get('name')}' status changed to {campaign.get('status')}"
        }
        return WebhookService.send_webhook(webhook_url, payload)
