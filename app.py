from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

API_KEY = "76e2c093354bc4b6d67c7fe2"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

CURRENCIES = {
    "USD": "美元",
    "EUR": "欧元",
    "JPY": "日元",
    "GBP": "英镑",
    "AUD": "澳元",
    "CAD": "加元",
    "CHF": "瑞士法郎",
    "CNY": "人民币",
    "HKD": "港币",
    "NZD": "新西兰元",
    "SEK": "瑞典克朗",
    "KRW": "韩元",
    "SGD": "新加坡元",
    "NOK": "挪威克朗",
    "MXN": "墨西哥比索",
    "INR": "印度卢比",
    "RUB": "俄罗斯卢布",
    "ZAR": "南非兰特",
    "TRY": "土耳其里拉",
    "BRL": "巴西雷亚尔",
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>汇率换算工具</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
        form { display: flex; flex-direction: column; gap: 10px; }
        select, input, button { padding: 10px; font-size: 16px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h1>汇率换算工具</h1>
    <form method="POST">
        <input type="number" name="amount" placeholder="金额" required step="0.01" min="0">
        <select name="from_currency" required>
            {% for code, name in currencies.items() %}
                <option value="{{ code }}">{{ code }} - {{ name }}</option>
            {% endfor %}
        </select>
        <select name="to_currency" required>
            {% for code, name in currencies.items() %}
                <option value="{{ code }}">{{ code }} - {{ name }}</option>
            {% endfor %}
        </select>
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
            return render_template_string(HTML_TEMPLATE, currencies=CURRENCIES, result=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    
    return render_template_string(HTML_TEMPLATE, currencies=CURRENCIES)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)