import json
import os
from datetime import datetime
import requests

def handle(event, context):
    """
    Daily fetcher function - triggered by CRON at 8 AM daily
    Publishes a message to NATS topic 'orders.import' to trigger file processing
    """
    try:
        current_date = datetime.now().isoformat()
        user_id = os.getenv('USER_ID', 'US17')

        message = {
            "date": current_date,
            "user_id": user_id,
            "action": "process_orders",
            "timestamp": current_date
        }

        gateway_host = os.getenv('GATEWAY_HOST', 'gateway.openfaas')
        nats_url = f"http://{gateway_host}:8080/async-function/file-transformer"

        headers = {
            'Content-Type': 'application/json',
            'X-Topic': 'orders.import'
        }
        response = requests.post(
            nats_url,
            json=message,
            headers=headers,
            timeout=10
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Daily fetcher failed",
                "details": str(e)
            })
        }