# dashboard/app.py
import streamlit as st
import pandas as pd
import requests
import time
import altair as alt
from collections import deque
import numpy as np
import os

st.set_page_config(page_title="AI Cybersecurity Intrusion Detector", layout="wide")

st.title("🧠 AI Cybersecurity Intrusion Detection Dashboard")

# Sidebar menu
page = st.sidebar.radio("Navigation", ["📡 Live Monitor", "📜 Attack History"])

# Shared paths
log_path_csv = "dashboard/logs.csv"

# ====================== PAGE 1: LIVE MONITOR ======================
if page == "📡 Live Monitor":
    st.markdown("Live AI-powered intrusion detection — streaming data to your model and visualizing results in real time.")

    # Sidebar controls
    st.sidebar.header("Live Monitor Settings")
    api_url = st.sidebar.text_input("FastAPI URL:", "http://127.0.0.1:8000/predict")
    dataset_path = st.sidebar.text_input("Dataset path:", "data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
    rate = st.sidebar.slider("Rows per second", 1, 20, 5)
    simulate = st.sidebar.button("Start Live Feed")

    # Buffers
    max_points = 100
    history = deque(maxlen=max_points)
    attack_count = st.sidebar.empty()
    alert_placeholder = st.empty()
    table_col, chart_col = st.columns([1, 1])

    if simulate:
        st.sidebar.success("Streaming real data... Stop by refreshing the page.")
        total_attacks = 0

        # Load dataset
        st.write("📂 Loading dataset... This may take a moment.")
        df_all = pd.read_csv(dataset_path, low_memory=False)
        df_all.columns = df_all.columns.str.strip()
        numeric_cols = df_all.select_dtypes(include=[np.number]).columns.tolist()

        for _, row in df_all.iterrows():
            feature_dict = {col: float(row[col]) if not pd.isna(row[col]) else 0.0 for col in numeric_cols}
            sample_flow = {"features": feature_dict}

            try:
                r = requests.post(api_url, json=sample_flow, timeout=3)
                data = r.json()
                timestamp = time.strftime("%H:%M:%S")
                prediction = data["prediction"]
                confidence = data["confidence"]

                history.append({
                    "time": timestamp,
                    "prediction": prediction,
                    "confidence": confidence
                })
                df = pd.DataFrame(history)

                # === ALERT HANDLER ===
                if prediction == "DDoS" and confidence > 0.9:
                    total_attacks += 1
                    alert_placeholder.markdown(
                        f"<div style='background-color:#ff4b4b;padding:10px;border-radius:10px;'>🚨 "
                        f"<strong>High-Confidence DDoS Detected!</strong> (Conf: {confidence:.2f})</div>",
                        unsafe_allow_html=True
                    )
                    st.balloons()
                else:
                    alert_placeholder.empty()

                # === LEFT: Table ===
                with table_col:
                    st.subheader("🧾 Recent Predictions")
                    def highlight_ddos(row):
                        color = 'background-color: #ffcccc' if row['prediction'] == 'DDoS' else ''
                        return [color]*len(row)
                    styled_df = df.tail(10).style.apply(highlight_ddos, axis=1)
                    st.dataframe(styled_df, use_container_width=True)

                # === RIGHT: Charts ===
                with chart_col:
                    st.subheader("📊 Attack Frequency Over Time")
                    freq_df = df.groupby(["time", "prediction"]).size().reset_index(name="count")
                    line_chart = (
                        alt.Chart(freq_df)
                        .mark_line(point=True)
                        .encode(x="time", y="count", color="prediction")
                        .properties(height=300)
                    )
                    st.altair_chart(line_chart, use_container_width=True)

                    st.subheader("📈 Confidence Trend")
                    conf_chart = (
                        alt.Chart(df)
                        .mark_line(point=True)
                        .encode(x="time", y="confidence", color="prediction")
                        .properties(height=250)
                    )
                    st.altair_chart(conf_chart, use_container_width=True)

                attack_count.markdown(f"**🧨 Total Attacks Detected:** `{total_attacks}`")

                # === LOG TO CSV ===
                log_entry = {"timestamp": timestamp, "prediction": prediction, "confidence": confidence}
                log_df = pd.DataFrame([log_entry])
                log_df.to_csv(log_path_csv, mode='a', header=not os.path.exists(log_path_csv), index=False)

                time.sleep(1 / rate)

            except Exception as e:
                st.error(f"Error: {e}")
                time.sleep(1)

# ====================== PAGE 2: ATTACK HISTORY ======================
elif page == "📜 Attack History":
    st.markdown("View all past detections logged by your system — automatically updates as new attacks are detected.")

    # Sidebar refresh rate control
    refresh_rate = st.sidebar.slider("Auto-refresh interval (seconds)", 3, 30, 5)
    auto_refresh = st.sidebar.checkbox("🔄 Enable auto-refresh", value=True)

    placeholder = st.empty()

    if not os.path.exists(log_path_csv):
        st.warning("No logs found yet. Run the live monitor first to collect detections.")
    else:
        while True:
            df_logs = pd.read_csv(log_path_csv)
            with placeholder.container():
                st.success(f"Loaded {len(df_logs)} logged detections.")
                st.dataframe(df_logs.tail(50), use_container_width=True)

                # Chart: Attack type count
                st.subheader("📊 Attack Type Distribution")
                count_chart = (
                    alt.Chart(df_logs)
                    .mark_bar()
                    .encode(x="prediction", y="count()", color="prediction")
                    .properties(height=300)
                )
                st.altair_chart(count_chart, use_container_width=True)

                # Chart: Confidence over time
                st.subheader("📈 Confidence Over Time (All Detections)")
                line_chart = (
                    alt.Chart(df_logs)
                    .mark_line(point=True)
                    .encode(x="timestamp", y="confidence", color="prediction")
                    .properties(height=300)
                )
                st.altair_chart(line_chart, use_container_width=True)

                # Export button
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
