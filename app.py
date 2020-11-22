from flask import Flask, jsonify, request
import json

app = Flask(__name__)
json_file = open('data.json')
mainData = json.load(json_file)

# Categories
types = mainData['types']
pokemons = mainData['pokemons']
moves = mainData['moves']

funcList = ['max', 'min', 'sortby','order']
funcListIndependent = ['max', 'min', 'sortby']
listAttributes = ['Special Attack(s)', 'Fast Attack(s)', 'effectiveAgainst', 'weakAgainst']


def nameCheck(category): 
# There are inconsistency in the keys in the data. Pokemon names are keyed as 'Name' but type and move names are keyed as 'name'.
# Considered that data is read-only.

    if category == pokemons: 
        name = "Name"
    else:
        name = "name"
    return name

def getItems(keys, key,name,data,category): 
    # This function filters the data.
    value = keys[key]
    if key == 'Name' or key == 'name':
        key = name   

    # There are some exceptions in the arguments in the API Request. 'Type', 'Weight' and 'Height' are these exceptions.
    elif key == 'Type' or key =='type' and category == pokemons:
        # There are two Type values in Data: 'Type I' and 'Type II'.  
        firstTypes = [item for item in data if item.get('Type I') if str(item['Type I'][0]).casefold() == str(value).casefold()]
        secondTypes = [item for item in data if item.get('Type II') if str(item['Type II'][0]).casefold() == str(value).casefold()]
        for item in secondTypes: # Merging 'Type I' and 'Type II' results.  
            firstTypes.append(item)
        data = firstTypes
        return data
    # 'Weight' and 'Height' values in the Data are strings with units. Here we add units to match the request with data. 
    # So that, user will not have to add 'kg' or 'm' in the request.
    elif key == 'Weight' or key == 'weight': 
        value = str(value) + ' kg'
    elif key == 'Height' or key == 'height':
        value = str(value) + ' m'
    elif key in listAttributes: # If key is a list (like Special Attack(s) or effectiveAgainst)
        data = [item for item in data if value in item[key]]
        return data
    data = [item for item in data if str(item[key]).casefold() == str(value).casefold()] 
    return data

def sortingSettings(keys):
    isDescOrder = True # Default sorting order is descending.
    if 'max' in keys: 
        key = keys['max'] 
        isDescOrder = True
        onlyFirstItem = True # We will check this right before we return the output. This value is 'True' in 'Max' and 'Min'. 
    elif 'min' in keys:
        key = keys['min']
        isDescOrder = False
        onlyFirstItem = True
    elif 'sortby' in keys:
        key = keys['sortby']
        onlyFirstItem = False
        if 'order' in keys:
            order = keys['order']
            if order.casefold() == 'desc':
                isDescOrder = True
            else:
                isDescOrder = False
    return key, isDescOrder, onlyFirstItem

def sortRegular(data,key,isDescOrder):
    # This function sorts the data based on their value. (BaseAttack, Name, Weight etc.)
    data = [item for item in data if item.get(key)]
    def sortFunction(myVal):
        # 'Weight' and 'Height' values are strings with units. Here we remove the units and convert them to float while sorting.
        # Also, decimal points are commas. We replace them with dots before converting to float.
        if key == 'Weight': 
            newVal = myVal[key][:-3]
            newVal = float(newVal.replace(',','.'))
        elif key == 'Height':
            newVal = myVal[key][:-2]
            newVal = float(newVal.replace(',','.'))
        else:
            newVal = myVal[key]
        return newVal
    data = sorted(data, key=sortFunction, reverse=isDescOrder) # Sorting the data with key function above. 
    return data

def sortLists(data,key,name,isDescOrder):
    # This function sorts the data based on their item counts (in short, length). (Special Attack(s), Fast Attack(s) etc.)
    valueCounts = {}
    for item in data:
        count = len(item[key])
        itemName = item[name]
        valueCounts[itemName] = count # Using a dict to store length of the lists. 
    orderedValueCounts = {myKey: myVal for myKey, myVal in sorted(valueCounts.items(), key=lambda x: x[1], reverse=isDescOrder)} # Sorting the dict.
    newData = []
    for keyValue in orderedValueCounts: # Getting the data based on the dict we sorted. 
        newItem = [item for item in data if item[name] == keyValue]
        newData.append(newItem[0])
    data = newData
    return data 

def onlyFirstItemCheck(onlyFirstItem,data):
    # 'sortby' and 'max' or 'min' are basically the same thing, only difference is that 'max' or 'min' show the first value while 'sortby' shows all.
    # This checks the onlyFirstItem value defined in function sortSettings.
    if onlyFirstItem == True:
        output = data[0]
    else:
        output = data
    return output
                
def getFunction(isCount, category):
    # This is the primary get function.
    name = nameCheck(category) 
    keys = request.args
    data = category 
    onlyFirstItem = False
    # This part checks the keys and filters the data. 
    for key in keys: 
        if not key in funcList: # If the key in arguments is not a function (max,min,sortby,order), it will search the key in the data.
            data = getItems(keys, key, name, data,category) 
        else:
            break
    # This part sorts the data.
    if any(item in keys for item in funcListIndependent): # Checks if any key in arguments is a function. ('order' is not included here since it is dependant on 'sortby') 
        key, isDescOrder, onlyFirstItem = sortingSettings(keys) # Calling sorting settings
        if key in listAttributes: # Checking if the key is a list or not.
            data = sortLists(data,key,name,isDescOrder) # If it is a list, it will run sortLists function.
        else:
            data = sortRegular(data,key,isDescOrder) # If it is not a list, it will sort as normal.
    data = onlyFirstItemCheck(onlyFirstItem,data) # Checks if the result will be one value ('max', 'min'), or not ('sortby').
    
    if len(data) < 1: # Raising an error if there are no results.
        raise mainErrorHandler('NotFound','No results have been found.',status_code=404)

    if isCount == True: # GET & COUNT are technically the same. Only the output changes.
        output = {'Count':len(data)}
    else:
        output = data

    return jsonify(output)

def mainFunction(isCount,category):
    # getFunction with error handling.
    try:
        return getFunction(isCount,category)
    except KeyError:
        raise mainErrorHandler('KeyError','Bad Request. Key not found.',status_code=400)

class mainErrorHandler(Exception): # To return more detailed error messages.
    
    def __init__(self, errorType, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.errorType = errorType

    def to_dict(self):
        response = {}
        response['error'] = self.errorType
        response['message'] = self.message
        response['statusCode'] = self.status_code
        
        return response
