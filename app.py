from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import datetime
from datetime import date
import math
from weather_data_processor import *
from collections import namedtuple
from functools import reduce
import itertools
import json


app = Flask(__name__)

# CORS
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG

# #===============================================================================================================================================#
simulation = None

@app.route('/processjson', methods=['POST'])
def processjson():
    soil_water_content = float(request.json['soil_water_content'])
    sunshine_hour = float(request.json['sunshine'])
    delta_evaporation = float(request.json['evaporation'])
    plant_age = float(request.json['plant_age'])

    simulation.input['SoilWaterContent'] = soil_water_content
    simulation.input['SunshineHour'] = sunshine_hour
    simulation.input['DeltaEvaporation'] = delta_evaporation
    simulation.input['PlantAge'] = plant_age

    print(">>>>>>>>>>>>>>>>>>>>>>>>")
    print(simulation)
    print(type(simulation))
    print(simulation.input)
    print(">>>>>>>>>>>>>>>>>>>>>>>>")

    simulation.compute()

    return jsonify(simulation.output), 200

@app.route('/config-update', methods=['POST'])
def processparams(params=None):
    newParamFlag = False
    if(params == None):
        params = request.json['params']
        newParamFlag = True


    # Asert Combination Count
    comb_count= reduce(lambda x, y: x*y, [len(i["membership"]) for i in params["input"]])
    if comb_count != len(params["rule"]):
        return jsonify({
            "response": "false combination count",
            "combination": comb_count,
            "rule-count" :len(params["rule"])
        }), 400

    # Antecedents, Consequents, and Trapmf
    antecedents = []
    for i in params["input"]:
        print(i["param_name"])
        antecedents.append(ctrl.Antecedent(np.arange(*i["universe"]), i["param_name"]))
        for key, value in i["membership"].items():
            antecedents[-1][key] = fuzz.trapmf(antecedents[-1].universe, value)
                          
    consequents = []
    for o in params["output"]:
        consequents.append(ctrl.Consequent(np.arange(*o["universe"]), o["param_name"]))
        for key, value in o["membership"].items():
            consequents[-1][key] = fuzz.trapmf(consequents[-1].universe, value)
        
    # Rules
    rule_list = []
    input_rule_list = list(itertools.product(*[i["membership"] for i in params["input"]]))

    for item in zip(input_rule_list, params["rule"]):

        antecedents_rule_buffer = None
        consequents_rule_buffer = None
        
        for i in range(len(antecedents)):
            antecedents_rule_buffer = antecedents[i][item[0][i]] if antecedents_rule_buffer == None else antecedents_rule_buffer & antecedents[i][item[0][i]]
        for i in range(len(consequents)):
            consequents_rule_buffer = consequents[i][item[1][i]] if consequents_rule_buffer == None else consequents_rule_buffer & consequents[i][item[1][i]]
        
        rule_buffer = ctrl.Rule(antecedents_rule_buffer, consequents_rule_buffer)
        rule_list.append(rule_buffer)

    # Output
    simulation_ctrl = ctrl.ControlSystem(rule_list)
    global simulation
    simulation = ctrl.ControlSystemSimulation(simulation_ctrl)

    if newParamFlag:
        with open("params_config.json", "w") as file:
            if(type(params) == dict):
                json.dump(params, file)

        return jsonify({"status": "ok"}), 200
    else:
        return True

