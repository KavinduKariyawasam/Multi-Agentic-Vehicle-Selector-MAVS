import streamlit as st

def render_inputs():
    st.header("Vehicle Search Criteria")
    location = st.text_input("Location", value="USA")
    budget = st.text_input("Budget (USD)", value="40000")
    allowed_sites_input = st.text_area(
        "Allowed Manufacturer Sites (optional, comma-separated)",
        placeholder="toyota.com, ford.com"
    )
    allowed_sites = [s.strip() for s in allowed_sites_input.split(",") if s.strip()]
    return location, budget, allowed_sites
