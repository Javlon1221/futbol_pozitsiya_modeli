# app/app.py
import streamlit as st
import pandas as pd
import joblib

# 1) Modelni yuklash
model = joblib.load("../models/model.pkl")

# 2) UI elementi
st.title("Yangi Futbolchi Pozitsiyasini Bashorat Qilish")

speed = st.slider("Tezlik", 0, 100)
strength = st.slider("Kuch", 0, 100)
passing = st.slider("Pas", 0, 100)
shooting = st.slider("Zarba", 0, 100)

input_df = pd.DataFrame([[speed, strength, passing, shooting]],
                        columns=["speed","strength","passing","shooting"])

if st.button("Pozitsiyani aniqlash"):
    pred = model.predict(input_df)
    st.success(f"Tavsiya etilgan pozitsiya: {pred[0]}")