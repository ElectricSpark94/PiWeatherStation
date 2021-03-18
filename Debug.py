import json

with open ('settings.json') as f:
    asd = json.loads(f)

print (asd)