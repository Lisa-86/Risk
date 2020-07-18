
function drawInstruction(){
    // prints the stats tables for each player, visible at all times
    redTroopNo.innerHTML = calcTroopNo(risk.player1)
    terCount = getTerNo(risk.player1)
    redTerNo.innerHTML = terCount

    blueTroopNo.innerHTML = calcTroopNo(risk.player2)
    blueTerCount = getTerNo(risk.player2)
    blueTerNo.innerHTML = blueTerCount

    // prints at the top of the screen which player is which
    var redWhoAreYou = document.getElementById("redWhoAreYou")
    var blueWhoAreYou = document.getElementById("blueWhoAreYou")
    if (risk.myID == risk.player1) {
        redWhoAreYou.innerHTML = "You are the RED PLAYER"
        blueWhoAreYou.innerHTML = "This is your OPPONENT"
    }
    else {
        blueWhoAreYou.innerHTML = "You are the BLUE PLAYER"
        redWhoAreYou.innerHTML = "This is your OPPONENT"
    }

    // prints whose go it is and what stage they're on, visible at all times
    var redcon = document.getElementById("redcon")
    var bluecon = document.getElementById('bluecon')
    if (risk.currentPlayer == risk.player1){
        redcon.innerHTML = 'It is your turn. Stage: <b>' + risk['stage'] + '</b>'
        bluecon.innerHTML = 'Your orders are to wait for your next turn.'
    }
    else {
        redcon.innerHTML = 'Your orders are to wait for your next turn.'
        bluecon.innerHTML = 'It is your turn. Stage: <b>' + risk['stage'] + '</b>'
    }

    // prints instructions for attack stage, only shows up at the attack stage
    drawDeploymentInstructions()
    drawAttackInstructions()
    drawReinforceInstructions()
    drawManInstructions()
    drawWinInstructions()
}

function drawDeploymentInstructions(){
    // prints how many troops the player has to reinforce with, only shows up at deployment stage
    var reinNo = risk['reinNo']
    var blueren = document.getElementById('bluereinforceno')
    var redren = document.getElementById("redreinforceno")

    if (risk['stage'] == 'DEPLOYMENT'){
        if (risk['currentPlayer'] == risk.player1 ){
            redren.innerHTML = 'You have <b>' + reinNo + '</b> troops to deploy.'
        }
        else {
            blueren.innerHTML = 'You have <b>' + reinNo  + '</b> troops to deploy.'
        }
    }
    else{
        redren.innerHTML = ''
        blueren.innerHTML = ''
    }
}

function drawAttackInstructions(){
    // Draws Attack instruction during the attack stage
    // but during every other stage, cleans up attack instructions
    var reinNo = risk['reinNo']
    var redops = document.getElementById("redops")
    var redatt = document.getElementById("redatt")
    var redend = document.getElementById("redend")

    var blueops = document.getElementById('blueops')
    var blueatt = document.getElementById("blueatt")
    var blueend = document.getElementById("blueend")

    if (risk['stage'] == 'ATTACK'){
        if (risk["currentPlayer"] == risk.player1) {
            redend.style.display = "inline"
        }
        if (risk["currentPlayer"] == risk.player2) {
            blueend.style.display = "inline"
        }
        // attacker territory selected
        if (local_risk['selOwnTer'] != undefined){
            // check if the neighbour opponent territory is selected
            attackable = neighAttackOps(local_risk['selOwnTer'])
            selOwnTer = local_risk['selOwnTer']

            if (attackable.indexOf(local_risk['selOppTer']) != -1 && risk['territories'][selOwnTer]['troopNo'] >= 2){
                // time to attack, show attack button
                if (risk["currentPlayer"] == risk.player1){
                    redatt.style.display = "inline"
                }
                else {
                    blueatt.style.display = "inline"
                }
            }
            else {
                // not time to attack, hide attack button
                redatt.style.display = "none"
                blueatt.style.display = "none"

                // print which territories one can attack, only visible when appropriate ters selected
                if (risk['currentPlayer'] == risk.player1){
                    redops.innerHTML = 'From ' + local_risk['selOwnTer'] + ' you can attack: ' + attackable
                }
                else {
                    blueops.innerHTML = 'From ' + local_risk['selOwnTer'] + ' you can attack: ' + attackable
                }
            }
        }
    }
    else{
        // clean up the attack instruction
        redend.style.display = "none"
        blueend.style.display = "none"
        redatt.style.display = "none"
        blueatt.style.display = "none"
    }

}


