# import streamlit as st
# import requests

# st.set_page_config(page_title="Supply Chain Prediction", layout="centered")

# st.title("📦 Supply Chain Geospatial Prediction Dashboard")

# st.markdown("### Enter the required details below and get predictions instantly!")

# # Layout with two columns
# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("📊 Order & Shipment Details")
#     days_for_shipment_scheduled = st.slider("Days for Shipment Scheduled", 1, 30, 3)
#     order_day_of_week = st.slider("Order Day of Week", 0, 6, 3)
#     shipping_day_of_week = st.slider("Shipping Day of Week", 0, 6, 3)

# with col2:
#     st.subheader("💰 Financial Details")
#     order_item_discount = st.number_input("Order Item Discount", value=0.0, step=0.1)
#     order_item_discount_rate = st.slider("Order Item Discount Rate (%)", 0, 100, 10)
#     order_item_profit_ratio = st.number_input("Order Item Profit Ratio", value=0.0, step=0.1)
#     order_item_quantity = st.number_input("Order Item Quantity", min_value=1, value=1, step=1)
#     sales = st.number_input("Sales", value=0.0)
#     order_profit_per_order = st.number_input("Order Profit per Order", value=0.0)
#     product_price = st.number_input("Product Price", value=0.0)

# # Expander for Payment Methods
# with st.expander("💳 Select Payment Method"):
#     type_cash = st.checkbox("Cash")
#     type_debit = st.checkbox("Debit Card")
#     type_payment = st.checkbox("Credit Card", value=True)  # Default
#     type_transfer = st.checkbox("Bank Transfer")

# # Expander for Customer Segment
# with st.expander("👥 Select Customer Segment"):
#     customer_segment_consumer = st.checkbox("Consumer", value=True)
#     customer_segment_corporate = st.checkbox("Corporate")
#     customer_segment_home_office = st.checkbox("Home Office")

# # Convert checkboxes to 1 (selected) or 0 (not selected)
# type_cash = int(type_cash)
# type_debit = int(type_debit)
# type_payment = int(type_payment)
# type_transfer = int(type_transfer)
# customer_segment_consumer = int(customer_segment_consumer)
# customer_segment_corporate = int(customer_segment_corporate)
# customer_segment_home_office = int(customer_segment_home_office)

# # Center-align the Predict button
# st.markdown("<br>", unsafe_allow_html=True)  # Add spacing

# # Predict Button
# if st.button("🚀 Predict Now", use_container_width=True):
#     data = {
#         "days_for_shipment_scheduled": days_for_shipment_scheduled,
#         "order_item_discount": order_item_discount,
#         "order_item_discount_rate": order_item_discount_rate,
#         "order_item_profit_ratio": order_item_profit_ratio,
#         "order_item_quantity": order_item_quantity,
#         "sales": sales,
#         "order_profit_per_order": order_profit_per_order,
#         "product_price": product_price,
#         "order_day_of_week": order_day_of_week,
#         "shipping_day_of_week": shipping_day_of_week,
#         "type_cash": type_cash,
#         "type_debit": type_debit,
#         "type_payment": type_payment,
#         "type_transfer": type_transfer,
#         "customer_segment_consumer": customer_segment_consumer,
#         "customer_segment_corporate": customer_segment_corporate,
#         "customer_segment_home_office": customer_segment_home_office,
#     }
    
#     response = requests.post("http://127.0.0.1:8000/predict1/", json=data)
    
#     if response.status_code == 200:
#         prediction = response.json()['prediction']
#         if prediction == 1:
#             st.error("🚨 **Supply Chain Failure Detected!** Immediate action required.")
#         else:
#             st.success("✅ **No Supply Chain Failure.** Everything is running smoothly.")
#     else:
#         st.error("❌ Error in prediction. Please try again.")


import streamlit as st
import requests
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from folium import CircleMarker
from matplotlib import cm, colors
import pandas as pd
import streamlit as st
import pandas as pd
import folium
from folium import Choropleth, GeoJsonTooltip, CircleMarker
from folium.plugins import HeatMap
from streamlit_folium import st_folium


st.set_page_config(page_title="Supply Chain Prediction", layout="centered")

st.title("📦 Supply Chain Geospatial Prediction Dashboard")

st.markdown("### Enter the required details below and get predictions instantly!")

# Add Images for Visualization
st.image("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/output1.png", caption="🛒 Store and Order Delivery Locations", use_container_width=True)
st.image("/Users/kdn_aisashwat/Desktop/supply_chain_resillience/output2.png", caption="🚚 Source-Destination Routes with Points", use_container_width=True)




# Dummy data (replace this with actual aggregated delay data)
csv_file = "/Users/kdn_aisashwat/Desktop/supply_chain_resillience/notebooks/aggregated_delay.csv"  # Change this to the actual file path
aggregated_delay = pd.read_csv(csv_file)

