
function drawInstruction(){
    // prints the stats tables for each player, visible at all times
    var TroopNo = document.getElementById("TroopNo")
    var TerNo = document.getElementById("TerNo")

    TroopNo.innerHTML = calcTroopNo(risk.currentPlayer)
    TerNo.innerHTML = getTerNo(risk.currentPlayer)

    // prints at the top of the screen which colour player you are
    var WhoAreYou = document.getElementById("WhoAreYou")
    if (risk.myID == risk.player1) {
        WhoAreYou.innerHTML = "You are the RED player"
    }
    else {
        WhoAreYou.innerHTML = "You are the BLUE player"
    }

    // prints whether it's your go or not
    var con = document.getElementById('con')
    if (risk.currentPlayer == risk.myID){
        con.innerHTML = 'It is your turn. Stage: <b>' + risk['stage'] + '</b>'
    }
    else {
        con.innerHTML = 'Your orders are to wait for your next turn.'
    }

    // prints instructions for attack stage, only visible at the attack stage
    drawDeploymentInstructions()
    drawAttackInstructions()
    drawReinforceInstructions()
    drawManInstructions()
    drawWinInstructions()
}

function drawDeploymentInstructions(){
    // prints how many troops the player has to reinforce with, only shows up at deployment stage
    // else cleans up when not deployment stage
    var ren = document.getElementById('reinforceno')

    if (risk.stage == 'DEPLOYMENT'){
        if (risk.currentPlayer == risk.myID ){
            ren.innerHTML = 'You have <b>' + risk.reinNo + '</b> troops to deploy.'
        }
        else {
            ren.innerHTML = ''
        }
    }
}

function drawAttackInstructions(){
    // Draws attack instructions during the attack stage
    // but during every other stage, cleans up attack instructions
    var ops = document.getElementById("ops")
    var att = document.getElementById("att")
    var end = document.getElementById("end")

    if (risk.stage == 'ATTACK'){
        if (risk.currentPlayer == risk.myID) {
            end.style.display = "inline"
        }

        // attacker territory selected
        if (local_risk['selOwnTer'] != undefined){
            // check if the neighbour opponent territory is selected
            attackable = neighAttackOps(local_risk['selOwnTer'])
            selOwnTer = local_risk['selOwnTer']

            if (attackable.indexOf(local_risk['selOppTer']) != -1 && risk['territories'][selOwnTer]['troopNo'] >= 2){
                // if time to attack, show attack button
                if (risk.currentPlayer == risk.myID){
                    att.style.display = "inline"
                }
            }
            else {
                // not time to attack, hide attack button
                att.style.display = "none"

                // print which territories one can attack, only visible when appropriate ters selected
                if (risk.currentPlayer == risk.myID){
                    ops.innerHTML = 'From ' + local_risk['selOwnTer'] + ' you can attack: ' + attackable
                }
            }
        }
    }
    else{
        // clean up the attack instruction
        end.style.display = "none"
        att.style.display = "none"
    }

}


function drawReinforceInstructions(){
    var ops = document.getElementById('ops')
    var result = document.getElementById("result")
    var boxdiv = document.getElementById("boxdiv")

    if (risk.stage == "REINFORCE") {
        var terFrom = local_risk['selOwnTer']
        var terTo = local_risk['selOppTer']
        var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
        if (risk.currentPlayer == risk.myID) {
            ops.innerHTML = ""
            result.innerHTML = "<p> You have <b> won </b> this battle! </p> <p> You can reinforce <b>" + terTo + "</b> with up to <b>" + maxTroopNo + "</b> troops. <p> How many troops would you like to move? </p>"
            boxdiv.style.display = "inline"
        }

    }
    // clean up uneeded instructions
    else {
        boxdiv.style.display = "none"
        result.innerHTML = ""
    }
}

function drawManInstructions(){
    var ops = document.getElementById("ops")
    var man = document.getElementById("man")
    var endturn = document.getElementById("endturn")

    if (risk["stage"] == "MANOEUVRE") {

        if (risk.currentPlayer == risk.myID) {
            endturn.style.display = "inline"
        }

        var terFrom = local_risk["selOwnTer"]
        var terTo = local_risk["selOwnTer2"]

        if (terFrom == undefined && terTo == undefined) {
            if (risk.currentPlayer == risk.myID) {
                man.style.display = "none"
                ops.innerHTML = "Please choose which troops you would like to manoeuvre into an <b> adjacent </b> territory."
            }
        }
        else if (terFrom != undefined && terTo != undefined) {
            var neighs = neighManOps(terFrom)
            var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
            if (risk.currentPlayer == risk.myID) {
                man.style.display = "inline"
                if (neighs.length >= 1 && maxTroopNo >= 1) {
                    ops.innerHTML = "From <b>" + terFrom + "</b> you can move up to <b>" + maxTroopNo + "</b> troops to: " + neighs
                }
                else {
                    ops.innerHTML = "Sadly, you cannot manoeuvre any troops from <b>" + terFrom + "</b>"
                }
            }
        }

        else if (terFrom != undefined && terTo == undefined) {
            man.style.display = "none"
            var neighs = neighManOps(terFrom)
            var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
            if (risk.currentPlayer == risk.myID) {
                if (neighs.length >= 1 && maxTroopNo >= 1) {
                    ops.innerHTML = "From <b>" + terFrom + "</b> you can move up to <b>" + maxTroopNo + "</b> troops to: " + neighs
                }
                else {
                    ops.innerHTML = "Sadly, you cannot manoeuvre any troops from <b>" + terFrom + "</b>"
                }
            }
        }
    }
    else{
        // clean up
        endturn.style.display = "none"
        ops.innerHTML = ''
        man.style.display = "none"
    }
}

function drawWinInstructions() {
    Win = document.getElementById("win")

    if (risk["stage"] == "WIN!") {
        winner = risk.currentPlayer

        if (winner == risk.myID) {
            Win.innerHTML = "YOU HAVE WON"
        }
        else {
            Win.innerHTML = "Sorry, You Have Lost"
        }
    }

}