import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import tensorflow_decision_forests as tfdf
import tensorflow as tf

# Check TensorFlow and TensorFlow Decision Forests versions
print("TensorFlow version:", tf.__version__)
print("TensorFlow Decision Forests version:", tfdf.__version__)

# Ensure compatibility:
# Recommended TensorFlow version: 2.12.0
# Recommended TensorFlow Decision Forests version: 0.5.0
# If versions are incompatible, install the recommended versions:
# !pip install tensorflow==2.12.0 tensorflow_decision_forests==0.5.0

# Wczytaj dane z folderów
def load_data_from_directory(directory):
    data = []
    labels = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            data.append(df.values)
            labels.append(directory)  # Zakładamy, że nazwa folderu to etykieta
    return data, labels

lewo_data, lewo_labels = load_data_from_directory('lewo')
przod_data, przod_labels = load_data_from_directory('przod')
avada_data, avada_labels = load_data_from_directory('avada')
lumos_data, lumos_labels = load_data_from_directory('lumos')
alohomora_data, alohomora_labels = load_data_from_directory('alohomora')
wingardium_data, wingardium_labels = load_data_from_directory('wingardium')

# Połącz dane i etykiety
X = lewo_data + przod_data + avada_data + lumos_data + alohomora_data + wingardium_data
y = lewo_labels + przod_labels + avada_labels + lumos_labels + alohomora_labels + wingardium_labels

# Spłaszcz dane
X = [item.flatten() for item in X]
X = np.array(X)

# Kodowanie etykiet
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Normalizacja danych
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Podziel dane na zestawy treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Tworzenie modelu
# Replace RandomForestClassifier with TensorFlow Decision Forests' RandomForestModel
model = tfdf.keras.RandomForestModel(num_trees=15)

# Trenowanie modelu
model.fit(X_train, y_train)

# Zapisz model w formacie TensorFlow
model.save("model_tf")

# Konwersja modelu TensorFlow do TFLite
converter = tf.lite.TFLiteConverter.from_saved_model("model_tf")
tflite_model = converter.convert()
with open("model.tflite", "wb") as f:
    f.write(tflite_model)

# Load and preprocess unknown data
unknown_data, _ = load_data_from_directory('unknown')
X_unknown = [item.flatten() for item in unknown_data]
X_unknown = np.array(X_unknown)
X_unknown = scaler.transform(X_unknown)

# Predict classes for unknown data
predicted_classes = model.predict(X_unknown)

# Print prediction results
for filename, label in zip(os.listdir('unknown'), predicted_classes):
    if filename.endswith(".csv"):
        label_name = label_encoder.inverse_transform([label])[0]
        print(f"{filename}: {label_name}")
