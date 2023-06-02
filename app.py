from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import skfuzzy as fuzz

app = Flask(__name__)

# CORS
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG

#===============================================================================================================================================#

# INPUT

# soil_water_content from 0 to 100
soil_water_content = ctrl.Antecedent(np.arange(0, 40, 0.1), 'soil_water_content')
# sun_radiation from 0 to 12
sunshine_hour = ctrl.Antecedent(np.arange(0, 12, 0.1), 'sunshine_hour')
# delta_evaporation from 0 to 6 mm
delta_evaporation = ctrl.Antecedent(np.arange(0, 6, 0.1), 'delta_evaporation')
# plant_age from 0 to 14 days
plant_age = ctrl.Antecedent(np.arange(0, 14, 0.1), 'plant_age')

# OUTPUT

# Water amount a plant needs
bobot_penyiraman = ctrl.Consequent(np.arange(0, 120, 0.1), 'bobot_penyiraman')

#===============================================================================================================================================#

# Soil Water Content
SWC_COND_1 = 'SangatKritis'
SWC_COND_2 = 'Kritis'
SWC_COND_3 = 'KurangBaik'
SWC_COND_4 = 'Baik'
soil_water_content[SWC_COND_1] = fuzz.trapmf(soil_water_content.universe, [0, 0, 26, 28])
soil_water_content[SWC_COND_2] = fuzz.trapmf(soil_water_content.universe, [27, 28, 29, 30])
soil_water_content[SWC_COND_3] = fuzz.trapmf(soil_water_content.universe, [29, 30, 34, 35])
soil_water_content[SWC_COND_4] = fuzz.trapmf(soil_water_content.universe, [34, 35, 40, 40])

# Delta Evaporation
DE_COND_1 = 'Small'
DE_COND_2 = 'MediumD'
DE_COND_3 = 'Large'
delta_evaporation[DE_COND_1] = fuzz.trapmf(delta_evaporation.universe, [0, 0, 1, 3])
delta_evaporation[DE_COND_2] = fuzz.trapmf(delta_evaporation.universe, [1, 3, 4, 5])
delta_evaporation[DE_COND_3] = fuzz.trapmf(delta_evaporation.universe, [3, 5, 6, 6])

# Sunshine Hour
SH_COND_1 = 'Short'
SH_COND_2 = 'Medium'
SH_COND_3 = 'Long'
sunshine_hour[SH_COND_1] = fuzz.trapmf(sunshine_hour.universe, [0, 0, 2, 6])
sunshine_hour[SH_COND_2] = fuzz.trapmf(sunshine_hour.universe, [2, 6, 7, 10])
sunshine_hour[SH_COND_3] = fuzz.trapmf(sunshine_hour.universe, [6, 10, 12, 12])

# Plant Age
PA_COND_1 = 'Germination'
PA_COND_2 = 'Tillering'
PA_COND_3 = 'Growth'
PA_COND_4 = 'Ripening'
plant_age[PA_COND_1] = fuzz.trapmf(plant_age.universe, [0, 0, 3, 6])
plant_age[PA_COND_2] = fuzz.trapmf(plant_age.universe, [3, 6, 8, 9])
plant_age[PA_COND_3] = fuzz.trapmf(plant_age.universe, [6, 9, 10, 12])
plant_age[PA_COND_4] = fuzz.trapmf(plant_age.universe, [9, 12, 15, 15])


# output ==== membership value

# Bobot Penyiraman
BA_COND_1 = 'Singkat'
BA_COND_2 = 'Lama'
BA_COND_3 = 'SangatLama'
bobot_penyiraman[BA_COND_1] = fuzz.trapmf(bobot_penyiraman.universe, [0, 0, 15, 30])
bobot_penyiraman[BA_COND_2] = fuzz.trapmf(bobot_penyiraman.universe, [15, 30, 60, 75])
bobot_penyiraman[BA_COND_3] = fuzz.trapmf(bobot_penyiraman.universe, [60, 75, 90, 100])

#===============================================================================================================================================#

