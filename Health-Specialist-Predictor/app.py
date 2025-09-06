# app.py (root)
import os
import re
import pickle
import streamlit as st

# ---------- paths ----------
ROOT = os.path.abspath(os.path.dirname(__file__))
MODELS_DIR = os.path.join(ROOT, "models")
STOP_PATH = os.path.join(ROOT, "stop_words.ob")

# ---------- load artifacts ----------
with open(os.path.join(MODELS_DIR, "classifier.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODELS_DIR, "vectorizer.pkl"), "rb") as f:
    vectorizer = pickle.load(f)

with open(STOP_PATH, "rb") as fp:
    domain_stop_word = pickle.load(fp)

# ---------- SAME cleaning as training ----------
def clean_text_func(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"[^A-Za-z0-9^,!?.\/'+]", " ", text)
    text = re.sub(r"\+", " ", text)
    text = re.sub(r"[,.!?']", " ", text)
    text = re.sub(r":", " : ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"[0-9]", " ", text)
    final_text = ""
    for x in text.split():
        if x not in domain_stop_word:
            final_text += x + " "
    return final_text.strip()

# ---------- UI ----------
st.set_page_config(page_title="Health Specialist Predictor", page_icon="🩺")
st.title("Health Specialist Predictor")
st.caption("Enter the patient's symptoms to get a suggested healthcare specialist.")

symptoms = st.text_area("Detail your symptoms:", value="", height=100, placeholder="heartburn, blood in stool, sharp pain in abdomen")
col1, col2 = st.columns([1, 2])
with col1:
    clear = st.button("Clear")
with col2:
    submit = st.button("Submit")

if clear:
    st.experimental_rerun()

if submit:
    if not symptoms.strip():
        st.warning("Please enter some symptoms.")
    else:
        cleaned = clean_text_func(symptoms)
        X = vectorizer.transform([cleaned])
        pred = model.predict(X)[0]
        st.success(pred)
