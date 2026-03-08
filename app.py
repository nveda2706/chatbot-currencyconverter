import os
from dotenv import load_dotenv
from flask import Flask,request,jsonify
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount=amount*cf
    response ={
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }

    return jsonify(response)

def fetch_conversion_factor(source,target):
    url="https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{}".format(source)
    response = requests.get(url)
    data = response.json()
    
    conversion_rate = data['conversion_rates'][target]
    return conversion_rate

if __name__=="__main__":
    app.run(debug=True)