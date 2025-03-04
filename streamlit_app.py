import streamlit as st
import pandas as pd
import random

# Define your password here
PASSWORD = "lla"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        password = st.text_input("Enter password", type="password")
        if st.button("Submit"):
            if password == PASSWORD:
                st.session_state["password_correct"] = True
                st.experimental_rerun()  # Rerun the app to update the view
            else:
                st.error("Incorrect password. Please try again.")
        return False
    return True

if check_password():
    @st.cache_data
    def load_data():
        sheet_url = "https://docs.google.com/spreadsheets/d/1L47EyHGWSRkEdCybjH1Sp_OLKbB9LpZshpq9GItqxNw/export?format=csv&
