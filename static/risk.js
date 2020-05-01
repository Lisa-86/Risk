// risk = {'territories': ter: {'location': [x, y], 'neighbours': [a, b, c], 'playerNo': playerNo, 'troopNo': troopNo},
//          'currentPlayer': currentPlayer, 'reinNo': reinNo, 'selOwnTer':'ter', 'selOppTer':ter, 'tolerance':tolerance}

function askWhoseTurn(responseSuccessF) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = responseSuccessF;
  xhttp.open("GET", "/REST/player", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}

function updateGameState(){
    if (this.readyState == 4 && this.status == 200) {
        risk = JSON.parse(this.responseText)
        drawInstruction()
    }
}

function updateServerDeployment(country) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = updateGameState;
  xhttp.open("PUT", "/REST/deployment/" + country, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}

function howManyReinforcements(responseSuccessF) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = responseSuccessF;
  xhttp.open("GET", "/REST/reinforce", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}

function drawInstruction(){
    var reinNo = risk['reinNo']
    var redren = document.getElementById('redreinforceno')
    var blueren = document.getElementById('bluereinforceno')
    var redops = document.getElementById('redops')
    var blueops = document.getElementById('blueops')
    var redTroopNo = document.getElementById('redTroopNo')
    var redTerNo = document.getElementById('redTerNo')
    var blueTroopNo = document.getElementById('blueTroopNo')
    var blueTerNo = document.getElementById('blueTerNo')

    redTroopNo.innerHTML = calcTroopNo(1)
    terCount = getTerNo(1)
    redTerNo.innerHTML = terCount

    blueTroopNo.innerHTML = calcTroopNo(2)
    blueTerCount = getTerNo(2)
    blueTerNo.innerHTML = blueTerCount

    if (risk['stage'] == 'REINFORCE'){
        if (risk['currentPlayer'] == 1 ){
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


    if (risk['stage'] == 'ATTACK'){
        // attacker territory selected?
        if (local_risk['selOwnTer'] != undefined){
            // check if the neighbour opponent territory is selected
            attackable = neighAttackOps(local_risk['selOwnTer'])
            redatt = document.getElementById("redatt")
            blueatt = document.getElementById("blueatt")

            if (attackable.indexOf(local_risk['selOppTer']) != -1){
                // time to attack
                if (risk["currentPlayer"] == 1){
                    redatt.style.display = "inline"
                }
                else {
                    blueatt.style.display = "inline"
                }
            }
            else {
                // not time to attack
                redatt.style.display = "none"
                blueatt.style.display = "none"

                // show which territories one can attack
                if (risk['currentPlayer'] == 1 ){
                    redops.innerHTML = 'From ' + local_risk['selOwnTer'] + ' you can attack: ' + attackable
                }
                else {
                    blueops.innerHTML = 'From ' + local_risk['selOwnTer'] + ' you can attack: ' + attackable
                }
            }
        }


    }


}

function neighAttackOps(ter){
    // console.log('ter', ter)
    var neighbours = risk['territories'][ter]['neighbours']
    // console.log('neighbours', neighbours)

    var attackable = []
    for (var i = 0; i < neighbours.length; i++){
        var name = neighbours[i]
        if (risk['territories'][name]['playerNo'] != risk['currentPlayer']){
            // console.log("you can attack", name)
            attackable.push(name)
        }
    }

    return attackable
}


function calcTroopNo(playerNo){
    var troopNo = 0
    var territories = risk['territories']
    for (i = 0; i < Object.keys(territories).length; i++){
        name = Object.keys(territories)[i]
        if (risk['territories'][name]['playerNo'] == playerNo){
            troopNo += risk['territories'][name]['troopNo']
        }
    }
    return troopNo
}

function reactToPlayerChoice(){
    if (this.readyState == 4 && this.status == 200) {
        risk = JSON.parse(this.responseText)
        console.log('Next Player Turn:  ' + risk['currentPlayer'])
        howManyReinforcements(updateGameState)
        redcon = document.getElementById('redcon')
        bluecon = document.getElementById('bluecon')
        if (risk['currentPlayer'] == 1){
            redcon.innerText = 'It is your turn.'
            bluecon.innerText = 'Your orders are to wait for your next turn.'
        }
        else {
            redcon.innerText = 'Your orders are to wait for your next turn.'
            bluecon.innerText = 'It is your turn.'
        }
    }
}

function fetchTroops(responseSuccessF) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = responseSuccessF;
  xhttp.open("GET", "/REST/countries", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
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

function troopsReceivedAction() {
  if (this.readyState == 4 && this.status == 200) {
    var img = document.getElementById('Map');
    var canvas = document.getElementById('myCanvas');
    var ctx = canvas.getContext('2d');
    //console.log("got the allocation: ", this.responseText);
    var risk_server = JSON.parse(this.responseText);
    // update client game representation
    risk = risk_server

    var territories = risk['territories']
    for (i = 0; i < Object.keys(territories).length; i++) {
      var city = Object.keys(territories)[i]
      var territory = territories[city]

      pointWidth = territory['loc'][0]
      var mapcol = $('#mapcol')
      var finalWidth = pointWidth * mapcol.width()

      pointHeight = territory['loc'][1]
      var widthScaler = mapcol.width() / img.naturalWidth
      NewImgHeight = img.naturalHeight * widthScaler
      finalHeight = (pointHeight * NewImgHeight)

      if (territory['playerNo'] == 1) {
        ctx.strokeStyle = 'red';
      } else {
        ctx.strokeStyle = 'blue';
      }
      ctx.strokeText(territory['troopNo'], finalWidth, finalHeight);

    };

    // troops drawn, now ask whose it is
    askWhoseTurn(reactToPlayerChoice)
  };
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

    var tolx = risk['tolerance'] * mapcol.width()
    var toly = risk['tolerance'] * NewImgHeight
    var fx = risk['factorX'] * mapcol.width()
    var fy = risk['factorY'] * NewImgHeight

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
    var terx = territory['loc'][0]
    var finalWidth = terx * mapcol.width()

    var widthScaler = mapcol.width() / img.naturalWidth
    var NewImgHeight = img.naturalHeight * widthScaler
    var tery = territory['loc'][1]
    var finalHeight = tery * NewImgHeight

    box = getTerBoundary(terx, tery)
    ctx.beginPath();
    ctx.rect(box[0], box[1], box[2], box[3]);

    if (territory['playerNo'] == 1){
        ctx.strokeStyle = 'red';
        if (local_risk['selOwnTer'] == city || local_risk['selOppTer'] == city){
            ctx.stroke();
        }
    }
    else {
        ctx.strokeStyle = 'blue';
        if (local_risk['selOwnTer'] == city || local_risk['selOppTer'] == city){
            ctx.stroke();
        }
    }

    ctx.strokeText(territory['troopNo'], finalWidth, finalHeight);
  };
}

function getTerNo(playerNo){
    var territories = risk['territories']
    var count = 0
    for (i = 0; i < Object.keys(territories).length; i++){
        var ter = Object.keys(territories)[i]
        if (territories[ter]['playerNo'] == playerNo){
            count += 1
        }
    }
    return count
}

window.onload = function() {
  // our global data on state of play
  risk = {}
  local_risk = {}

  // draw pure map without troops
  drawMap()
  // fetch and draw (callback)
  fetchTroops(troopsReceivedAction)
};


window.onresize = function() {
  console.log('resize window')
  drawMap()
  drawTroops()
  drawInstruction()
};


function attackPressed() {
    terFrom = local_risk['selOwnTer']
    terTo = local_risk['selOppTer']
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = battleResults;
    xhttp.open("PUT", "/REST/diceroll/" + terFrom + "/" + terTo, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}


function battleResults() {
    if (this.readyState == 4 && this.status == 200) {

        var redcon = document.getElementById("redcon")
        var redops = document.getElementById("redops")
        var redren = document.getElementById("redreinforceno")
        var redatt = document.getElementById("redatt")
        var redresult = document.getElementById("redresult")
        var redboxdiv = document.getElementById("redboxdiv")

        var bluecon = document.getElementById("bluecon")
        var blueops = document.getElementById("blueops")
        var blueren = document.getElementById("bluereinforceno")
        var blueatt = document.getElementById("blueatt")
        var blueresult = document.getElementById("blueresult")
        var blueboxdiv = document.getElementById("blueboxdiv")

        var terFrom = local_risk['selOwnTer']
        console.log("terFrom", terFrom)
        var terTo = local_risk['selOppTer']
        console.log("terTo", terTo)
        var outcomeList = JSON.parse(this.responseText);
        var outcomeAtt = outcomeList[0]
        var outcomeDef = outcomeList[1]
        console.log("outcomes:", outcomeAtt, outcomeDef)
        risk['territories'][terFrom]['troopNo'] = outcomeAtt
        risk['territories'][terTo]['troopNo'] = outcomeDef
        if (outcomeDef == 0) {
            risk['territories'][terTo]['playerNo'] = risk["currentPlayer"]
            risk['territories'][terTo]['troopNo'] = 1
            risk['territories'][terFrom]['troopNo'] -= 1
            maxTroopNo = risk['territories'][terFrom]['troopNo'] - 1

            if (risk["currentPlayer"] == 1) {
                redcon.innerHTML = ""
                redops.innerHTML = ""
                redren.innerHTML = ""
                redatt.style.display = "none"
                redresult.innerHTML = "<p> You have <b> won </b> this battle! </p> <p> You can reinforce " + terTo + " with up to <b>" + maxTroopNo + "</b> troops. <p> How many troops would you like to move? </p>"
                blueresult.innerHTML = "Sadly, you have lost <b>" + terTo + "</b>"
                redboxdiv.style.display = "inline"
            }
            else{
                bluecon.style.display = "none"
                blueops.style.display = "none"
                blueren.style.display = "none"
                blueatt.style.display  = "none"
                blueresult.innerHTML = "<p> You have <b> won </b> this battle! </p> <p> You can reinforce " + terTo + " with up to <b>" + maxTroopNo + "</b> troops. <p> How many troops would you like to move? </p>"
                redresult.innerHTML = "Sadly, you have lost <b>" + terTo + "</b>"
                blueboxdiv.style.display = "inline"
            }
        }
        else {
            redboxdiv.style.display = "none"
            blueboxdiv.style.display = "none"
        }
        drawMap()
        drawTroops()
    }
}


function reinPressed() {
    console.log ("pressed")
}


function getCursorPosition(canvas, event) {
  const rect = canvas.getBoundingClientRect()
  const click_x = event.clientX - rect.left
  const click_y = event.clientY - rect.top
  //console.log('x: ' + x + ' y: ' + y)
  // normalise with respect to the image
  var mapcol = $('#mapcol')
  var img = document.getElementById('Map');
  var widthScaler = mapcol.width() / img.naturalWidth
  var disp_img_height = img.naturalHeight * widthScaler
  // console.log("norm new", norm_x, norm_y)

  // look up where it belongs
  var territories = risk['territories']
  for (i = 0; i < Object.keys(territories).length; i++) {
    var name = Object.keys(territories)[i]
    var territory = territories[name]
    var loc = territory['loc']

    // consider that troops are drawn from the bottom left corner
    // ie centre the position of the territory to the centre of the number
    var box = getTerBoundary(loc[0], loc[1])

    if (click_x > box[0] && click_x < box[0] + box[2] &&
        click_y > box[1] && click_y < box[1] + box[3]) {

        if (risk['currentPlayer'] == risk['territories'][name]['playerNo']){
            local_risk['selOwnTer'] = name
        }
        else {
            local_risk['selOppTer'] = name
        }

        console.log('clicked', name, risk['territories'][name]['playerNo'], 'currentPlayer', risk['currentPlayer'])
        console.log('reinNo', risk['reinNo'])
        if (risk['reinNo'] > 0 && risk['currentPlayer'] == risk['territories'][name]['playerNo']){
            risk['reinNo'] -= 1
            risk['territories'][name]['troopNo'] += 1
            console.log("update", risk['reinNo'], "troopNo", risk['territories'][name]['troopNo'])
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
  getCursorPosition(canvas, e)
});
