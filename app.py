import streamlit as st
from streamlit_demo.letter_interpreter import run_interpreter

# -----------------
# Streamlit UI
# -----------------
st.set_page_config(page_title="Gestura", page_icon="🤟", layout="wide")

st.title("🤟 Gestura - Real-Time Gesture Translator")
st.markdown("Translate hand gestures into live subtitles **with speech output** 🎤")

st.sidebar.header("⚙️ Controls")
run = st.sidebar.checkbox("📷 Start Camera")

if run:
    run_interpreter()
else:
    st.info("👆 Turn on the camera from the sidebar to start gesture recognition.")

#streamlit run app.py
