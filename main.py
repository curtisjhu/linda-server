from flask import Flask, jsonify, render_template_string
from alpaca.trading.client import TradingClient
import matplotlib.pyplot as plt
import io
import base64

from helper import *

# Initialize Alpaca Trading Client
trading_client = TradingClient(api_key, api_secret, paper=True)

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    try:
        # Fetch all current positions
        positions = trading_client.get_all_positions()
        account = trading_client.get_account()

        # Convert positions to a list of dictionaries
        positions_data = [
            {
                'symbol': position.symbol,
                'qty': float(position.qty),
                'market_value': float(position.market_value),
                'cost_basis': float(position.cost_basis),
                'unrealized_pl': float(position.unrealized_pl)
            }
            for position in positions
        ]

        # Generate pie chart
        labels = [position['symbol'] for position in positions_data]
        sizes = [position['market_value'] for position in positions_data]
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title('Portfolio Distribution')
        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # HTML template for rendering the table and pie chart
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Current Positions</title>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
            <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        </head>
        <body class="prose m-5">
            <div class="my-5">
                <h1>Account</h1>
				<table>
					<thead>
						<tr>
							<th>Cash</th>
							<th>Equity</th>
							<th>Buying Power</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>{{ account.cash }}</td>
							<td>{{ account.equity }}</td>
							<td>{{ account.buying_power }}</td>
						</tr>
					</tbody>
				</table>
            </div>

			<div class="my-5">
				<h1>Current Positions</h1>
				<table>
					<thead>
						<tr>
							<th>Symbol</th>
							<th>Quantity</th>
							<th>Market Value</th>
							<th>Cost Basis</th>
							<th>Unrealized P/L</th>
						</tr>
					</thead>
					<tbody>
						{% for position in positions %}
						<tr>
							<td>{{ position.symbol }}</td>
							<td>{{ position.qty }}</td>
							<td>{{ position.market_value }}</td>
							<td>{{ position.cost_basis }}</td>
							<td>{{ position.unrealized_pl }}</td>
						</tr>
						{% endfor %}
					</tbody>
				</table>
			</div>

            <p>
                This is not all of my money of course.
            </p>
        </body>
        </html>
        """

        # Render the HTML template with positions data and plot URL
        return render_template_string(html_template, positions=positions_data, account=account, plot_url=plot_url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)