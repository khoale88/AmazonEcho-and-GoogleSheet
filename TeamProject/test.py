import json

r = open('input.json','r')
s = json.loads(r.read())
output = []

for sublist in s:
    item = {}
    item['name'] = str(sublist[0])
    item['price'] = str(sublist[1])
    output.append(item)
    
print output