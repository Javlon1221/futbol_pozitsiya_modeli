import joblib
import numpy as np

# 1. Model va encoder'ni yuklash
model = joblib.load("models/model.pkl")
encoder = joblib.load("models/encoder.pkl")

# 2. Foydalanuvchidan input olish
print("Iltimos, o'yinchi statistikalarini kiriting:")
age = int(input("Yoshi: "))
matches = int(input("O'yinlar soni: "))
goals = int(input("Gollar soni: "))
assists = int(input("Assistlar soni: "))
yellow_cards = int(input("Sariq kartochkalar soni: "))
red_cards = int(input("Qizil kartochkalar soni: "))

# 3. Kiritilgan qiymatlarni model uchun formatlash
input_data = np.array([[age, matches, goals, assists, yellow_cards, red_cards]])

# 4. Bashorat qilish
predicted_label = model.predict(input_data)
predicted_position = encoder.inverse_transform(predicted_label)

# 5. Natijani chiqarish
print(f"\n🔮 Bashorat qilingan pozitsiya: {predicted_position[0]}")
