def transform_output(output: dict) -> list:
    result = [{
        'param_name': key,
        'value': output[key]
    } for key in output.keys()]
    return result