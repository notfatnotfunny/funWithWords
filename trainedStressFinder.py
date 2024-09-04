# import stressFinder as sf
# import numpy as np
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.pipeline import Pipeline
# from sklearn.model_selection import train_test_split
 
# #load the dataset and split it into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30, random_state = 101) 
# model = Pipeline([
#     ('vectorizer', TfidfVectorizer()),
#     ('classifier', LogisticRegression())
# ])
# model.fit(X_train,y_train)
# data = ['curioso', 'attico', 'città']
# print(data, model.predict(data))


import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

dataX,datay = np.loadtxt('dataset.txt', delimiter=',', dtype = str, encoding='UTF-8', unpack = 1)
X = []
y = []
# Convert words to character-level features
def word_to_features(word):
    return [ord(c) for c in word]

def word_to_labels(word_no_accent, word_with_accent):
    labels = []
    for i in range(len(word_no_accent)):
        if len(word_no_accent) == len(word_with_accent):
            if word_no_accent[i] == word_with_accent[i]:
                labels.append(0)  # No accent
            else:
                labels.append(ord(word_with_accent[i]))  # ASCII value of the accented character
        # else: 
        #     print(word_no_accent, word_with_accent)
    return labels

for i in range(len(dataX)):
    X.append(word_to_features(dataX[i]))
    y.append(word_to_labels(dataX[i],datay[i]))

# Padding the sequences to have the same length
max_len = max(len(x) for x in X)
X = np.array([x + [0] * (max_len - len(x)) for x in X])  # Padding with 0
y = np.array([l + [0] * (max_len - len(l)) for l in y])  # Padding with 0

# # Flatten the problem: predict the accent per character position
# X_flat = X.reshape(-1, max_len)
# y_flat = y.flatten()


# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Example prediction function
def predict_accent(word):
    features = word_to_features(word)
    features = np.array(features + [0] * (max_len - len(features))).reshape(1, -1)
    predictions = model.predict(features).reshape(-1)
    
    accented_word = list(word)
    for i, p in enumerate(predictions):
        if p != 0:  # If the prediction is not 0, replace the character
            accented_word[i] = chr(p)
    return ''.join(accented_word)

# Test the model
test_word = 'ricoprimento'
predicted_word = predict_accent(test_word)
print(f'{test_word} -> {predicted_word}')

## mistakes
# approfittare
# eticità 
# chiacchiericcio
# buffonesco
# appallottolare
# additare

