from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import re
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    role = request.args.get('role')
    return render_template("login.html", role=role)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/buyer-dashboard")
def buyer_dashboard():
    return render_template("buyer-dashboard.html")

@app.route("/buyer-exchange")
def buyer_exchange():
    return render_template("buyer-exchange.html")

@app.route("/buyer-fresh-produce")
def buyer_fresh_produce():
    return render_template("buyer-fresh-produce.html")

@app.route("/buyer-vendor")
def buyer_vendor():
    return render_template("buyer-vendor.html")

@app.route("/shared-live-map")
def shared_live_map():
    return render_template("shared-live-map.html")

@app.route("/shared-profile")
def shared_profile():
    return render_template("shared-profile.html")

@app.route("/shared-stories-feed")
def shared_stories_feed():
    return render_template("shared-stories-feed.html")

@app.route("/vendor-dashboard")
def vendor_dashboard():
    return render_template("vendor-dashboard.html")

@app.route("/vendor-orders")
def vendor_orders():
    return render_template("vendor-orders.html")

@app.route("/vendor-produce")
def vendor_produce():
    return render_template("vendor-produce.html")

@app.route("/vendor-stories")
def vendor_stories():
    return render_template("vendor-stories.html")
@app.route("/buyer-cart")
def buyer_cart():
    return render_template("buyer-cart.html")

# Put your Gemini API key somewhere secure!
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyA2Ar6RM4JmRc_cJOT_GqF5laWOtm8j1lU"
genai.configure(api_key=GEMINI_API_KEY)

# --- Use the correct model name! ---
# From your model list, use one of:
MODEL_NAME = "models/gemini-1.5-pro-latest"
# MODEL_NAME = "models/gemini-1.5-pro"

@app.route("/api/gemini_geocode", methods=["POST"])
def gemini_geocode():
    data = request.get_json()
    address = data.get("address")
    if not address:
        return jsonify({"error": "address required"}), 400

    # Prompt: be very explicit, suppress commentary
    prompt = (
        "Respond ONLY with valid JSON (no markdown, no explanation): "
        "{{\"lat\": xx.xxxxx, \"lng\": yy.yyyyy}} as decimal values for this address: "
        f"{address}\nNo code block, no prefix, no extra text."
    )
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        print("1")
        print("-" * 40)
        print("GEMINI RAW OUTPUT:", repr(response.text))  # Always print!
        # Try robust extraction
        # 1. JSON object
        match = re.search(r'\{[^\{\}]*"lat"[^\{\}]*\}', response.text)
        if match:
            coords = json.loads(match.group(0))
            lat = float(coords.get("lat") or coords.get("latitude"))
            lng = float(coords.get("lng") or coords.get("longitude"))
            return jsonify({"lat": lat, "lng": lng})

        # 2. Fallback: labeled numbers (Latitude: ##, Longitude: ##)
        match2 = re.search(r"Lat(?:itude)?[: ]\s*([0-9\.\-]+)[^\n,]*[,\n ]+Lng(?:itude)?[: ]\s*([0-9\.\-]+)", response.text, re.IGNORECASE)
        if match2:
            lat = float(match2.group(1))
            lng = float(match2.group(2))
            return jsonify({"lat": lat, "lng": lng})

        # 3. Fallback: first two floats in reply
        floats = re.findall(r"([+-]?[0-9]+(?:\.[0-9]+)?)", response.text)
        if len(floats) >= 2:
            lat = float(floats[0])
            lng = float(floats[1])
            return jsonify({"lat": lat, "lng": lng})

        # Fail all
        return jsonify({"error": "Could not find coordinates"}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()  # Prints the stack trace in your Flask terminal
        print("EXCEPTION:", str(e))
        return jsonify({"error": f"Gemini failure: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
