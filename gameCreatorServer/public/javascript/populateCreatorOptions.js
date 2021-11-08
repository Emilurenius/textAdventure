function populateCreatorOptions() {
    const creatorOptions = document.getElementById('creatorOptions')

    const buttons = {
        assetCreator: {
            name: "Asset/Mod Creator",
            href: `${url}/assetCreator`
        },
        gameCreator: {
            name: "Game Creator",
            href: `${url}/gameCreator`
        }
    }

    for (const [k, v] of Object.entries(buttons)) {
        const button = document.createElement('a')
        button.innerHTML = v.name
        button.href = v.href
        button.className = "button"
        creatorOptions.appendChild(button)
    }
}populateCreatorOptions()