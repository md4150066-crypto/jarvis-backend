import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API Key from environment variables
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Jarvis Cloud Core Mainframe Online.", 200

@app.route("/api", methods=["POST"])
def jarvis_brain():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"reply": "I received an empty packet, sir."}), 400
            
        user_prompt = data["text"]
        
        # Initialize the Gemini Flash model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Add system context so it talks like Jarvis
        full_prompt = f"You are Jarvis, a helpful AI assistant. Answer this query cleanly and concisely: {user_prompt}"
        response = model.generate_content(full_prompt)
        
        return jsonify({"reply": response.text})
        
    except Exception as e:
        return jsonify({"reply": f"Cloud processing error: {str(e)}, sir."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