# Create Folium Map
m_2 = folium.Map(location=[20.9614, 6.6797], tiles="cartodb darkmatter", zoom_start=2)

# Define color mapping
min_delay = aggregated_delay['average_shipping_delay'].min()
max_delay = aggregated_delay['average_shipping_delay'].max()
norm = colors.Normalize(vmin=min_delay, vmax=max_delay)
cmap = cm.get_cmap('RdYlGn_r')

def get_color(delay):
    rgba = cmap(norm(delay)) 
    return colors.to_hex(rgba)

# Add circles for shipping delay
for idx, row in aggregated_delay.iterrows():
    delay = row.average_shipping_delay
    if not delay:
        continue
    CircleMarker(
        location=[row.latitude, row.longitude],
        radius=2 + 12 * abs(delay),
        tooltip=f'Country: {row.country}, Avg. Shipping Delay: {delay} Days',
        color=get_color(delay),
        fill=True,
        fill_opacity=0.8,
        stroke=True,
        weight=0.5
    ).add_to(m_2)

# Display Folium Map in Streamlit
st.markdown("### 🌍 Global Shipping Delay Map")
st_folium(m_2, width=700, height=500)





# Layout with two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Order & Shipment Details")
    days_for_shipment_scheduled = st.slider("Days for Shipment Scheduled", 1, 30, 3)
    order_day_of_week = st.slider("Order Day of Week", 0, 6, 3)
    shipping_day_of_week = st.slider("Shipping Day of Week", 0, 6, 3)

# with col2:
#     st.subheader("💰 Financial Details")
#     order_item_discount = st.number_input("Order Item Discount", value=0.0, step=0.1)
#     order_item_discount_rate = st.slider("Order Item Discount Rate (%)", 0, 100, 10)
#     order_item_profit_ratio = st.number_input("Order Item Profit Ratio", value=0.0, step=0.1)
#     order_item_quantity = st.number_input("Order Item Quantity", min_value=1, value=1, step=1)
#     sales = st.number_input("Sales", value=0.0)
#     order_profit_per_order = st.number_input("Order Profit per Order", value=0.0)
#     product_price = st.number_input("Product Price", value=0.0)

# Expander for Payment Methods
# with st.expander("💳 Select Payment Method"):
#     type_cash = st.checkbox("Cash")
#     type_debit = st.checkbox("Debit Card")
#     type_payment = st.checkbox("Credit Card", value=True)  # Default
#     type_transfer = st.checkbox("Bank Transfer")

# # Expander for Customer Segment
# with st.expander("👥 Select Customer Segment"):
#     customer_segment_consumer = st.checkbox("Consumer", value=True)
#     customer_segment_corporate = st.checkbox("Corporate")
#     customer_segment_home_office = st.checkbox("Home Office")

# Convert checkboxes to 1 (selected) or 0 (not selected)
# type_cash = int(type_cash)
# type_debit = int(type_debit)
# type_payment = int(type_payment)
# type_transfer = int(type_transfer)
# customer_segment_consumer = int(customer_segment_consumer)
# customer_segment_corporate = int(customer_segment_corporate)
# customer_segment_home_office = int(customer_segment_home_office)

# Center-align the Predict button
st.markdown("<br>", unsafe_allow_html=True)  # Add spacing

# Predict Button
if st.button("🚀 Predict Now", use_container_width=True):
    data = {
        "days_for_shipment_scheduled": days_for_shipment_scheduled,
        #"order_item_discount": order_item_discount,
        # "order_item_discount_rate": order_item_discount_rate,
        # "order_item_profit_ratio": order_item_profit_ratio,
        # "order_item_quantity": order_item_quantity,
        # "sales": sales,
        # "order_profit_per_order": order_profit_per_order,
        # "product_price": product_price,
        "order_day_of_week": order_day_of_week,
        "shipping_day_of_week": shipping_day_of_week,
        # "type_cash": type_cash,
        # "type_debit": type_debit,
        # "type_payment": type_payment,
        # "type_transfer": type_transfer,
        # "customer_segment_consumer": customer_segment_consumer,
        # "customer_segment_corporate": customer_segment_corporate,
        # "customer_segment_home_office": customer_segment_home_office,
    }
    
    response = requests.post("http://127.0.0.1:8000/predict1/", json=data)
    
    if response.status_code == 200:
        prediction = response.json()['prediction']
        if prediction == 1:
            st.error("🚨 **Supply Chain Failure Detected!** Immediate action required.")
        else:
            st.success("✅ **No Supply Chain Failure.** Everything is running smoothly.")
    else:
        st.error("❌ Error in prediction. Please try again.")
