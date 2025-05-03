from flask import Flask, request, jsonify
import pandas as pd
import xgboost as xgb
import numpy as np
import random
import re

app = Flask(__name__)

# Load dataset
df = pd.read_csv("final_recommendation_data.csv")
df["Item"] = df["Item"].astype(str).str.strip().str.lower()

# Ensure location columns are boolean
df.iloc[:, df.columns.str.startswith("Location_")] = df.iloc[:, df.columns.str.startswith("Location_")].astype(bool)

# Helper function to filter by category
def filter_by_category(data, category):
    if category and f"Category_{category}" in data.columns:
        return data[data[f"Category_{category}"] == True]
    return data

# Get top profitable items
def get_profitable_items(top_n=10, category=None):
    filtered_df = filter_by_category(df, category)
    return filtered_df.nlargest(top_n, "Profit_Margin")["Item"].tolist()

# Inventory-based recommendation
def inventory_based_recommendation(shop_id, category=None):
    filtered_df = df[df["Shop_ID"] == shop_id]
    filtered_df = filter_by_category(filtered_df, category)
    return filtered_df.nlargest(10, "Stock_Level")["Item"].tolist()

# Stock recommendation
def get_stock_recommendation(shop_id, category=None):
    filtered_df = df[df["Shop_ID"] == shop_id]
    filtered_df = filter_by_category(filtered_df, category)
    return filtered_df.nsmallest(10, "Stock_to_Sales_Ratio")["Item"].tolist()

# Dynamic Pricing Suggestion
def suggest_dynamic_price(item, category=None):
    item_data = df[df["Item"] == item]
    if category:
        item_data = item_data[item_data[f"Category_{category}"] == True]
    
    if item_data.empty:
        return None
    
    base_price = item_data["Profit_Margin"].mean() * 10  
    demand_factor = item_data["Demand_Score"].mean() / 100  
    stock_factor = 1 - (item_data["Stock_Level"].mean() / 100)
    
    dynamic_price = base_price * (1 + demand_factor) * (1 + stock_factor)
    return round(dynamic_price, 2)

# Flask API Endpoints
@app.route('/recommend/popular', methods=['GET'])
def recommend_popular():
    top_n = int(request.args.get("top_n", 10))
    category = request.args.get("category", "").strip()
    return jsonify({"popular_items": get_profitable_items(top_n, category)})

@app.route('/recommend/profitable', methods=['GET'])
def recommend_profitable():
    top_n = int(request.args.get("top_n", 10))
    category = request.args.get("category")
    return jsonify({"profitable_items": get_profitable_items(top_n, category)})

@app.route('/recommend/location', methods=['GET'])
def recommend_location():
    location = request.args.get("location")
    category = request.args.get("category")
    if not location:
        return jsonify({"error": "Location is required"}), 400
    location_column = f"Location_{location}"
    if location_column not in df.columns:
        return jsonify({"error": f"Invalid location: {location}"})
    df[location_column] = df[location_column].astype(bool)
    location_items = df[df[location_column]]
    location_items = filter_by_category(location_items, category)
    if location_items.empty:
        return jsonify({"error": f"No items found for location: {location}"})
    top_location_items = location_items.groupby("Item")["Sales_Count"].sum().sort_values(ascending=False)
    return jsonify({"location_recommendations": top_location_items.head(10).index.tolist()})

@app.route('/recommend/inventory', methods=['GET'])
def recommend_inventory():
    shop_id = request.args.get("shop_id", "").strip()
    category = request.args.get("category")
    if not shop_id:
        return jsonify({"error": "Shop ID is required"}), 400
    return jsonify({"shop_id": shop_id, "inventory_based_items": inventory_based_recommendation(shop_id, category)})

@app.route('/recommend/stock', methods=['GET'])
def recommend_stock():
    shop_id = request.args.get("shop_id")
    category = request.args.get("category")
    if not shop_id:
        return jsonify({"error": "Shop ID is required"}), 400
    return jsonify({"stock_recommendation": get_stock_recommendation(shop_id, category)})

@app.route('/recommend/dynamic-pricing', methods=['GET'])
def recommend_dynamic_pricing():
    item = request.args.get("item")
    category = request.args.get("category")
    if not item:
        return jsonify({"error": "Item is required"}), 400
    item = re.sub(r'[\r\n]+', '', item.strip().lower())
    return jsonify({"suggested_price": suggest_dynamic_price(item, category)})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
