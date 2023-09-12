# Python program to read
# json file

import json

# JSON string
j_string = '{"name": "Bob", "languages": "English"}'

# deserializes into dict and returns dict.
y = json.loads(j_string)

print("JSON string = ", y)
print()

# JSON file
f = open ('config.json', "w")

# Reading from file
data = json.loads(f.read())

# Iterating through the json list
for i in data['emp_details']:
	print(i)

# Closing file
f.close()
