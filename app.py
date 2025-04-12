import streamlit as st
from preprocess import load_and_clean_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = load_and_clean_data("Sample - Superstore.csv")

st.set_page_config(page_title="Superstore Dashboard", layout="wide")
st.title("📦 Superstore Sales Dashboard")

st.image("https://cdn-icons-png.flaticon.com/512/1170/1170576.png", width=100)

#  Dashboard Landing Summary
st.markdown("""

### 💡 Key Features:
- Filter by Date Range, Region, and Category
- Visualize Sales, Profit, and Quantity by Segment and Sub-Category
- Discover Best-Selling Products and Top Customers
- Track Profit Over Time
- Understand Regional Sales Distribution on the Map
- Gain Business Insights via AI Narrative Layer

Use this dashboard to make data-driven decisions and unlock growth potential!
""")


# Sidebar Filters
st.sidebar.header("📌 Filter Data")

# Date Range
min_date = df['Order Date'].min()
max_date = df['Order Date'].max()
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Region Filter
region_filter = st.sidebar.multiselect("Select Region", df['Region'].unique(), default=df['Region'].unique())

# Category Filter
category_filter = st.sidebar.multiselect("Select Category(s)", df['Category'].unique(), default=df['Category'].unique())

# Filter DataFrame
filtered_df = df[
    (df['Order Date'] >= pd.to_datetime(date_range[0])) &
    (df['Order Date'] <= pd.to_datetime(date_range[1])) &
    (df['Region'].isin(region_filter)) &
    (df['Category'].isin(category_filter))
]

# Show Filtered Data
with st.expander("🔍 View Filtered Data"):
    st.write(filtered_df)

