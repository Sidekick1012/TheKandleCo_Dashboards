import streamlit as st

def load_css(file_name="styles.css"):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def metric_card(title, value, sub_value, card_class, icon="📊"):
    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-icon" style="font-size: 1.0rem; margin-bottom: 0.2rem;">{icon}</div>
        <div style="font-size: 0.7rem; opacity: 0.8; margin-bottom: 0.1rem;">{title}</div>
        <div style="font-size: 1.25rem; font-weight: bold;">{value}</div>
        <div style="font-size: 0.6rem; opacity: 0.7; margin-top: 0.1rem;">{sub_value}</div>
    </div>
    """, unsafe_allow_html=True)

def observation_item(title, days_left, percent, color="#38A169"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 6px;">
            <div style="width: 28px; height: 28px; border-radius: 50%; border: 2px solid {color}; display: flex; align-items: center; justify-content: center; font-weight: bold; color: {color}; font-size: 0.65rem;">
                {percent}%
            </div>
            <div>
                <div style="font-weight: 600; font-size: 0.8rem;">{title}</div>
                <div style="font-size: 0.6rem; color: #718096;">{days_left}</div>
            </div>
        </div>
        <div style="font-size: 0.9rem; color: #CBD5E0;">⋮</div>
    </div>
    """, unsafe_allow_html=True)

def stats_item(label, value, icon_color, icon="🛒"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
        <div style="width: 26px; height: 26px; background-color: {icon_color}20; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: {icon_color}; margin-right: 8px; font-size: 0.8rem;">
            {icon}
        </div>
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 1px;">
                <span style="font-size: 0.7rem; color: #718096;">{label}</span>
                <span style="font-size: 0.7rem; font-weight: 600;">{value}</span>
            </div>
            <div class="progress-bar-bg" style="background-color: #EDF2F7; height: 3px; border-radius: 1.5px; width: 100%;">
                <div style="background-color: {icon_color}; height: 3px; border-radius: 1.5px; width: {value};"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
