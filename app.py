import streamlit as st
import pandas as pd
from datetime import datetime
from langdetect import detect

st.title("🪔 Local Lore Collector")
st.markdown("Preserve your region's stories, proverbs, and history.")


with st.form("lore_form"):
    name = st.text_input("Your Name (optional)")
    region = st.text_input("Your Region (e.g., Andhra Pradesh)")
    
    language = st.selectbox("Language", ["Telugu", "Hindi", "Tamil", "Marathi", "Odia", "Other"])
    category = st.radio("Type of Entry", ["Folk Story", "Proverb", "Local History"])
    text = st.text_area("Write your lore here", height=200)
    audio = st.file_uploader("Optional: Upload audio file", type=["mp3", "wav"])
    submit = st.form_submit_button("Submit")

if submit and text.strip():
    try:
        detected_lang = detect(text)
    except:
        detected_lang = "unknown"

    submission = {
        "timestamp": datetime.now().isoformat(),
        "name": name,
        "region": region,
        "language_selected": language,
        "category": category,
        "text": text,
        "detected_lang": detected_lang
    }


    df = pd.DataFrame([submission])
    df.to_csv("submissions.csv", mode='a', header=False, index=False)

    st.success("✅ Thank you! Your lore has been saved.")
    st.markdown(f"Detected Language: **{detected_lang}**")

else:
    if submit:
        st.warning("Please enter the text before submitting.")
