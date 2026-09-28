import streamlit as st
import joblib
import numpy as np
import shap
import matplotlib.pyplot as plt

# ---------- CONFIG ----------

st.set_page_config(
    page_title="PCOS App",
    layout="wide"
)

# ---------- LOAD MODEL ----------

model = joblib.load("pcos_model.pkl")
explainer = shap.TreeExplainer(model)

# ---------- HEADER ----------

st.markdown("""
<h1 style='text-align:center; color:#0a3d62;'>PCOS Health Assistant</h1>
<p style='text-align:center; font-size:18px;'>
Smart AI-based Women's Health Companion
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- LAYOUT ----------

col1, col2 = st.columns([1, 1])

# ---------- LEFT SIDE ----------

with col1:

    st.markdown("## 🧪 PCOS Prediction")

    age = st.number_input(
        "Age",
        min_value=10,
        max_value=60,
        value=21
    )

    height = st.number_input(
        "Height (cm)",
        min_value=100.0,
        max_value=220.0,
        value=160.0,
        step=0.1
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=20.0,
        max_value=150.0,
        value=50.0,
        step=0.1
    )

    # Auto BMI Calculation
    bmi = weight / ((height / 100) ** 2)

    predict = st.button("Check Health")

    if predict:

        if age <= 0 or weight <= 0 or bmi <= 0:
            st.warning("⚠️ Enter valid values")

        else:
            data = np.array([[age, weight, bmi]])

            result = model.predict(data)
            prob = model.predict_proba(data)[0][1]

            # RESULT
            if result[0] == 1:
                st.warning("⚠️ There may be a risk of PCOS")
            else:
                st.success("✅ You are in a healthy range")

            st.write(f"📊 Risk Level: {prob*100:.2f}%")

            st.markdown("---")
            # ---------- SUGGESTIONS ----------
            st.subheader("💡 Personalized Suggestions")

            if result[0] == 1:
                st.write("⚠️ Based on your result, consider the following:")
                st.write("🥗 Maintain a balanced diet (low sugar, high fiber)")
                st.write("🏃‍♀️ Exercise regularly (30–45 minutes daily)")
                st.write("🧘 Practice stress management techniques")
                st.write("💧 Stay hydrated and maintain a healthy weight")
                st.write("👩‍⚕️ Consult a gynecologist for further evaluation")
            else:
                st.write("✅ You are doing well! Keep maintaining:")
                st.write("🥗 Healthy and balanced diet")
                st.write("🏃‍♀️ Regular physical activity")
                st.write("🩺 Routine health checkups")
                st.write("😌 Stress-free lifestyle")

            st.markdown("---")

            # ---------- SHAP ----------
            st.subheader("🔍 Factors Influencing Prediction")

            shap_values = explainer.shap_values(data)

            if isinstance(shap_values, list):
                shap_vals = shap_values[1][0]
            else:
                shap_vals = shap_values[0]

            if len(shap_vals.shape) > 1:
                shap_vals = shap_vals[:, 1]

            features = ["Age", "Weight", "BMI"]

            fig, ax = plt.subplots()
            ax.barh(features, shap_vals, color=["#ff4b6e","#ff9f43","#1dd1a1"])
            ax.set_xlabel("Impact")
            ax.set_title("Feature Contribution")

            st.pyplot(fig)

# ---------- RIGHT SIDE (PREMIUM INFO UI) ----------
with col2:

    st.markdown("""
    <div style="
        background:#24384d;
        border:1px solid #3b6ea5;
        border-radius:18px;
        padding:25px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.3);
    ">
        <h2 style="color:white;">📊 BMI Calculator</h2>
    </div>
    """, unsafe_allow_html=True)

    st.metric(
        label="Your BMI",
        value=f"{bmi:.2f}"
    )

    if bmi < 18.5:
        st.info("🔵 Underweight")
    elif bmi < 25:
        st.success("🟢 Normal Weight")
    elif bmi < 30:
        st.warning("🟡 Overweight")
    else:
        st.error("🔴 Obese")

    st.markdown("---")

    st.subheader("📌 BMI Categories")

    st.markdown("""
| BMI | Category |
|------|----------|
| Below 18.5 | 🔵 Underweight |
| 18.5 – 24.9 | 🟢 Normal Weight |
| 25 – 29.9 | 🟡 Overweight |
| 30+ | 🔴 Obese |
""")