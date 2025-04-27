# dashboard/app.py

import streamlit as st
import io
import pandas as pd
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tests import test_login, test_send_message, test_receive_message, test_delivery_status, test_logout

st.set_page_config(layout="wide")
st.image("assets/divider_dark.png", width=100)
st.title("🧪 WhatsApp Web Tester Dashboard")

col1, col2 = st.columns([1, 2])

# Session State Initialization
if 'driver' not in st.session_state:
    st.session_state.driver = None
if 'login_completed' not in st.session_state:
    st.session_state.login_completed = False
if 'logs_master' not in st.session_state:
    st.session_state.logs_master = []
if 'show_send_message_inputs' not in st.session_state:
    st.session_state.show_send_message_inputs = False
if 'show_delivery_status_button' not in st.session_state:
    st.session_state.show_delivery_status_button = False
if 'show_logout_button' not in st.session_state:
    st.session_state.show_logout_button = False

def create_summary_table(logs):
    actions, results = [], []
    for entry in logs:
        parts = entry.split('] [')
        if len(parts) >= 3:
            status = parts[2].replace(']', '')
            message = ']'.join(parts[3:]).replace(']', '')
            actions.append(message.strip())
            results.append(status.strip())
    return pd.DataFrame({"Status": actions, "Result": results})

with col1:
    st.markdown("#### 🔧 Test Controls")

    if st.button("▶️ Run Login Test"):
        driver, logs, login_successful = test_login.test_login()
        st.session_state.logs_master.extend(logs)
        if login_successful:
            st.session_state.driver = driver
            st.session_state.login_completed = True
            st.success("✅ Login successful!")
        else:
            st.error("⚠️ Login test failed. Please retry.")

    if st.session_state.login_completed:
        if not st.session_state.show_send_message_inputs:
            if st.button("▶️ Run Send Message Test"):
                st.session_state.show_send_message_inputs = True

    if st.session_state.show_delivery_status_button:
        if st.button("▶️ Run Delivery Status Test"):
            driver = st.session_state.driver
            logs_delivery = test_delivery_status.test_delivery_status(driver)
            st.session_state.logs_master.extend(logs_delivery)
            st.session_state.show_logout_button = True
            st.success("✅ Delivery Status Checked!")

    if st.session_state.show_logout_button:
        if st.button("▶️ Run Logout Test"):
            driver = st.session_state.driver
            logs_logout = test_logout.test_logout(driver)
            st.session_state.logs_master.extend(logs_logout)
            if driver:
                driver.quit()
            st.success("✅ Logged Out Successfully!")

with col2:
    st.markdown("#### 📝 Test Logs & Inputs")

    if st.session_state.show_send_message_inputs:
        contact_name = st.text_input("Enter Contact Name:", "Test Contact")
        custom_message = st.text_area("Enter Message:", "Hello from WhatsApp Web Tester Bot! 🚀")
        if st.button("✅ Send Message"):
            driver = st.session_state.driver
            logs_send = test_send_message.test_send_message(driver, contact_name, custom_message)
            st.session_state.logs_master.extend(logs_send)
            logs_receive = test_receive_message.test_receive_message(driver)
            st.session_state.logs_master.extend(logs_receive)
            st.success("✅ Message Sent and Received Checked!")
            st.session_state.show_delivery_status_button = True

    if st.session_state.logs_master:
        final_summary_df = create_summary_table(st.session_state.logs_master)
        st.dataframe(final_summary_df)

        csv = final_summary_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Full Test Summary CSV",
            data=csv,
            file_name="full_test_summary.csv",
            mime="text/csv"
        )

        result_counts = final_summary_df['Result'].value_counts().reset_index()
        result_counts.columns = ['Result', 'Count']
        fig_pie = px.pie(result_counts, names='Result', values='Count', title="📈 Test Result Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

        actions, timestamps = [], []
        for entry in st.session_state.logs_master:
            parts = entry.split('] [')
            if len(parts) >= 2:
                timestamp = parts[0].replace('[', '').strip()
                action = ']'.join(parts[3:]).replace(']', '').strip()
                timestamps.append(timestamp)
                actions.append(action)

        df_timeline = pd.DataFrame({"Action": actions, "Timestamp": timestamps})
        fig_timeline = px.timeline(df_timeline, x_start="Timestamp", x_end="Timestamp", y="Action", color_discrete_sequence=["#636EFA"], title="📊 Test Execution Timeline")
        fig_timeline.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_timeline, use_container_width=True)

        fig_bar = px.bar(df_timeline, x="Timestamp", y="Action", color_discrete_sequence=["#636EFA"], title="📊 Test Execution Timeline (Bar Chart)")
        fig_bar.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_bar, use_container_width=True)

# ─── Footer ───
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
footer_html = """
    <p style="text-align:center; color:gray; font-size:0.8em; margin:0;">
      Built with 💡 by | be | © 2025
    </p>
    """
col2.markdown(footer_html, unsafe_allow_html=True)