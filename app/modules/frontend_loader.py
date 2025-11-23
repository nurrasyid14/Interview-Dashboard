import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Resolve frontend folder absolutely, no matter where Streamlit is run from
BASE = Path(__file__).resolve().parent.parent.parent / "frontend"

def load_css(name="style.css"):
    path = BASE / "static" / name
    if path.exists():
        st.markdown(f"<style>{path.read_text()}</style>", unsafe_allow_html=True)

def load_js(name="script.js"):
    path = BASE / "static" / name
    if path.exists():
        st.markdown(f"<script>{path.read_text()}</script>", unsafe_allow_html=True)

def render_template(name, height=600):
    path = BASE / "templates" / name
    if path.exists():
        components.html(path.read_text(), height=height, scrolling=True)
