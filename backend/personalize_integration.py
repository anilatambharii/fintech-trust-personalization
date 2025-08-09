import os
from dotenv import load_dotenv

load_dotenv()

class PersonalizeClient:
    def __init__(self):
        self.campaign_arn = os.getenv("AWS_PERSONALIZE_CAMPAIGN_ARN", "")
        self.tracking_id = os.getenv("AWS_PERSONALIZE_TRACKING_ID", "")
        
        # Only initialize boto3 if we have a real ARN
        self.is_demo_mode = not self.campaign_arn.startswith("arn:aws:personalize")
        if not self.is_demo_mode:
            import boto3
            self.personalize = boto3.client("personalize-runtime")
            self.personalize_events = boto3.client("personalize-events")

    def get_recommendations(self, user_id):
        if self.is_demo_mode:
            print("⚠️ Running in DEMO MODE (no AWS call).")
            return [
                {"itemId": "loan-offer-001", "score": 0.98},
                {"itemId": "investment-plan-123", "score": 0.93},
                {"itemId": "credit-card-upgrade", "score": 0.91}
            ]
        
        # LIVE AWS call
        response = self.personalize.get_recommendations(
            campaignArn=self.campaign_arn,
            userId=str(user_id)
        )
        return response.get("itemList", [])

    def put_event(self, event):
        if self.is_demo_mode:
            print(f"⚠️ DEMO MODE: Event not sent to AWS: {event}")
            return
        
        self.personalize_events.put_events(
            trackingId=self.tracking_id,
            userId=event.get("user_id", "unknown"),
            sessionId="session-1",
            eventList=[{
                "itemId": event.get("item_id", "unknown"),
                "eventType": event.get("event_type", "click")
            }]
        )
