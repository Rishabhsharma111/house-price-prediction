import streamlit as st
import pickle
import pandas as pd
import os

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="HomeValue AI",
    page_icon="🏠",
    layout="centered"
)

# -------------------------------
# Styling
# -------------------------------
st.markdown("""
<style>
h1, h2, h3 {
    font-family: Arial;
}
.block-container {
    padding-top: 2rem;
}
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    font-size: 18px;
    border-radius: 10px;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Model
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))
columns = pickle.load(open(os.path.join(BASE_DIR, "columns.pkl"), "rb"))

# -------------------------------
# Branding
# -------------------------------
st.title("🏠 HomeValue AI")
st.caption("Smart ML-based house price predictor")

st.markdown("---")

# -------------------------------
# Input Sections
# -------------------------------
st.markdown("### 📐 Property Details")

lot_area = st.number_input("🏡 Lot Area (sq ft)", 500, 50000, 9000)
gr_liv_area = st.number_input("📐 Living Area (sq ft)", 300, 5000, 1500)

st.markdown("### 🏗️ Construction Details")

year_built = st.number_input("📅 Year Built", 1900, 2025, 2000)
overall_qual = st.slider("⭐ Quality (1-10)", 1, 10, 5)

location = st.selectbox("🌍 Location Type", ["Urban", "Suburban", "Rural"])

st.markdown("---")

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict Price 💰"):

    if lot_area < 500:
        st.warning("Lot area too small!")
    else:
        with st.spinner("Analyzing property data... ⏳"):

            input_df = pd.DataFrame(columns=columns)
            input_df.loc[0] = 0

            input_df["LotArea"] = lot_area
            input_df["OverallQual"] = overall_qual
            input_df["YearBuilt"] = year_built
            input_df["GrLivArea"] = gr_liv_area

            prediction = model.predict(input_df)[0]

            low = prediction * 0.9
            high = prediction * 1.1

            # -------------------------------
            # Result Section (PRO 🔥)
            # -------------------------------
            st.markdown("### 💰 Prediction Result")

            st.metric("Estimated Price", f"₹ {prediction:,.0f}")
            st.info(f"📊 Price Range: ₹ {low:,.0f} - ₹ {high:,.0f}")

            st.caption("⚠️ This is an estimated price based on trained ML model")

            # -------------------------------
            # Smart Insight
            # -------------------------------
            if overall_qual >= 8:
                st.success("🏆 High quality house → Higher price expected")
            elif overall_qual <= 4:
                st.warning("⚠️ Low quality → Lower price expected")

            # -------------------------------
            # Input Summary
            # -------------------------------
            summary = {
                "Lot Area": lot_area,
                "Living Area": gr_liv_area,
                "Year Built": year_built,
                "Quality": overall_qual,
                "Location": location
            }

            st.markdown("### 📋 Input Summary")
            st.table(pd.DataFrame([summary]))

            # -------------------------------
            # Save History
            # -------------------------------
            if "history" not in st.session_state:
                st.session_state.history = []

            st.session_state.history.append(prediction)

# -------------------------------
# History Section
# -------------------------------
st.markdown("---")
st.markdown("### 📜 Recent Predictions")

if "history" in st.session_state:
    for i, val in enumerate(st.session_state.history[-5:][::-1]):
        st.write(f"{i+1}. ₹ {val:,.0f}")

# -------------------------------
# Reset Button
# -------------------------------
if st.button("Reset 🔄"):
    st.rerun()

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Developed by Rishabh Sharma | ML Project 🚀")