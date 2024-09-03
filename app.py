from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='templates')

API_KEY = "76e2c093354bc4b6d67c7fe2"  # 请替换为您的实际API密钥
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        amount = float(request.form["amount"])
        from_currency = request.form["from_currency"]
        to_currency = request.form["to_currency"]
        
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}/{amount}")
        result = response.json()
        
        if result["result"] == "success":
            converted_amount = result["conversion_result"]
            return render_template("index.html", result=f"{amount} {from_currency} = {converted_amount} {to_currency}")
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)