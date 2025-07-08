
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ✅ 1) Load your CSV dataset
# Your CSV must have 2 columns: 'query' and 'label'
df = pd.read_csv("SQLiV3_cleaned.csv")

print(f"Loaded {len(df)} samples")
print(df.head())

#   Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df['query'], df['label'], test_size=0.2, random_state=42
)

#  Create pipeline: TF-IDF + Naive Bayes
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        lowercase=True,
        strip_accents='unicode',
        stop_words='english'
    )),
    ('clf', MultinomialNB())
])

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Accuracy:", accuracy_score(y_test, y_pred))

# Save the model
joblib.dump(pipeline, "sqli_detector.pkl")
print("\n✅ Model saved as sqli_detector.pkl")
