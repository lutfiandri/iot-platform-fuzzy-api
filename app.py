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

# # transform input
# def transform_input(input: dict) -> dict:
    


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
        'input': input,
        'output': output,
        'rule': config['rule']
    }

    return result


@app.route('/fuzzy', methods=['POST'])
def inference():
    input = request.json["input"]
    config = request.json["config"]

    params = transform_config(config)

    print(params['input'], len(params['rule']))

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
    simulation_ctrl = ctrl.ControlSystem(rule_list)


    # FUZZY INFERENCE FOR EACH BLOCK ===========================
    results = []
    for block in input:
        simulation = ctrl.ControlSystemSimulation(simulation_ctrl)

        print(block)

        for key, value in block["data"].items():
            simulation.input[key] = float(value)

        simulation.compute()
        result = {
            "id": block["id"],
            "output": simulation.output
        }
        results.append(result)

    return jsonify({
        "results": results
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
