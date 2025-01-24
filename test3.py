import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from micromlgen import port

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

# Wczytanie danych z różnych folderów
lewo_data, lewo_labels = load_data_from_directory('lewo')
przod_data, przod_labels = load_data_from_directory('przod')
avada_data, avada_labels = load_data_from_directory('avada2')
lumos_data, lumos_labels = load_data_from_directory('lumos')
alohomora_data, alohomora_labels = load_data_from_directory('alohomora')
wingardium_data, wingardium_labels = load_data_from_directory('wingardium')

# Połącz dane i etykiety
X = lewo_data + przod_data + avada_data + lumos_data + alohomora_data + wingardium_data
y = lewo_labels + przod_labels + avada_labels + lumos_labels + alohomora_labels + wingardium_labels

# Spłaszcz dane
X = [item.flatten() for item in X]

# Podziel dane na zestawy treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicjalizuj i wytrenuj model
model = RandomForestClassifier(n_estimators=15, random_state=42)
model.fit(X_train, y_train)

# Dokonaj predykcji i oceń model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.2f}%")

# Generowanie kodu C++ za pomocą micromlgen
# Mapowanie etykiet klas
class_map = {label: i for i, label in enumerate(set(y))}  # Mapuj unikalne etykiety na indeksy

# Wytrenuj model ponownie z mapowaniem
model.fit(X_train, y_train)

# Portowanie modelu do C++
c_code = port(model, classmap={v: k for k, v in class_map.items()})  # Odwrócone mapowanie dla generowania etykiet

# Zapisz wygenerowany kod do pliku
with open("model_with_labels.h", "w") as f:
    f.write(c_code)

print("Model został wyeksportowany do pliku 'model_with_labels.h'.")

# Wczytaj dane z folderu 'unknown' i przeprowadź dodatkowe analizy
unknown_X, unknown_Y = load_data_from_directory('unknown2')
unknown_X = [item.flatten() for item in unknown_X]

# Prawdopodobieństwa przewidywań
proba = model.predict_proba(unknown_X)
print("Prediction probabilities:")
print(proba)

# Przewidywania z poszczególnych drzew
all_tree_predictions = np.array([tree.predict(unknown_X) for tree in model.estimators_]).T
print("Predictions from individual trees:")
print(all_tree_predictions)

# Ostateczne przewidywania
final_predictions = model.predict(unknown_X)
print("Final predictions:")
print(final_predictions)