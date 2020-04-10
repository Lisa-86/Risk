function fetchTroops(responseSuccessF) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = responseSuccessF;
    xhttp.open("GET", "/countries", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}

function getOffsetX(){
    return ((window.innerWidth - (window.innerWidth * 0.65)) / 2) - 6
}

function drawMap(){
    var canvas = document.getElementById('myCanvas');
    canvas.width = window.screen.width
    canvas.height = window.innerHeight - 65
    var ctx = canvas.getContext('2d');
    var img = document.getElementById('Map');
    var width = window.innerWidth
    var offsetX = getOffsetX()
    var widthScaler = (width * 0.65) / img.naturalWidth
    ctx.font = '18px hancock';
    ctx.drawImage(img, offsetX, 0, width * 0.65, img.naturalHeight * widthScaler );
};

function troopsReceivedAction() {
     if (this.readyState == 4 && this.status == 200) {
        var img = document.getElementById('Map');
        var canvas = document.getElementById('myCanvas');
        var ctx = canvas.getContext('2d');
         //console.log("got the allocation: ", this.responseText);
         troopsAllocation = JSON.parse(this.responseText);

          p1ters = troopsAllocation["player 1 territories"]
          p2ters = troopsAllocation["player 2 territories"]

          territories = p1ters.concat(p2ters)
          risk['territories'] = territories


          for (i = 0; i < territories.length; i++){
              city = territories[i][0]

              pointWidth = territories[i][1][0]
              NewImgWidth = window.innerWidth * 0.65
              var offset = ((window.innerWidth - (window.innerWidth * 0.65)) / 2) - 6
              finalWidth = offset + (pointWidth * NewImgWidth)

              pointHeight = territories[i][1][1]
              var widthScaler = (window.innerWidth * 0.65) / img.naturalWidth
              NewImgHeight = img.naturalHeight * widthScaler
              finalHeight = (pointHeight * NewImgHeight)

               if (p1ters.indexOf(territories[i]) >= 0){
                    ctx.strokeStyle = 'red';
               }
               else {
                    ctx.strokeStyle = 'blue';
               }
                ctx.strokeText('3', finalWidth, finalHeight);

          };
     };
};

window.onload = function() {
    // draw pure map without troops
    drawMap()
    // fetch and draw (callback)
    fetchTroops(troopsReceivedAction)
    // our current data on state of play
    risk = {}
};


window.onresize = function() {
    // draw pure map without troops
    drawMap()
    // fetch and draw (callback)
    fetchTroops(troopsReceivedAction)

    // redraw(updated_troops)
    // drawTroops
};


function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    const click_x = event.clientX - rect.left
    const click_y = event.clientY - rect.top
    //console.log('x: ' + x + ' y: ' + y)
    // subtract the offset from x
    // normalise with respect to the image
    var disp_img_width = window.innerWidth * 0.65
    var img = document.getElementById('Map');
    var widthScaler = (window.innerWidth * 0.65) / img.naturalWidth
    //
    var norm_click_x =  (click_x - getOffsetX()) / disp_img_width

    var disp_img_height = img.naturalHeight * widthScaler
    var norm_click_y = click_y / disp_img_height
    // console.log("norm new", norm_x, norm_y)

    // look up where it belongs
    console.log()
    var territories = risk['territories']
    for (i=0 ; i<territories.length ; i++){
        var territory = territories[i]
//        console.log('terr', territory[1])
        var loc = territory[1]
        // consider that troops are drawn from the bottom left corner
        var x = loc[0] + 0.0025
        var y = loc[1] - 0.005

        var tolerance = 0.02

        if (norm_click_x > x - tolerance && norm_click_x < x + tolerance &&
            norm_click_y > y - tolerance && norm_click_y < y + tolerance){
            console.log('clicked', territory[0])
        }

    }


};

const canvas = document.getElementById('myCanvas')
canvas.addEventListener('mousedown', function(e) {
    getCursorPosition(canvas, e)
});

