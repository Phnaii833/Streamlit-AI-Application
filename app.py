# app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from langdetect import detect
from pathlib import Path

# Import the dictionary containing state and region data
from states_data import state_regions

# --- CONFIGURATION & CONSTANTS ---
st.set_page_config(page_title="Local Lore Collector", layout="centered")

CSV_PATH = Path("submissions.csv")
UPLOAD_DIR = Path("uploads")

# Placeholders for select boxes
STATE_PLACEHOLDER = "Select State"
REGION_PLACEHOLDER = "Select Region"

# Ensure the upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True)


# --- CALLBACK FUNCTION ---
def on_state_change():
    """Resets the region selection when the state changes."""
    st.session_state.region_select = REGION_PLACEHOLDER


# --- HELPER FUNCTION ---
def handle_submission(name, state, region, language, category, text, audio):
    """Processes and saves a single form submission."""
    # 1. Validate inputs
    if not name.strip():
        st.warning("Please enter your name. This field is required.")
        return
        
    if not text.strip():
        st.warning("Please enter the text for your lore before submitting.")
        return

    # 2. Process data and files
    timestamp = datetime.now().isoformat()
    audio_saved_path = ""
    detected_lang = "unknown"

    try:
        detected_lang = detect(text)
    except Exception:
        st.warning("Could not automatically detect the language.")

    if audio:
        try:
            safe_time = timestamp.replace(":", "-").replace(".", "_")
            safe_name = f"{safe_time}_{audio.name}"
            audio_saved_path = UPLOAD_DIR / safe_name
            with open(audio_saved_path, "wb") as f:
                f.write(audio.getbuffer())
        except Exception as e:
            st.error(f"Failed to save uploaded audio: {e}")
            audio_saved_path = ""

    # 3. Structure data for saving
    submission = {
        "timestamp": timestamp,
        "name": name,
        "state": state,
        "region": region,
        "language_selected": language,
        "category": category,
        "text": text,
        "detected_lang": detected_lang,
        "audio_path": str(audio_saved_path),
    }

    # 4. Save to CSV
    try:
        df = pd.DataFrame([submission])
        write_header = not CSV_PATH.exists()
        df.to_csv(CSV_PATH, mode="a", header=write_header, index=False, encoding="utf-8")
        
        # 5. Update session state on success and rerun
        st.session_state.form_submitted = True
        st.rerun()

    except Exception as e:
        st.error(f"Failed to save submission to CSV: {e}")


# --- INITIALIZE SESSION STATE ---
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "state_select" not in st.session_state:
    st.session_state.state_select = STATE_PLACEHOLDER
if "region_select" not in st.session_state:
    st.session_state.region_select = REGION_PLACEHOLDER
# ADDED: Session state for the name input
if "name_input" not in st.session_state:
    st.session_state.name_input = ""

# --- UI RENDERING ---
st.title("🪔 Local Lore Collector")
st.markdown("Preserve your region's stories, proverbs, and history.")

# Display success message and "Submit Another" button
if st.session_state.form_submitted:
    st.success("🎉 Your submission was recorded. Thank you for contributing!")
    if st.button("➕ Submit Another Entry"):
        st.session_state.form_submitted = False
        st.session_state.state_select = STATE_PLACEHOLDER
        st.session_state.region_select = REGION_PLACEHOLDER
        # ADDED: Reset the name field for the next submission
        st.session_state.name_input = ""
        st.rerun()
else:
    # --- STEP 1: SHARE YOUR DETAILS (OUTSIDE THE FORM) ---
    # CHANGED: Updated the subheader text
    st.subheader("Step 1: Share Your Details")
    
    # MOVED: The name input is now here, outside the form
    st.text_input("Your Name*", key="name_input")
    
    available_states = sorted(list(state_regions.keys()))
    state_options = [STATE_PLACEHOLDER] + available_states
    
    st.selectbox(
        "Select Your State",
        options=state_options,
        key="state_select",
        on_change=on_state_change,
    )
    
    selected_state = st.session_state.state_select
    
    if selected_state != STATE_PLACEHOLDER:
        regions_for_state = sorted(state_regions[selected_state])
        region_options = [REGION_PLACEHOLDER] + regions_for_state
    else:
        region_options = [REGION_PLACEHOLDER]

    st.selectbox(
        "Select Your Region / District",
        options=region_options,
        key="region_select",
        disabled=(selected_state == STATE_PLACEHOLDER),
    )
    selected_region = st.session_state.region_select

    st.divider()

    # --- STEP 2: LORE SUBMISSION (INSIDE THE FORM) ---
    # CHANGED: The form will only appear after all details in Step 1 are filled
    if st.session_state.name_input.strip() and selected_state != STATE_PLACEHOLDER and selected_region != REGION_PLACEHOLDER:
        st.subheader("Step 2: Share Your Lore")
        with st.form("lore_form"):
            # REMOVED: Name input is no longer in the form
            language = st.selectbox("Language", ["Telugu", "Hindi", "Tamil", "Marathi", "Odia", "Other"])
            category = st.radio("Type of Entry", ["Folk Story", "Proverb", "Local History"])
            text = st.text_area("Write your lore here", height=200, placeholder="Start writing your story or proverb...")
            audio = st.file_uploader("Optional: Upload an audio recording", type=["mp3", "wav", "m4a"])
            
            submit_button = st.form_submit_button("Submit Lore")

        if submit_button:
            # CHANGED: Pass the name from session_state into the handler
            handle_submission(st.session_state.name_input, selected_state, selected_region, language, category, text, audio)
    else:
        # CHANGED: Updated the prompt text
        st.info("Please enter your name and select a state and region to proceed.")