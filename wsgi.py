from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ask', methods=['GET', 'POST'])
def ask_jarvis():
    user_query = request.args.get('text', '')
    if not user_query:
        user_query = request.values.get('text', '')
        
    if not user_query or user_query.strip().lower() == 'wake':
        return jsonify({"reply": "Core systems initialized and awake, sir."})
        
    ai_models = ["openai", "mistral", "qwen"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for model in ai_models:
        try:
            url = f"https://pollinations.ai{requests.utils.quote(user_query)}?model={model}"
            response = requests.get(url, headers=headers, timeout=12)
            
            if response.status_code == 200 and response.text.strip():
                clean_reply = response.text.strip()
                if "<html" not in clean_reply.lower() and "error" not in clean_reply.lower():
                    # This ensures the output is always delivered as a valid JSON reply dictionary block
                    return jsonify({"reply": clean_reply})
        except Exception:
            continue

    return jsonify({"reply": "My remote cognitive processors are re-routing your data packet matrix, sir. Please repeat instructions."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

  
