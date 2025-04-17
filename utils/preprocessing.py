# utils/preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Misol uchun, NaN qiymatlarni o'chirish yoki to'ldirish
    df.dropna(inplace=True)
    return df


def scale_features(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    scaler = StandardScaler()
    df[cols] = scaler.fit_transform(df[cols])
    return df


def preprocess_data(df):
    # Nom, mamlakat, klub va pozitsiya modelda ishlatilmaydi
    df = df.drop(columns=['Name', 'Country', 'Club', 'Position'], errors='ignore')

    # Bo‘sh qiymatlarni 0 bilan to‘ldiramiz
    df = df.fillna(0)

    return df
