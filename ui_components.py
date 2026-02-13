import streamlit as st

def load_css(file_name="styles.css"):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def metric_card(title, value, sub_value, card_class, icon="📊"):
    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-icon">{icon}</div>
        <div style="font-size: 0.8rem; opacity: 0.8; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 1.8rem; font-weight: bold;">{value}</div>
        <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 0.5rem;">{sub_value}</div>
    </div>
    """, unsafe_allow_html=True)

def observation_item(title, days_left, percent, color="#38A169"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 40px; height: 40px; border-radius: 50%; border: 2px solid {color}; display: flex; align-items: center; justify-content: center; font-weight: bold; color: {color};">
                {percent}%
            </div>
            <div>
                <div style="font-weight: 600; font-size: 0.9rem;">{title}</div>
                <div style="font-size: 0.7rem; color: #718096;">{days_left} days left</div>
            </div>
        </div>
        <div style="font-size: 1.2rem; color: #CBD5E0;">⋮</div>
    </div>
    """, unsafe_allow_html=True)

def stats_item(label, value, icon_color, icon="🛒"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 15px;">
        <div style="width: 35px; height: 35px; background-color: {icon_color}20; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: {icon_color}; margin-right: 12px;">
            {icon}
        </div>
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-size: 0.8rem; color: #718096;">{label}</span>
                <span style="font-size: 0.8rem; font-weight: 600;">{value}</span>
            </div>
            <div class="progress-bar-bg" style="background-color: #EDF2F7; height: 6px; border-radius: 3px; width: 100%;">
                <div style="background-color: {icon_color}; height: 6px; border-radius: 3px; width: {value};"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
