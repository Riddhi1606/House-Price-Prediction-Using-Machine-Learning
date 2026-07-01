import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏡",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.main-title{
font-size:42px;
font-weight:700;
color:#2E86C1;
text-align:center;
}

.subtitle{
font-size:18px;
text-align:center;
color:gray;
margin-bottom:25px;
}

.metric-box{
padding:20px;
border-radius:15px;
text-align:center;
color:white;
}

.metric-value{
font-size:32px;
font-weight:bold;
}

.metric-label{
font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- MODEL ----------------

model = joblib.load("house_price_model.pkl")

# ---------------- HEADER ----------------

st.markdown(
'<p class="main-title">🏡 House Price Prediction System</p>',
unsafe_allow_html=True
)

st.markdown(
'<p class="subtitle">Predict Property Prices using Machine Learning</p>',
unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("📌 About Project")

st.sidebar.info("""

Model Used

Random Forest Regressor


Dataset Features

• Square Footage

• Bedrooms

• Bathrooms

• Year Built

• Neighborhood Tier

• Pool Availability

• Transit Distance

• Garage Capacity


Technologies

Python

Scikit-Learn

Plotly

Streamlit

Joblib

""")

st.sidebar.markdown("---")

st.sidebar.success("AI & ML Project")

# ---------------- INPUTS ----------------

st.subheader("Property Information")

c1,c2,c3 = st.columns(3)

with c1:

    property_id = st.number_input(
        "Property ID",
        0,
        100000,
        100
    )

    square_footage = st.slider(
        "Square Footage",
        500,
        6000,
        2500
    )

    num_bedrooms = st.slider(
        "Bedrooms",
        1,
        10,
        3
    )

with c2:

    num_bathrooms = st.slider(
        "Bathrooms",
        1.0,
        6.0,
        2.0
    )

    year_built = st.slider(
        "Year Built",
        1950,
        2025,
        2000
    )

    neighborhood = st.selectbox(

        "Neighborhood Tier",

        ["Low","Medium","High"]

    )

    neighborhood_map = {

        "Low":0,

        "Medium":1,

        "High":2

    }

    neighborhood_tier = neighborhood_map[neighborhood]

with c3:

    pool = st.selectbox(

        "Swimming Pool",

        ["No","Yes"]

    )

    has_pool = 1 if pool=="Yes" else 0

    distance_to_transit = st.slider(

        "Distance to Transit",

        0.0,

        20.0,

        5.0

    )

    garage_capacity = st.slider(

        "Garage Capacity",

        0,

        5,

        2

    )

# ---------------- RADAR ----------------

st.markdown("---")

st.subheader("Property Profile")

values = [

square_footage/6000,

num_bedrooms/10,

num_bathrooms/6,

garage_capacity/5,

(2025-year_built)/75,

has_pool

]

labels = [

"Area",

"Bedrooms",

"Bathrooms",

"Garage",

"Age",

"Pool"

]

fig = go.Figure()

fig.add_trace(

go.Scatterpolar(

r=values+values[:1],

theta=labels+labels[:1],

fill='toself'

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

# ---------------- PREDICT ----------------

predict = st.button(

"🚀 Predict House Price",

use_container_width=True

)

if predict:

    data = pd.DataFrame({

        'property_id':[property_id],

        'square_footage':[square_footage],

        'num_bedrooms':[num_bedrooms],

        'num_bathrooms':[num_bathrooms],

        'year_built':[year_built],

        'neighborhood_tier':[neighborhood_tier],

        'has_pool':[has_pool],

        'distance_to_transit':[distance_to_transit],

        'garage_capacity':[garage_capacity]

    })

    prediction = model.predict(data)[0]

    prediction = int(prediction)

    if prediction < 200000:

        category = "Budget"

    elif prediction < 400000:

        category = "Mid Range"

    elif prediction < 700000:

        category = "Premium"

    elif prediction < 1000000:

        category = "Luxury"

    else:

        category = "Ultra Luxury"

    st.markdown("---")

    st.subheader("Prediction Results")

    a,b,c = st.columns(3)

    with a:

        st.metric(

            "Predicted Price",

            f"${prediction:,.0f}"

        )

    with b:

        st.metric(

            "Category",

            category

        )

    with c:

        age = 2025-year_built

        st.metric(

            "Property Age",

            age

        )

    st.progress(

        min(

            int(

                prediction/10000

            ),

            100

        )

    )

    # Gauge

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

                    'color':"#2E86C1"

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

    insights=[]

    if square_footage>3000:

        insights.append(

            "✅ Large area increases price."

        )

    if num_bedrooms>=4:

        insights.append(

            "✅ More bedrooms positively affect value."

        )

    if has_pool:

        insights.append(

            "✅ Swimming pool adds premium value."

        )

    if garage_capacity>=2:

        insights.append(

            "✅ Garage capacity improves valuation."

        )

    if neighborhood_tier==2:

        insights.append(

            "✅ Premium neighborhood boosts market price."

        )

    if distance_to_transit<3:

        insights.append(

            "✅ Excellent transit access."

        )

    for i in insights:

        st.write(i)

    st.subheader(

        "Property Summary"

    )

    st.dataframe(

        data,

        use_container_width=True

    )

# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(

"🏡 House Price Prediction System | RIDDHI SHARMA | AI & ML Project"

)
