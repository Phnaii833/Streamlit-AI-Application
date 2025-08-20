import streamlit as st
import pandas as pd
from datetime import datetime
from langdetect import detect

st.title("🪔 Local Lore Collector")
st.markdown("Preserve your region's stories, proverbs, and history.")

# Initialize session state
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

# List of Indian states (you can add more if needed)
states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
    "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab",
    "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal",
    "Delhi", "Jammu and Kashmir", "Ladakh", "Puducherry"
]

if not st.session_state.form_submitted:
    # Show the form
    with st.form("lore_form", clear_on_submit=True):
        name = st.text_input("Your Name (optional)")

        state = st.selectbox("Select Your State", states)
        region = st.text_input("Enter Your Region/District")

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
            "state": state,
            "region": region,
            "language_selected": language,
            "category": category,
            "text": text,
            "detected_lang": detected_lang
        }

        df = pd.DataFrame([submission])
        df.to_csv("submissions.csv", mode='a', header=False, index=False)

        # Mark as submitted
        st.session_state.form_submitted = True
        st.rerun()   # 👈 force refresh so the "Submit Another Entry" button shows

    elif submit:
        st.warning("Please enter the text before submitting.")

else:
    # Show thank you + button for new entry
    st.success("🎉 Your submission was recorded.")
    if st.button("➕ Submit Another Entry"):
        st.session_state.form_submitted = False
        st.rerun()