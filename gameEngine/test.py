from benedict import benedict

initCommands = benedict({
    'import': {
        'mod': 'loadMod',
        'asset': 'loadAsset'
        }
    },keypath_separator='.')

print(initCommands.get('import.asset'))