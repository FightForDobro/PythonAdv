import json

dict_to_json = '''{
    'data_list': ['data1', 'data2', 'data3'],
    'simple_data_int': 1,
    'simple_data_string': 'one',
    'embedded_dict': {
        'one': (1, ),
        'two': 2

    }
}'''


new_obj = '{"data1": 1}'

python_obj = json.loads(new_obj)

print(python_obj['data1'])
