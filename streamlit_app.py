import streamlit as st
import requests
import datetime

# from exception.exceptions import TradingBotException
import sys

BASE_URL = "http://localhost:8000"  # Backend endpoint


# Streamlit layout options: "centered" (default) or "wide"
st.set_page_config(
    page_title="Travel Planner Agentic Application",
    page_icon="🌍",
    layout="wide",  # Change to "centered" for a narrower layout
    initial_sidebar_state="expanded",
)

st.title("✈️ Travel Plan With Agentic App 🚗")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.header("How can I help you in planning a trip? Let me know where do you want to visit.")

# Chat input box at bottom
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("User Input", placeholder="e.g. Plan a trip to Delhi for 5 days")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input.strip():
    try:

        with st.spinner("🧳 Keep calm, your trip plan is brewing..."):
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            markdown_content = f"""## 🗺️ Your Travel Itinerary - AI Generated

            {answer}
            """
            
            st.caption(f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d at %H:%M')}")
            st.markdown(markdown_content)
        else:
            st.error(" Bot failed to respond: " + response.text)

    except Exception as e:
        raise f"The response failed due to {e}"