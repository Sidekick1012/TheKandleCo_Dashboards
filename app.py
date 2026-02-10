import streamlit as st
import time
from login import init_db, check_login

st.set_page_config(
    page_title="🕯️ The Kandle Co",
    page_icon="🕯️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ========================= CSS =========================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Cormorant+Garamond:wght@300;400;500&family=Montserrat:wght@300;400;500;600&display=swap');
    
    /* Root Variables */
    :root {
        --primary-gold: #D4AF37;
        --accent-gold: #F4E4C1;
        --primary-dark: #1a1a1a;
        --secondary-dark: #2d2d2d;
        --bg-cream: #f9f7f3;
        --text-light: #666;
        --white: #ffffff;
        --shadow: rgba(0, 0, 0, 0.1);
        --glow: rgba(212, 175, 55, 0.3);
    }
    
    /* Global Resets */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        font-family: 'Inter', sans-serif;
    }
    
    
    /* Login-only background override */
    body:has(.login-container) .stApp {
        background: linear-gradient(135deg, 
            #667eea 0%, 
            #764ba2 25%, 
            #f093fb 50%, 
            #4facfe 75%, 
            #667eea 100%);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        font-family: 'Montserrat', sans-serif;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Global Scroll Control */
    html, body {
        overflow-x: hidden;
        overflow-y: auto;
    }
    
    /* Remove scrollbar on login page specifically */
    body:has(.login-container) {
        overflow: hidden !important;
    }
    
    body:has(.login-container) .main {
        overflow: hidden !important;
    }
    
    /* Ensure no horizontal scroll */
    * {
        max-width: 100%;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    header[data-testid="stHeader"] {
        visibility: visible;
        background-color: transparent;
        z-index: 10000;
    }
    
    /* Make the hamburger menu white */
    [data-testid="stHeader"] button {
        color: white !important;
    }
    
    /* Container Padding */
    /* Container Padding */
    .block-container {
        padding: 6rem 1rem 1rem 1rem !important;
        max-width: 1200px !important;
    }
    
    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Playfair Display', serif !important;
        color: #1a1a1a !important;
    }

    /* Force Main Text Color to Black */
    .stApp .main .block-container, 
    .stApp .main p, 
    .stApp .main li, 
    .stApp .main div,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stMarkdownContainer"] b {
        color: #1a1a1a !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        color: #1a1a1a !important;
    }
    [data-testid="stMetricLabel"] {
        color: #666 !important;
    }
    
    /* Table Styling */
    div[data-testid="stTable"] th, 
    div[data-testid="stTable"] td, 
    div[data-testid="stDataFrame"] th, 
    div[data-testid="stDataFrame"] td {
        color: #1a1a1a !important;
        background-color: white !important; /* Ensure bg is white */
    }
    
    /* Alert Text */
    div[data-testid="stAlert"] {
        color: #1a1a1a !important;
    }
    div[data-testid="stAlert"] p {
        color: #1a1a1a !important;
    }
    
    /* Caption Text */
    div[data-testid="stCaptionContainer"] {
        color: #666 !important;
    }

    /* Sidebar Background & Text Overrides */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fdfbf7 0%, #f4e4c1 100%) !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1a1a1a !important;
        font-family: 'Montserrat', sans-serif !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* ==================== CANDLE ANIMATION ==================== */
    .candle-container {
        position: fixed;
        top: 20%;
        left: 5%;
        z-index: 1;
        perspective: 1000px;
    }
    
    .candle-container-right {
        position: fixed;
        top: 20%;
        right: 5%;
        z-index: 1;
        perspective: 1000px;
    }
    
    .candle {
        position: relative;
        width: 60px;
        height: 100px;
        background: linear-gradient(to bottom, #fff9e6 0%, #f5e6d3 50%, #e6d4b8 100%);
        border-radius: 8px 8px 4px 4px;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.2),
            inset 0 -2px 10px rgba(212, 175, 55, 0.3);
        animation: candle-flicker 3s ease-in-out infinite;
    }
    
    .candle::before {
        content: '';
        position: absolute;
        top: -5px;
        left: 50%;
        transform: translateX(-50%);
        width: 6px;
        height: 12px;
        background: #2d2d2d;
        border-radius: 50% 50% 0 0;
    }
    
    .flame {
        position: absolute;
        top: -25px;
        left: 50%;
        transform: translateX(-50%);
        width: 14px; /* Slightly wider */
        height: 35px; /* Slightly taller */
        background: linear-gradient(to top, 
            rgba(255, 120, 0, 0.95) 0%, 
            rgba(255, 180, 0, 0.9) 40%, 
            rgba(255, 230, 80, 0.6) 80%, 
            rgba(255, 255, 255, 0.3) 100%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        box-shadow: 
            0 0 20px rgba(255, 140, 0, 0.9),
            0 0 40px rgba(255, 100, 0, 0.5),
            0 0 60px rgba(255, 200, 0, 0.2);
        animation: flame-dance 1s ease-in-out infinite; /* Faster */
        filter: blur(0.5px);
    }
    
    .flame::after {
        content: '';
        position: absolute;
        top: 6px;
        left: 50%;
        transform: translateX(-50%);
        width: 9px;
        height: 22px;
        background: linear-gradient(to top, 
            rgba(255, 220, 50, 0.95) 0%, 
            rgba(255, 255, 150, 0.7) 100%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        animation: flame-dance 0.7s ease-in-out infinite reverse; /* Faster */
    }
    
    .glow {
        position: absolute;
        top: -45px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px; /* Larger glow */
        height: 80px;
        background: radial-gradient(circle, 
            rgba(255, 180, 50, 0.45) 0%, 
            rgba(255, 140, 0, 0.2) 40%,
            transparent 75%);
        border-radius: 50%;
        animation: glow-pulse 1.8s ease-in-out infinite;
    }
    
    @keyframes flame-dance {
        0%, 100% { transform: translateX(-50%) scaleY(1) scaleX(1) rotate(0deg); }
        25% { transform: translateX(-52%) scaleY(1.1) scaleX(0.9) rotate(-1deg); }
        50% { transform: translateX(-48%) scaleY(0.9) scaleX(1.1) rotate(1deg); }
        75% { transform: translateX(-51%) scaleY(1.05) scaleX(0.95) rotate(-0.5deg); }
    }
    
    @keyframes glow-pulse {
        0%, 100% { opacity: 0.7; transform: translateX(-50%) scale(1); }
        50% { opacity: 0.9; transform: translateX(-50%) scale(1.25); }
    }
    
    @keyframes candle-flicker {
        0%, 100% { box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2), inset 0 -2px 10px rgba(212, 175, 55, 0.3); transform: scale(1); }
        50% { box-shadow: 0 10px 40px rgba(255, 140, 0, 0.2), inset 0 -2px 15px rgba(212, 175, 55, 0.4); transform: scale(1.01); }
    }
    
    /* ==================== BRAND HEADER ==================== */
    .brand-header {
        text-align: center;
        margin: 1rem 0 1.5rem 0;
        animation: fade-in-down 0.8s ease-out;
    }
    
    .brand-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(2rem, 6vw, 4rem);
        font-weight: 600;
        letter-spacing: 0.3em;
        color: var(--primary-dark);
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .brand-subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(0.85rem, 2.5vw, 1.3rem);
        font-weight: 300;
        letter-spacing: 0.2em;
        color: var(--text-light);
        margin-top: 0.5rem;
        text-transform: uppercase;
    }
    
    .divider {
        width: 80px;
        height: 1px;
        background: linear-gradient(to right, transparent, var(--primary-gold), transparent);
        margin: 1.5rem auto;
    }
    
    /* ==================== MODERN LOGIN FORM DESIGN ==================== */
    .login-container {
        background: linear-gradient(145deg, 
            rgba(255, 255, 255, 0.25) 0%, 
            rgba(255, 255, 255, 0.1) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 16px;
        padding: 1.2rem 1.2rem;
        box-shadow: 
            0 8px 32px 0 rgba(31, 38, 135, 0.15),
            0 0 0 1px rgba(255, 255, 255, 0.18),
            inset 0 0 60px rgba(255, 255, 255, 0.05);
        margin: 0.8rem auto;
        max-width: 280px;
        position: relative;
        overflow: visible;
        animation: float-in 1s cubic-bezier(0.34, 1.56, 0.64, 1);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Animated gradient border */
    .login-container::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
            #ff6b9d 0%,
            #c06bff 25%,
            #00d4ff 50%,
            #ffd700 75%,
            #ff6b9d 100%);
        background-size: 400% 400%;
        border-radius: 16px;
        z-index: -1;
        animation: gradient-rotate 8s ease infinite;
        opacity: 0.4;
        filter: blur(5px);
    }
    
    @keyframes gradient-rotate {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating orbs background */
    .login-container::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(138, 43, 226, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(255, 107, 157, 0.1) 0%, transparent 40%),
            radial-gradient(circle at 40% 60%, rgba(0, 212, 255, 0.08) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
        border-radius: 16px;
        animation: orb-float 6s ease-in-out infinite;
    }
    
    @keyframes orb-float {
        0%, 100% { transform: scale(1) translateY(0); }
        50% { transform: scale(1.05) translateY(-10px); }
    }
    
    .login-content {
        position: relative;
        z-index: 1;
    }
    
    .login-icon {
        text-align: center;
        margin-bottom: 0.6rem;
    }
    
    .login-icon-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.3),
            0 0 0 5px rgba(255, 255, 255, 0.1),
            inset 0 -3px 8px rgba(0, 0, 0, 0.2);
        animation: icon-bounce 3s ease-in-out infinite;
        position: relative;
    }
    
    .login-icon-circle::before {
        content: '🔐';
        font-size: 1.3rem;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    }
    
    /* Glow effect */
    .login-icon-circle::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.4) 0%, transparent 70%);
        animation: pulse-glow 2s ease-in-out infinite;
    }
    
    @keyframes icon-bounce {
        0%, 100% { 
            transform: translateY(0) scale(1);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        50% { 
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.45);
        }
    }
    
    @keyframes pulse-glow {
        0%, 100% { opacity: 0.4; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.3); }
    }
    
    .login-title {
        font-family: 'Playfair Display', serif;
        font-size: clamp(1rem, 2.8vw, 1.2rem);
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.25rem;
        letter-spacing: 0.02em;
        animation: text-shimmer 3s ease-in-out infinite;
        background-size: 200% auto;
    }
    
    @keyframes text-shimmer {
        0%, 100% { background-position: 0% center; }
        50% { background-position: 100% center; }
    }
    
    .login-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: clamp(0.65rem, 1.4vw, 0.75rem);
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        font-weight: 500;
        letter-spacing: 0.05em;
    }
    
    
    /* Enhanced Input Fields */
    .stTextInput > div > div > input {
        border: 2px solid rgba(102, 126, 234, 0.2);
        border-radius: 8px;
        padding: 0.6rem 0.8rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        color: #2d3748 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(145deg, #ffffff 0%, #f7fafc 100%);
        box-shadow: 
            inset 0 2px 8px rgba(0, 0, 0, 0.05),
            0 2px 10px rgba(102, 126, 234, 0.1);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 
            0 0 0 4px rgba(102, 126, 234, 0.15),
            0 8px 24px rgba(102, 126, 234, 0.2),
            inset 0 2px 8px rgba(102, 126, 234, 0.1);
        background: #ffffff;
        transform: translateY(-2px);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #a0aec0;
        font-style: italic;
        font-size: 0.75rem;
    }
    
    /* Enhanced Labels */
    .stTextInput > label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.25rem;
        display: block;
    }
    
    .stTextInput > label::before {
        content: '●';
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-right: 8px;
        vertical-align: middle;
        font-size: 0.6rem;
    }
    
    /* Enhanced Submit Button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: 200% 100%;
        color: #ffffff;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 1.2rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        margin-top: 0.9rem;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button[kind="primary"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.3) 50%, 
            transparent 100%);
        transition: left 0.6s ease;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 15px 40px rgba(102, 126, 234, 0.6),
            0 0 0 4px rgba(102, 126, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        background-position: 100% 0;
    }
    
    .stButton > button[kind="primary"]:hover::before {
        left: 100%;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(-1px) scale(1);
        box-shadow: 
            0 8px 20px rgba(102, 126, 234, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
    }
    
    /* ==================== DASHBOARD ==================== */
    .dashboard-welcome {
        text-align: center;
        margin: 2rem 0;
        animation: fade-in 1s ease-out;
    }
    
    .welcome-user {
        font-family: 'Playfair Display', serif;
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        font-weight: 600;
        color: var(--primary-dark);
        margin-bottom: 0.5rem;
    }
    
    .welcome-subtitle {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(1rem, 2.5vw, 1.4rem);
        color: var(--text-light);
        font-style: italic;
    }
    
    /* Dashboard Buttons */
    .stButton > button {
        background: var(--white);
        color: var(--primary-dark);
        border: 2px solid var(--primary-gold);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
        color: var(--primary-gold);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.3);
    }
    
    /* Logout Button Specific */
    .stButton > button:last-child {
        border-color: #8b7355;
    }
    
    .stButton > button:last-child:hover {
        background: linear-gradient(135deg, #8b7355 0%, #6d5a45 100%);
        color: var(--white);
        border-color: #8b7355;
    }
    
    /* ==================== FOOTER ==================== */
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1.5rem 1rem;
        border-top: 1px solid rgba(212, 175, 55, 0.2);
        animation: fade-in 1.2s ease-out;
    }
    
    .footer-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(0.75rem, 2vw, 0.9rem);
        color: var(--text-light);
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin: 0.3rem 0;
    }
    
    /* ==================== ALERTS ==================== */
    .stAlert {
        border-radius: 12px;
        border: none;
        animation: slide-in 0.4s ease-out;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Success Alert */
    div[data-baseweb="notification"] > div {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #4caf50;
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);
    }
    
    /* Error Alert */
    .stAlert[data-baseweb="notification"] {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 5px solid #f44336;
        box-shadow: 0 4px 15px rgba(244, 67, 54, 0.2);
    }
    
    /* ==================== ANIMATIONS ==================== */
    @keyframes fade-in {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fade-in-down {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fade-in-up {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fade-in-scale {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes float-in {
        from {
            opacity: 0;
            transform: translateY(30px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes slide-in {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    
    /* ==================== RESPONSIVE DESIGN ==================== */
    
    /* Tablet and Below */
    @media (max-width: 992px) {
        .brand-title {
            letter-spacing: 0.25em;
        }
        
        .candle-container {
            top: 18%;
            left: 4%;
        }
        
        .candle-container-right {
            top: 18%;
            right: 4%;
        }
        
        .candle {
            width: 50px;
            height: 85px;
        }
        
        .flame {
            width: 10px;
            height: 25px;
            top: -22px;
        }
    }
    
    /* Mobile Landscape and Below */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.5rem 0.5rem !important;
        }
        
        .login-container {
            padding: 2rem 1.5rem;
            margin: 0.5rem auto;
            border-radius: 24px;
            max-width: 95%;
        }
        
        .candle-container {
            top: 12%;
            left: 2%;
        }
        
        .candle-container-right {
            top: 12%;
            right: 2%;
        }
        
        .candle {
            width: 40px;
            height: 70px;
        }
        
        .flame {
            width: 8px;
            height: 20px;
            top: -20px;
        }
        
        .glow {
            width: 50px;
            height: 50px;
            top: -35px;
        }
        
        .login-icon-circle {
            width: 60px;
            height: 60px;
        }
        
        .login-icon-circle::before {
            font-size: 1.8rem;
        }
        
        .brand-header {
            margin: 0.5rem 0 1rem 0;
        }
        
        .brand-title {
            letter-spacing: 0.2em;
        }
        
        .brand-subtitle {
            letter-spacing: 0.15em;
        }
        
        .stButton > button {
            padding: 1.2rem 1.5rem;
            font-size: 0.85rem;
            letter-spacing: 0.1em;
        }
        
        .stTextInput > div > div > input {
            padding: 1.3rem 1.5rem;
            font-size: 1.1rem;
        }
        
        .stTextInput > div > div > input::placeholder {
            font-size: 1rem;
        }
        
        .dashboard-welcome {
            margin: 1.5rem 0;
        }
        
        .footer {
            margin-top: 2rem;
            padding: 1rem 0.5rem;
        }
    }
    
    /* Mobile Portrait */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.3rem 0.3rem !important;
        }
        
        .login-container {
            padding: 1.8rem 1.2rem;
            border-radius: 20px;
            margin: 0.3rem auto;
        }
        
        .candle-container {
            top: 8%;
            left: 1%;
        }
        
        .candle-container-right {
            top: 8%;
            right: 1%;
        }
        
        .candle {
            width: 30px;
            height: 55px;
        }
        
        .candle::before {
            width: 5px;
            height: 10px;
        }
        
        .flame {
            width: 6px;
            height: 16px;
            top: -18px;
        }
        
        .glow {
            width: 40px;
            height: 40px;
            top: -30px;
        }
        
        .login-title {
            letter-spacing: 0.08em;
        }
        
        .login-subtitle {
            margin-bottom: 1.5rem;
            letter-spacing: 0.05em;
        }
        
        .login-icon {
            margin-bottom: 0.8rem;
        }
        
        .login-icon-circle {
            width: 55px;
            height: 55px;
        }
        
        .login-icon-circle::before {
            font-size: 1.5rem;
        }
        
        .stTextInput > div > div > input {
            padding: 1.2rem 1.3rem;
            font-size: 1rem;
            border-radius: 12px;
        }
        
        .stTextInput > div > div > input::placeholder {
            font-size: 0.9rem;
        }
        
        .stTextInput > label {
            font-size: 0.75rem;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button[kind="primary"] {
            padding: 1.1rem 2rem;
            font-size: 0.9rem;
            letter-spacing: 0.15em;
            margin-top: 1.2rem;
            border-radius: 12px;
        }
        
        .stButton > button {
            padding: 1rem 1.2rem;
            font-size: 0.75rem;
            letter-spacing: 0.08em;
            border-radius: 10px;
        }
        
        .brand-header {
            margin: 0.3rem 0 0.8rem 0;
        }
        
        .brand-title {
            letter-spacing: 0.15em;
        }
        
        .brand-subtitle {
            letter-spacing: 0.1em;
        }
        
        .divider {
            width: 60px;
            margin: 1rem auto;
        }
        
        .dashboard-welcome {
            margin: 1rem 0;
        }
        
        .footer {
            margin-top: 1.5rem;
            padding: 1rem 0.5rem;
        }
    }
    
    /* Extra Small Mobile */
    @media (max-width: 360px) {
        .candle-container,
        .candle-container-right {
            display: none;
        }
        
        .login-container {
            padding: 1.5rem 1rem;
        }
        
        .stTextInput > div > div > input {
            padding: 1rem 1.2rem;
            font-size: 0.95rem;
        }
        
        .stButton > button[kind="primary"] {
            padding: 1rem 1.5rem;
            font-size: 0.85rem;
        }
        
        .brand-title {
            letter-spacing: 0.1em;
        }
    }
    
    /* ==================== COLUMN SPACING ==================== */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    @media (max-width: 768px) {
        [data-testid="column"] {
            padding: 0 0.3rem;
        }
    }
    
    @media (max-width: 480px) {
        [data-testid="column"] {
            padding: 0 0.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ================= CANDLE HTML =================
if not st.session_state.get('logged_in', False):
    st.markdown("""
    <div class="candle-container">
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
    </div>
    <div class="candle-container-right">
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= LOGIC =================
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("""
    <div class="brand-header">
        <h1 class="brand-title">THE KANDLE CO.</h1>
        <div class="divider"></div>
        <p class="brand-subtitle">Luxury Home Fragrance</p>
    </div>
    """, unsafe_allow_html=True)
    
   # st.markdown('<div class="login-container"><div class="login-content">', unsafe_allow_html=True)
    
    # Login Icon
    st.markdown('''
    <div class="login-icon">
        <div class="login-icon-circle"></div>
    </div>
    ''', unsafe_allow_html=True)
    
    with st.form("login_form"):
        #st.markdown('<h1 class="login-title">Welcome Back</h1>', unsafe_allow_html=True)
        #st.markdown('<p class="login-subtitle">Sign in to access your account</p>', unsafe_allow_html=True)
        
        user = st.text_input("Username", placeholder="Enter your username")
        pwd = st.text_input("Password", type="password", placeholder="Enter your password")
    
        
        submit = st.form_submit_button("SIGN IN", type="primary")
        
        if submit:
            if check_login(user, pwd):
                st.session_state.logged_in = True
                st.session_state.username = user
                st.success("✓ Authentication successful")
                time.sleep(1)
                st.rerun()
            else:
                st.error("✗ Invalid username or password")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ================= DASHBOARD =================
else:
    import data_utils
    # Import Views from our modular structure
    # Import Views from our modular structure
    from views import (
        executive_command, revenue_sales, product_profitability,
        cost_margin, seasonality, cash_flow, yoy_comparison,
        early_warning, customer_channel
    )

    # --- Fixed Top Header for Dashboard ---
    st.markdown("""<div style='position: fixed; top: 0; left: 0; width: 100%; background: linear-gradient(90deg, #000000 0%, #1a1a1a 50%, #000000 100%); border-bottom: 2px solid #D4AF37; height: 100px; z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; box-shadow: 0 4px 25px rgba(0,0,0,0.4); overflow: hidden;'>
<div style='margin-left: 260px; text-align: center; display: flex; flex-direction: column; align-items: center;'>
    <h1 style='font-family: "Playfair Display", serif; color: #D4AF37; font-size: 1.8rem; letter-spacing: 0.4em; margin: 0; text-shadow: 0 0 15px rgba(212, 175, 55, 0.4); font-weight: 700; text-transform: uppercase;'>The Kandle Co.</h1>
    <div style='transform: scale(0.35); display: flex; gap: 15px; align-items: flex-end; margin-top: -15px;'>
        <div class="candle" style="position: relative; top: auto; left: auto; animation-delay: 0s; height: 65px; background: linear-gradient(to bottom, #d4af37 0%, #b8962e 100%);">
            <div class="glow"></div>
            <div class="flame" style="animation-duration: 1.2s; animation-delay: 0.1s;"></div>
        </div>
        <div class="candle" style="position: relative; top: auto; left: auto; animation-delay: 1.5s; height: 85px; background: linear-gradient(to bottom, #d4af37 0%, #b8962e 100%);">
            <div class="glow" style="animation-delay: 0.5s;"></div>
            <div class="flame" style="animation-delay: 0.5s; animation-duration: 0.9s;"></div>
        </div>
        <div class="candle" style="position: relative; top: auto; left: auto; animation-delay: 0.5s; height: 100px; background: linear-gradient(to bottom, #d4af37 0%, #b8962e 100%);">
            <div class="glow"></div>
            <div class="flame" style="animation-duration: 1.5s;"></div>
        </div>
        <div class="candle" style="position: relative; top: auto; left: auto; animation-delay: 1.2s; height: 80px; background: linear-gradient(to bottom, #d4af37 0%, #b8962e 100%);">
            <div class="glow" style="animation-delay: 0.8s;"></div>
            <div class="flame" style="animation-delay: 0.8s; animation-duration: 0.8s;"></div>
        </div>
        <div class="candle" style="position: relative; top: auto; left: auto; animation-delay: 0.2s; height: 115px; background: linear-gradient(to bottom, #d4af37 0%, #b8962e 100%);">
            <div class="glow"></div>
            <div class="flame" style="animation-duration: 1.4s;"></div>
        </div>
    </div>
</div>
</div>""", unsafe_allow_html=True)

    # Sidebar Navigation
    st.sidebar.markdown(f"""
    <div style='text-align: center; padding: 1rem; border: 1px solid var(--primary-gold); border-radius: 12px; margin-bottom: 1.5rem;'>
        <h2 style='font-family: "Playfair Display", serif; color: #1a1a1a !important; font-size: 1.2rem; letter-spacing: 0.2em; margin: 0;'>NAVIGATOR</h2>
    </div>
    """, unsafe_allow_html=True)
    
    dashboards = {
        "Executive Command Center": executive_command,
        "Revenue & Sales Deep Dive": revenue_sales,
        "Product Profitability": product_profitability,
        "Cost Structure & Margin": cost_margin,
        "Seasonality & Planning": seasonality,
        "Cash Flow Intelligence": cash_flow,
        "YoY Comparative Analysis": yoy_comparison,
        "Early Warning System": early_warning,
        "Customer & Channel": customer_channel,
    }
    
    selected_dash_name = st.sidebar.radio("", list(dashboards.keys()))
    
    # ------------------ FILTERS ------------------
    st.sidebar.markdown("---")
    st.sidebar.markdown("<h3 style='color: #1a1a1a !important;'>🔍 Global Filters</h3>", unsafe_allow_html=True)
    
    # Year Filter
    years = [2024, 2025]
    if 'selected_year' not in st.session_state: st.session_state.selected_year = 2024
    selected_year = st.sidebar.selectbox("Select Year", years, index=years.index(2025) if 2025 in years else 0)
    st.session_state.selected_year = selected_year

    # Month Filter
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    if 'selected_months' not in st.session_state: st.session_state.selected_months = months
    selected_months = st.sidebar.multiselect("Select Months", months, default=months)
    st.session_state.selected_months = selected_months
    
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 LOGOUT", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Load Selected Dashboard View
    if selected_dash_name in dashboards:
        dashboards[selected_dash_name].load_view()



# ================= FOOTER =================
st.markdown("""
<div class="footer">
    <div class="divider"></div>
    <p class="footer-text">Est. 2024 • Handcrafted Luxury</p>
    <p class="footer-text">Developed by Sidekick</p>
</div>
""", unsafe_allow_html=True)