# KPIs
st.markdown("## 📊 Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    total_sales = filtered_df['Sales'].sum()
    st.metric("Total Sales", f"${total_sales:,.2f}")

with kpi2:
    total_profit = filtered_df['Profit'].sum()
    st.metric("Total Profit", f"${total_profit:,.2f}")

with kpi3:
    total_orders = filtered_df['Order ID'].nunique()
    st.metric("Total Orders", total_orders)

# Row 1: Category Sales + Profit Over Time
st.markdown("## 📁 Sales and Profit Overview")

col1, col2 = st.columns(2)

with col1:
    sales_by_category = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig1 = px.bar(sales_by_category, x="Category", y="Sales", color="Category", title="Total Sales by Category")
    st.plotly_chart(fig1, use_container_width=True)

    top_category = sales_by_category.sort_values(by="Sales", ascending=False).iloc[0]
    st.markdown(
        f"""
            🔎 **Insight**: The highest revenue-generating category is **{top_category['Category']}** with sales of **${top_category['Sales']:,.2f}**. 
            This indicates a strong customer demand in this segment and potential for increased focus or marketing investment.
            """
    )

with col2:
    st.markdown("### 📈 Profit Over Time")
    agg_level = st.selectbox("Aggregation Level", ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"])
    freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}

    profit_over_time = filtered_df.set_index('Order Date')['Profit'].resample(freq_map[agg_level]).sum().reset_index()
    fig2 = px.line(profit_over_time, x="Order Date", y="Profit", title=f"Profit Over Time ({agg_level})")
    st.plotly_chart(fig2, use_container_width=True)

    max_profit = profit_over_time['Profit'].max()
    max_profit_date = profit_over_time.loc[profit_over_time['Profit'].idxmax(), 'Order Date'].strftime('%B %Y')

    st.markdown(
        f"""
            🔎 **Insight**: The highest profit was recorded in **{max_profit_date}**, reaching **${max_profit:,.2f}**. 
            Monitoring such peaks can help identify seasonal trends or successful campaigns.
            """
    )

# Row 2: Top Products + Region Pie Chart
st.markdown("## 🏆 Product & Region Insights")
col3, col4 = st.columns(2)

with col3:
    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig3 = px.bar(top_products, x="Sales", y="Product Name", orientation="h", title="Top 10 Best-Selling Products")
    st.plotly_chart(fig3, use_container_width=True)

    best_product = top_products.iloc[0]
    st.markdown(
        f"""
            🔎 **Insight**: The best-selling product is **{best_product['Product Name']}** with total sales of **${best_product['Sales']:,.2f}**. 
            This product is a key driver of revenue and should be prioritized for promotion or stock.
            """
    )

with col4:
    sales_by_region = filtered_df.groupby("Region")["Sales"].sum().reset_index()
    fig4 = px.pie(sales_by_region, names="Region", values="Sales", title="Sales by Region", hole=0.4)
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Profit Heatmap by Region and Category
st.markdown("## 🔥 Profitability Heatmap")

pivot_table = filtered_df.pivot_table(index="Region", columns="Category", values="Profit", aggfunc="sum", fill_value=0)
fig5 = go.Figure(data=go.Heatmap(
    z=pivot_table.values,
    x=pivot_table.columns,
    y=pivot_table.index,
    colorscale="RdBu",
    reversescale=True
))
fig5.update_layout(title="Profit Heatmap: Region vs Category", xaxis_title="Category", yaxis_title="Region")
st.plotly_chart(fig5, use_container_width=True)

# Row 4: Sub-category Drilldown
st.markdown("## 🔎 Category Drilldown")

selected_category = st.selectbox("Select a Category to Explore Sub-Categories", df["Category"].unique())

subcat_data = (
    filtered_df[filtered_df["Category"] == selected_category]
    .groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig6 = px.bar(subcat_data, x="Sub-Category", y="Sales", color="Sub-Category", title=f"Sales by Sub-Category: {selected_category}")
st.plotly_chart(fig6, use_container_width=True)
fig6.update_layout(plot_bgcolor="white")

# Row 5: Geo Map

st.markdown("## 🗺️ Geo Map: U.S. State-wise Performance")

# Select metric
metric = st.selectbox("Select Metric to Display", ["Sales", "Profit"])

# Aggregate by state
state_data = (
    filtered_df.groupby("State")[[metric]]
    .sum()
    .reset_index()
    .sort_values(by=metric, ascending=False)
)

# Add state codes
us_state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}
state_data["State Code"] = state_data["State"].map(us_state_abbrev)
state_data = state_data.dropna(subset=["State Code"])

# Add formatted label
state_data["Label"] = state_data[metric].apply(lambda x: f"${x:,.0f}")

# Centroids for all states
state_centers = {
    'AL': [-86.7911, 32.8067], 'AK': [-152.4044, 61.3707], 'AZ': [-111.4312, 33.7298],
    'AR': [-92.3731, 34.9697], 'CA': [-119.4179, 36.7783], 'CO': [-105.3111, 39.5501],
    'CT': [-72.7554, 41.6032], 'DE': [-75.5071, 38.9108], 'FL': [-81.5158, 27.6648],
    'GA': [-82.9001, 32.1656], 'HI': [-155.5828, 19.8968], 'ID': [-114.742, 44.0682],
    'IL': [-89.3985, 40.6331], 'IN': [-86.126, 40.2672], 'IA': [-93.0977, 41.878],
    'KS': [-98.4842, 39.0119], 'KY': [-84.270, 37.8393], 'LA': [-91.9623, 30.9843],
    'ME': [-69.4455, 45.2538], 'MD': [-76.6413, 39.0458], 'MA': [-71.5301, 42.4072],
    'MI': [-85.6024, 44.3148], 'MN': [-94.6859, 46.7296], 'MS': [-89.3985, 32.3547],
    'MO': [-91.8318, 37.9643], 'MT': [-110.3626, 46.8797], 'NE': [-99.9018, 41.4925],
    'NV': [-116.4194, 38.8026], 'NH': [-71.5724, 43.1939], 'NJ': [-74.4057, 40.0583],
    'NM': [-105.8701, 34.5199], 'NY': [-74.0059, 40.7128], 'NC': [-79.0193, 35.7596],
    'ND': [-101.002, 47.5515], 'OH': [-82.9071, 40.4173], 'OK': [-97.0929, 35.4676],
    'OR': [-120.5542, 43.8041], 'PA': [-77.1945, 41.2033], 'RI': [-71.4774, 41.5801],
    'SC': [-81.1637, 33.8361], 'SD': [-99.9018, 43.9695], 'TN': [-86.5804, 35.5175],
    'TX': [-99.9018, 31.9686], 'UT': [-111.0937, 39.3209], 'VT': [-72.5778, 44.5588],
    'VA': [-78.6569, 37.4316], 'WA': [-120.7401, 47.7511], 'WV': [-80.4549, 38.5976],
    'WI': [-89.6165, 43.7844], 'WY': [-107.2903, 43.0759]
}

state_data["lon"] = state_data["State Code"].map(lambda x: state_centers.get(x, [None, None])[0])
state_data["lat"] = state_data["State Code"].map(lambda x: state_centers.get(x, [None, None])[1])

# Build choropleth map
choropleth = go.Choropleth(
    locations=state_data["State Code"],
    z=state_data[metric],
    locationmode="USA-states",
    colorscale="Cividis",
    colorbar_title=f"{metric}",
    marker_line_color='white'
)

# State abbreviations overlay
labels = go.Scattergeo(
    locationmode="USA-states",
    lon=state_data["lon"],
    lat=state_data["lat"],
    text=state_data["State Code"],
    mode="text",
    textfont=dict(size=10, color="white"),
    showlegend=False
)

fig_geo = go.Figure(data=[choropleth, labels])
fig_geo.update_layout(
    geo_scope='usa',
    title=f"{metric} by U.S. State",
    margin=dict(l=0, r=0, t=50, b=0),


)

# Display map and top states bar chart
left_col, right_col = st.columns([2, 1])
with left_col:
    st.plotly_chart(fig_geo, use_container_width=True)

with right_col:
    top_states = state_data.head(5).sort_values(by=metric)
    fig_bar = px.bar(
        top_states,
        x=metric,
        y="State",
        orientation="h",
        color="State",
        text=top_states[metric].apply(lambda x: f"${x:,.0f}"),
        color_discrete_sequence=px.colors.sequential.Cividis
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        title=f"🏆 Top 5 States by {metric}",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=300,
        margin=dict(t=40, b=20, l=0, r=0)
    )
    st.plotly_chart(fig_bar, use_container_width=True)


# 🧾 Download Filtered Data
st.markdown("### 📥 Download Filtered Dataset")
csv_data = filtered_df.to_csv(index=False).encode("latin-1")
st.download_button(
    label="⬇️ Download as CSV",
    data=csv_data,
    file_name="filtered_superstore_data.csv",
    mime="text/csv"
)









