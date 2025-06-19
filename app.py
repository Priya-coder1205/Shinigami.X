from flask import Flask, request
import requests

app = Flask(__name__)

# Use your actual OpenRouter API key here
OPENROUTER_API_KEY = "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"

def get_chatgpt_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourname.com",  # Replace with any URL
        "X-Title": "whatsapp-agent"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  # or any supported one like meta/llama-3
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body')
    from_number = request.form.get('From')
    
    if not incoming_msg:
        return "<Response><Message>Send something!</Message></Response>"

    reply = get_chatgpt_response(incoming_msg)

    return f"""
    <Response>
        <Message>{reply}</Message>
    </Response>
    """

if __name__ == "__main__":
    app.run(debug=True)

