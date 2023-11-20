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

# ctrl caching
# map[str]ctrl.ControlSystem
# map[config_id]ctrl_system_with_the_config
ctrl_system_cache = {}

# transform input
def transform_input_item(item: dict) -> dict:
    data = {}
    for d in item['data']:
        data[d['param_name']] = d['value']

    result = {
        'id': item['id'],
        'data': data
    }

    return result

def transform_input(input: list) -> list:
    result = [transform_input_item(x) for x in input]
    return result

# transform config
def transform_config_item(item: dict) -> dict:
    universe = [
        item['universe']['min'],
        item['universe']['max'],
        item['universe']['precision'],
    ]

    membership = {}
    for m in item['membership']:
        membership[m['name']] = m['value']

    result = {
        'param_name': item['param_name'],
        'universe': universe,
        'membership': membership,
    }

    return result

def transform_config(config: dict) -> dict:
    input = [transform_config_item(x) for x in config['input']]
    output = [transform_config_item(x) for x in config['output']]

    result = {
        'id': config['id'],
        'input': input,
        'output': output,
        'rule': config['rule']
    }

    return result

# Do fuzzy inference for each block
def fuzzy_inference_batch(ctrl_system: ctrl.ControlSystem, input: list):
    results = []
    for block in input:
        simulation = ctrl.ControlSystemSimulation(ctrl_system)

        for key, value in block["data"].items():
            simulation.input[key] = float(value)

        simulation.compute()
        result = {
            "id": block["id"],
            "output": simulation.output
        }
        results.append(result) 

    return results

@app.route('/fuzzy', methods=['POST'])
def inference():
    input = request.json["input"]
    config = request.json["config"]

    input = transform_input(input)
    params = transform_config(config)

    # LOOK FOR CTRL SYSTEM CACHE
    if params['id'] in ctrl_system_cache:
        ctrl_system = ctrl_system_cache[params['id']]
        results = fuzzy_inference_batch(ctrl_system, input)
        return jsonify({
            "results": results
        })

    # CREATE FUZZY RULE FROM CONFIG ======================

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

    # CREATE FUZZY CONTROL SYSTEM SIMULATION ===================
    ctrl_system = ctrl.ControlSystem(rule_list)
    ctrl_system_cache[params['id']] = ctrl_system

    # FUZZY INFERENCE FOR EACH BLOCK ===========================
    results = fuzzy_inference_batch(ctrl_system, input)

    return jsonify({
        "results": results
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
