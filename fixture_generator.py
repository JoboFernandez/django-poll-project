import json
import lorem


filename = input("Enter filename: ")
model = input("Enter model: ")
fields = []
while True:
    _field = input("Enter field name and data type: ")
    try:
        field, dtype = _field.strip().split()
        fields.append((field, dtype.lower()))
    except Exception as e:
        pass

