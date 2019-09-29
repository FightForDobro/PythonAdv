country_dict = {
    'Ukraine': 'Kiev',
    'Russia': 'Moscow',
    'Belarus': 'Minsk'
}

country_list = ['Ukraine', 'Russia', 'Belarus', 'Latvia']

for i in country_list:

    if i in country_dict.keys():
        print(country_dict[i])