from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from skfuzzy import control as ctrl
from weather_data_processor import *
from collections import namedtuple
from functools import reduce

from utils import *

app = Flask(__name__)

# CORS
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG

# CTRL SYSTEM CACHING
# map[str]ctrl.ControlSystem
# map[config_id]ctrl_system_with_the_config
ctrl_system_cache = {}

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
    
    # CHECK COMBINATION RULES
    combination_check_result = check_fuzzy_combination_count(params)
    if not combination_check_result['ok']:
        del combination_check_result['ok']
        return jsonify(combination_check_result), 400

    # CREATE FUZZY CONTROL SYSTEM SIMULATION ===================
    rules = create_fuzzy_rules(params)
    ctrl_system = ctrl.ControlSystem(rules)
    ctrl_system_cache[params['id']] = ctrl_system

    # FUZZY INFERENCE ==========================================
    results = fuzzy_inference_batch(ctrl_system, input)

    return jsonify({
        "results": results
    })


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
