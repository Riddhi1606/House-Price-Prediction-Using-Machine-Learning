import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------

@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

# ---------------- CSS ----------------

st.markdown("""
<style>

.big-title{
font-size:58px;
font-weight:800;
color:#2E86C1;
text-align:center;
}

.subtitle{
font-size:20px;
color:gray;
text-align:center;
margin-bottom:25px;
}

.metric-box{
padding:20px;
border-radius:15px;
background:#f8f9fa;
box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown(
"""
<div class='big-title'>
🏡 House Price Prediction
</div>

<div class='subtitle'>
AI Powered Real Estate Valuation System
</div>
""",
unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("📌 Project Overview")

st.sidebar.info("""

Random Forest Regressor

Dataset Features

• Square Footage

• Bedrooms

• Bathrooms

• Year Built

• Neighborhood Tier

• Pool

• Transit Access

• Garage Capacity

""")

st.sidebar.success("Developed by Riddhi Sharma")

# ---------------- INPUTS ----------------

st.subheader("Property Information")

col1,col2,col3 = st.columns(3)

with col1:

    property_id = st.number_input(
        "Property ID",
        0,
        999999,
        100
    )

    square_footage = st.slider(
        "Square Footage",
        500,
        10000,
        2500
    )

    num_bedrooms = st.slider(
        "Bedrooms",
        1,
        10,
        3
    )

with col2:

    num_bathrooms = st.slider(
        "Bathrooms",
        1.0,
        6.0,
        2.0,
        0.5
    )

    year_built = st.slider(
        "Year Built",
        1900,
        datetime.now().year,
        2000
    )

    neighborhood = st.selectbox(

        "Neighborhood Tier",

        ["Low","Medium","High"]

    )

with col3:

    pool = st.selectbox(

        "Swimming Pool",

        ["No","Yes"]

    )

    distance_to_transit = st.slider(

        "Distance to Transit (km)",

        0.0,

        20.0,

        5.0

    )

    garage_capacity = st.slider(

        "Garage Capacity",

        0,

        6,

        2

    )

# ---------------- ENCODING ----------------

neighborhood_map = {

    "Low":0,

    "Medium":1,

    "High":2

}

neighborhood_tier = neighborhood_map[neighborhood]

has_pool = 1 if pool=="Yes" else 0

# ---------------- RADAR CHART ----------------

st.markdown("---")

st.subheader("Property Profile")

values=[

square_footage/10000,

num_bedrooms/10,

num_bathrooms/6,

garage_capacity/6,

has_pool,

1-(distance_to_transit/20)

]

labels=[

"Area",

"Bedrooms",

"Bathrooms",

"Garage",

"Pool",

"Transit"

]

fig = go.Figure()

fig.add_trace(

go.Scatterpolar(

r=values+[values[0]],

theta=labels+[labels[0]],

fill='toself',

line_color='#2E86C1'

)

)

fig.update_layout(

polar=dict(

radialaxis=dict(

visible=True,

range=[0,1]

)

),

showlegend=False,

height=400

)

st.plotly_chart(

fig,

use_container_width=True

)

# ---------------- PREDICTION ----------------

if st.button(

"🚀 Predict House Price",

use_container_width=True

):

    input_df = pd.DataFrame({

        "property_id":[property_id],

        "square_footage":[square_footage],

        "num_bedrooms":[num_bedrooms],

        "num_bathrooms":[num_bathrooms],

        "year_built":[year_built],

        "neighborhood_tier":[neighborhood_tier],

        "has_pool":[has_pool],

        "distance_to_transit":[distance_to_transit],

        "garage_capacity":[garage_capacity]

    })

    prediction = float(

        model.predict(

            input_df

        )[0]

    )

    age = datetime.now().year-year_built

    if prediction<200000:

        category="Affordable"

    elif prediction<400000:

        category="Mid Range"

    elif prediction<700000:

        category="Premium"

    elif prediction<1000000:

        category="Luxury"

    else:

        category="Ultra Luxury"

    st.markdown("---")

    st.subheader(

        "Prediction Results"

    )

    c1,c2,c3=st.columns(3)

    with c1:

        st.metric(

            "Predicted Price",

            f"${prediction:,.0f}"

        )

    with c2:

        st.metric(

            "Category",

            category

        )

    with c3:

        st.metric(

            "Property Age",

            f"{age} Years"

        )

    st.progress(

        min(

            int(

                prediction/

                10000

            ),

            100

        )

    )

    gauge = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=prediction,

            number={

                'prefix':"$"

            },

            gauge={

                'axis':{

                    'range':[0,1000000]

                },

                'bar':{

                    'color':'#2E86C1'

                }

            }

        )

    )

    gauge.update_layout(

        height=350

    )

    st.plotly_chart(

        gauge,

        use_container_width=True

    )

    st.subheader(

        "AI Insights"

    )

    if square_footage>3000:

        st.success(

            "Large property size positively impacts price."

        )

    if has_pool:

        st.success(

            "Swimming pool increases valuation."

        )

    if neighborhood_tier==2:

        st.success(

            "Premium neighborhood boosts market value."

        )

    if garage_capacity>=2:

        st.success(

            "Garage capacity contributes positively."

        )

    if distance_to_transit<3:

        st.success(

            "Excellent transit connectivity."

        )

    st.subheader(

        "Input Summary"

    )

    st.dataframe(

        input_df,

        use_container_width=True

    )

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(

"🏡 House Price Prediction | Built with Streamlit, Random Forest & Plotly"

)
