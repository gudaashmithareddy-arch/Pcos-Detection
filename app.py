import streamlit as st
from PIL import Image

# ================= SESSION STATE =================


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PCOS Analytics & AI Platform",
    layout="wide"
)


# ================= SIDEBAR DESIGN =================

st.sidebar.markdown("""
<style>

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071226 0%, #0b1830 100%);
}

/* Sidebar motivational card */
.sidebar-card {
    background: linear-gradient(145deg, #152945, #0e1d35);
    border: 1px solid #29466e;
    border-radius: 14px;
    padding: 16px 14px 10px 14px;
    margin-top: 25px;
    margin-bottom: 10px;
    text-align: left;
    box-shadow: 0 3px 12px rgba(0,0,0,0.25);
}

.sidebar-card-title {
    color: white;
    font-size: 17px;
    font-weight: 600;
    line-height: 1.7;
    margin-bottom: 8px;
}

.sidebar-card-title span {
    color: #ff8fb3;
}

/* Sidebar woman image */
[data-testid="stSidebar"] [data-testid="stImage"] img {
    border-radius: 12px;
    width: 100%;
    object-fit: cover;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR MOTIVATIONAL CARD ----------------

st.sidebar.markdown("""
<div class="sidebar-card">
    <div class="sidebar-card-title">
        <span>♡</span> Early Detection.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Better Care.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;Healthier Lives.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR WOMAN IMAGE ----------------

st.sidebar.image(
    "pcos_sidebar_woman.png",
    use_container_width=True
)


# ---------------- REMOVE PADDING ----------------

st.markdown("""
<style>

/* Main page */
.block-container{
    max-width:100%;
    padding-top:0.5rem;
    padding-left:0.8rem;
    padding-right:0.8rem;
    padding-bottom:2rem;
}

/* Remove top spacing */
header{
    visibility:hidden;
}

/* Remove footer */
footer{
    visibility:hidden;
}

/* Stretch image */
[data-testid="stImage"] img{
    width:100% !important;
    border-radius:15px;
}

/* Remove extra gap */
[data-testid="stImage"]{
    margin-top:0rem;
    margin-bottom:1rem;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HERO IMAGE ----------------

hero = Image.open("hero.png")

# Resize to banner
hero = hero.resize((1500, 450))

st.image(hero, use_container_width=True)


# ================= TAGLINE =================

st.markdown("""
<p style="
text-align:center;
font-size:24px;
font-weight:600;
color:#d8d8d8;
font-style:italic;
margin-top:12px;
margin-bottom:10px;">
Early Detection. Better Care. Healthier Lives for Every Woman.
</p>
""", unsafe_allow_html=True)


# ================= TITLE =================

st.markdown("""
<h2 style='text-align:center; color:#ff4b7d; font-size:42px;'>
🔍 Explore Our Platform
</h2>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)


# ---------------- ABOUT PCOS ----------------

with col1:
    st.markdown(
        """
<div style="background:#24384d;
border:1px solid #3b6ea5;
border-radius:16px;
padding:18px;
min-height:210px;
box-shadow:0 3px 10px rgba(0,0,0,0.25);">

<h3 style="color:white;font-size:22px;margin-bottom:12px;">
🩺 About PCOS
</h3>

<p style="color:white;font-size:16px;line-height:1.6;">
✔ What is PCOS?<br>
✔ Causes<br>
✔ Symptoms<br>
✔ Prevention
</p>

<p style="color:#9fd3ff;font-weight:bold;">
🔍 Explore →
</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ---------------- PATIENT ANALYTICS ----------------

with col2:
    st.markdown("""
    <div style="
        background:#1f344a;
        border:1px solid #3b6ea5;
        border-radius:16px;
        padding:15px;
        min-height:210px;
        box-shadow:0 3px 10px rgba(0,0,0,0.25);">

    <h3 style="color:white; margin-bottom:10px; font-size:22px;">
    📊 Patient Analytics
    </h3>

    <p style="color:white; line-height:1.5; font-size:16px; margin:0;">
    ✔ Age Distribution<br>
    ✔ BMI Analysis<br>
    ✔ Hormonal Trends<br>
    ✔ Health Insights
    </p>

    <p style="color:#9fd3ff; font-weight:bold; margin-top:10px; font-size:16px;">
    📈 View Analytics →
    </p>

    </div>
    """, unsafe_allow_html=True)


# ---------------- HOW OUR APP HELPS ----------------

with col3:
    st.markdown("""
    <div style="
        background:#1f344a;
        border:1px solid #3b6ea5;
        border-radius:16px;
        padding:15px;
        min-height:210px;
        box-shadow:0 3px 10px rgba(0,0,0,0.25);">

    <h3 style="color:white; margin-bottom:10px; font-size:22px;">
    ❤️ How Our App Helps
    </h3>

    <p style="color:white; line-height:1.5; font-size:16px; margin:0;">
    ✔ Early Risk Prediction<br>
    ✔ Personalized Insights<br>
    ✔ Lifestyle Guidance<br>
    ✔ Better Healthcare Support
    </p>

    <p style="color:#9fd3ff; font-weight:bold; margin-top:10px; font-size:16px;">
    🤖 Learn More →
    </p>

    </div>
    """, unsafe_allow_html=True)