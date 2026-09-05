# Optional extension: train a resume category classifier.
# Expected CSV columns: text, category
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

DATA_PATH = "data/resumes.csv"
MODEL_PATH = "models/resume_classifier.pkl"

df = pd.read_csv(DATA_PATH).dropna(subset=["text","category"])
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["category"], test_size=0.2, random_state=42, stratify=df["category"]
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=10000)),
    ("clf", LogisticRegression(max_iter=2000))
])

model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test)))
joblib.dump(model, MODEL_PATH)
print("Saved:", MODEL_PATH)
