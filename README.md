Citizen Query — Chat demo

This workspace contains a simple frontend (`citizenQuery.html`) and a minimal Flask API (`server.py`) that accepts a POST to `/ask` and returns JSON.

Quick start (Windows PowerShell):

1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

2. Install dependencies

```powershell
pip install -r requirements.txt
```

3. Run the Flask API (listens on port 5001)

```powershell
python server.py
```

4. Serve the frontend or open the HTML directly

- Recommended: serve the folder so the browser allows fetch requests.

```powershell
# from the repository root
python -m http.server 8000
# then open http://localhost:8000/citizenQuery.html in your browser
```

Notes
- The chat widget in `citizenQuery.html` sends POST requests to `http://localhost:5001/ask` with JSON {"question": "..."} and expects a JSON response. The demo `server.py` responds with a canned answer or an echo reply.
- CORS is enabled in the Flask app to allow requests from the browser origin. If you open the HTML via `file://` the browser may restrict cross-origin requests; serving via `http.server` avoids this.
- This is a minimal demo. For production, add authentication, rate limiting, input validation and proper error handling.
