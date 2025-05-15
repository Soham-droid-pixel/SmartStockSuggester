import streamlit as st
import requests

BASE_URL = "https://smartstocksuggester.onrender.com"

st.set_page_config(page_title="Smart Stock Suggester", layout="wide")

# Sidebar Menu for Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Choose an Option",
    [
        "Get Profitable Items",
        "Get Popular Items",
        "Get Location-Based Recommendations",
        "Get Inventory-Based Recommendations",
        "Get Stock Recommendation",
        "Get Dynamic Pricing Suggestion"
    ]
)

st.title("Smart Stock Suggester")

# Function to fetch and display API results
def fetch_data(endpoint, params=None):
    response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    if response.status_code == 200:
        data = response.json()
        
        if isinstance(data, dict):
            # Convert dictionary values to a readable format
            formatted_data = []
            for key, value in data.items():
                if isinstance(value, list):
                    formatted_data.append(f"{key}: " + ", ".join(map(str, value)))
                else:
                    formatted_data.append(f"{key}: {value}")
            return "\n".join(formatted_data)
        
        elif isinstance(data, list):
            # Handle direct list responses
            return "\n".join(map(str, data))
        
        else:
            return str(data)  # If it's a simple string or number
    else:
        return f"Error: {response.status_code} - Unable to fetch data"

# Handle menu selection
if menu == "Get Profitable Items":
    st.subheader("Top Profitable Items")
    if st.button("Fetch Profitable Items"):
        result = fetch_data("recommend/profitable")
        st.text(result)

elif menu == "Get Popular Items":
    st.subheader("Top Popular Items")
    if st.button("Fetch Popular Items"):
        result = fetch_data("recommend/popular")
        st.text(result)

elif menu == "Get Location-Based Recommendations":
    st.subheader("Find Best-Selling Items by Location")
    location = st.text_input("Enter Location:")
    if st.button("Fetch Location-Based Recommendations"):
        result = fetch_data("recommend/location", {"location": location})
        st.text(result)

elif menu == "Get Inventory-Based Recommendations":
    st.subheader("Get Inventory-Based Item Recommendations")
    shop_id = st.text_input("Enter Shop ID:")
    if st.button("Fetch Inventory-Based Recommendations"):
        result = fetch_data("recommend/inventory", {"shop_id": shop_id})
        st.text(result)

elif menu == "Get Stock Recommendation":
    st.subheader("Stock Recommendation for Shops")
    shop_id = st.text_input("Enter Shop ID:")
    if st.button("Fetch Stock Recommendations"):
        result = fetch_data("recommend/stock", {"shop_id": shop_id})
        st.text(result)

elif menu == "Get Dynamic Pricing Suggestion":
    st.subheader("Suggested Dynamic Pricing for an Item")
    item = st.text_input("Enter Item Name:")
    if st.button("Fetch Dynamic Pricing Suggestion"):
        result = fetch_data("recommend/dynamic-pricing", {"item": item})
        st.text(result)
