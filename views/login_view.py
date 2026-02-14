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
    font-size: 32px !important;
    letter-spacing: 4px !important;
    font-weight: 700 !important;
    color: #2a1f16 !important; /* Matches Sidekick footer color */
    margin: 0 !important;
    line-height: 1.2 !important;
}

.brand-subtitle {
    margin-top: 5px !important;
    font-size: 10px !important;
    letter-spacing: 4px !important;
    color: #8c6b4f !important;
    text-transform: uppercase !important;
}

/* ===== LOGIN BOX ===== */
/* Dark card to support the light text usage requested */
.login-box {
    width: 320px !important;
    padding: 30px 25px !important;
    border-radius: 15px !important;
    background: #2a1f16 !important; /* Dark Brown background */
    border: 1px solid #3e2f24 !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15) !important;
    text-align: center !important;
    animation: fadeUp 1.0s ease-out !important;
    margin: 0 auto !important;
    transition: transform 0.3s ease;
}

.login-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.25) !important;
}

.login-header {
    font-family: 'Playfair Display', serif !important;
    margin-bottom: 15px !important;
    font-size: 22px !important;
    color: #e6c79c !important; /* RESTORED GOLD COLOR */
    font-weight: 600 !important;
}

/* ===== INPUTS ===== */
/* Target the outermost container of the input */
div[data-testid="stTextInput"] {
    margin-bottom: 15px !important;
}

/* Target the BaseWeb input container (the box) */
div[data-baseweb="input"] {
    background-color: rgba(255, 255, 255, 0.08) !important; /* Restored glass style */
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    color: white !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}

div[data-baseweb="input"]:focus-within {
    border-color: #e6c79c !important;
    background-color: rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 0 0 2px rgba(230, 199, 156, 0.2) !important;
}

/* Target the actual input element */
input[type="text"], input[type="password"] {
    background: transparent !important;
    color: #fff !important; /* Restored White Text */
    font-family: 'Poppins', sans-serif !important;
    font-size: 12px !important;
    caret-color: #e6c79c !important;
    padding: 10px 12px !important;
}

/* Remove default focus borders */
div[data-baseweb="base-input"] {
    background: transparent !important;
    border: none !important;
}

input::placeholder {
    color: #aaa !important; /* Restored lighter placeholder */
    font-size: 12px !important;
}

/* Remove default labels */
div[data-testid="stTextInput"] label {
    display: none !important;
}

/* ===== BUTTON ===== */
.stButton > button {
    width: 100% !important;
    padding: 10px !important;
    border-radius: 8px !important;
    border: none !important;
    background: #c89b6d !important; /* Restored lighter button */
    color: #2a1f16 !important; /* Dark text on button */
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 1px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin-top: 5px !important;
    box-shadow: 0 4px 15px rgba(200, 155, 109, 0.2) !important;
}

.stButton > button:hover {
    background: #e6c79c !important;
    color: #2a1f16 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(200, 155, 109, 0.3) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ===== FOOTER ===== */
.custom-footer {
    position: fixed !important;
    bottom: 20px !important;
    width: 100% !important;
    text-align: center !important;
    font-size: 11px !important;
    color: #8c6b4f !important; /* Darker footer for white bg */
    left: 0 !important;
    animation: fadeIn 2s ease-in;
}

.custom-footer span {
    color: #2a1f16 !important; 
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
            <h1 class="brand-title">THE KANDLE CO</h1>
            <p class="brand-subtitle">LUXURY CANDLE STUDIO</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login Bo
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-header">Member Login</h2>', unsafe_allow_html=True)
        
        # Inputs (Streamlit widgets wrapped to match style)
        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
        
        if st.button("Sign In"):
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
