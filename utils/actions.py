import os
import psutil
import keyboard
import streamlit as st

def exit_application():
    """Handle application exit"""
    keyboard.press_and_release('ctrl+w')
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()
    st.stop()

def handle_reset():
    """Handle form reset"""
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Force a rerun
    st.rerun()