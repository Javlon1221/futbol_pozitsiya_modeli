import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# 1. Ma'lumotlarni yuklash
df = pd.read_csv("data/players.csv")

# 2. Foydalaniladigan ustunlar
features = ['Age', 'Matches', 'Goals', 'Assists', 'Yellow Cards', 'Red Cards']
X = df[features]
y = df['Position']

# 3. LabelEncoder bilan pozitsiyalarni sonli qiymatlarga o'girish
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 4. Modelni train/testga ajratish
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 5. Modelni o'qitish
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Model va encoder'ni saqlash
os.makedirs("models", exist_ok=True)  # <== papkani to‘g‘ri nomda yaratish
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/encoder.pkl", "wb") as f:  # <== nomni o‘zgartirdik
    pickle.dump(label_encoder, f)

print("✅ Model va encoder saqlandi!")