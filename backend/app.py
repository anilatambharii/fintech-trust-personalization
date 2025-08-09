from flask import Flask, request, jsonify
from personalize_integration import PersonalizeClient
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#app = Flask(__name__)
client = PersonalizeClient()

@app.route("/")
def health():
    return jsonify({"status": "ok", "message": "Fintech Personalization API running"})

@app.route("/recommendations")
def recommend():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    try:
        recs = client.get_recommendations(user_id)
        return jsonify({"user_id": user_id, "recommendations": recs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/events", methods=["POST"])
def events():
    data = request.json
    if not data:
        return jsonify({"error": "No JSON payload"}), 400
    try:
        client.put_event(data)
        return jsonify({"status": "event recorded"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    print(f"✅ API running at: http://127.0.0.1:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)
