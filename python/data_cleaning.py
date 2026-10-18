from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
OUT = ROOT / "data" / "processed" / "telco_churn_clean.csv"


def clean(df):
    df = df.copy()
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    return df


def validate(df):
    assert len(df) == 7043, "Row count changed"
    assert df["customerID"].is_unique, "customerID is not unique"
    assert pd.api.types.is_numeric_dtype(df["TotalCharges"]), "TotalCharges is not numeric"
    assert df["TotalCharges"].isnull().sum() == 11, "Unexpected number of NaN in TotalCharges"
    assert (df["TotalCharges"].isnull() == (df["tenure"] == 0)).all(), "NaN TotalCharges do not match tenure = 0"
    assert set(df["Churn"].unique()) == {"Yes", "No"}, "Churn has unexpected values"


if __name__ == "__main__":
    raw = pd.read_csv(RAW)
    cleaned = clean(raw)
    validate(cleaned)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUT, index=False)
    print("Cleaned file saved:", cleaned.shape)    