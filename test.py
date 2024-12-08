import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Function to load data from CSV files in a directory
def load_data_from_directory(directory):
    data = []
    labels = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            data.append(df.values)
            labels.append(directory.split('/')[-1])  # Assuming directory name is the label
    return data, labels

# Load data from 'lewo' and 'przod' directories
lewo_data, lewo_labels = load_data_from_directory('lewo')
przod_data, przod_labels = load_data_from_directory('przod')

# Combine data and labels
X = lewo_data + przod_data
y = lewo_labels + przod_labels

# Flatten the data
X = [item.flatten() for item in X]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {accuracy * 100:.2f}%")


unknown_X, unknown_Y = load_data_from_directory('unknown')
unknown_X = [item.flatten() for item in unknown_X]

print(model.predict(unknown_X))
