# Streamlit-Data-analysis-Dashboard
That is my portfolio project on data analysis


# Superstore Sales Dashboard

An interactive data analysis dashboard built with **Streamlit**, designed to uncover key insights from the Superstore sales dataset. Ideal for business users, analysts, and decision-makers who want to explore performance trends, customer behavior, and profitability across regions, products, and time periods.

---

## Features

- **Dynamic Filters**: Filter by date range, region, and product category
- **KPIs**: Real-time metrics for total sales, profit, and orders
- **Category & Profit Trends**: Visualize sales and profit trends over time with flexible aggregation (daily to yearly)
- **Top Performers**: Discover top-selling products and best-performing states
- **Profit Heatmap**: Identify high- and low-profit zones by region and category
- **Geo Map**: Choropleth map for state-wise performance in sales or profit
- **Download**: Export filtered data to CSV

---

## Business Insights Powered

Each chart includes narrative insights to support decision-making and highlight patterns in the data (e.g., best-performing months, categories with high ROI, top regions).

---

## Folder Structure

```
superstore-dashboard/
│
├── app.py                  # Main Streamlit app
├── preprocess.py           # Data cleaning and preprocessing logic
├── Sample - Superstore.csv # Dataset
├── README.md               # Project documentation
└── requirements.txt        # Dependencies
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/superstore-dashboard.git
cd superstore-dashboard
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the app**

```bash
streamlit run app.py
```

---

## Dataset

- **Source**: Kaggle
- **Size**: ~10k rows of sales data from a US-based office supplies retailer


## Future Improvements

- Add predictive analytics (e.g., sales forecasting with Prophet)
- Role-based access for business vs. analyst users
- Deeper NLP insights using AI for automated recommendations

---

## Credits

Created by [Your Name] – BS Artificial Intelligence  
Powered by Python, Streamlit, Plotly, and Pandas

---

## License

MIT License – use it, remix it, share it.
