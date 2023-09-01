import yfinance as yf
from flask import request, render_template, jsonify, Flask

app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')

## Hello
@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        ticker = request.get_json()['ticker']
        data = yf.Ticker(ticker).history(period='1y')  # Use the 'ticker' variable, not the string 'ticker'

        if data.empty:
            return jsonify({'error': 'No data available for this ticker'}), 400

        return jsonify({'current_price': data.iloc[-1].Close, 'open_price': data.iloc[-1].Open})

    except KeyError:
        return jsonify({'error': 'Invalid request data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
