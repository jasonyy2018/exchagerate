from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_KEY = "76e2c093354bc4b6d67c7fe2"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>汇率换算工具</title>
</head>
<body>
    <h1>汇率换算工具</h1>
    <form method="POST">
        <input type="number" name="amount" placeholder="金额" required>
        <input type="text" name="from_currency" placeholder="从货币 (例如: USD)" required>
        <input type="text" name="to_currency" placeholder="到货币 (例如: CNY)" required>
        <button type="submit">换算</button>
    </form>
    {% if result %}
    <p>{{ result }}</p>
    {% endif %}
</body>
</html>
"""

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
            return render_template_string(HTML_TEMPLATE, result=f"{amount} {from_currency} = {converted_amount} {to_currency}")
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)