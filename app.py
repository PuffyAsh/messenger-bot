from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = "myCustomVerifyToken"
PAGE_ACCESS_TOKEN = "PASTE_YOUR_PAGE_ACCESS_TOKEN_HERE"

@app.route("/", methods=["GET"])
def verify():
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return str(challenge)
    return "Invalid verification token", 403

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook received:", data)

    if data["object"] == "page":
        for entry in data["entry"]:
            for message_event in entry.get("messaging", []):
                sender_id = message_event["sender"]["id"]
                if "message" in message_event:
                    message_text = message_event["message"].get("text")
                    if message_text:
                        send_message(sender_id, f"You said: {message_text}")
    return "OK", 200

def send_message(recipient_id, response_text):
    url = "https://graph.facebook.com/v19.0/me/messages"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': response_text}
    }
    params = {
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code != 200:
        print("Error sending message:", response.text)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