@app.route('/evapotranspiration', methods=['POST'])
def calculate_evapotranspiration():
    constant_pressure = 1.013 * (10 ** -3)

    # Required
    date_string         = request.json['date']
    year, month, day    = map(int, date_string.split('-'))
    date_input          = date(year, month, day)
    temp_min            = float(request.json['temp_min'])
    temp_max            = float(request.json['temp_max'])
    altitude            = float(request.json['altitude'])
    latitude            = float(request.json['latitude'])
    anemometer_height   = float(request.json['anemometer_height'])

    # Optional, but strongly inputted
    wind_speed      = float(request.json['wind_speed']) if request.json.get('wind_speed') is not None else None
    sunlight_hours  = float(request.json['sunlight_hours']) if request.json.get('sunlight_hours') is not None else None
    radiation       = float(request.json['radiation']) if request.json.get('radiation') is not None else None

    # Optional
    temp_dry        = float(request.json['temp_dry']) if request.json.get('temp_dry') is not None else None
    temp_wet        = float(request.json['temp_wet']) if request.json.get('temp_wet') is not None else None
    temp_dew        = float(request.json['temp_dew']) if request.json.get('temp_dew') is not None else None
    rh_min          = float(request.json['rh_min']) if request.json.get('rh_min') is not None else None
    rh_max          = float(request.json['rh_max']) if request.json.get('rh_max') is not None else None
    rh_mean         = float(request.json['rh_mean']) if request.json.get('rh_mean') is not None else None

    # Calculation
    temp_mean                                       = (temp_min + temp_max) / 2
    dew_point                                       = calculate_dew_point(date_input, temp_min, temp_dew)
    day_in_year                                     = (date_input - datetime.date(date_input.year, 1, 1)).days + 1
    atmospheric_pressure                            = round(101.3 * ( (293-0.0065 * altitude) / 293) ** 5.26, 2)
    psychrometric_constant                          = (constant_pressure * atmospheric_pressure) / (0.622 * 2.45)
    slope_saturation_vapour_pressure                = round((4098 * (0.6108 * math.exp((17.27 * temp_mean) / (temp_mean + 237.3)))) / ((temp_mean + 237.3) ** 2), 4)
    sun_declination_radians                         = 0.409  * math.sin( (2*math.pi/365) * day_in_year - 1.39)
    sherzodr                                        = round(1+0.033 * math.cos( (2*math.pi/365) * day_in_year), 4)
    latitude_radians                                = round((latitude / 180) * math.pi, 3)
    sunset_hour_angle                               = math.acos( - 1 * math.tan(latitude_radians) * math.tan(sun_declination_radians))
    extraterrestrial_solar_radiation                = ((24 * 60) / math.pi) * 0.082 * sherzodr * ((sunset_hour_angle * math.sin(latitude_radians) * math.sin(sun_declination_radians)) + (math.cos(latitude_radians) * math.cos(sun_declination_radians) * math.sin(sunset_hour_angle)))
    dailight_hours                                  = ( 24 / math.pi) * sunset_hour_angle
    saturration_vappour_pressure_at_temp_min        = calculate_saturration_vappour_pressure_at_temp(temp_min)
    saturration_vappour_pressure_at_temp_max        = calculate_saturration_vappour_pressure_at_temp(temp_max)
    saturration_vappour_pressure_at_temp_wet_bulb   = calculate_saturration_vappour_pressure_at_temp(temp_wet)
    saturration_vappour_pressure                    = (saturration_vappour_pressure_at_temp_max+saturration_vappour_pressure_at_temp_min)/2
    saturration_vappour_pressure_at_temp_dew        = calculate_saturration_vappour_pressure_at_temp(dew_point)
    actual_vappour_pressure                         = calculate_actual_vappour_pressure(temp_dry, temp_wet, temp_dew, rh_min, rh_max, rh_mean, saturration_vappour_pressure_at_temp_min, saturration_vappour_pressure_at_temp_max, saturration_vappour_pressure_at_temp_wet_bulb, saturration_vappour_pressure_at_temp_dew, atmospheric_pressure)
    vappour_pressure_deficit                        = saturration_vappour_pressure-actual_vappour_pressure
    solar_radiation_clear_sky                       = calculate_solar_radiation_clear_sky(extraterrestrial_solar_radiation)
    solar_radiation_recorded                        = calculate_solar_radiation_recorded(radiation, sunlight_hours, dailight_hours, temp_min, temp_max, extraterrestrial_solar_radiation)
    shortwave_radiation_net                         = calculate_shortwave_radiation_net(solar_radiation_recorded)
    longwave_radiation_net                          = calculate_longwave_radiation_net(temp_max, temp_min, actual_vappour_pressure, solar_radiation_recorded, solar_radiation_clear_sky)
    radiation_net                                   = shortwave_radiation_net - longwave_radiation_net
    windspeed_at_2m_alt                             = calculate_windspeed_at_2m_alt(anemometer_height, wind_speed)
    evapotranspiration_fao                          = ((0.408 * slope_saturation_vapour_pressure * (radiation_net-0))   + psychrometric_constant * (900 / (temp_mean+273) ) * max( windspeed_at_2m_alt, 0.5) * vappour_pressure_deficit) / (slope_saturation_vapour_pressure  + psychrometric_constant*(1+0.34 * max(windspeed_at_2m_alt, 0.5)))
    evapotranspiration_hargreaves                   = 0.0023 * (temp_mean+17.8) * math.sqrt(temp_max-temp_min)*extraterrestrial_solar_radiation * 0.408

    Output = namedtuple('Output', ['temp_mean', 'dew_point', 'day_in_year', 'atmospheric_pressure', 'psychrometric_constant', 'slope_saturation_vapour_pressure', 'sun_declination_radians', 'sherzodr', 'latitude_radians', 'sunset_hour_angle', 'extraterrestrial_solar_radiation', 'dailight_hours', 'saturration_vappour_pressure_at_temp_min', 'saturration_vappour_pressure_at_temp_max', 'saturration_vappour_pressure_at_temp_wet_bulb', 'saturration_vappour_pressure', 'saturration_vappour_pressure_at_temp_dew', 'actual_vappour_pressure', 'vappour_pressure_deficit', 'solar_radiation_clear_sky', 'solar_radiation_recorded', 'shortwave_radiation_net', 'longwave_radiation_net', 'radiation_net', 'windspeed_at_2m_alt', 'evapotranspiration_fao', 'evapotranspiration_hargreaves'])
    output = Output(temp_mean, dew_point, day_in_year, atmospheric_pressure, psychrometric_constant, slope_saturation_vapour_pressure, sun_declination_radians, sherzodr, latitude_radians, sunset_hour_angle, extraterrestrial_solar_radiation, dailight_hours, saturration_vappour_pressure_at_temp_min, saturration_vappour_pressure_at_temp_max, saturration_vappour_pressure_at_temp_wet_bulb, saturration_vappour_pressure, saturration_vappour_pressure_at_temp_dew, actual_vappour_pressure, vappour_pressure_deficit, solar_radiation_clear_sky, solar_radiation_recorded, shortwave_radiation_net, longwave_radiation_net, radiation_net, windspeed_at_2m_alt, evapotranspiration_fao, evapotranspiration_hargreaves)._asdict()

    return jsonify(output), 200

with open("params_config.json", "r") as file:
    params = json.load(file)
    processparams(params)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
