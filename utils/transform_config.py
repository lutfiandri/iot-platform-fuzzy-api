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