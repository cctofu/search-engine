import json

# Load the data JSON file
with open('cite.json', 'r') as f:
    data = json.load(f)
print("loaded patent data")

with open('citations2.json', 'r') as f:
    testcase = json.load(f)
print("loaded citation data")

for key,value in data.items():
    value["citation"] = [item["citation"] for item in testcase[key]]

with open("testcase.json","w") as file:
    json.dump(data,file,indent=4)