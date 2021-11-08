function editors() {

    weaponsEditor = document.getElementById("weaponsEditor")

    function activateWeapons() {
        console.log("Activated weapons")
        weaponsEditor.style = "display:block"
    }

    function activateConsumables() {
        console.log("Deactivated weapons")
        weaponsEditor.style = "display:none"
    }

    funcs = {
        "weapons": activateWeapons,
        "consumables": activateConsumables
    }
    assetType = document.getElementById("assetType")
    funcs[assetType.value]()
    
    assetType.addEventListener("change", (event) => {
        funcs[assetType.value]()
    })

}editors()