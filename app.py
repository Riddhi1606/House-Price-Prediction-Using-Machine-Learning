import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- THEME / CSS ----------------
st.markdown("""
<style>
    .main {
        background: #f7faff;
    }

    .hero {
        background: linear-gradient(135deg, #0f62fe 0%, #2E86C1 100%);
        padding: 28px 28px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 10px 30px rgba(15, 98, 254, 0.18);
        margin-bottom: 24px;
    }

    .hero h1 {
        margin: 0;
        font-size: 36px;
        font-weight: 800;
        line-height: 1.2;
    }

    .hero p {
        margin: 8px 0 0 0;
        font-size: 15px;
        opacity: 0.92;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #1f2d3d;
        margin-bottom: 8px;
    }

    .section-subtitle {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .card {
        background: white;
        border: 1px solid rgba(15, 23, 42, 0.06);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
    }

    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 18px 16px;
        box-shadow: 0 4px 18px rgba(15, 23, 42, 0.05);
        border: 1px solid rgba(15, 23, 42, 0.06);
    }

    .stButton > button {
        background: linear-gradient(135deg, #0f62fe 0%, #2E86C1 100%);
        color: white;
        border: none;
        border-radius: 14px;
        font-weight: 700;
        padding: 0.75rem 1rem;
        box-shadow: 0 8px 20px rgba(15, 98, 254, 0.20);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 24px rgba(15, 98, 254, 0.25);
    }

    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 13px;
        margin-top: 18px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>🏡 House Price Prediction System</h1>
    <p>Estimate property prices instantly using machine learning with a clean and modern dashboard.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Project Info")
st.sidebar.info("A polished ML app for predicting house prices using a Random Forest Regressor.")
st.sidebar.markdown("### Features")
st.sidebar.write(
    "- Square footage\n"
    "- Bedrooms\n"
    "- Bathrooms\n"
    "- Year built\n"
    "- Neighborhood tier\n"
    "- Pool availability\n"
    "- Distance to transit\n"
    "- Garage capacity"
)
st.sidebar.markdown("### Technology Stack")
st.sidebar.write("Python • Streamlit • pandas • scikit-learn • Plotly • joblib")
st.sidebar.success("AI & ML Project by Riddhi Sharma")

# ---------------- PRESETS ----------------
st.markdown("## Property Details")
st.caption("Use the inputs below to generate a price prediction. You can also try a preset example.")

preset = st.selectbox(
    "Choose a sample property",
    ["Custom", "Budget Condo", "Family Home", "Luxury Villa"]
)

preset_values = {
    "Budget Condo": {
        "square_footage": 900, "num_bedrooms": 1, "num_bathrooms": 1.0,
        "year_built": 1998, "neighborhood": "Low", "pool": "No",
        "distance_to_transit": 0.8, "garage_capacity": 0
    },
    "Family Home": {
        "square_footage": 2200, "num_bedrooms": 3, "num_bathrooms": 2.0,
        "year_built": 2008, "neighborhood": "Medium", "pool": "No",
        "distance_to_transit": 4.5, "garage_capacity": 2
    },
    "Luxury Villa": {
        "square_footage": 5200, "num_bedrooms": 5, "num_bathrooms": 4.5,
        "year_built": 2019, "neighborhood": "High", "pool": "Yes",
        "distance_to_transit": 1.2, "garage_capacity": 3
    }
}

vals = preset_values.get(preset, {})

# ---------------- INPUTS ----------------
with st.form("prediction_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        property_id = st.number_input("Property ID", 0, 999999, 100, help="Unique identifier for the property.")
        square_footage = st.slider("Square Footage", 500, 10000, vals.get("square_footage", 2500), step=50)
        num_bedrooms = st.slider("Bedrooms", 0, 10, vals.get("num_bedrooms", 3))

    with c2:
        num_bathrooms = st.slider("Bathrooms", 0.5, 6.0, vals.get("num_bathrooms", 2.0), step=0.5)
        year_built = st.slider("Year Built", 1900, datetime.now().year, vals.get("year_built", 2000))
        neighborhood = st.selectbox("Neighborhood Tier", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(vals.get("neighborhood", "Medium")))

    with c3:
        pool = st.selectbox("Swimming Pool", ["No", "Yes"], index=0 if vals.get("pool", "No") == "No" else 1)
        distance_to_transit = st.slider("Distance to Transit (km)", 0.0, 20.0, vals.get("distance_to_transit", 5.0), step=0.1)
        garage_capacity = st.slider("Garage Capacity", 0, 6, vals.get("garage_capacity", 2))

    submit = st.form_submit_button("🚀 Predict House Price")

neighborhood_map = {"Low": 0, "Medium": 1, "High": 2}
neighborhood_tier = neighborhood_map[neighborhood]
has_pool = 1 if pool == "Yes" else 0

# ---------------- PROFILE SECTION ----------------
st.markdown("### Property Profile")
st.caption("A quick visual snapshot of the property features.")

radar_values = [
    min(square_footage / 10000, 1),
    min(num_bedrooms / 10, 1),
    min(num_bathrooms / 6, 1),
    min(garage_capacity / 6, 1),
    min((datetime.now().year - year_built) / 100, 1),
    has_pool
]

labels = ["Area", "Bedrooms", "Bathrooms", "Garage", "Age", "Pool"]

radar = go.Figure()
radar.add_trace(go.Scatterpolar(
    r=radar_values + radar_values[:1],
    theta=labels + labels[:1],
    fill="toself",
    line=dict(color="#0f62fe", width=3),
    fillcolor="rgba(15, 98, 254, 0.22)"
))
radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="lightgray")),
    margin=dict(l=20, r=20, t=20, b=20),
    height=380,
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.plotly_chart(radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("**Quick Summary**")
    st.write(f"**Year Built:** {year_built}")
    st.write(f"**Neighborhood:** {neighborhood}")
    st.write(f"**Pool:** {pool}")
    st.write(f"**Transit Distance:** {distance_to_transit} km")
    st.write(f"**Garage:** {garage_capacity} cars")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
if submit:
    input_data = pd.DataFrame({
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

    prediction = int(model.predict(input_data)[0])
    age = datetime.now().year - year_built

    if prediction < 200000:
        category = "Budget"
        color = "#16a34a"
    elif prediction < 400000:
        category = "Mid Range"
        color = "#0284c7"
    elif prediction < 700000:
        category = "Premium"
        color = "#7c3aed"
    elif prediction < 1000000:
        category = "Luxury"
        color = "#c2410c"
    else:
        category = "Ultra Luxury"
        color = "#991b1b"

    st.markdown("---")
    st.markdown("## Prediction Results")
    st.caption("The estimated market price and a simple category based on the predicted value.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Predicted Price", f"${prediction:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Price Category", category)
        st.markdown('</div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Property Age", f"{age} years")
        st.markdown('</div>', unsafe_allow_html=True)

    st.progress(min(int(prediction / 10000), 100))

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        number={"prefix": "$", "valueformat": ",.0f"},
        gauge={
            "axis": {"range": [0, 1200000]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, 200000], "color": "#eef6ff"},
                {"range": [200000, 400000], "color": "#dbeafe"},
                {"range": [400000, 700000], "color": "#c7d2fe"},
                {"range": [700000, 1000000], "color": "#e9d5ff"},
                {"range": [1000000, 1200000], "color": "#fecaca"},
            ],
        }
    ))
    gauge.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(gauge, use_container_width=True)

    st.markdown("## AI Insights")
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

    if insights:
        for item in insights:
            st.success(f"✅ {item}")
    else:
        st.info("No strong premium features detected for this property.")

    st.markdown("## Input Summary")
    st.dataframe(input_data, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown('<div class="footer">House Price Prediction System • Riddhi Sharma • AI & ML Project</div>', unsafe_allow_html=True)
