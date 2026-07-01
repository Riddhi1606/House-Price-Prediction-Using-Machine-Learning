import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from datetime import datetime

#---------------- PAGE CONFIG ----------------
st.set_page_config(
page_title="House Price Prediction",
page_icon="🏡",
layout="wide",
initial_sidebar_state="auto"
)

#---------------- STYLES ----------------

st.markdown(
"""
<style>
:root{
--primary:#2E86C1;
--muted:#6c757d;
--card:#ffffff;
--bg:#f7fbff;
--accent:#f0f6fb;
}
.app-header{
display:flex;
align-items:center;
gap:16px;
background:linear-gradient(90deg, rgba(46,134,193,0.12), rgba(46,134,193,0.04));
padding:18px;
border-radius:12px;
margin-bottom:18px;
}
.app-title{ font-size:30px; font-weight:700; color:var(--primary); margin:0; }
.app-sub{ color:var(--muted); margin:0; font-size:13px; }
.metric-box{ background:var(--card); padding:14px; border-radius:10px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.small-muted{ color:var(--muted); font-size:13px; }
.stButton>button { background-color:var(--primary); border: none; color: white; }
/* make charts responsive inside cards */
.chart-card { background:var(--card); padding:12px; border-radius:10px; box-shadow: 0 1px 6px rgba(16,24,40,0.04); }
</style>
""",
unsafe_allow_html=True,
)

#---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model(path="house_price_model.pkl"):
 return joblib.load(path)

model = load_model()

#---------------- HEADER ----------------
st.markdown(
"""
<div class="app-header">
<div style="font-size:32px">🏡</div>
<div>
<p class="app-title">House Price Prediction</p>
<p class="app-sub">Estimate property value with an explainable ML model — enter property details and get instant insights.</p>
</div>
</div>
""",
unsafe_allow_html=True
)

#---------------- SIDEBAR ----------------
st.sidebar.header("About this project")
st.sidebar.info(
"Random Forest Regressor trained on tabular housing features. Use the inputs to the right (or open the example presets) and press Predict."
)
st.sidebar.markdown("### Dataset features")
st.sidebar.write(
"- Square footage\n- Bedrooms\n- Bathrooms\n- Year built\n- Neighborhood tier\n- Pool availability\n- Distance to transit (km)\n- Garage capacity"
)
st.sidebar.markdown("---")
st.sidebar.write("Tech: Python, scikit-learn, Streamlit, Plotly, joblib")
st.sidebar.success("AI & ML Project — Developed by Riddhi Sharma")
st.sidebar.caption("Tip: Use the Example presets to quickly try common property types.")

# ---------------- EXAMPLE PRESETS ----------------
presets = {
"Select a preset": None,
"Urban Premium (Large house)": {
"square_footage": 4200, "num_bedrooms": 5, "num_bathrooms": 4,
"year_built": 2015, "neighborhood_tier": 2, "has_pool": 1,
"distance_to_transit": 1.0, "garage_capacity": 3
},
"Suburban Mid (Family home)": {
"square_footage": 2000, "num_bedrooms": 3, "num_bathrooms": 2,
"year_built": 2005, "neighborhood_tier": 1, "has_pool": 0,
"distance_to_transit": 6.0, "garage_capacity": 2
},
"Budget Condo": {
"square_footage": 850, "num_bedrooms": 1, "num_bathrooms": 1,
"year_built": 1998, "neighborhood_tier": 0, "has_pool": 0,
"distance_to_transit": 0.5, "garage_capacity": 0
}
}

preset_choice = st.selectbox("Example presets", options=list(presets.keys()))
preset = presets[preset_choice]

# ---------------- INPUTS (MAIN) ----------------
st.subheader("Property Information")
with st.form("property_form"):
col1, col2, col3 = st.columns()

with col1:
property_id = st.number_input("Property ID", min_value=0, max_value=999999, value=100, help="Unique numeric ID for this property (optional).")
square_footage = st.slider("Square Footage (sq ft)", 500, 10000, value=2500, step=50, help="Total built-up or carpet area.")
num_bedrooms = st.slider("Bedrooms", 0, 10, value=3, help="Number of bedrooms.")

with col2:
num_bathrooms = st.slider("Bathrooms", 0.5, 6.0, value=2.0, step=0.5, help="Number of bathrooms (can be fractional).")
year_built = st.slider("Year Built", 1900, datetime.now().year, value=2000, help="Construction year of the property.")
neighborhood = st.selectbox("Neighborhood Tier", ["Low", "Medium", "High"], index=1, help="Relative socioeconomic tier of the neighborhood.")

with col3:
pool = st.selectbox("Swimming Pool", ["No", "Yes"], index=0, help="Does the property have a pool?")
distance_to_transit = st.slider("Distance to Transit (km)", 0.0, 20.0, value=5.0, step=0.1, help="Walking distance to the nearest transit in kilometers.")
garage_capacity = st.slider("Garage Capacity (cars)", 0, 6, value=2, help="Number of cars that can fit in the garage.")

