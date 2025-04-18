import joblib
import numpy as np
import pandas as pd

# 1. Model va encoder'ni yuklash
model = joblib.load("models/model.pkl")
encoder = joblib.load("models/encoder.pkl")

# 2. Foydalanuvchidan ism va statistikalarni olish
name = input("O'yinchi ismini kiriting: ")
print(f"\n{name}, o'yinchi statistikasini kiriting:")
age = int(input("Yoshi: "))
matches = int(input("O'yinlar soni: "))
goals = int(input("Gollar soni: "))
assists = int(input("Assistlar soni: "))
yellow_cards = int(input("Sariq kartochkalar soni: "))
red_cards = int(input("Qizil kartochkalar soni: "))

# 3. Feature nomlari bilan DataFrame (xatolikni oldini oladi)
input_data = pd.DataFrame([{
    'Age': age,
    'Matches': matches,
    'Goals': goals,
    'Assists': assists,
    'Yellow Cards': yellow_cards,
    'Red Cards': red_cards
}])

# 4. Bashorat qilish
predicted_label = model.predict(input_data)
predicted_position = encoder.inverse_transform(predicted_label)

# 5. Natijani chiqarish
print(f"\n🔮 {name} uchun bashorat qilingan pozitsiya: {predicted_position[0]}")
