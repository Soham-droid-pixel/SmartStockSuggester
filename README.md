# 📦 Smart Stock Suggester for Local Shop Owners

Smart Stock Suggester is an intelligent system built to assist local shopkeepers in optimizing their inventory, pricing, and product choices based on location-specific demand, stock levels, and profitability. The system consists of a **Flask-based backend API** and a **Streamlit frontend dashboard**, connected to a preprocessed dataset (`final_recommendation_data.csv`) generated using the Faker library.

---

## 🚀 Features

* 🔥 **Top Profitable Items**: Identify the most profitable items to prioritize for stocking.
* 🌍 **Location-Based Recommendations**: Get demand-driven suggestions specific to your locality.
* 🏬 **Inventory-Based Suggestions**: Discover what to sell based on current inventory levels.
* 📉 **Low Stock Alerts**: Know which items have a poor stock-to-sales ratio and need replenishment.
* 💸 **Dynamic Pricing Engine**: Suggest price points based on real-time demand and stock metrics.

---

## 🗂️ Project Structure

```
SmartStockSuggester/
│
├── app.py                          # Flask backend with recommendation endpoints
├── final_recommendation_data.csv  # Preprocessed dataset
├── SmartStockSuggester.ipynb      # Jupyter Notebook for data generation and preprocessing
├── frontend/
│   └── streamlit_app.py           # Streamlit UI for interaction with Flask APIs
└── README.md                      # Project documentation (this file)
```

---

## ⚙️ Setup Instructions

### 1. 📦 Clone the Repository

```bash
git clone https://github.com/Soham-droid-pixel/SmartStockSuggester.git
cd SmartStockSuggester
```

### 2. 🐍 Create a Virtual Environment and Activate It

```bash
python -m venv venv
source venv/bin/activate     # On Windows use: venv\Scripts\activate
```

### 3. 📚 Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet created, install manually:

```bash
pip install flask pandas xgboost numpy streamlit requests faker
```

---

## ▶️ Running the Project

### Step 1: Run the Flask Backend

```bash
python app.py
```

* The backend will start at: `http://127.0.0.1:5000`
* Provides REST API endpoints for various recommendation and pricing features.

### Step 2: Run the Streamlit Frontend

```bash
cd frontend
streamlit run streamlit_app.py
```

* The frontend UI will be available at: `http://localhost:8501`
* Use the sidebar to navigate features.

---

## 📡 API Endpoints Summary

| Endpoint                     | Description                             | Query Parameters       |
| ---------------------------- | --------------------------------------- | ---------------------- |
| `/recommend/profitable`      | Returns most profitable items           | `top_n`, `category`    |
| `/recommend/popular`         | Returns most popular items              | `top_n`, `category`    |
| `/recommend/location`        | Recommends based on locality            | `location`, `category` |
| `/recommend/inventory`       | Inventory-based suggestions for a shop  | `shop_id`, `category`  |
| `/recommend/stock`           | Low stock-to-sales items for restocking | `shop_id`, `category`  |
| `/recommend/dynamic-pricing` | Suggests optimal price for an item      | `item`, `category`     |

---

## 📊 Dataset Overview

The dataset `final_recommendation_data.csv` includes:

* `Item`, `Shop_ID`, `Sales_Count`, `Stock_Level`
* `Demand_Score`, `Profit_Margin`, `Stock_to_Sales_Ratio`, `Demand_to_Stock_Ratio`
* One-hot encoded location and category fields like `Location_Bangalore`, `Category_Electronics`

Data was generated using the **Faker** library and preprocessed in the **SmartStockSuggester.ipynb** notebook.

---

## 📸 Streamlit UI Preview

* Clean sidebar for navigation
* Real-time API integration
* Easy-to-use interface for shopkeepers with minimal input fields

---

## 💡 Future Improvements

* Add authentication for shopkeepers
* Integrate real-world sales data and forecasting
* Add charts/graphs to visualize recommendations and trends
* Add support for reinforcement learning for dynamic inventory control

---

## 🧑‍💻 Authors

* **You** – Flask backend, data preprocessing, API design

