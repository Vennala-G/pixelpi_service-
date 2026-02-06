from flask import Flask, render_template, request, redirect, jsonify
import json

app = Flask(__name__)

# Load services from JSON
with open("services.json") as f:
    services = json.load(f)

@app.route("/")
def home():
    return render_template("index.html", services=services)

@app.route("/api/services")
def get_services():
    return jsonify(services)

@app.route("/book", methods=["POST"])
def book_service():
    data = request.form
    # Save booking to a file (simple demo)
    with open("bookings.json", "a") as f:
        f.write(json.dumps(data) + "\n")
    return "Service booked successfully!"

@app.route("/chat")
def chat_redirect():
    # Redirect to WhatsApp with your number
    whatsapp_url = "https://wa.me/917204724293?text=Hi%20I%20want%20to%20book%20a%20service"
    return redirect(whatsapp_url, code=302)

if __name__ == "__main__":
    app.run(debug=True)
