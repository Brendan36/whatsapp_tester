# dashboard/app.py

import streamlit as st
import io
import pandas as pd
import sys
import os
import plotly.express as px

# Setup Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tests import test_login, test_send_message, test_receive_message, test_delivery_status, test_logout

# Page Setup
st.set_page_config(layout="wide")
st.image("assets/divider_dark.png", width=100)
st.title("🧪 WhatsApp Web Tester Dashboard")

# Columns
col1, col2 = st.columns([1, 2])

# Session State Initialization
for key, value in {
    'driver': None,
    'login_completed': False,
    'logs_master': [],
    'logout_completed': False,
    'show_send_message_inputs': False,
    'show_delivery_status_button': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Helper Functions
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

# Left Column - Controls
with col1:
    st.markdown("#### 🔧 Test Controls")

    # --- Buttons Always Visible ---

    if st.button("▶️ Run Login Test"):
        if not st.session_state.login_completed and not st.session_state.logout_completed:
            driver, logs, login_successful = test_login.test_login()
            st.session_state.logs_master.extend(logs)
            if login_successful:
                st.session_state.driver = driver
                st.session_state.login_completed = True
                st.success("✅ Login successful!")
            else:
                st.error("⚠️ Login test failed. Please retry.")
        else:
            st.info("ℹ️ Already logged in or session ended. Restart app to login again.")

    if st.button("▶️ Run Send Message Test"):
        if st.session_state.login_completed:
            st.session_state.show_send_message_inputs = True
        else:
            st.warning("⚠️ Please login first before sending a message!")

    if st.button("▶️ Run Delivery Status Test"):
        if st.session_state.login_completed:
            st.session_state.show_delivery_status_button = True
        else:
            st.warning("⚠️ Please login first before checking delivery status!")

    if st.button("▶️ Run Logout Test"):
        if st.session_state.login_completed and not st.session_state.logout_completed:
            driver = st.session_state.driver
            logs = test_logout.test_logout(driver)
            st.session_state.logs_master.extend(logs)
            if driver:
                driver.quit()
            st.session_state.logout_completed = True
            st.success("✅ Logged Out Successfully!")
        else:
            st.warning("⚠️ Cannot logout without login or already logged out.")

# Right Column - Inputs, Results, Graphs
with col2:
    st.markdown("#### 📝 Test Inputs & Results")

    if st.session_state.show_send_message_inputs and st.session_state.login_completed:
        with st.expander("✉️ Send Message Inputs", expanded=True):
            contact_name = st.text_input("Enter Contact Name:", "Test Contact")
            custom_message = st.text_area("Enter Message:", "Hello from WhatsApp Web Tester Bot! 🚀")
            if st.button("✅ Send Now"):
                driver = st.session_state.driver
                logs_send = test_send_message.test_send_message(driver, contact_name, custom_message)
                logs_receive = test_receive_message.test_receive_message(driver)
                st.session_state.logs_master.extend(logs_send + logs_receive)
                st.success("✅ Message Sent and Receive Check Completed!")

    if st.session_state.logs_master:
        with st.expander("📄 View Test Results", expanded=True):
            final_summary_df = create_summary_table(st.session_state.logs_master)
            st.dataframe(final_summary_df)

            csv = final_summary_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download Full Test Summary CSV",
                data=csv,
                file_name="full_test_summary.csv",
                mime="text/csv"
            )

    if st.session_state.logout_completed:
        with st.expander("📈 View Final Graphs", expanded=False):
            final_summary_df = create_summary_table(st.session_state.logs_master)

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
            fig_timeline = px.timeline(df_timeline, x_start="Timestamp", x_end="Timestamp", y="Action",
                                       color_discrete_sequence=["#636EFA"], title="📊 Test Execution Timeline")
            fig_timeline.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_timeline, use_container_width=True)

            fig_bar = px.bar(df_timeline, x="Timestamp", y="Action",
                             color_discrete_sequence=["#636EFA"], title="📊 Test Execution Timeline (Bar Chart)")
            fig_bar.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_bar, use_container_width=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
footer_html = """
<p style="text-align:center; color:gray; font-size:0.8em; margin:0;">
Built with 💡 by | be | © 2025
</p>
"""
col2.markdown(footer_html, unsafe_allow_html=True)
