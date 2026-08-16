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
        
    # Smart Retry Matrix - If one engine fails, it instantly holds and processes via fallback
    ai_models = ["openai", "mistral", "qwen"]
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    for model in ai_models:
        try:
            url = f"https://pollinations.ai{requests.utils.quote(user_query)}?model={model}"
            response = requests.get(url, headers=headers, timeout=12)
            
            if response.status_code == 200 and response.text.strip():
                clean_reply = response.text.strip()
                # Ensure it didn't fetch a corrupted HTML wrapper error page
                if "<html" not in clean_reply.lower() and "error" not in clean_reply.lower():
                    return jsonify({"reply": clean_reply})
        except Exception:
            continue  # Silently hops to the next backup engine to handle processing

    return jsonify({"reply": "My remote cognitive servers are re-routing your data packet matrix, sir. Please repeat instructions."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


  
