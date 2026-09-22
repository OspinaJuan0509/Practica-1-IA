import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definición variables de entrada
cantidad_residuo = ctrl.Antecedent(np.arange(0, 101), 'cantidad_residuo')
nivel_contaminacion = ctrl.Antecedent(np.arange(0, 101), 'nivel_contaminacion')
porcentaje_acumulacion = ctrl.Antecedent(np.arange(0, 101), 'porcentaje_acumulacion')

# Definición variable de salida. Método de defuzzificación usado: centroide (por defecto)
nivel_prioridad = ctrl.Consequent(np.arange(0, 101), 'nivel_prioridad')

# Funciones de pertenencia (trapezoidal, triangular y gaussiana)
cantidad_residuo['baja'] = fuzz.trapmf(cantidad_residuo.universe, [0, 0, 15, 40])
cantidad_residuo['media'] = fuzz.trimf(cantidad_residuo.universe, [30, 50, 70])
cantidad_residuo['alta'] = fuzz.gaussmf(cantidad_residuo.universe, 100, 12.5)

nivel_contaminacion['bajo'] = fuzz.trapmf(cantidad_residuo.universe, [0, 0, 15, 40])
nivel_contaminacion['medio'] = fuzz.trimf(cantidad_residuo.universe, [30, 50, 70])
nivel_contaminacion['alto'] = fuzz.gaussmf(cantidad_residuo.universe, 100, 12.5)

porcentaje_acumulacion['bajo'] = fuzz.trapmf(cantidad_residuo.universe, [0, 0, 15, 40])
porcentaje_acumulacion['medio'] = fuzz.trimf(cantidad_residuo.universe, [30, 50, 70])
porcentaje_acumulacion['alto'] = fuzz.gaussmf(cantidad_residuo.universe, 100, 12.5)

nivel_prioridad['bajo'] = fuzz.trapmf(cantidad_residuo.universe, [0, 0, 15, 40])
nivel_prioridad['medio'] = fuzz.trimf(cantidad_residuo.universe, [30, 50, 70])
nivel_prioridad['alto'] = fuzz.gaussmf(cantidad_residuo.universe, 100, 12.5)

# Definición de reglas 
rule1 = ctrl.Rule(cantidad_residuo['alta'] & nivel_contaminacion['alto'], nivel_prioridad['alto'])
rule2 = ctrl.Rule(cantidad_residuo['media'] & nivel_contaminacion['medio'], nivel_prioridad['medio'])
rule3 = ctrl.Rule(cantidad_residuo['baja'] & nivel_contaminacion['bajo'], nivel_prioridad['bajo'])

rule4 = ctrl.Rule(nivel_contaminacion['alto'] | porcentaje_acumulacion['alto'], nivel_prioridad['alto'])
rule5 = ctrl.Rule(cantidad_residuo['alta'] | porcentaje_acumulacion['alto'], nivel_prioridad['alto'])
rule6 = ctrl.Rule(cantidad_residuo['media'] & porcentaje_acumulacion['medio'], nivel_prioridad['medio'])

rule7 = ctrl.Rule(cantidad_residuo['baja'] & porcentaje_acumulacion['bajo'], nivel_prioridad['bajo'])
rule8 = ctrl.Rule(nivel_contaminacion['alto'] & porcentaje_acumulacion['alto'], nivel_prioridad['alto'])
rule9 = ctrl.Rule(nivel_contaminacion['medio'] | porcentaje_acumulacion['medio'], nivel_prioridad['medio'])

rule10 = ctrl.Rule(~ nivel_contaminacion['alto'] & cantidad_residuo['baja'], nivel_prioridad['bajo'])
rule11 = ctrl.Rule(cantidad_residuo['alta'] & nivel_contaminacion['medio'], nivel_prioridad['alto'])
rule12 = ctrl.Rule(~ cantidad_residuo['alta'] & nivel_contaminacion['bajo'], nivel_prioridad['bajo'])

# 
sistema_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, 
                                    rule7, rule8, rule9, rule10, rule11, rule12])
calculador_prioridad = ctrl.ControlSystemSimulation(sistema_control)

calculador_prioridad.input['cantidad_residuo'] = 30
calculador_prioridad.input['nivel_contaminacion'] = 80
calculador_prioridad.input['porcentaje_acumulacion'] = 35

calculador_prioridad.compute()
print(f"Nivel de prioridad calculado: {calculador_prioridad.output['nivel_prioridad']:.2f}")

nivel_prioridad.view(sim = calculador_prioridad)
plt.show()