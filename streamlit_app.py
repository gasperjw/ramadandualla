import streamlit as st
import pandas as pd
import random

# Cache data loading to improve performance
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

# Initialize session state
if 'cards' not in st.session_state:
    st.session_state.cards = load_data()

if 'current_card' not in st.session_state:
    st.session_state.current_card = 0

# Navigation functions with instant response
def navigate(delta):
    st.session_state.current_card = (st.session_state.current_card + delta) % len(st.session_state.cards)
    st.experimental_rerun()

def shuffle_cards():
    random.shuffle(st.session_state.cards)
    st.session_state.current_card = 0
    st.experimental_rerun()

# CSS remains the same as previous version...

# Display
current = st.session_state.cards[st.session_state.current_card]

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.button("← Previous", on_click=navigate, args=(-1,), key='prev')
with col3:
    st.button("Next →", on_click=navigate, args=(1,), key='next')

st.markdown(f"""
<div class="card">
    <div class="dua-text">"{current['text']}"</div>
    <div class="person-name">{current['person']}</div>
</div>
""", unsafe_allow_html=True)

# Add shuffle button and card counter
st.button("🔀 Shuffle Cards", on_click=shuffle_cards, use_container_width=True)
st.markdown(f"<div style='text-align: center; color: #95a5a6; margin-top: 1rem;'>"
            f"Card {st.session_state.current_card + 1} of {len(st.session_state.cards)}</div>", 
            unsafe_allow_html=True)
