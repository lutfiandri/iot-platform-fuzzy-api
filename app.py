from flask import Flask, request, jsonify


import skfuzzy as fuzz
from skfuzzy import control as ctrl


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import skfuzzy as fuzz


app = Flask(__name__)

#===============================================================================================================================================#

# INPUT
# soil_water_content from 0 to 100
soil_water_content = ctrl.Antecedent(np.arange(0, 40, 1), 'soil_water_content')

# sun_radiation from 0 to 12
sunshine_hour = ctrl.Antecedent(np.arange(0, 12, 1), 'sunshine_hour')

# delta_evaporation from 0 to 6 mm
delta_evaporation = ctrl.Antecedent(
    np.arange(0, 6, 1), 'delta_evaporation')

# plant_age from 0 to 14 days
plant_age = ctrl.Antecedent(np.arange(0, 14, 1), 'plant_age')

# OUTPUT
# Water amount a plant needs
bobot_penyiraman = ctrl.Consequent(np.arange(0, 120, 1), 'bobot_penyiraman')

#===============================================================================================================================================#

# soil_water_content
soil_water_content['SangatKritis'] = fuzz.trapmf(
    soil_water_content.universe, [0, 0, 26, 28])
soil_water_content['Kritis'] = fuzz.trapmf(
    soil_water_content.universe, [27, 28, 29, 30])
soil_water_content['KurangBaik'] = fuzz.trapmf(
    soil_water_content.universe, [29, 30, 34, 35])
soil_water_content['Baik'] = fuzz.trapmf(
    soil_water_content.universe, [34, 35, 40, 40])

delta_evaporation['Small'] = fuzz.trapmf(
    delta_evaporation.universe, [0, 0, 1, 3])
delta_evaporation['MediumD'] = fuzz.trapmf(
    delta_evaporation.universe, [1, 3, 4, 5])
delta_evaporation['Large'] = fuzz.trapmf(
    delta_evaporation.universe, [3, 5, 6, 6])

# sunshine_hour
sunshine_hour['Short'] = fuzz.trapmf(sunshine_hour.universe, [0, 0, 2, 6])
sunshine_hour['Medium'] = fuzz.trapmf(sunshine_hour.universe, [2, 6, 7, 10])
sunshine_hour['Long'] = fuzz.trapmf(sunshine_hour.universe, [6, 10, 12, 12])


plant_age['Germination'] = fuzz.trapmf(plant_age.universe, [0, 0, 3, 6])
plant_age['Tillering'] = fuzz.trapmf(plant_age.universe, [3, 6, 8, 9])
plant_age['Growth'] = fuzz.trapmf(plant_age.universe, [6, 9, 10, 12])
plant_age['Ripening'] = fuzz.trapmf(
    plant_age.universe, [9, 12, 15, 15])


# output ==== membership value
bobot_penyiraman['Singkat'] = fuzz.trapmf(
    bobot_penyiraman.universe, [0, 0, 15, 30])
bobot_penyiraman['Lama'] = fuzz.trapmf(
    bobot_penyiraman.universe, [15, 30, 60, 75])
bobot_penyiraman['SangatLama'] = fuzz.trapmf(
    bobot_penyiraman.universe, [60, 75, 90, 100])

#===============================================================================================================================================#

# We define set of rules

rule1 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule2 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule3 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule4 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Singkat'])
rule5 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule6 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule7 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule8 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule9 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule10 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule11 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule12 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule13 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule14 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule15 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule16 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Singkat'])
rule17 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule18 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule19 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule20 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule21 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule22 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule23 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule24 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule25 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule26 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule27 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule28 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule29 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule30 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule31 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule32 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule33 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule34 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule35 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['SangatLama'])
rule36 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Germination'] | plant_age['Ripening']), bobot_penyiraman['Lama'])
rule37 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule38 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule39 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule40 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule41 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] &
                   delta_evaporation['Small'] & (plant_age['Tillering']), bobot_penyiraman['Lama'])
rule42 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule43 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule44 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule45 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule46 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule47 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule48 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule49 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule50 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule51 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule52 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule53 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] &
                   delta_evaporation['MediumD'] & (plant_age['Tillering']), bobot_penyiraman['Lama'])
rule54 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule55 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule56 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule57 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule58 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule59 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule60 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule61 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule62 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule63 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule64 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule65 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] &
                   delta_evaporation['Large'] & (plant_age['Tillering']), bobot_penyiraman['Lama'])
rule66 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule67 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule68 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Singkat'])
rule69 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['SangatLama'])
rule70 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule71 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule72 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Tillering']), bobot_penyiraman['Lama'])
rule73 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule74 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule75 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule76 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule77 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] &
                   delta_evaporation['Small'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule78 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule79 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule80 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule81 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] &
                   delta_evaporation['Small'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule82 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Lama'])
rule83 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule84 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['Small'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule85 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule86 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule87 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule88 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule89 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium'] &
                   delta_evaporation['MediumD'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule90 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule91 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule92 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule93 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] &
                   delta_evaporation['MediumD'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule94 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule95 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule96 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['MediumD'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule97 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Short'] &
                   delta_evaporation['Large'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule98 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Lama'])
rule99 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule100 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Short'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule101 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Medium']
                    & delta_evaporation['Large'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule102 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Lama'])
rule103 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule104 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Medium'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])
rule105 = ctrl.Rule(soil_water_content['SangatKritis'] & sunshine_hour['Long'] &
                    delta_evaporation['Large'] & (plant_age['Growth']), bobot_penyiraman['Lama'])
rule106 = ctrl.Rule(soil_water_content['Kritis'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Lama'])
rule107 = ctrl.Rule(soil_water_content['KurangBaik'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Lama'])
rule108 = ctrl.Rule(soil_water_content['Baik'] & sunshine_hour['Long'] & delta_evaporation['Large'] & (
    plant_age['Growth']), bobot_penyiraman['Singkat'])


#===============================================================================================================================================#

# Set rules needed to operate the fuzzy logic
water_ctrl1 = ctrl.ControlSystem(
    [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
        rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18,
        rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27,
        rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36,
        rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45,
        rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54,
        rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63,
        rule64, rule65, rule66, rule67, rule68, rule69, rule70, rule71, rule72,
        rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80, rule81,
        rule82, rule83, rule84, rule85, rule86, rule87, rule88, rule89, rule90,
        rule91, rule92, rule93, rule94, rule95, rule96, rule97, rule98, rule99,
        rule100, rule101, rule102, rule103, rule104, rule105, rule106, rule107,
        rule108

     ])

# Add the simulation to control system
water = ctrl.ControlSystemSimulation(water_ctrl1)


@app.route('/processjson', methods=['POST'])
def processjson():
    #===============================================================================================================================================#

    #req_data = request.get_json()
    soil_water_content_in = request.json['soil_water_content']
    sunshine_hour_in = request.json['sunshine']
    delta_evaporation_in = request.json['evaporation']
    plant_age_in = request.json['plant_age']

    soil_water_content = int(soil_water_content_in)
    sunshine_hour = int(sunshine_hour_in)
    delta_evaporation = int(delta_evaporation_in)
    plant_age = int(plant_age_in)

    # return '{}'.format(soil_water_content+sunshine_hour)

    water.input['soil_water_content'] = soil_water_content
    water.input['sunshine_hour'] = sunshine_hour
    water.input['delta_evaporation'] = delta_evaporation
    water.input['plant_age'] = plant_age

    water.compute()

    return jsonify(water.output)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
