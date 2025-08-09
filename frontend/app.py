import streamlit as st
from services.api_client import APIClient
from components.inputs import render_inputs
from components.results import render_results

st.set_page_config(page_title="Vehicle Recommender", layout="wide")

st.title("🚗 Vehicle Recommender")
st.write("Find the best vehicle options based on your budget and location.")

api_client = APIClient()

# Health check
if not api_client.health_check():
    st.error("Backend API is not reachable. Please check if FastAPI is running.")
    st.stop()

# Input form
with st.form("vehicle_form"):
    location, budget, allowed_sites = render_inputs()
    submitted = st.form_submit_button("Get Recommendations")

if submitted:
    with st.spinner("Fetching recommendations..."):
        data = api_client.get_recommendations(location, budget, allowed_sites)
    render_results(data)
