# fintech-trust-personalization
Built a real-time recommendation API leveraging AWS Personalize, focusing on trust, consent, and ethical data use—tested with open‐source fintech dataset and complete working demo

Steps:
Clone repo
Place dataset (.csv) in data/
Set AWS credentials and personalize campaign/tracking IDs
cd backend & pip install -r requirements.txt
python app.py to start service on localhost:5000
Test with GET /recommendations?user_id=123 and POST /events
