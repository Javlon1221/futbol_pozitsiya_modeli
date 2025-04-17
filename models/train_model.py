# models/train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 1) Ma'lumotni yuklash
df = pd.read_csv("C:/Users/zafki/Desktop/futbol_pozitsiya_modeli/data/players.csv")

# 2) X va y ni ajratish
X = df.drop("position", axis=1)
y = df["position"]

# 3) Bo'lib bo'lish\ nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4) Model yaratish va o'qitish
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 5) Baholash
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

# 6) Modelni saqlash
joblib.dump(model, "model.pkl")