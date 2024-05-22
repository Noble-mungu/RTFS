from flask import Flask, jsonify
from pymongo import MongoClient
import os 
from flask_restful import Resource, Api
app = Flask(__name__)

atlas_connection_string = "mongodb+srv://mungunoble:ZXeFVujGHAJszjWH@cluster0.8zkuwy4.mongodb.net/rtfs?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(atlas_connection_string)
db = client["rtfs"] 
non_fraud_table = db["non-fraud"]

@app.route("/api/customer/<cc_num>", methods=["GET"])
def get_customer_info(cc_num):
    customer_info = non_fraud_table.find_one({"cc_num": cc_num}, {"_id": 0})
    if customer_info:
        return jsonify(customer_info)
    else:
        return jsonify({"message": "Customer not found"}), 404

@app.route("/api/statement/<cc_num>", methods=["GET"])
def get_transaction_statement(cc_num):
    transactions = non_fraud_table.find({"cc_num": cc_num}).sort("trans_time", 1)
    statement = [transaction for transaction in transactions]
    return jsonify(statement)

if __name__ == "__main__":
     app.run(host="localhost", port=8000, debug=True)



