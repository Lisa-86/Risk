
function fetchTroops(responseSuccessF) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = responseSuccessF;
    xhttp.open("GET", "/countries", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send("Your JSON Data Here");
}

window.onload = function() {
    var canvas = document.getElementById('myCanvas');
    canvas.width = window.screen.width
    canvas.height = window.innerHeight - 65
    var ctx = canvas.getContext('2d');
    var img = document.getElementById('Map');
    var width = window.innerWidth
    var offset = ((width - (width * 0.65)) / 2) - 6
    var widthScaler = (width * 0.65) / img.naturalWidth
    ctx.font = '18px hancock';
    ctx.strokeStyle = 'red';
    ctx.drawImage(img, offset, 0, width * 0.65, img.naturalHeight * widthScaler );

    var mapWidth = 1536;
    var mapHeight = 999;

    function troopsReceivedAction() {
         if (this.readyState == 4 && this.status == 200) {
             //console.log("got the allocation: ", this.responseText);
             troopsAllocation = JSON.parse(this.responseText);

              p1ters = troopsAllocation["player 1 territories"]
              p2ters = troopsAllocation["player 2 territories"]

              territories = p1ters.concat(p2ters)

              for (i = 0; i < territories.length; i++){
                  city = territories[i][0]

                  pointWidth = territories[i][1][0]
                  pointWScaler = pointWidth / img.naturalWidth
                  NewImgWidth = width * 0.65
                  finalWidth = offset + (pointWScaler * NewImgWidth)

                  pointHeight = territories[i][1][1]
                  pointHScaler = pointHeight / img.naturalHeight
                  NewImgHeight = img.naturalHeight * widthScaler
                  finalHeight = (pointHScaler * NewImgHeight)

                   if (p1ters.indexOf(territories[i]) >= 0){
                        ctx.strokeStyle = 'red';
                   }
                   else {
                        ctx.strokeStyle = 'blue';
                   }
                    ctx.strokeText('1', finalWidth, finalHeight);
              };
         };
    };

    fetchTroops(troopsReceivedAction)

};

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    //console.log('x: ' + x + ' y: ' + y)
};

const canvas = document.getElementById('myCanvas')
canvas.addEventListener('mousedown', function(e) {
    getCursorPosition(canvas, e)
});
