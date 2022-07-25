from benedict import benedict

testDict = {
    'value': 'This is a value',
    'nested': {
        'nestedValue': 'This is a nested value'
    }
}

testDict = benedict(testDict, keypath_separator='.')

print(testDict.get('nested.nestedValue'))