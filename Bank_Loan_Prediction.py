import streamlit as st
import pickle
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ · Approval Predictor",
    page_icon="🏦",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    min-height: 100vh;
}

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 2rem;
}
.hero-icon {
    font-size: 3rem;
    display: block;
    margin-bottom: .5rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: #e8d5b7;
    margin: 0 0 .4rem;
    letter-spacing: -0.5px;
}
.hero p {
    color: rgba(255,255,255,0.45);
    font-size: .95rem;
    margin: 0;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: .7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #c9a96e;
    margin: 2rem 0 .75rem;
    padding-bottom: .4rem;
    border-bottom: 1px solid rgba(201,169,110,0.2);
}

/* ── Input overrides ── */
.stTextInput input,
.stNumberInput input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: #c9a96e !important;
    box-shadow: 0 0 0 2px rgba(201,169,110,0.15) !important;
}
label, .stSelectbox label, .stNumberInput label, .stTextInput label {
    color: rgba(255,255,255,0.7) !important;
    font-size: .85rem !important;
    font-weight: 400 !important;
}

/* ── Submit button ── */
.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #c9a96e, #e8d5b7) !important;
    color: #1a1a3e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.5px;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    margin-top: 1.5rem;
    transition: all 0.25s ease;
    box-shadow: 0 4px 20px rgba(201,169,110,0.3);
}
.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(201,169,110,0.45) !important;
}

/* ── Result cards ── */
.result-card {
    border-radius: 16px;
    padding: 1.75rem 2rem;
    margin-top: 1.5rem;
    text-align: center;
    animation: slideUp .4s ease;
}
.result-approved {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.08));
    border: 1px solid rgba(16,185,129,0.35);
}
.result-rejected {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(185,28,28,0.08));
    border: 1px solid rgba(239,68,68,0.35);
}
.result-card .result-icon { font-size: 2.8rem; display: block; margin-bottom: .6rem; }
.result-card h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    margin: 0 0 .5rem;
}
.result-approved h2 { color: #6ee7b7; }
.result-rejected h2 { color: #fca5a5; }
.result-card p { color: rgba(255,255,255,0.6); font-size: .9rem; margin: 0; line-height: 1.6; }
.result-card .applicant-name {
    font-weight: 600;
    color: rgba(255,255,255,0.9);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.07) !important; }

/* ── Misc fixes ── */
.stSelectbox > div { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Load model ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_model():
    model_path = './Model/ML_Model.pkl'
    if not os.path.exists(model_path):
        st.error("⚠️ Model file not found at `./Model/ML_Model.pkl`. Please ensure the model is trained and saved.")
        st.stop()
    with open(model_path, 'rb') as f:
        return pickle.load(f)

model = load_model()


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-icon">🏦</span>
  <h1>LoanIQ</h1>
  <p>AI-powered loan approval prediction · Instant results</p>
</div>
""", unsafe_allow_html=True)


# ── Form ───────────────────────────────────────────────────────────────────────
with st.form("loan_form"):

    # ── Personal Info ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Personal Information</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fn = st.text_input("Full Name", placeholder="e.g. Jane Smith")
    with col2:
        account_no = st.text_input("Account Number", placeholder="e.g. ACC-00123")

    col3, col4, col5 = st.columns(3)
    with col3:
        gen_display = ["Female", "Male"]
        gen = st.selectbox("Gender", range(len(gen_display)), format_func=lambda x: gen_display[x])
    with col4:
        mar_display = ["Single / Not Married", "Married"]
        mar = st.selectbox("Marital Status", range(len(mar_display)), format_func=lambda x: mar_display[x])
    with col5:
        dep_display = ["None", "1 Dependent", "2 Dependents", "3 or More"]
        dep = st.selectbox("Dependents", range(len(dep_display)), format_func=lambda x: dep_display[x])

    col6, col7 = st.columns(2)
    with col6:
        edu_display = ["Not Graduate", "Graduate"]
        edu = st.selectbox("Education", range(len(edu_display)), format_func=lambda x: edu_display[x])
    with col7:
        emp_display = ["Salaried / Job", "Self-Employed / Business"]
        emp = st.selectbox("Employment Type", range(len(emp_display)), format_func=lambda x: emp_display[x])

    # ── Financial Details ──────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Financial Details</div>', unsafe_allow_html=True)

    col8, col9 = st.columns(2)
    with col8:
        mon_income = st.number_input("Monthly Income ($)", min_value=0, value=5000, step=100)
    with col9:
        co_mon_income = st.number_input("Co-Applicant Income ($)", min_value=0, value=0, step=100)

    col10, col11 = st.columns(2)
    with col10:
        loan_amt = st.number_input("Loan Amount ($)", min_value=0, value=150, step=5,
                                   help="Enter amount in thousands (e.g. 150 = $150,000)")
    with col11:
        dur_display = ["2 Months (60 days)", "6 Months (180 days)", "8 Months (240 days)",
                       "1 Year (360 days)", "16 Months (480 days)"]
        dur_values  = [60, 180, 240, 360, 480]
        dur_idx = st.selectbox("Loan Duration", range(len(dur_display)),
                               index=3, format_func=lambda x: dur_display[x])

    # ── Property & Credit ──────────────────────────────────────────────────────
    st.markdown('<div class="section-label">Property & Credit</div>', unsafe_allow_html=True)

    col12, col13 = st.columns(2)
    with col12:
        prop_display = ["Rural", "Semi-Urban", "Urban"]
        prop = st.selectbox("Property Area", range(len(prop_display)),
                            format_func=lambda x: prop_display[x])
    with col13:
        # Credit History: 1 = good (met guidelines), 0 = bad
        # Model was trained with Credit_History 0/1 where 1 means good history
        cred_display = ["Poor (no/bad credit history)", "Good (met repayment guidelines)"]
        cred = st.selectbox("Credit History", range(len(cred_display)),
                            index=1,  # default to Good
                            format_func=lambda x: cred_display[x])

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔍  Predict Loan Approval")


# ── Prediction ─────────────────────────────────────────────────────────────────
if submitted:
    if not fn.strip():
        st.warning("Please enter the applicant's full name.")
    elif not account_no.strip():
        st.warning("Please enter an account number.")
    else:
        duration = dur_values[dur_idx]

        # Feature vector — must match training order exactly:
        # Gender, Married, Dependents, Education, Self_Employed,
        # ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term,
        # Credit_History, Property_Area
        features = [[gen, mar, dep, edu, emp,
                     mon_income, co_mon_income, loan_amt,
                     duration, cred, prop]]

        prediction = model.predict(features)[0]

        if prediction == 1:
            st.markdown(f"""
            <div class="result-card result-approved">
                <span class="result-icon">🎉</span>
                <h2>Loan Approved!</h2>
                <p>Congratulations, <span class="applicant-name">{fn}</span>!<br>
                Based on the information provided, your loan application
                <strong style="color:#6ee7b7;">meets our approval criteria</strong>.<br><br>
                <em>Account: {account_no}</em></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card result-rejected">
                <span class="result-icon">📋</span>
                <h2>Not Approved</h2>
                <p>Hello, <span class="applicant-name">{fn}</span>.<br>
                Based on the details provided, your application
                <strong style="color:#fca5a5;">does not meet our current criteria</strong>.<br>
                We encourage you to review your credit history and financials before reapplying.<br><br>
                <em>Account: {account_no}</em></p>
            </div>
            """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;color:rgba(255,255,255,0.2);font-size:.75rem;margin-top:.5rem;">
LoanIQ · Predictive analytics for financial decisions · Not financial advice
</p>
""", unsafe_allow_html=True)
