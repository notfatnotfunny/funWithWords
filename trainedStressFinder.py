import stressFinder as sf
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
 
#load the dataset and split it into training and testing sets
X,y = np.loadtxt('dataset.txt', delimiter=',', dtype = str, encoding='UTF-8', unpack = 1)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30, random_state = 101) 
model = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', LogisticRegression())
])
model.fit(X_train,y_train)
data = ['curioso', 'attico', 'città']
print(data, model.predict(data))