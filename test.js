const creep = {
    memory: {
        target: {
            obj1: {
                hp: 50,
                maxHP: 100
            },
            obj2: {
                hp: 100,
                maxHP: 100
            },
            obj3: {
                hp: 30,
                maxHP: 100
            },
        }
    }
}

const objects = creep.memory.target
console.log(objects)

for (const [k, v] of Object.entries(objects)) {
    if (v.hp == v.maxHP) {
        delete creep.memory.target[k]
    }
}

console.log(creep.memory.target)