

data = {'one':0}
if 'two' not in data:
    print('no soup')
else:
    print(data['two'])

data['two'] = 'soup'
if 'two' in data:
    print(data['two'])
else:
    print('no soup')