import streamlit as st

def load_css(file_name="styles.css"):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def metric_card(title, value, sub_value, card_class, icon="📊"):
    st.markdown(f"""
    <div class="{card_class}">
        <div class="card-icon" style="font-size: 1.2rem; margin-bottom: 0.2rem;">{icon}</div>
        <div style="font-size: 0.75rem; opacity: 0.8; margin-bottom: 0.2rem;">{title}</div>
        <div style="font-size: 1.4rem; font-weight: bold;">{value}</div>
        <div style="font-size: 0.65rem; opacity: 0.7; margin-top: 0.2rem;">{sub_value}</div>
    </div>
    """, unsafe_allow_html=True)

def observation_item(title, days_left, percent, color="#38A169"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; border: 2px solid {color}; display: flex; align-items: center; justify-content: center; font-weight: bold; color: {color}; font-size: 0.7rem;">
                {percent}%
            </div>
            <div>
                <div style="font-weight: 600; font-size: 0.85rem;">{title}</div>
                <div style="font-size: 0.65rem; color: #718096;">{days_left}</div>
            </div>
        </div>
        <div style="font-size: 1rem; color: #CBD5E0;">⋮</div>
    </div>
    """, unsafe_allow_html=True)

def stats_item(label, value, icon_color, icon="🛒"):
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <div style="width: 30px; height: 30px; background-color: {icon_color}20; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: {icon_color}; margin-right: 10px; font-size: 0.9rem;">
            {icon}
        </div>
        <div style="flex-grow: 1;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 2px;">
                <span style="font-size: 0.75rem; color: #718096;">{label}</span>
                <span style="font-size: 0.75rem; font-weight: 600;">{value}</span>
            </div>
            <div class="progress-bar-bg" style="background-color: #EDF2F7; height: 4px; border-radius: 2px; width: 100%;">
                <div style="background-color: {icon_color}; height: 4px; border-radius: 2px; width: {value};"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
