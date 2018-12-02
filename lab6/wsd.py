import json

data = None
with open('bank-senses.json', 'r') as f:
    data = json.load(f)
    f.close()

context = "After withdrawing all the money, he went to the bank to watch the river " \
          "for the last time."
for key, val in data.items():
    print(key)
    slope = val['slope']
    str.translate()
    examples = ' '.join(val['examples'])
    print(slope)
    print(examples)

    glosses = ""



