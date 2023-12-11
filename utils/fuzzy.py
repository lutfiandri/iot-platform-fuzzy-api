import numpy as np
from skfuzzy import control as ctrl
import skfuzzy as fuzz
from functools import reduce
import itertools
from flask import jsonify


from .transform_output import transform_output

def fuzzy_inference_batch(ctrl_system: ctrl.ControlSystem, input: list):
    results = []
    for block in input:
        simulation = ctrl.ControlSystemSimulation(ctrl_system)

        for key, value in block["data"].items():
            simulation.input[key] = float(value)

        simulation.compute()

        output = transform_output(simulation.output)
        result = {
            "id": block["id"],
            "output": output
        }

        results.append(result) 

    return results

def check_fuzzy_combination_count(params: dict) -> dict:
    comb_count= reduce(lambda x, y: x*y, [len(i["membership"]) for i in params["input"]])
    n_rules = len(params['rule'])
    
    result = {
        'ok': comb_count == n_rules,
        'error': 'false combination count',
        'combination': comb_count,
        'rule_count': n_rules
    }

    print(result)
    
    return result

def create_fuzzy_rules(params: dict):
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
    rules = []
    input_rules = list(itertools.product(*[i["membership"] for i in params["input"]]))

    for item in zip(input_rules, params["rule"]):

        antecedents_rule_buffer = None
        consequents_rule_buffer = None
        
        for i in range(len(antecedents)):
            antecedents_rule_buffer = antecedents[i][item[0][i]] if antecedents_rule_buffer == None else antecedents_rule_buffer & antecedents[i][item[0][i]]
        for i in range(len(consequents)):
            consequents_rule_buffer = consequents[i][item[1][i]] if consequents_rule_buffer == None else consequents_rule_buffer & consequents[i][item[1][i]]
        
        rule_buffer = ctrl.Rule(antecedents_rule_buffer, consequents_rule_buffer)
        rules.append(rule_buffer)

    return rules