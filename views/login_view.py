import streamlit as st
from login import check_login
import time

def show_login_page():
    # Inject Custom CSS
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
    /* Force fullpage background */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #2a1f16 0%, #0f0c09 70%) !important;
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
        margin-bottom: 40px;
        animation: fadeDown 1.2s ease;
    }

    .brand-title {
        font-family: 'Playfair Display', serif !important;
        font-size: 52px !important;
        letter-spacing: 6px !important;
        font-weight: 600 !important;
        color: #e6c79c !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }

    .brand-subtitle {
        margin-top: 10px !important;
        font-size: 12px !important;
        letter-spacing: 6px !important;
        color: #b08968 !important;
        text-transform: uppercase !important;
    }

    /* ===== LOGIN BOX ===== */
    .login-box {
        width: 380px !important;
        padding: 50px 40px !important;
        border-radius: 20px !important;
        background: rgba(255,255,255,0.05) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 0 60px rgba(212,163,115,0.2) !important;
        text-align: center !important;
        animation: fadeUp 1.2s ease !important;
        margin: 0 auto !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }

    .login-header {
        font-family: 'Playfair Display', serif !important;
        margin-bottom: 30px !important;
        font-size: 28px !important;
        color: #e6c79c !important;
    }

    /* ===== INPUTS ===== */
    /* 1. Target the outermost container of the input */
    div[data-testid="stTextInput"] {
        background: transparent !important;
    }

    /* 2. Target the BaseWeb input container (the box) */
    div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 5px !important;
    }

    /* 3. Target the actual input element */
    input[type="text"], input[type="password"] {
        background: transparent !important;
        color: white !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 14px !important;
        caret-color: #e6c79c !important;
    }

    /* 4. Remove default focus borders */
    div[data-baseweb="base-input"] {
        background: transparent !important;
        border: none !important;
    }

    input::placeholder {
        color: #aaa !important;
    }

    /* Remove default labels */
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    
    /* Remove top margin/padding from Streamlit widgets */
    .stTextInput {
        margin-bottom: 20px !important;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        width: 100% !important;
        padding: 14px !important;
        border-radius: 10px !important;
        border: none !important;
        background: #c89b6d !important;
        color: #2a1f16 !important;
        font-weight: 600 !important;
        letter-spacing: 2px !important;
        cursor: pointer !important;
        transition: 0.3s ease !important;
        margin-top: 10px !important;
    }

    .stButton > button:hover {
        background: #e6c79c !important;
        transform: scale(1.03) !important;
        color: #2a1f16 !important;
        border: none !important;
    }
    
    .stButton > button:focus {
        color: #2a1f16 !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    .stButton > button:active {
        color: #2a1f16 !important;
        background: #c89b6d !important;
    }

    /* ===== FOOTER ===== */
    .custom-footer {
        position: fixed !important;
        bottom: 30px !important;
        width: 100% !important;
        text-align: center !important;
        font-size: 14px !important;
        color: #8c6b4f !important;
        left: 0 !important;
    }

    .custom-footer span {
        color: #e6c79c !important;
        font-weight: 500 !important;
    }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media(max-width: 420px) {
        .login-box { width: 90% !important; }
        .brand-title { font-size: 38px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

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
        
        # Login Box
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
