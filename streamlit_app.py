import streamlit as st
import pandas as pd
from itertools import chain

# Read Google Sheet data
sheet_url = "https://docs.google.com/spreadsheets/d/1L47EyHGWSRkEdCybjH1Sp_OLKbB9LpZshpq9GItqxNw/export?format=csv"
df = pd.read_csv(sheet_url)

# Process data to create individual cards
cards = []
for _, row in df.iterrows():
    person = row['Person']
    for i in range(1, 4):
        dua = row[f'Dua {i}']
        if pd.notna(dua):
            cards.append({
                "text": dua,
                "person": person
            })

# Initialize session state for card navigation
if 'current_card' not in st.session_state:
    st.session_state.current_card = 0

# Function to handle navigation
def navigate(direction):
    if direction == 'next':
        st.session_state.current_card = (st.session_state.current_card + 1) % len(cards)
    else:
        st.session_state.current_card = (st.session_state.current_card - 1) % len(cards)

# Custom CSS for styling
st.markdown("""
<style>
    .card {
        padding: 2rem;
        margin: 2rem 0;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #ffffff;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .dua-text {
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .person-name {
        font-size: 1rem;
        color: #666666;
        margin-top: auto;
    }
    .nav-button {
        width: 100px;
    }
</style>
""", unsafe_allow_html=True)

# Display current card
if cards:
    current = cards[st.session_state.current_card]
    
    # Card container
    st.markdown(f"""
    <div class="card">
        <div class="dua-text">{current['text']}</div>
        <div class="person-name">- {current['person']} -</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.button("← Previous", on_click=navigate, args=('prev',), key='prev', use_container_width=True)
    with col3:
        st.button("Next →", on_click=navigate, args=('next',), key='next', use_container_width=True)
else:
    st.write("No duas found in the spreadsheet")

# Card counter
st.caption(f"Card {st.session_state.current_card + 1} of {len(cards)}")
