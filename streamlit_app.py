import streamlit as st
import pandas as pd
import random

# Define your password here
PASSWORD = "your_password"

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
        sheet_url = "https://docs.google.com/spreadsheets/d/1L47EyHGWSRkEdCybjH1Sp_OLKbB9LpZshpq9GItqxNw/export?format=csv&gid=1747270692"
        df = pd.read_csv(sheet_url)
        cards = []
        for _, row in df.iterrows():
            person = row['Name']
            for i in range(1, 4):
                dua = row[f"Du'a {i}"]
                if pd.notna(dua):
                    cards.append({"text": dua, "person": person})
        random.shuffle(cards)  # Initial shuffle
        return cards

    # Load data and assign to the global variable
    cards = load_data()

    # Initialize session state for card navigation
    if 'current_card' not in st.session_state:
        st.session_state.current_card = 0

    # Navigation functions
    def next_card():
        st.session_state.current_card = (st.session_state.current_card + 1) % len(cards)

    def prev_card():
        st.session_state.current_card = (st.session_state.current_card - 1) % len(cards)

    # Custom CSS with improved styling
    st.markdown("""
    <style>
        .card {
            padding: 3rem;
            margin: 2rem auto;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
            background: white;
            max-width: 600px;
            min-height: 400px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        .dua-text {
            font-size: 1.8rem;
            line-height: 1.6;
            margin-bottom: 2rem;
            color: #2c3e50;
        }
        .person-name {
            font-size: 1.2rem;
            color: #7f8c8d;
            margin-top: auto;
            font-style: italic;
        }
        .nav-button {
            padding: 0.8rem 2rem;
            border-radius: 8px;
            font-size: 1.1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    # Card display
    if cards:
        current = cards[st.session_state.current_card]
        st.markdown(f"""
        <div class="card">
            <div class="dua-text">"{current['text']}"</div>
            <div class="person-name">{current['person']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.button("← Previous", on_click=prev_card, use_container_width=True, key='prev')
        with col3:
            st.button("Next →", on_click=next_card, use_container_width=True, key='next')

        # Card counter
        st.markdown(f"<div style='text-align: center; color: #95a5a6; margin-top: 1rem;'>"
                    f"Card {st.session_state.current_card + 1} of {len(cards)}</div>", 
                    unsafe_allow_html=True)
    else:
        st.error("No cards found. Please check the spreadsheet format.")
