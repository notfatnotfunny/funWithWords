import stressFinder as sf
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

data = np.loadtxt("95000_parole_italiane_con_nomi_propri.txt", dtype=str, encoding='UTF-8')
data = data[:50]
X = []
y = []

for i in data:
    stress = sf.fetchURL(i)
    if stress:
        X.append(i)
        y.append(stress)



X_train,X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)
# select the model
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', LogisticRegression())
    ])
pipeline.fit(X_train,y_train)
y_pred = pipeline.predict(X_test)
score = accuracy_score(y_pred,y_test)
print(y_pred)