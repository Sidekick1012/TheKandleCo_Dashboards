import streamlit as st
from login import check_login
import base64
import os
import time
import textwrap

def show_login_page():
    # Helper for Base64 image
    def get_base64_of_bin_file(bin_file):
        if not os.path.exists(bin_file):
            return ""
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    logo_b64 = get_base64_of_bin_file("assets/sidekick_logo.png")
    logo_src = f"data:image/png;base64,{logo_b64}" if logo_b64 else ""

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
    width: 350px !important; /* Slightly wider */
    padding: 15px 25px !important; /* Even slimmer height */
    border-radius: 15px !important;
    background: #ffffff !important; /* White background */
    border: 1px solid #D4AF37 !important; /* Vibrant Gold Border */
    box-shadow: 0 10px 40px rgba(212, 175, 55, 0.1) !important;
    text-align: center !important;
    animation: fadeUp 1.0s ease-out !important;
    margin: 0px auto 40px auto !important; /* Moved slightly higher, increased bottom gap */
    transition: transform 0.3s ease;
}

.login-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0,0,0,0.12) !important;
}

.login-header {
    font-family: 'Playfair Display', serif !important;
    margin-bottom: 5px !important;
    font-size: 22px !important;
    color: #2a1f16 !important;
    font-weight: 600 !important;
}

.login-subheader {
    font-family: 'Poppins', sans-serif !important;
    font-size: 10px !important;
    color: #A8855F !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    margin-bottom: 5px !important;
    font-weight: 500 !important;
}

.header-accent-line {
    width: 40px !important;
    height: 2px !important;
    background: #D4AF37 !important;
    margin: 5px auto 10px auto !important; /* Reduced bottom gap */
    border-radius: 2px !important;
}

/* Move the form/fields higher */
[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    margin-top: -5px !important;
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
    background: linear-gradient(90deg, #D4AF37 calc(100% - 32px), #1A202C calc(100% - 32px)) !important;
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
    color: #D4AF37 !important;
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
    border-bottom: 6px solid #B69121 !important; /* Darker Gold for fold */
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
    font-size: 13px !important;
    color: #000000 !important; /* Bold black */
    left: 0 !important;
    animation: fadeIn 2s ease-in;
    font-weight: 500 !important;
}

.custom-footer span {
    display: inline-block !important;
    vertical-align: middle !important;
}

.footer-logo {
    height: 20px !important; /* Increased for better prominence */
    width: auto !important;
    vertical-align: middle !important;
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

/* ===== PROGRESS BAR ===== */
.progress-outer {
    width: 100% !important;
    height: 6px !important;
    background: rgba(42, 31, 22, 0.1) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    margin: 20px 0 10px 0 !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
}

.progress-inner {
    height: 100% !important;
    background: linear-gradient(90deg, #D4AF37, #F6E05E, #D4AF37) !important;
    background-size: 200% 100% !important;
    animation: shimmer 2s infinite linear !important;
    width: 0%;
    transition: width 0.5s ease !important;
}

.status-text {
    font-family: 'Poppins', sans-serif !important;
    font-size: 11px !important;
    color: #A8855F !important;
    font-weight: 500 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

/* ===== LOGIN PAGE CANDLES ===== */
.login-candle-container {
    position: absolute !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    z-index: 5 !important;
}

.candle-left {
    left: -80px !important;
}

.candle-right {
    right: -80px !important;
}

.candle-jar {
    width: 35px !important;
    height: 45px !important;
    background: linear-gradient(135deg, #2D3748 0%, #1A202C 100%) !important;
    border-radius: 4px 4px 8px 8px !important;
    position: relative !important;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
}

.candle-flame {
    position: absolute !important;
    top: -14px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 8px !important;
    height: 16px !important;
    background: #D4AF37 !important;
    border-radius: 50% 50% 50% 50% / 60% 60% 40% 40% !important;
    background: linear-gradient(to bottom, #FFF8E1 0%, #D4AF37 100%) !important;
    filter: blur(0.5px) !important;
    box-shadow: 0 0 10px #D4AF37, 0 0 20px rgba(212, 175, 55, 0.4) !important;
    animation: flicker 2.5s infinite alternate !important;
}

.candle-glow {
    position: absolute !important;
    top: -20px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: 50px !important;
    height: 50px !important;
    background: radial-gradient(circle, rgba(212, 175, 55, 0.2) 0%, transparent 70%) !important;
    border-radius: 50% !important;
    animation: glow-pulse 4s infinite ease-in-out !important;
}

@keyframes flicker {
    0% { transform: translateX(-50%) scale(1); opacity: 0.9; }
    20% { transform: translateX(-52%) scale(1.05); opacity: 1; }
    40% { transform: translateX(-48%) scale(0.95); opacity: 0.85; }
    60% { transform: translateX(-51%) scale(1.02); opacity: 0.95; }
    80% { transform: translateX(-49%) scale(0.98); opacity: 0.9; }
    100% { transform: translateX(-50%) scale(1.05); opacity: 1; }
}

@keyframes glow-pulse {
    0%, 100% { transform: translateX(-50%) scale(1); opacity: 0.3; }
    50% { transform: translateX(-50%) scale(1.2); opacity: 0.6; }
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
        st.markdown('''
<div style="position: relative; width: 350px; margin: 0 auto;">
<!-- Left Candle -->
<div class="login-candle-container candle-left">
<div class="candle-jar">
<div class="candle-glow"></div>
<div class="candle-flame"></div>
</div>
</div>
<!-- Right Candle -->
<div class="login-candle-container candle-right">
<div class="candle-jar">
<div class="candle-glow"></div>
<div class="candle-flame"></div>
</div>
</div>
<div class="login-box" style="margin: 0 !important; width: 100% !important;">
<h2 class="login-header">Member Login</h2>
<p class="login-subheader">Business Intelligence Suite</p>
<div class="header-accent-line"></div>
''', unsafe_allow_html=True)
        
        # Form for Enter key support
        with st.form("login_form"):
            # Inputs (Streamlit widgets wrapped to match style)
            username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
            
            submitted = st.form_submit_button("LOGIN")
            
            if submitted:
                if check_login(username, password):
                    # Heavy Animated Progress Bar
                    status_placeholder = st.empty()
                    progress_placeholder = st.empty()
                    
                    statuses = [
                        "Initializing Neural Sync...",
                        "Authorizing Credentials...",
                        "Synchronizing Financial Data...",
                        "Decrypting Intelligence Suite...",
                        "Finalizing Secure Connection..."
                    ]
                    
                    for i, status in enumerate(statuses):
                        percent = (i + 1) * 20
                        status_placeholder.markdown(f'<div class="status-text">{status}</div>', unsafe_allow_html=True)
                        progress_placeholder.markdown(f'''
                            <div class="progress-outer">
                                <div class="progress-inner" style="width: {percent}%;"></div>
                            </div>
                        ''', unsafe_allow_html=True)
                        time.sleep(0.4)
                    
                    st.session_state.authenticated = True
                    st.session_state.needs_sync = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        st.markdown('</div></div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown(f"""
        <div class="custom-footer">
            Designed & Developed by<span><img src="{logo_src}" class="footer-logo"></span>
        </div>
        """, unsafe_allow_html=True)
