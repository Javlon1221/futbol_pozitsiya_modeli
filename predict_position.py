import joblib
import numpy as np
import pandas as pd
import psycopg2

# ========== Model va encoder'ni yuklash ==========
model = joblib.load("model/model.pkl")
encoder = joblib.load("model/label_encoder.pkl")

# ========== Ma'lumotlar bazasiga saqlash yoki yangilash ==========
def save_or_update_player(name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position):
    try:
        conn = psycopg2.connect(
            dbname="futbol_db",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        check_query = "SELECT * FROM players WHERE name = %s AND age = %s"
        cursor.execute(check_query, (name, age))
        existing_player = cursor.fetchone()

        if existing_player:
            print("\n⚠️ Bunday o'yinchi allaqachon mavjud.")
            update = input("🛠️ Ma'lumotni yangilamoqchimisiz? (ha/yo'q): ").lower()
            if update == "ha":
                update_query = """
                    UPDATE players
                    SET matches = %s,
                        goals = %s,
                        assists = %s,
                        yellow_cards = %s,
                        red_cards = %s,
                        predicted_position = %s
                    WHERE name = %s AND age = %s
                """
                cursor.execute(update_query, (matches, goals, assists, yellow_cards, red_cards, predicted_position, name, age))
                conn.commit()
                print("✅ Ma'lumot yangilandi!")
            else:
                print("ℹ️ Ma'lumot o'zgartirilmadi.")
        else:
            insert_query = """
                INSERT INTO players (name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position))
            conn.commit()
            print("✅ Yangi o'yinchi qo'shildi!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Xatolik:", e)

# ========== O'yinchi o'chirish funksiyasi ==========
def delete_player():
    try:
        name = input("🗑️ O'chirish uchun o'yinchi ismini kiriting: ")
        age = int(input("Yoshini kiriting: "))

        conn = psycopg2.connect(
            dbname="futbol_db",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM players WHERE name = %s AND age = %s", (name, age))
        player = cursor.fetchone()
        if player:
            confirm = input("Rostdan ham o‘chirmoqchimisiz? (ha/yoq): ").lower()
            if confirm == "ha":
                cursor.execute("DELETE FROM players WHERE name = %s AND age = %s", (name, age))
                conn.commit()
                print("✅ O'yinchi o'chirildi.")
            else:
                print("❌ O'chirish bekor qilindi.")
        else:
            print("🚫 Bunday o'yinchi topilmadi.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ O'chirishda xatolik:", e)

# ========== O'yinchi qidirish funksiyasi ==========
def search_player():
    try:
        name = input("🔍 Qidirilayotgan o'yinchi ismi: ")
        age = int(input("Yoshi: "))

        conn = psycopg2.connect(
            dbname="futbol_db",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM players WHERE name = %s AND age = %s", (name, age))
        result = cursor.fetchone()

        if result:
            print("\n🧾 Topilgan o'yinchi ma'lumotlari:")
            print(result)
        else:
            print("🚫 Bunday o'yinchi topilmadi.")

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Qidirishda xatolik:", e)

# ========== Yangi o'yinchi qo'shish ==========
def add_new_player():
    print("\n📝 Iltimos, o'yinchi ma'lumotlarini kiriting:")
    name = input("Ismi: ")
    age = int(input("Yoshi: "))
    matches = int(input("O'yinlar soni: "))
    goals = int(input("Gollar soni: "))
    assists = int(input("Assistlar soni: "))
    yellow_cards = int(input("Sariq kartochkalar soni: "))
    red_cards = int(input("Qizil kartochkalar soni: "))

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

    print(f"\n📊 Bashorat qilingan pozitsiya: {predicted_position}")
    save_or_update_player(name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position)

# ========== Barcha o'yinchilarni ko‘rish ==========
def view_all_players():
    try:
        conn = psycopg2.connect(
            dbname="futbol_db",
            user="postgres",
            password="0000",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players")
        rows = cursor.fetchall()

        print("\n📋 Barcha o'yinchilar ro'yxati:")
        for row in rows:
            print(row)

        cursor.close()
        conn.close()

    except Exception as e:
        print("❌ Ma'lumotlarni chiqarishda xatolik:", e)

# ========== MENU ==========
def menu():
    while True:
        print("\n====== 🏆 FUTBOL O'YINCHILAR BAZASI ======")
        print("1. Yangi o'yinchi qo'shish / yangilash")
        print("2. Barcha o'yinchilarni ko‘rish")
        print("3. O'yinchi ma'lumotini o‘chirish")
        print("4. O'yinchi qidirish (ism va yosh bo‘yicha)")
        print("5. Chiqish")

        choice = input("Tanlov (1-5): ")

        if choice == "1":
            add_new_player()
        elif choice == "2":
            view_all_players()
        elif choice == "3":
            delete_player()
        elif choice == "4":
            search_player()
        elif choice == "5":
            print("👋 Dasturdan chiqildi.")
            break
        else:
            print("🚫 Noto‘g‘ri tanlov!")

# ========== Dasturni ishga tushirish ==========
menu()


# select * from players


# CREATE TABLE team (
#     id SERIAL PRIMARY KEY,
#     team_name VARCHAR(100) NOT NULL,
#     country VARCHAR(100),
#     founded_year INTEGER,
#     coach_name VARCHAR(100)
# );


# COPY team(team_name, country, founded_year, coach_name)
# FROM 'C:/Users/zafki/Desktop/futbol_pozitsiya_modeli/data/players.csv'
# DELIMITER ','
# CSV HEADER;


# -- psql terminalda (emas pgAdmin)
# \copy team FROM 'C:/Users/zafki/Desktop/futbol_pozitsiya_modeli/data/players.csv' DELIMITER ',' CSV HEADER;
