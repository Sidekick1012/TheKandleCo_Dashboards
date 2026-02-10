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
    
    
    /* Login-only background - Clean Professional */
    body:has(.login-container) .stApp {
        background: #f5f5f5;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* AGGRESSIVE NO SCROLL - Force everything to fit viewport */
    body:has(.login-container),
    body:has(.login-container) html,
    body:has(.login-container) .stApp,
    body:has(.login-container) .main,
    body:has(.login-container) .block-container,
    body:has(.login-container) [data-testid="stAppViewContainer"],
    body:has(.login-container) [data-testid="stHeader"] {
        overflow: hidden !important;
        overflow-y: hidden !important;
        overflow-x: hidden !important;
        height: 100vh !important;
        max-height: 100vh !important;
        position: fixed !important;
        width: 100% !important;
    }
    
    body:has(.login-container) .block-container {
        padding: 0.3rem 1rem !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Hide Streamlit header and footer on login */
    body:has(.login-container) [data-testid="stHeader"],
    body:has(.login-container) footer {
        display: none !important;
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
    
    
    
    /* ==================== HEADER CANDLE LINE (Dashboard Only) ==================== */
    /* Candle line container - simple selector for reliability */
    .candle-line-container {
        position: fixed !important;
        top: 80px !important;
        left: 0 !important;
        right: 0 !important;
        width: 100% !important;
        height: 100px !important;
        display: flex !important;
        justify-content: space-evenly !important;
        align-items: flex-start !important;
        padding: 0 5% !important;
        z-index: 9999 !important;
        pointer-events: none !important;
        overflow: visible !important;
    }
    
    /* Individual candles - increased size for better visibility */
    .candle-line-container .candle {
        position: relative !important;
        width: 40px !important;
        height: 70px !important;
        background: linear-gradient(to bottom, #fff9e6 0%, #f5e6d3 50%, #e6d4b8 100%) !important;
        border-radius: 6px 6px 3px 3px !important;
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.15),
            inset 0 -2px 8px rgba(212, 175, 55, 0.3) !important;
        animation: candle-flicker 3s ease-in-out infinite !important;
    }
    
    /* Stagger animation delays for natural effect */
    .candle-line-container .candle:nth-child(1) { animation-delay: 0s; }
    .candle-line-container .candle:nth-child(2) { animation-delay: 0.3s; }
    .candle-line-container .candle:nth-child(3) { animation-delay: 0.6s; }
    .candle-line-container .candle:nth-child(4) { animation-delay: 0.9s; }
    .candle-line-container .candle:nth-child(5) { animation-delay: 1.2s; }
    .candle-line-container .candle:nth-child(6) { animation-delay: 0.4s; }
    .candle-line-container .candle:nth-child(7) { animation-delay: 0.7s; }
    
    .candle-line-container .candle::before {
        content: '';
        position: absolute;
        top: -4px;
        left: 50%;
        transform: translateX(-50%);
        width: 4px;
        height: 8px;
        background: #2d2d2d;
        border-radius: 50% 50% 0 0;
    }
    
    .candle-line-container .flame {
        position: absolute;
        top: -16px;
        left: 50%;
        transform: translateX(-50%);
        width: 10px;
        height: 24px;
        background: linear-gradient(to top, 
            rgba(255, 120, 0, 0.95) 0%, 
            rgba(255, 180, 0, 0.9) 40%, 
            rgba(255, 230, 80, 0.6) 80%, 
            rgba(255, 255, 255, 0.3) 100%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        box-shadow: 
            0 0 15px rgba(255, 140, 0, 0.8),
            0 0 30px rgba(255, 100, 0, 0.4);
        animation: flame-dance 1s ease-in-out infinite;
        filter: blur(0.4px);
    }
    
    .candle-line-container .flame::after {
        content: '';
        position: absolute;
        top: 4px;
        left: 50%;
        transform: translateX(-50%);
        width: 6px;
        height: 14px;
        background: linear-gradient(to top, 
            rgba(255, 220, 50, 0.95) 0%, 
            rgba(255, 255, 150, 0.7) 100%);
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        animation: flame-dance 0.7s ease-in-out infinite reverse;
    }
    
    .candle-line-container .glow {
        position: absolute;
        top: -28px;
        left: 50%;
        transform: translateX(-50%);
        width: 50px;
        height: 50px;
        background: radial-gradient(circle, 
            rgba(255, 180, 50, 0.4) 0%, 
            rgba(255, 140, 0, 0.15) 40%,
            transparent 70%);
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

    
    
    /* ==================== MINIMAL BRAND HEADER ==================== */
    .brand-header {
        text-align: center;
        margin: 0 0 0.2rem 0;
        padding-top: 0;
    }
    
    .brand-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.2em;
        color: #1a1a1a;
        margin: 0;
    }
    
    .brand-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.65rem;
        font-weight: 400;
        letter-spacing: 0.1em;
        color: #666;
        margin-top: 0.15rem;
        text-transform: uppercase;
    }
    
    .divider {
        width: 40px;
        height: 2px;
        background: #0066cc;
        margin: 0.4rem auto;
    }
    
    /* ==================== MINIMAL PROFESSIONAL LOGIN ==================== */
    .login-container {
        background: #ffffff;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin: 0.2rem auto;
        max-width: 300px;
        border: 1px solid #e0e0e0;
    }
    
    .login-content {
        position: relative;
    }
    
    .login-icon {
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .login-icon-circle {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        background: #0066cc;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0, 102, 204, 0.2);
    }
    
    .login-icon-circle::before {
        content: '🔒';
        font-size: 1.3rem;
    }
    
    
    .login-title {
        font-family: 'Montserrat', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        text-align: center;
        color: #1a1a1a;
        margin-bottom: 0.25rem;
    }
    
    .login-subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        text-align: center;
        color: #666;
        margin-bottom: 0.9rem;
    }
    
    
    /* Professional Input Fields */
    .stTextInput > div > div > input {
        border: 1px solid #d0d0d0;
        border-radius: 4px;
        padding: 0.65rem 0.85rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.85rem;
        font-weight: 400;
        color: #1a1a1a !important;
        transition: all 0.2s ease;
        background: #ffffff;
        box-shadow: none;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
        background: #ffffff;
        outline: none;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #999;
        font-style: normal;
        font-size: 0.85rem;
    }
    
    /* Professional Labels */
    .stTextInput > label {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        color: #1a1a1a;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
        display: block;
    }
    
    .stTextInput > label::before {
        display: none;
    }
    
    .stButton > button[kind="primary"] {
        background: #0066cc;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 0.65rem 1.1rem;
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
        margin-top: 0.7rem;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #0052a3;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3);
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 102, 204, 0.2);
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

# ================= CANDLE LINE HEADER (Dashboard Only) =================
# Show candle line across header when logged in (on dashboard pages, not login page)
if st.session_state.get('logged_in', False):
    st.markdown("""
    <div class="candle-line-container">
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
        <div class="candle">
            <div class="glow"></div>
            <div class="flame"></div>
        </div>
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