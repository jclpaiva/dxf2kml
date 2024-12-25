import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown("""
        <style>
        .stButton button[kind="secondary"] {
            background-color: #28a745;
            color: white;
        }
        .stButton button[kind="secondary"]:hover {
            background-color: #218838;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)