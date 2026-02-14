import streamlit as st
from login import check_login
import time

def show_login_page():
    # Inject Custom CSS
    # CSS Style Definition
    LOGIN_STYLE = """
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
<style>
/* Force fullpage white background */
[data-testid="stAppViewContainer"] {
    background-color: #ffffff !important;
    background-image: none !important;
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Hide standard Streamlit elements */
header, footer, #MainMenu {visibility: hidden !important;}

/* Center container override */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100vh !important;
    flex-direction: column !important;
}

/* ===== BRAND ===== */
.brand-container {
    text-align: center;
    margin-bottom: 25px;
    animation: fadeDown 1.0s ease-out;
}

.brand-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 42px !important;
    letter-spacing: 4px !important;
    font-weight: 700 !important;
    color: #D4AF37 !important; /* Premium Vibrant Gold */
    margin: 0 !important;
    line-height: 1.2 !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
}

.brand-subtitle {
    margin-top: 5px !important;
    font-size: 10px !important;
    letter-spacing: 4px !important;
    color: #A8855F !important; /* Fresher contrast */
    text-transform: uppercase !important;
}

/* ===== LOGIN BOX ===== */
.login-box {
    width: 320px !important;
    padding: 30px 25px !important;
    border-radius: 15px !important;
    background: #ffffff !important; /* White background */
    border: 1px solid #D4AF37 !important; /* Vibrant Gold Border */
    box-shadow: 0 10px 40px rgba(212, 175, 55, 0.1) !important;
    text-align: center !important;
    animation: fadeUp 1.0s ease-out !important;
    margin: 0 auto !important;
    transition: transform 0.3s ease;
}

.login-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.12) !important;
}

.login-header {
    font-family: 'Playfair Display', serif !important;
    margin-bottom: 15px !important;
    font-size: 22px !important;
    color: #2a1f16 !important; /* Dark text for contrast */
    font-weight: 600 !important;
}

/* ===== INPUTS ===== */
/* Target the outermost container of the input */
div[data-testid="stTextInput"] {
    margin-bottom: 15px !important;
}

/* Target the BaseWeb input container (the box) */
div[data-baseweb="input"] {
    background-color: #f7f7f7 !important; /* Light grey bg */
    border: 1px solid #D4AF37 !important; /* Gold border for inputs */
    border-radius: 8px !important;
    color: #333 !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}

div[data-baseweb="input"]:focus-within {
    border-color: #D4AF37 !important;
    background-color: #fff !important;
    box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.15) !important;
}

/* Target the actual input element */
input[type="text"], input[type="password"] {
    background: transparent !important;
    color: #333 !important; /* Dark text */
    font-family: 'Poppins', sans-serif !important;
    font-size: 12px !important;
    caret-color: #c89b6d !important;
    padding: 10px 12px !important;
}

/* Remove default focus borders */
div[data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
}

input::placeholder {
    color: #999 !important;
    font-size: 12px !important;
}

/* Remove default labels */
div[data-testid="stTextInput"] label {
    display: none !important;
}

/* ===== RIBBON BUTTON ===== */
.stButton > button,
[data-testid="stFormSubmitButton"] button {
    position: relative !important;
    background: linear-gradient(90deg, #d4af37 calc(100% - 32px), #1A202C calc(100% - 32px)) !important;
    color: #0F172A !important;
    border: none !important;
    border-radius: 0 4px 4px 0 !important;
    width: 100% !important;
    height: 32px !important;
    font-weight: 900 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    padding-right: 38px !important;
    padding-left: 10px !important;
    text-align: left !important;
    margin-top: 10px !important;
    overflow: visible !important;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1) !important;
    font-size: 0.75rem !important;
    white-space: nowrap !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] button:hover {
    transform: scale(1.02) !important;
    box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
}

/* Dark Section with Arrow */
.stButton > button::after,
[data-testid="stFormSubmitButton"] button::after {
    content: "➜" !important;
    position: absolute !important;
    right: 0 !important;
    top: 0 !important;
    width: 32px !important;
    height: 100% !important;
    background: #1A202C !important;
    color: #ecc94b !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 0.9rem !important;
    border-radius: 0 4px 4px 0 !important;
}

/* Ribbon Fold */
.stButton > button::before,
[data-testid="stFormSubmitButton"] button::before {
    content: "" !important;
    position: absolute !important;
    left: 0 !important;
    top: -6px !important;
    width: 0 !important;
    height: 0 !important;
    border-left: 8px solid transparent !important;
    border-bottom: 6px solid #b7902d !important;
}

/* Ensure inner text is visible and bold */
.stButton > button p,
[data-testid="stFormSubmitButton"] button p {
    margin: 0 !important;
    font-weight: 900 !important;
    color: #0F172A !important;
    font-size: 0.75rem !important;
}

/* ===== FOOTER ===== */
.custom-footer {
    position: fixed !important;
    bottom: 20px !important;
    width: 100% !important;
    text-align: center !important;
    font-size: 11px !important;
    color: #aaa !important;
    left: 0 !important;
    animation: fadeIn 2s ease-in;
}

.custom-footer span {
    color: #c89b6d !important;
    font-weight: 500 !important;
}

/* ===== ANIMATIONS ===== */
@keyframes fadeDown {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@media(max-width: 420px) {
    .login-box { width: 85% !important; }
    .brand-title { font-size: 28px !important; }
}
</style>
"""
    st.html(LOGIN_STYLE)

    # HTML Structure
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Brand Header
        st.markdown("""
        <div class="brand-container">
            <h1 class="brand-title">The Kandle CO.</h1>
            <p class="brand-subtitle">LUXURY CANDLE STUDIO</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login Box
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-header">Member Login</h2>', unsafe_allow_html=True)
        
        # Form for Enter key support
        with st.form("login_form"):
            # Inputs (Streamlit widgets wrapped to match style)
            username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            submitted = st.form_submit_button("LOGIN")
            
            if submitted:
                if check_login(username, password):
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="custom-footer">
            Designed & Developed by <span>Sidekick</span>
        </div>
        """, unsafe_allow_html=True)
