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