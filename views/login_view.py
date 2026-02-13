import streamlit as st
from login import check_login
import time

def show_login_page():
    # Inject Custom CSS
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
    /* Force fullpage background */
    .stApp {
        background: radial-gradient(circle at center, #2a1f16 0%, #0f0c09 70%);
        font-family: 'Poppins', sans-serif;
    }

    /* Hide standard Streamlit elements */
    header, footer, #MainMenu {visibility: hidden !important;}
    
    /* Center container override */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }

    /* ===== BRAND ===== */
    .brand-container {
        text-align: center;
        margin-bottom: 40px;
        animation: fadeDown 1.2s ease;
    }

    .brand-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        letter-spacing: 6px;
        font-weight: 600;
        color: #e6c79c;
        margin: 0;
    }

    .brand-subtitle {
        margin-top: 10px;
        font-size: 12px;
        letter-spacing: 6px;
        color: #b08968;
        text-transform: uppercase;
    }

    /* ===== LOGIN BOX ===== */
    .login-box {
        width: 380px;
        padding: 50px 40px;
        border-radius: 20px;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        box-shadow: 0 0 60px rgba(212,163,115,0.2);
        text-align: center;
        animation: fadeUp 1.2s ease;
        margin: 0 auto;
    }

    .login-header {
        font-family: 'Playfair Display', serif;
        margin-bottom: 30px;
        font-size: 28px;
        color: #e6c79c;
    }

    /* ===== INPUTS ===== */
    /* Targeting Streamlit Widgets */
    .stTextInput > div > div > input {
        width: 100%;
        padding: 14px;
        border-radius: 10px;
        border: none;
        outline: none;
        background: rgba(255,255,255,0.08);
        color: #fff;
        font-size: 14px;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #aaa;
    }
    
    /* Remove default labels if we want clean look */
    .stTextInput label {
        display: none;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        width: 100%;
        padding: 14px;
        border-radius: 10px;
        border: none;
        background: #c89b6d;
        color: #2a1f16;
        font-weight: 600;
        letter-spacing: 2px;
        cursor: pointer;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background: #e6c79c;
        transform: scale(1.03);
        color: #2a1f16;
    }
    
    .stButton > button:focus {
        color: #2a1f16;
    }

    /* ===== FOOTER ===== */
    .custom-footer {
        position: fixed;
        bottom: 30px;
        width: 100%;
        text-align: center;
        font-size: 14px;
        color: #8c6b4f;
    }

    .custom-footer span {
        color: #e6c79c;
        font-weight: 500;
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
        .login-box { width: 90%; }
        .brand-title { font-size: 38px; }
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
