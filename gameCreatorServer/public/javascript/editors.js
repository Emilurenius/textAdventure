function editors() {
    var asset = {}
    const weaponsEditor = document.getElementById("weaponsEditor")
    const addWeapon = document.getElementById("addWeapon")

    function showAsset() {
        const textContainer = document.getElementById("jsonTextContainer")
        textContainer.innerHTML = ""

        const assetStringified = JSON.stringify(asset, null, 4)
        textContainer.innerHTML = assetStringified

        const data = "text/json;charset=utf-8," + encodeURIComponent(assetStringified);
        const a = document.getElementById("downloadJSON")
        a.href = 'data:' + data
        a.download = 'asset.json'
    }

    function activateWeapons() {
        console.log("Activated weapons")
        weaponsEditor.style = "display:block"
    }

    function activateConsumables() {
        console.log("Deactivated weapons")
        weaponsEditor.style = "display:none"
    }

    const funcs = {
        "weapons": activateWeapons,
        "consumables": activateConsumables
    }
    const assetType = document.getElementById("assetType")
    funcs[assetType.value]()
    
    assetType.addEventListener("change", (event) => {
        funcs[assetType.value]()
    })

    addWeapon.addEventListener("click", (event) => {
        const weaponName = document.getElementById("weaponName").value
        const weaponDesc = document.getElementById("weaponDesc").value
        const dDiceMultiplier = document.getElementById("dDiceMultiplier").value
        const dDiceType = document.getElementById("dDiceType").value
        const hDiceMultiplier = document.getElementById("hDiceMultiplier").value
        const hDiceType = document.getElementById("hDiceType").value
        const weaponDT = document.getElementById("weaponDT").value
        const weaponWeight = document.getElementById("weaponWeight").value


        if (!asset.hasOwnProperty("weapons")) {
            console.log("No weapons added previously")
            asset["weapons"] = {}
        }
        asset["weapons"][weaponName] = {
            desc: weaponDesc,
            damageDice: `${dDiceMultiplier}d${dDiceType}`,
            hitDice: `${hDiceMultiplier}d${hDiceType}`,
            damageType: weaponDT,
            weight: weaponWeight
        }
        console.log(asset)
        showAsset()
    })

}editors()