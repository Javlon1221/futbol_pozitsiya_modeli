import pandas as pd
import psycopg2

df = pd.read_csv("C:/Users/zafki/Desktop/futbol_pozitsiya_modeli/data/team_players_200.csv")

conn = psycopg2.connect(
    dbname="futbol_db",
    user="postgres",
    password="0000",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Har bir qatorni `teams` jadvaliga qo‘shish
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO teams (name, age, matches, goals, assists, yellow_cards, red_cards, predicted_position)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['name'], row['age'], row['matches'], row['goals'],
        row['assists'], row['yellow_cards'], row['red_cards'], row['predicted_position']
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ 200 ta jamoa o'yinchilari ma'lumotlari 'teams' jadvaliga muvaffaqiyatli yuklandi.")
