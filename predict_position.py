import joblib
import numpy as np
import pandas as pd
import psycopg2

# ========== Model va encoder'ni yuklash ==========
model = joblib.load("model/model.pkl")
encoder = joblib.load("model/label_encoder.pkl")

# ========== Ma'lumotlar bazasiga saqlash funksiyasi ==========
def save_to_db(name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position):
    try:
        conn = psycopg2.connect(
            dbname="futbol_db",
            user="postgres",
            password="0000",  # kerak bo‘lsa bu yerda parolni o‘zgartiring
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO players (name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        data = (name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position)
        cursor.execute(insert_query, data)
        conn.commit()

        print("✅ Ma'lumotlar bazaga saqlandi!")

        # ========== Barcha o'yinchilarni chiqarish ==========
        cursor.execute("SELECT * FROM players")
        rows = cursor.fetchall()

        print("\n📋 Barcha o'yinchilar ro'yxati:")
        for row in rows:
            print(row)

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Ma'lumot saqlashda xatolik:", e)

# ========== Yangi o'yinchi qo'shish funksiyasi ==========
def add_new_player():
    print("\nIltimos, o'yinchi ma'lumotlarini kiriting:")
    name = input("Ismi: ")
    age = int(input("Yoshi: "))
    matches = int(input("O'yinlar soni: "))
    goals = int(input("Gollar soni: "))
    assists = int(input("Assistlar soni: "))
    yellow_cards = int(input("Sariq kartochkalar soni: "))
    red_cards = int(input("Qizil kartochkalar soni: "))

    # Taxmin qilish
    input_data = pd.DataFrame([{
        "Age": age,
        "Matches": matches,
        "Goals": goals,
        "Assists": assists,
        "Yellow Cards": yellow_cards,
        "Red Cards": red_cards
    }])
    prediction = model.predict(input_data)[0]
    predicted_position = encoder.inverse_transform([prediction])[0]
    print(f"🏟️ Bashorat qilingan pozitsiya: {predicted_position}")

    # Saqlash
    save_to_db(name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position)

# ========== Menyu ==========
def main():
    while True:
        print("\n======== MENYU ========")
        print("1. Yangi o'yinchi qo'shish")
        print("2. Chiqish")

        choice = input("Tanlang (1 yoki 2): ")

        if choice == '1':
            add_new_player()
        elif choice == '2':
            print("Chiqmoqda...")
            break
        else:
            print("❌ Noto'g'ri tanlov! Iltimos, 1 yoki 2 ni tanlang.")

# ========== Dastur ishga tushadi ==========
main()