# We define set of rules
rule1   = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule2   = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule3   = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule4   = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_1])
rule5   = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule6   = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule7   = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule8   = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule9   = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule10  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule11  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule12  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule13  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule14  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule15  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule16  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_1])
rule17  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule18  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule19  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule20  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule21  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule22  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule23  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule24  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule25  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule26  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule27  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule28  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule29  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule30  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule31  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule32  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule33  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule34  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule35  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_3])
rule36  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_1] | plant_age[PA_COND_4]), bobot_penyiraman[BA_COND_2])
rule37  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule38  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule39  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule40  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule41  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule42  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule43  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule44  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule45  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule46  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule47  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule48  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule49  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule50  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule51  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule52  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule53  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule54  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule55  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule56  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule57  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule58  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule59  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule60  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule61  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule62  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule63  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule64  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule65  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule66  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule67  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule68  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_1])
rule69  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_3])
rule70  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule71  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule72  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_2]), bobot_penyiraman[BA_COND_2])
rule73  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule74  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule75  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule76  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule77  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule78  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule79  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule80  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule81  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule82  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule83  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule84  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_1] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule85  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule86  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule87  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule88  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule89  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule90  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule91  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule92  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule93  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule94  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule95  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule96  = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_2] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule97  = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule98  = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule99  = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule100 = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_1] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule101 = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule102 = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule103 = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule104 = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_2] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])
rule105 = ctrl.Rule(soil_water_content[SWC_COND_1] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule106 = ctrl.Rule(soil_water_content[SWC_COND_2] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule107 = ctrl.Rule(soil_water_content[SWC_COND_3] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_2])
rule108 = ctrl.Rule(soil_water_content[SWC_COND_4] & sunshine_hour[SH_COND_3] & delta_evaporation[DE_COND_3] & (plant_age[PA_COND_3]), bobot_penyiraman[BA_COND_1])


#===============================================================================================================================================#

# Set rules needed to operate the fuzzy logic
water_ctrl1 = ctrl.ControlSystem(
    [
        rule1  , rule2  , rule3  , rule4  , rule5  , rule6  , rule7  , rule8  , rule9  , 
        rule10 , rule11 , rule12 , rule13 , rule14 , rule15 , rule16 , rule17 , rule18 , 
        rule19 , rule20 , rule21 , rule22 , rule23 , rule24 , rule25 , rule26 , rule27 , 
        rule28 , rule29 , rule30 , rule31 , rule32 , rule33 , rule34 , rule35 , rule36 , 
        rule37 , rule38 , rule39 , rule40 , rule41 , rule42 , rule43 , rule44 , rule45 , 
        rule46 , rule47 , rule48 , rule49 , rule50 , rule51 , rule52 , rule53 , rule54 , 
        rule55 , rule56 , rule57 , rule58 , rule59 , rule60 , rule61 , rule62 , rule63 , 
        rule64 , rule65 , rule66 , rule67 , rule68 , rule69 , rule70 , rule71 , rule72 , 
        rule73 , rule74 , rule75 , rule76 , rule77 , rule78 , rule79 , rule80 , rule81 , 
        rule82 , rule83 , rule84 , rule85 , rule86 , rule87 , rule88 , rule89 , rule90 , 
        rule91 , rule92 , rule93 , rule94 , rule95 , rule96 , rule97 , rule98 , rule99 , 
        rule100, rule101, rule102, rule103, rule104, rule105, rule106, rule107, rule108
    ]
)

# Add the simulation to control system
water = ctrl.ControlSystemSimulation(water_ctrl1)


@app.route('/processjson', methods=['POST'])
def processjson():
    #===============================================================================================================================================#

    #req_data = request.get_json()
    soil_water_content = int(request.json['soil_water_content'])
    sunshine_hour = int(request.json['sunshine'])
    delta_evaporation = int(request.json['evaporation'])
    plant_age = int(request.json['plant_age'])

    water.input['soil_water_content'] = soil_water_content
    water.input['sunshine_hour'] = sunshine_hour
    water.input['delta_evaporation'] = delta_evaporation
    water.input['plant_age'] = plant_age

    water.compute()

    return jsonify(water.output['bobot_penyiraman']), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
