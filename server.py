from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# A tiny demo knowledge base to return more helpful canned answers for common queries.
KB = {
    'tax': 'To pay property or income tax, sign in to the Tax service from the portal and choose "Make a payment". You can pay by card or bank transfer. Deadlines and penalties are visible on your statement.',
    'pension': 'Pension queries: visit the Pension service to view balances and contribution history. To apply for benefits, complete the online form and upload required documents.',
    'transport': 'For transport: buy transit passes under Transport -> Passes, or check schedules in the Transport section.',
    'health': 'Healthcare: you can book appointments and view your referrals in the Healthcare service. For emergencies, call local emergency services.'
}

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    question = data.get('question') if isinstance(data, dict) else None
    if not question:
        return jsonify({'error': 'Missing "question" in JSON body.'}), 400

    # simulate a small processing delay
    time.sleep(0.4)

    q = question.lower()
    for k, a in KB.items():
        if k in q:
            return jsonify({'answer': a, 'source': 'kb', 'question': question})

    # default fallback reply (echo-like)
    reply = f"I received your question: '{question}'. This is a sample reply from the demo Flask API."
    return jsonify({'answer': reply, 'source': 'echo', 'question': question})


# Backwards-compatible alias for frontend which may call /ask_llm
@app.route('/ask_llm', methods=['POST'])
def ask_llm():
    return ask()


@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    # Expecting a form file field named 'file'
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(f.filename)
    if not filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    save_path = os.path.join(uploads_dir, filename)
    try:
        f.save(save_path)
    except Exception as e:
        return jsonify({'error': 'Failed to save file', 'details': str(e)}), 500

    return jsonify({'message': 'File uploaded', 'filename': filename, 'size': os.path.getsize(save_path)})

if __name__ == '__main__':
    # Listen on all interfaces so the host machine and browser can reach it
    app.run(host='0.0.0.0', port=5001, debug=True)
