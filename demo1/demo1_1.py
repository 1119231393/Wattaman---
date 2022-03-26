import json

data = json.load(open('./boxes.json'))
for box in data['boxes']:
    if box.get('name') == "box_b":
        print(box.get('rectangle'))
