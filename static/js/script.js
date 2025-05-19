let mode = document.getElementById("mode")
let modeBtn = document.getElementById("modeBtn")
let forwardBtn = document.getElementById("forward")
let backwardBtn = document.getElementById("backward")

if(mode === "automated") {
    backwardBtn.disabled = true
    forwardBtn.disabled = true
}

function swapMode() {
    modeBtn.disabled = true
    console.log("MODUS WIRD GEWECHSELT")
    fetch("/mode").then(res => res.json()).then(data => {
        mode.innerHTML = data.mode
        modeBtn.disabled = false
        if(data.mode === "automated") {
            forwardBtn.disabled = true
            backwardBtn.disabled = true
        } else {
            forwardBtn.disabled = false
            backwardBtn.disabled = false
        }
    })
}

function forward() {
    modeBtn.disabled = true
    backwardBtn.disabled = true
    forwardBtn.disabled = true

    fetch("/bandforward").then(res => res.json()).then(data => {
        modeBtn.disabled = false
        backwardBtn.disabled = false
        forwardBtn.disabled = false
    })
}

function backward() {
    modeBtn.disabled = true
    backwardBtn.disabled = true
    forwardBtn.disabled = true

    fetch("/bandbackward").then(res => res.json()).then(data => {
        modeBtn.disabled = false
        backwardBtn.disabled = false
        forwardBtn.disabled = false
    })
}