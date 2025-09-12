# Predecir la lluvia
# El sistema analiza temperatura y humedad, aplicando las reglas aprendidas,
#y emite una conclusión automática.
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# ===== 1. BASE DE CONOCIMIENTO (datos históricos) =====
# Datos: [Temperatura(°C), Humedad(%)]
X = np.array([
    [30, 40], [22, 85], [25, 65], [20, 90],
    [28, 50], [18, 95], [27, 60], [21, 80]
])
# 1 = Lloverá, 0 = No lloverá
y = np.array([0, 1, 0, 1, 0, 1, 0, 1])

# ===== 2. MOTOR DE INFERENCIA =====
modelo = DecisionTreeClassifier()
modelo.fit(X, y)

# ===== 3. INTERFAZ DE USUARIO =====
print("=== Sistema Experto: ¿Necesitas paraguas? ===")
temp = float(input("Temperatura actual (°C): "))
hum = float(input("Humedad actual (%): "))

prediccion = modelo.predict([[temp, hum]])[0]

if prediccion == 1:
    print("Recomendación: Lleva paraguas, hay alta probabilidad de lluvia.")
else:
    print("Recomendación: No parece que vaya a llover, paraguas opcional.")
