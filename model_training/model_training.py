#
# Model Training and Dumping for use on another app
#

import numpy  as np 
import pandas as pd
from  sklearn.neighbors import KNeighborsClassifier

path  = 'appdata.csv'
train = pd.read_csv(path, sep=',')

# remove the time and category
del train['time']
del train['category']


# place the label on a different list
label = train['label'].values

# remove the label from the training set
del train['label']


# Train the KNN Classifier
neigh = KNeighborsClassifier(n_neighbors=4)
neigh.fit(train, label) 


# Dumping a KNN model into a pickle file
from sklearn.externals import joblib
filename = 'simulator.pkl'
joblib.dump(neigh, filename) 

