import requests
import pandas as pd
from newspaper import Article
from tqdm import tqdm  # progress bar for nicer output
import time

import matplotlib.pyplot as plt
import sklearn
import numpy as np

### sin wave
# x = np.arange(0, 5*np.pi, 0.1)
# y = np.sin(x)

# plt.plot(x, y)
# plt.show()


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# iris = load_iris()
# x,y = iris.data,iris.target

# xtrain,xtest,ytrain,ytest = train_test_split(x,y,test_size=0.3)
# model = DecisionTreeClassifier
# model.fit(xtrain, ytrain)

# y_pred = model.predict(xtest)

# print(accuracy_score(ytest, y_pred))


from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense

# df = pd.DataFrame([112, 3142, 63, 134, 457])

# df.to_csv("C:\\Users\\Woochoel Shin\\Pictures\\Ezras stuff temporary\\coding\\Stemforall\\testing_folder\\creationnametest.csv")

import os

# Define the path for the new directory, including parent directories

# Create the directories
# for x in range(0, 5):
#     path = f"C:\\Users\\Woochoel Shin\\Pictures\\Ezras stuff temporary\\coding\\Stemforall\\{x}"

#     try:
#         os.makedirs(path)
#         print(f"Folders '{path}' created successfully.")
#     except FileExistsError:
#         print(f"Folders '{path}' already exist.")
#     except OSError as e:
#         print(f"Error creating folders: {e}")