# Populate from preset if chosen
if preset is not None:
square_footage = st.session_state.get("square_footage", preset["square_footage"])
num_bedrooms = st.session_state.get("num_bedrooms", preset["num_bedrooms"])
num_bathrooms = st.session_state.get("num_bathrooms", preset["num_bathrooms"])
year_built = st.session_state.get("year_built", preset["year_built"])
neighborhood = ("Low","Medium","High")[preset["neighborhood_tier"]]
pool = "Yes" if preset["has_pool"] else "No"
distance_to_transit = st.session_state.get("distance_to_transit", preset["distance_to_transit"])
garage_capacity = st.session_state.get("garage_capacity", preset["garage_capacity"])

submit_btn = st.form_submit_button("🚀 Predict House Price")

map neighborhood
neighborhood_map = {"Low": 0, "Medium": 1, "High": 2}
neighborhood_tier = neighborhood_map.get(neighborhood, 1)
has_pool = 1 if pool == "Yes" else 0

# ---------------- PROPERTY PROFILE (RADAR) ----------------
st.markdown("---")
st.subheader("Property Profile")
area_score = min(square_footage / 10000, 1.0)
bed_score = min(num_bedrooms / 10, 1.0)
bath_score = min(num_bathrooms / 6, 1.0)
garage_score = min(garage_capacity / 6, 1.0)
age_score = min((datetime.now().year - year_built) / 100, 1.0)
pool_score = has_pool

radar_values = [area_score, bed_score, bath_score, garage_score, age_score, pool_score]
radar_labels = ["Area", "Bedrooms", "Bathrooms", "Garage", "Age", "Pool"]

radar_fig = go.Figure()
radar_fig.add_trace(
go.Scatterpolar(
r=radar_values + radar_values[:1],
theta=radar_labels + radar_labels[:1],
fill="toself",
name="Profile",
line_color="#2E86C1"
)
)
radar_fig.update_layout(
polar=dict(radialaxis=dict(visible=True, range=)),

showlegend=False,
margin=dict(l=20, r=20, t=20, b=20),
height=380
)

col_a, col_b = st.columns()

with col_a:
st.plotly_chart(radar_fig, use_container_width=True)
with col_b:
st.markdown("### Quick facts")
st.write(f"- Year built: {year_built}")
st.write(f"- Neighborhood tier: {neighborhood}")
st.write(f"- Distance to transit: {distance_to_transit} km")
st.write(f"- Garage capacity: {garage_capacity}")

# ---------------- PREDICTION ----------------
if submit_btn:
input_df = pd.DataFrame({
"property_id": [int(property_id)],
"square_footage": [int(square_footage)],
"num_bedrooms": [int(num_bedrooms)],
"num_bathrooms": [float(num_bathrooms)],
"year_built": [int(year_built)],
"neighborhood_tier": [int(neighborhood_tier)],
"has_pool": [int(has_pool)],
"distance_to_transit": [float(distance_to_transit)],
"garage_capacity": [int(garage_capacity)]
})

pred = model.predict(input_df)
pred = int(pred)

if pred < 200000:
category = "Budget"
elif pred < 400000:
category = "Mid Range"
elif pred < 700000:
category = "Premium"
elif pred < 1000000:
category = "Luxury"
else:
category = "Ultra Luxury"

age = datetime.now().year - year_built

st.markdown("---")
st.subheader("Prediction Results")

m1, m2, m3 = st.columns(3)
with m1:
st.markdown('<div class="metric-box">', unsafe_allow_html=True)
st.metric(label="Predicted Price", value=f"${pred:,.0f}")
st.markdown('</div>', unsafe_allow_html=True)
with m2:
st.markdown('<div class="metric-box">', unsafe_allow_html=True)
st.metric(label="Category", value=category)
st.markdown('</div>', unsafe_allow_html=True)
with m3:
st.markdown('<div class="metric-box">', unsafe_allow_html=True)
st.metric(label="Property Age", value=f"{age} years")
st.markdown('</div>', unsafe_allow_html=True)

# Progress bar scaled to $1,000,000
progress_val = min(max(int(pred / 10000), 0), 100)
st.progress(progress_val)

# Gauge (improved styling)
gauge = go.Figure(
go.Indicator(
mode="gauge+number+delta",
value=pred,
delta={'reference': 400000, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
number={'prefix': "$", 'valueformat': ",.0f"},
gauge={
'axis': {'range': },
'steps': [
{'range': , 'color': '#e6f2ff'},
{'range': , 'color': '#cfe9ff'},
{'range': , 'color': '#a3d1ff'},
{'range': , 'color': '#66b0ff'},
{'range': , 'color': '#2E86C1'},
],
'bar': {'color': "#0b63a8"}
}
)
)
gauge.update_layout(height=360, margin=dict(l=20, r=20, t=20, b=20))

st.plotly_chart(gauge, use_container_width=True)

# AI Insights
st.subheader("AI Insights")
insights = []
if square_footage > 3000:
insights.append("Large area increases price.")
if num_bedrooms >= 4:
insights.append("More bedrooms positively affect value.")
if has_pool:
insights.append("Swimming pool adds premium value.")
if garage_capacity >= 2:
insights.append("Garage capacity improves valuation.")
if neighborhood_tier == 2:
insights.append("Premium neighborhood boosts market price.")
if distance_to_transit < 3:
insights.append("Excellent transit access.")

for ins in insights:
st.write(f"✅ {ins}")

st.subheader("Input Summary")
st.dataframe(input_df, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("House Price Prediction - Riddhi Sharma - Built with Streamlit & scikit-learn")