function drawReinforceInstructions(){
    var reinNo = risk['reinNo']

    var redops = document.getElementById("redops")
    var redresult = document.getElementById("redresult")
    var redboxdiv = document.getElementById("redboxdiv")

    var blueops = document.getElementById('blueops')
    var blueresult = document.getElementById("blueresult")
    var blueboxdiv = document.getElementById("blueboxdiv")

    if (risk['stage'] == "REINFORCE") {
        var terFrom = local_risk['selOwnTer']
        var terTo = local_risk['selOppTer']
        var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
        if (risk["currentPlayer"] == risk.player1) {
            redops.innerHTML = ""
            redresult.innerHTML = "<p> You have <b> won </b> this battle! </p> <p> You can reinforce <b>" + terTo + "</b> with up to <b>" + maxTroopNo + "</b> troops. <p> How many troops would you like to move? </p>"
            blueresult.innerHTML = "Sadly, you have lost <b>" + terTo + "</b>"
            redboxdiv.style.display = "inline"
        }
        else {
            blueops.innerHTML = ""
            blueresult.innerHTML = "<p> You have <b> won </b> this battle! </p> <p> You can reinforce <b>" + terTo + "</b> with up to <b>" + maxTroopNo + "</b> troops. <p> How many troops would you like to move? </p>"
            redresult.innerHTML = "Sadly, you have lost <b>" + terTo + "</b>"
            blueboxdiv.style.display = "inline"
        }
    }
    else {
        redboxdiv.style.display = "none"
        blueboxdiv.style.display = "none"
        redresult.innerHTML = ""
        blueresult.innerHTML = ""
    }
}

function drawManInstructions(){
    var redops = document.getElementById("redops")
    var redman = document.getElementById("redman")
    var redendturn = document.getElementById("redendturn")

    var blueops = document.getElementById('blueops')
    var blueman = document.getElementById("blueman")
    var blueendturn = document.getElementById("blueendturn")

    if (risk["stage"] == "MANOEUVRE") {

        if (risk["currentPlayer"] == risk.player1) {
            redendturn.style.display = "inline"
        }
        else {
            blueendturn.style.display = "inline"
        }

        var terFrom = local_risk["selOwnTer"]
        var terTo = local_risk["selOwnTer2"]

        if (terFrom == undefined && terTo == undefined) {
            if (risk["currentPlayer"] == risk.player1) {
                redman.style.display = "none"
                redops.innerHTML = "Please choose which troops you would like to manoeuvre into an <b> adjacent </b> territory."
            }
            else {
                blueman.style.display = "none"
                blueops.innerHTML = "Please choose which troops you would like to manoeuvre into an <b> adjacent </b> territory."
            }
        }
        else if (terFrom != undefined && terTo != undefined) {
            var neighs = neighManOps(terFrom)
            var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
            if (risk["currentPlayer"] == risk.player1) {
                redman.style.display = "inline"
                if (neighs.length >= 1 && maxTroopNo >= 1) {
                    redops.innerHTML = "From <b>" + terFrom + "</b> you can move up to <b>" + maxTroopNo + "</b> troops to: " + neighs
                }
                else {
                    redops.innerHTML = "Sadly, you cannot manoeuvre any troops from <b>" + terFrom + "</b>"
                }
            }
            else {
                blueman.style.display = "inline"
                if (neighs.length >= 1 && maxTroopNo >= 1) {
                    blueops.innerHTML = "From <b>" + terFrom + "</b> you can move up to <b>" + maxTroopNo + "</b> troops to: " + neighs
                }
                else {
                    blueops.innerHTML = "Sadly, you cannot manoeuvre any troops from <b>" + terFrom + "</b>"
                }
            }
        }

        else if (terFrom != undefined && terTo == undefined) {
            redman.style.display = "none"
            blueman.style.display = "none"
            var neighs = neighManOps(terFrom)
            var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
            if (risk["currentPlayer"] == risk.player1) {
                if (neighs.length >= 1 && maxTroopNo >= 1) {
                    redops.innerHTML = "From <b>" + terFrom + "</b> you can move up to <b>" + maxTroopNo + "</b> troops to: " + neighs
                }
                else {
                    redops.innerHTML = "Sadly, you cannot manoeuvre any troops from <b>" + terFrom + "</b>"
                }
            }
            else {
                if (neighs.length >= 1 && maxTroopNo >= 1) {
                    blueops.innerHTML = "From <b>" + terFrom + "</b> you can move up to <b>" + maxTroopNo + "</b> troops to: " + neighs
                }
                else {
                    blueops.innerHTML = "Sadly, you cannot manoeuvre any troops from <b>" + terFrom + "</b>"
                }
            }
        }
    }
    else{
        // clean up
        redendturn.style.display = "none"
        blueendturn.style.display = "none"
        redops.innerHTML = ''
        blueops.innerHTML = ''
        redman.style.display = 'none'
        blueman.style.display = 'none'
    }
}

function drawWinInstructions() {
    redWin = document.getElementById("redwin")
    blueWin = document.getElementById("bluewin")

    if (risk["stage"] == "WIN!") {
        winner = risk["currentPlayer"]

        if (winner == risk.player1) {
            redWin.innerHTML = "You Have Won!"
            blueWin.innerHTML = "Sorry, You Have Lost"
        }

        else {
            blueWin.innerHTML = "You Have Won!"
            redWin.innerHTML = "Sorry, You Have Lost"
        }
    }

}