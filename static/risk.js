// risk = {'territories': ter: {'location': [x, y], 'neighbours': [a, b, c], 'owner': ownerNo, 'troopNo': troopNo},
//          'currentPlayer': currentPlayer, 'reinNo': reinNo, 'selOwnTer':'ter', 'selOppTer':ter, 'tolerance':tolerance}


function updateGameState(){
    if (this.readyState == 4 && this.status == 200) {
        risk = JSON.parse(this.responseText)

        if (risk['stage'] == 'MANOEUVRE'){
            // deselect territories
            console.log('Manoeuvre: deselect territories')
            local_risk['selOwnTer'] = undefined
            local_risk['selOwnTer2'] = undefined
            local_risk['selOppTer'] = undefined
        }

        drawMap()
        drawTroops()
        drawInstruction()
    }
}

// updates the server after reincforcement click
function updateServerDeployment(country) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = updateGameState;
  xhttp.open("PUT", "/REST/deployment/" + risk['id'] + "/" + country, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}


function fetchGame(responseSuccessF) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = responseSuccessF;
  // get the current url and extract from it the game ID no
  var gameNo = window.location.href.split("/").pop()
  xhttp.open("GET", "/REST/game/" +  gameNo, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}


function attackPressed() {
    terFrom = local_risk['selOwnTer']
    terTo = local_risk['selOppTer']
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = updateGameState;
    xhttp.open("PUT", "/REST/diceroll/" + risk["id"] + "/" + terFrom + "/" + terTo, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}


// check the input is valid
function reinPressed() {
    var terFrom = local_risk['selOwnTer']
    var terTo = local_risk['selOppTer']
    var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1
    if (maxTroopNo == 0) {
        return updateInput(0)
    }
    if (risk['currentPlayer'] == risk.player1) {
        // serve the player with the left column (red) -
        // checks player has entered appropriate no and updates the instructions writen on the screen
        input = document.getElementById("redbox").value
        if (input == "") {
            input = "0"
            return updateInput(input)
        }
        else if (input < 0) {
            document.getElementById("redresult").innerHTML =  "<p> You can't move negative troops! </p>"
            redboxdiv.style.display = "inline"
        }
        else if (input > maxTroopNo) {
            document.getElementById("redresult").innerHTML = "<p> You can only move up to <b>" + maxTroopNo + "</b> troops. </p>"
            redboxdiv.style.display = "inline"
        }
        else {
            return updateInput(input)
        }
    }
    else {
        // does the same for player 2 on the right column (blue)
        input = document.getElementById("bluebox").value
        if (input == "") {
            input = "0"
            return updateInput(input)
        }
        else if (input < 0) {
            document.getElementById("blueresult").innerHTML =  "<p> You can't move negative troops! </p>"
            blueboxdiv.style.display = "inline"
        }
        else if (input > maxTroopNo) {
            document.getElementById("blueresult").innerHTML = "<p> You can only move up to <b>" + maxTroopNo + "</b> troops. </p>"
            blueboxdiv.style.display = "inline"
        }
        else {
            return updateInput(input)
        }
    }
}


function updateInput(validInput) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = updateGameState;
    xhttp.open("PUT", "/REST/reinforcement/" + risk["id"] + "/" + validInput, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}


function endMovePressed() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = updateGameState;
    xhttp.open("PUT", "/REST/endmove/" + risk["id"], true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}


function manPressed() {
    var terFrom = local_risk['selOwnTer']
    var terTo = local_risk['selOwnTer2']
    var maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1

    // checks the red player has put in an appropriate number and writes instructions on the screen
    if (risk['currentPlayer'] == risk.player1) {
        input = document.getElementById("redmanbox").value
        if (input == "") {
            input = "0"
            return updateManInput(input)
        }
        else if (input < 0) {
            document.getElementById("redresult").innerHTML =  "<p> You can't move negative troops! </p>"
            redmanbox.style.display = "inline"
        }
        else if (input > maxTroopNo) {
            document.getElementById("redresult").innerHTML = "<p> You can only move up to <b>" + maxTroopNo + "</b> troops. </p>"
            redmanbox.style.display = "inline"
        }
        else {
            return updateManInput(input)
        }
    }
    else {
        // does the same for the blue player
        input = document.getElementById("bluemanbox").value
        if (input == "") {
            input = "0"
            return updateManInput(input)
        }
        else if (input < 0) {
            document.getElementById("blueresult").innerHTML =  "<p> You can't move negative troops! </p>"
            bluemanbox.style.display = "inline"
        }
        else if (input > maxTroopNo) {
            document.getElementById("blueresult").innerHTML = "<p> You can only move up to <b>" + maxTroopNo + "</b> troops. </p>"
            bluemanbox.style.display = "inline"
        }
        else {
            return updateManInput(input)
        }
    }
}


function updateManInput(troopNo) {
    var terFrom = local_risk['selOwnTer']
    var terTo = local_risk['selOwnTer2']
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = updateGameState;
    xhttp.open("PUT", "/REST/man/" + risk["id"] + "/" + terFrom + "/" + terTo + "/" + troopNo, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}


function endTurnPressed() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = updateGameState;
    xhttp.open("PUT", "/REST/endTurn/" + risk["id"], true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}

function neighAttackOps(ter){
    var neighbours = risk['territories'][ter]['neighbours']
    var attackable = []
    for (var i = 0; i < neighbours.length; i++){
        var name = neighbours[i]
        if (risk['territories'][name]['owner'] != risk['currentPlayer']){
            attackable.push(name)
        }
    }
    return attackable
}


function neighManOps(ter){
    var neighbours = risk['territories'][ter]['neighbours']
    var moveable = []
    for (var i = 0; i < neighbours.length; i++){
        var name = neighbours[i]
        if (risk['territories'][name]['owner'] == risk['currentPlayer']){
            moveable.push(name)
        }
    }
    return moveable
}


function calcTroopNo(playerNo){
    var troopNo = 0
    var territories = risk['territories']
    for (i = 0; i < Object.keys(territories).length; i++){
        name = Object.keys(territories)[i]
        if (risk['territories'][name]['owner'] == playerNo){
            troopNo += risk['territories'][name]['troopNo']
        }
    }
    return troopNo
}


function getTerNo(playerNo){
    var territories = risk['territories']
    var count = 0
    for (i = 0; i < Object.keys(territories).length; i++){
        var ter = Object.keys(territories)[i]
        if (territories[ter]['owner'] == playerNo){
            count += 1
        }
    }
    return count
}


function drawMap() {
    var canvas = document.getElementById('myCanvas');
    var mapcol = $('#mapcol')
    canvas.width = mapcol.width()
    canvas.height = window.innerHeight - 65
    var ctx = canvas.getContext('2d');
    var img = document.getElementById('Map');
    var widthScaler = mapcol.width() / img.naturalWidth
    ctx.font = '18px hancock';
    ctx.drawImage(img, 0, 0, mapcol.width(), img.naturalHeight * widthScaler);
};


function getTerBoundary(x, y){
    // x, y of the territory
    // This function adjust x,y to the middle of the troop number drawn on the map
    // and then calculates a box around it giving a rectangle area
    var mapcol = $('#mapcol')
    var img = document.getElementById('Map');
    var widthScaler = mapcol.width() / img.naturalWidth
    var NewImgHeight = img.naturalHeight * widthScaler

    var finalWidth = x * mapcol.width()
    var finalHeight = y * NewImgHeight

    var tolx = local_risk['tolerance'] * mapcol.width()
    var toly = local_risk['tolerance'] * NewImgHeight
    var fx = local_risk['factorX'] * mapcol.width()
    var fy = local_risk['factorY'] * NewImgHeight

    // return top-left x, top-left y, width, height
    return [finalWidth + fx - tolx, finalHeight + fy - toly, tolx * 2, toly * 2]
}


function drawTroops() {
  var territories = risk['territories']
  var img = document.getElementById('Map');
  var canvas = document.getElementById('myCanvas');
  var ctx = canvas.getContext('2d');

  for (i = 0; i < Object.keys(territories).length; i++) {
    var city = Object.keys(territories)[i]
    var territory = territories[city]

    var mapcol = $('#mapcol')
    var terx = territory['locx']
    var finalWidth = terx * mapcol.width()

    var widthScaler = mapcol.width() / img.naturalWidth
    var NewImgHeight = img.naturalHeight * widthScaler
    var tery = territory['locy']
    var finalHeight = tery * NewImgHeight

    box = getTerBoundary(terx, tery)
    ctx.beginPath();
    ctx.rect(box[0], box[1], box[2], box[3]);

    // draws in red boxes around places
    if (territory['owner'] == risk.player1){
        ctx.strokeStyle = 'red';
        if (local_risk['selOwnTer'] == city || local_risk['selOwnTer2'] == city || local_risk['selOppTer'] == city){
            ctx.stroke();
        }
    }
    // does the same for the blue player
    else {
        ctx.strokeStyle = 'blue';
        if (local_risk['selOwnTer'] == city || local_risk['selOwnTer2'] == city || local_risk['selOppTer'] == city){
            ctx.stroke();
        }
    }

    ctx.strokeText(territory['troopNo'], finalWidth, finalHeight);
  };
}


window.onload = function() {
  // our global data on state of play
  risk = {}
  local_risk = {
    'tolerance': 0.02,
    'factorX': 0.015,
    'factorY': -0.015
  }
  fetchGame(updateGameState)
};


window.onresize = function() {
  console.log('resize window')
  drawMap()
  drawTroops()
  drawInstruction()
};


function mapPressed(canvas, event) {
  const rect = canvas.getBoundingClientRect()
  const click_x = event.clientX - rect.left
  const click_y = event.clientY - rect.top

  // normalise with respect to the image
  var mapcol = $('#mapcol')
  var img = document.getElementById('Map');
  var widthScaler = mapcol.width() / img.naturalWidth
  var disp_img_height = img.naturalHeight * widthScaler

  // look up where it belongs
  var territories = risk['territories']
  for (i = 0; i < Object.keys(territories).length; i++) {
    var name = Object.keys(territories)[i]
    var territory = territories[name]

    // consider that troops are drawn from the bottom left corner
    // ie centre the position of the territory to the centre of the number
    var box = getTerBoundary(territory['locx'], territory['locy'])

     // check if the click is within the territory box
     if (click_x > box[0] && click_x < box[0] + box[2] &&
        click_y > box[1] && click_y < box[1] + box[3]) {

        if (risk['currentPlayer'] == risk['territories'][name]['owner']){

            if (risk["stage"] != "MANOEUVRE") {
                local_risk['selOwnTer'] = name
                local_risk['selOwnTer2'] = undefined
            }
            else {
                // MANOEUVRE stage
                // two variables to handle two territories
                // 1) local_risk['selOwnTer']
                // 2) local_risk['selOwnTer2']
                // we have to keep track of which click is the oldest one

                if (local_risk['selOwnTer'] == undefined){
                    local_risk['selOwnTer'] = name
                }
                else {
                    // selOwnTer is defined,
                    if (local_risk['selOwnTer2'] == undefined){
                        local_risk['selOwnTer2'] = name
                    }
                    else{
                        local_risk['selOwnTer'] = name
                        local_risk['selOwnTer2'] = undefined
                    }

                }
            }
        }
        else {
            local_risk['selOppTer'] = name
        }

        if (risk['reinNo'] > 0 && risk['currentPlayer'] == risk['territories'][name]['owner']){
            updateServerDeployment(name)
        }

      drawMap()
      drawTroops()
      drawInstruction()
    }
  }


};

const canvas = document.getElementById('myCanvas')
canvas.addEventListener('mousedown', function(e) {
    mapPressed(canvas, e)
});