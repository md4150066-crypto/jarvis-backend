from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/ask', methods=['GET'])
def ask_jarvis():
    user_query = request.args.get('text', '')
    if not user_query:
        return jsonify({"reply": "No instructions received, sir."})
        
    try:
        # High-speed open routing text processor engine proxy
        url = f"https://pollinations.ai{requests.utils.quote(user_query)}?model=openai"
        headers = {"User-Agent": "Mozilla/5.0"}
        
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            return jsonify({"reply": response.text.strip()})
            
    except Exception as e:
        return jsonify({"reply": f"Cognitive relay error: {str(e)}, sir."})
        
    return jsonify({"reply": "My remote cognitive servers are currently re-calibrating, sir."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
