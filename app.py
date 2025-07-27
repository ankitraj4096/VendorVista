from flask import Flask, render_template, request

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

if __name__ == "__main__":
    app.run(debug=True)
