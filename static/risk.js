// risk = {'territories': ter: {'location': [x, y], 'neighbours': [a, b, c], 'playerNo': playerNo, 'troopno': troopNo},
//          'currentPlayer': currentPlayer, 'reinNo': reinNo, 'selOwnTer':'ter', 'selOppTer':ter, 'tolerance':tolerance}

function askWhoseTurn(responseSuccessF) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = responseSuccessF;
  xhttp.open("GET", "/REST/player", true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}

function updateServerDeployment(country) {
  var xhttp = new XMLHttpRequest();
//  xhttp.onreadystatechange = responseSuccessF;
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

    if (reinNo > 0){
        if (risk['currentPlayer'] == 1 ){
            redren.innerHTML = 'You have <b>' + reinNo + '</b> troops to deploy.'
        }
        else {
            blueren.innerHTML = 'You have <b>' + reinNo  + '</b> troops to deploy.'
        }
    }

    if (reinNo == 0){
        if (risk['currentPlayer'] == 1 ){
            redren.innerHTML = 'Please choose which territory you want to launch an attack from'
            redops.innerHTML = 'From ' + risk['selOwnTer'] + ' you can attack: '
        }
        else {
            blueren.innerHTML = 'Please choose which territory you want to launch an attack from'
            bluedops.innerHTML = 'From ' + risk['selOwnTer'] + ' you can attack: '
        }
    }
}

function updateTroops(){
    if (this.readyState == 4 && this.status == 200) {
        console.log('Has ' + this.responseText + ' many  more troops')
        risk['reinNo'] = Number(this.responseText)
        drawInstruction()
    }
}

function reactToPlayerChoice(){
    if (this.readyState == 4 && this.status == 200) {
        console.log('Next Player Turn:  ' + this.responseText)
        risk['currentPlayer'] = Number(this.responseText)
        howManyReinforcements(updateTroops)
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

        redTroopNo = document.getElementById('redTroopNo')
        redTroopNo.innerText = '63'
        redTerNo = document.getElementById('redTerNo')
        terCount = getTerNo(1)
        redTerNo.innerText = terCount
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
    var territories = JSON.parse(this.responseText);
    risk['territories'] = territories

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

function drawTroops() {
  var territories = risk['territories']
  var img = document.getElementById('Map');
  var canvas = document.getElementById('myCanvas');
  var ctx = canvas.getContext('2d');

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


    ctx.beginPath();
    var tolx = risk['tolerance'] * mapcol.width()
    var toly = risk['tolerance'] * NewImgHeight
    var fx = risk['factorX'] * mapcol.width()
    var fy = risk['factorY'] * NewImgHeight
    ctx.rect(finalWidth + fx - tolx,
             finalHeight + fy - toly,
             tolx * 2,
             toly * 2);

    if (territory['playerNo'] == 1) {
      ctx.strokeStyle = 'red';
      if (risk['selOwnTer'] == city){
        ctx.stroke();
      }
    }
    else {
        ctx.strokeStyle = 'blue';
        if (risk['selOppTer'] == city){
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
  // defines the clickable square around the number
  risk['tolerance'] = 0.02
  risk['factorX'] = 0.015
  risk['factorY'] = -0.015

  // draw pure map without troops
  drawMap()
  // fetch and draw (callback)
  fetchTroops(troopsReceivedAction)
};


window.onresize = function() {
  drawMap()
  drawTroops()
  drawInstruction()
};


function getCursorPosition(canvas, event) {
  const rect = canvas.getBoundingClientRect()
  const click_x = event.clientX - rect.left
  const click_y = event.clientY - rect.top
  //console.log('x: ' + x + ' y: ' + y)
  // normalise with respect to the image
  var mapcol = $('#mapcol')
  var img = document.getElementById('Map');
  var widthScaler = mapcol.width() / img.naturalWidth
  var norm_click_x = click_x / mapcol.width()
  var disp_img_height = img.naturalHeight * widthScaler
  var norm_click_y = click_y / disp_img_height
  // console.log("norm new", norm_x, norm_y)

  // look up where it belongs
  var territories = risk['territories']
  for (i = 0; i < Object.keys(territories).length; i++) {
    var name = Object.keys(territories)[i]
    var territory = territories[name]
    var loc = territory['loc']
    // consider that troops are drawn from the bottom left corner
    // ie centre the position of the territory to the centre of the number
    var x = loc[0] + risk['factorX']
    var y = loc[1] + risk['factorY']
    var tolerance = risk['tolerance']

    if (norm_click_x > x - tolerance && norm_click_x < x + tolerance &&
    norm_click_y > y - tolerance && norm_click_y < y + tolerance) {

        if (risk['currentPlayer'] == risk['territories'][name]['playerNo']){
            risk['selOwnTer'] = name
        }
        else {
            risk['selOppTer'] = name
        }

        console.log('clicked', name, risk['territories'][name]['playerNo'], 'currentPlayer', risk['currentPlayer'])
        if (risk['reinNo'] > 0 && risk['currentPlayer'] == risk['territories'][name]['playerNo']){
            risk['reinNo'] -= 1
            risk['territories'][name]['troopNo'] += 1
            console.log("update", risk['reinNo'], "troopNo", risk['territories'][name]['troopNo'])
        }

      updateServerDeployment(name)
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
