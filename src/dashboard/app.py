# dashboard/app.py
import streamlit as st
import pandas as pd
import requests
import time
import altair as alt
from collections import deque
import numpy as np
import os
from pathlib import Path

st.set_page_config(
    page_title="AI Cybersecurity Intrusion Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS ======================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Root Variables */
    :root {
        --bg-primary: #FFFFFF;
        --bg-secondary: #F5F5F5;
        --bg-tertiary: #E8E8E8;
        --accent-yellow: #FFD700;
        --accent-blue: #2196F3;
        --text-primary: #212121;
        --text-secondary: #757575;
        --text-tertiary: #BDBDBD;
        --border-radius: 12px;
        --border-radius-large: 16px;
        --shadow-card: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-hover: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        background-color: var(--bg-secondary);
    }
    
    /* Header Section - User Greeting Style */
    .header-container {
        background: linear-gradient(135deg, var(--accent-yellow) 0%, #FFEB3B 100%);
        padding: 24px 32px;
        border-radius: var(--border-radius-large);
        margin-bottom: 32px;
        box-shadow: var(--shadow-card);
    }
    
    .header-title {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        line-height: 1.2;
    }
    
    .header-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-top: 8px;
        font-weight: 400;
    }
    
    /* Card Styling */
    .card {
        background: var(--bg-primary);
        border-radius: var(--border-radius);
        padding: 24px;
        box-shadow: var(--shadow-card);
        margin-bottom: 24px;
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .card-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 16px;
    }
    
    /* List Item Styling */
    .list-item {
        background: var(--bg-secondary);
        border-radius: var(--border-radius);
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .list-item:hover {
        background: var(--bg-tertiary);
        box-shadow: var(--shadow-hover);
    }
    
    .list-item-content {
        display: flex;
        align-items: center;
        gap: 12px;
        flex: 1;
    }
    
    .list-item-icon {
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--accent-blue);
        border-radius: 8px;
        color: white;
        font-size: 18px;
    }
    
    .list-item-text {
        flex: 1;
    }
    
    .list-item-title {
        font-size: 16px;
        font-weight: 500;
        color: var(--text-primary);
        margin: 0;
    }
    
    .list-item-meta {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 4px;
    }
    
    .list-item-value {
        font-size: 18px;
        font-weight: 600;
        color: var(--accent-blue);
    }
    
    .list-item-arrow {
        color: var(--text-secondary);
        font-size: 16px;
    }
    
    /* Alert Badge */
    .alert-badge {
        background: #ff4b4b;
        color: white;
        padding: 12px 20px;
        border-radius: var(--border-radius);
        font-weight: 600;
        box-shadow: var(--shadow-card);
        margin-bottom: 24px;
    }
    
    /* Stat Card */
    .stat-card {
        background: var(--bg-primary);
        border-radius: var(--border-radius);
        padding: 20px;
        text-align: center;
        box-shadow: var(--shadow-card);
    }
    
    .stat-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--accent-blue);
        margin: 8px 0;
    }
    
    .stat-label {
        font-size: 14px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: var(--bg-primary);
    }
    
    /* Button Styling */
    .stButton > button {
        background: var(--text-primary);
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #000000;
        box-shadow: var(--shadow-hover);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid var(--bg-tertiary);
    }
    
    /* Slider Styling */
    .stSlider > div > div {
        background: var(--bg-tertiary);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HEADER SECTION ======================
def render_header(active_alerts=0):
    st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">🛡️ AI Cybersecurity Intrusion Detection</h1>
        <p class="header-subtitle">{active_alerts} active alerts • Real-time monitoring</p>
    </div>
    """, unsafe_allow_html=True)

# ====================== CARD COMPONENTS ======================
def render_stat_card(title, value, icon="📊"):
    st.markdown(f"""
    <div class="stat-card">
        <div style="font-size: 24px; margin-bottom: 8px;">{icon}</div>
        <div class="stat-value">{value}</div>
        <div class="stat-label">{title}</div>
    </div>
    """, unsafe_allow_html=True)

def render_list_item(icon, title, meta, value, color="#2196F3"):
    st.markdown(f"""
    <div class="list-item">
        <div class="list-item-content">
            <div class="list-item-icon" style="background: {color};">{icon}</div>
            <div class="list-item-text">
                <div class="list-item-title">{title}</div>
                <div class="list-item-meta">{meta}</div>
            </div>
        </div>
        <div class="list-item-value">{value}</div>
        <div class="list-item-arrow">→</div>
    </div>
    """, unsafe_allow_html=True)

# ====================== MAIN APP ======================
# Sidebar menu
st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("", ["📡 Live Monitor", "📜 Attack History"], label_visibility="collapsed")

# Shared paths
log_path_csv = Path(__file__).parent.parent.parent / "dashboard" / "logs.csv"

# ====================== PAGE 1: LIVE MONITOR ======================
if page == "📡 Live Monitor":
    # Initialize session state
    if 'total_attacks' not in st.session_state:
        st.session_state.total_attacks = 0
    if 'history' not in st.session_state:
        st.session_state.history = deque(maxlen=100)
    
    # Render header
    render_header(active_alerts=st.session_state.total_attacks)
    
    # Sidebar controls
    st.sidebar.markdown("### ⚙️ Settings")
    api_url = st.sidebar.text_input("FastAPI URL:", "http://127.0.0.1:8000/predict")
    dataset_path = st.sidebar.text_input("Dataset path:", "data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
    rate = st.sidebar.slider("Rows per second", 1, 20, 5)
    simulate = st.sidebar.button("▶️ Start Live Feed", type="primary")
    
    # Main content area
    if simulate:
        st.sidebar.success("✅ Streaming active... Refresh to stop.")
        
        # Load dataset
        with st.spinner("📂 Loading dataset..."):
            df_all = pd.read_csv(dataset_path, low_memory=False)
            df_all.columns = df_all.columns.str.strip()
            numeric_cols = df_all.select_dtypes(include=[np.number]).columns.tolist()
        
        # Two column layout
        left_col, right_col = st.columns([1.2, 1])
        
        # Left column: Analytics and Threat List
        with left_col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">⚡ AI Threat Analytics</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Real-time detection summary</div>', unsafe_allow_html=True)
            
            # Stats row
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                render_stat_card("Total Detections", len(st.session_state.history), "🔍")
            with stats_col2:
                render_stat_card("Attacks", st.session_state.total_attacks, "🚨")
            with stats_col3:
                if len(st.session_state.history) > 0:
                    avg_conf = np.mean([h['confidence'] for h in st.session_state.history])
                    render_stat_card("Avg Confidence", f"{avg_conf:.1%}", "📊")
                else:
                    render_stat_card("Avg Confidence", "0%", "📊")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Threat List
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🎯 Recent Detections</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Latest threat predictions</div>', unsafe_allow_html=True)
            
            # Show recent threats
            if len(st.session_state.history) > 0:
                recent = list(st.session_state.history)[-5:]
                for item in reversed(recent):
                    threat_type = item['prediction']
                    conf = item['confidence']
                    time_str = item['time']
                    
                    # Color coding
                    if threat_type == "DDoS":
                        color = "#ff4b4b"
                        icon = "🚨"
                    else:
                        color = "#4CAF50"
                        icon = "✅"
                    
                    render_list_item(
                        icon=icon,
                        title=threat_type,
                        meta=f"Detected at {time_str}",
                        value=f"{conf:.1%}",
                        color=color
                    )
            else:
                st.info("No detections yet. Start the feed to begin monitoring.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Right column: Controls and Charts
        with right_col:
            # Alert placeholder
            alert_placeholder = st.empty()
            
            # Control Card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">🌡️ Real-time Monitor</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-subtitle">Active monitoring status</div>', unsafe_allow_html=True)
            
            # Current status
            if len(st.session_state.history) > 0:
                latest = st.session_state.history[-1]
                current_pred = latest['prediction']
                current_conf = latest['confidence']
                
                status_color = "#ff4b4b" if current_pred == "DDoS" else "#4CAF50"
                status_icon = "🚨" if current_pred == "DDoS" else "✅"
                
                st.markdown(f"""
                <div style="text-align: center; padding: 24px;">
                    <div style="font-size: 48px; margin-bottom: 16px;">{status_icon}</div>
                    <div style="font-size: 32px; font-weight: 700; color: {status_color}; margin-bottom: 8px;">
                        {current_pred}
                    </div>
                    <div style="font-size: 18px; color: var(--text-secondary);">
                        Confidence: {current_conf:.1%}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 24px; color: var(--text-secondary);">
                    Waiting for data...
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Charts Card
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="card-title">📊 Attack Frequency</div>', unsafe_allow_html=True)
            
            if len(st.session_state.history) > 0:
                df = pd.DataFrame(st.session_state.history)
                freq_df = df.groupby(["time", "prediction"]).size().reset_index(name="count")
                
                chart = (
                    alt.Chart(freq_df)
                    .mark_line(point=True, strokeWidth=3)
                    .encode(
                        x=alt.X("time:O", title="Time"),
                        y=alt.Y("count:Q", title="Count"),
                        color=alt.Color("prediction:N", scale=alt.Scale(
                            domain=["DDoS", "BENIGN"],
                            range=["#ff4b4b", "#4CAF50"]
                        ))
                    )
                    .properties(height=250)
                )
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Chart will appear once data is streaming.")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Streaming loop
        for _, row in df_all.iterrows():
            feature_dict = {col: float(row[col]) if not pd.isna(row[col]) else 0.0 for col in numeric_cols}
            sample_flow = {"features": feature_dict}
            
            try:
                r = requests.post(api_url, json=sample_flow, timeout=3)
                data = r.json()
                timestamp = time.strftime("%H:%M:%S")
                prediction = data["prediction"]
                confidence = data["confidence"]
                
                st.session_state.history.append({
                    "time": timestamp,
                    "prediction": prediction,
                    "confidence": confidence
                })
                
                # Alert handling
                if prediction == "DDoS" and confidence > 0.9:
                    st.session_state.total_attacks += 1
                    alert_placeholder.markdown(
                        f"""
                        <div class="alert-badge">
                            🚨 High-Confidence DDoS Detected! (Confidence: {confidence:.1%})
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.balloons()
                else:
                    alert_placeholder.empty()
                
                # Log to CSV
                log_entry = {"timestamp": timestamp, "prediction": prediction, "confidence": confidence}
                log_df = pd.DataFrame([log_entry])
                log_df.to_csv(log_path_csv, mode='a', header=not log_path_csv.exists(), index=False)
                
                time.sleep(1 / rate)
                st.experimental_rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
                time.sleep(1)
    
    else:
        # Initial state - show instructions
        st.markdown("""
        <div class="card">
            <div class="card-title">🚀 Getting Started</div>
            <div class="card-subtitle">Configure settings and start monitoring</div>
            <p style="color: var(--text-secondary); line-height: 1.6;">
                1. Verify your FastAPI URL in the sidebar<br>
                2. Set your dataset path<br>
                3. Adjust the streaming rate<br>
                4. Click "Start Live Feed" to begin
            </p>
        </div>
        """, unsafe_allow_html=True)

# ====================== PAGE 2: ATTACK HISTORY ======================
elif page == "📜 Attack History":
    render_header()
    
    st.sidebar.markdown("### ⚙️ Settings")
    refresh_rate = st.sidebar.slider("Auto-refresh interval (seconds)", 3, 30, 5)
    auto_refresh = st.sidebar.checkbox("🔄 Enable auto-refresh", value=True)
    
    placeholder = st.empty()
    
    if not log_path_csv.exists():
        st.markdown("""
        <div class="card">
            <div class="card-title">📋 No History Yet</div>
            <p style="color: var(--text-secondary);">
                Run the live monitor first to collect detections.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        while True:
            df_logs = pd.read_csv(log_path_csv)
            
            with placeholder.container():
                # Stats
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    render_stat_card("Total Logs", len(df_logs), "📊")
                with stats_col2:
                    attack_count = len(df_logs[df_logs['prediction'] == 'DDoS'])
                    render_stat_card("Attacks", attack_count, "🚨")
                with stats_col3:
                    avg_conf = df_logs['confidence'].mean()
                    render_stat_card("Avg Confidence", f"{avg_conf:.1%}", "📈")
                
                # Attack Distribution Chart
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">📊 Attack Type Distribution</div>', unsafe_allow_html=True)
                
                count_chart = (
                    alt.Chart(df_logs)
                    .mark_bar(cornerRadius=8)
                    .encode(
                        x=alt.X("prediction:N", title="Attack Type"),
                        y=alt.Y("count()", title="Count"),
                        color=alt.Color("prediction:N", scale=alt.Scale(
                            domain=["DDoS", "BENIGN"],
                            range=["#ff4b4b", "#4CAF50"]
                        ))
                    )
                    .properties(height=300)
                )
                st.altair_chart(count_chart, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Data table
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">📋 Detection Log</div>', unsafe_allow_html=True)
                st.markdown('<div class="card-subtitle">Last 50 detections</div>', unsafe_allow_html=True)
                st.dataframe(df_logs.tail(50), use_container_width=True, height=400)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="⬇️ Download Full Log CSV",
                    data=df_logs.to_csv(index=False).encode('utf-8'),
                    file_name="attack_logs.csv",
                    mime="text/csv"
                )
            
            if not auto_refresh:
                break
            time.sleep(refresh_rate)
            st.experimental_rerun()
