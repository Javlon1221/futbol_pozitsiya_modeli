# app.py
import streamlit as st
import pickle

# Modelni yuklash
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("model/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# Interfeys
st.title("⚽ Yangi futbolchi uchun pozitsiyani aniqlash")

age = st.slider("Yosh", 16, 40, 22)
matches = st.number_input("O'yinlar soni", 0, 1000, 20)
goals = st.number_input("Gollar", 0, 100, 5)
assists = st.number_input("Assistlar", 0, 100, 3)

if st.button("Taxmin qilish"):
    prediction = model.predict([[age, matches, goals, assists]])
    position = le.inverse_transform(prediction)[0]
    st.success(f"✅ Taxmin qilingan pozitsiya: **{position}**")