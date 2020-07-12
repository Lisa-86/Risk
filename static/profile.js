

function acceptGame(email){
    console.log('Accepting a game with ' + email)
    // notify the server that we want to accept this game using REST protocol.
    acceptGameREST(email, acceptGameCallback)
}

function acceptGameREST(email, callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = callback;
  xhttp.open("PUT", "/REST/accept/" + email, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}

function acceptGameCallback(){
    if (this.readyState == 4 && this.status == 200) {
        var acceptedGame = JSON.parse(this.responseText)
        console.log('We received :' + acceptedGame['email'] + acceptedGame["game_id"])

        // reload the page to update the information
        location.reload();
    }
}

function rejectGameREST(email, callback) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = callback;
  xhttp.open("PUT", "/REST/reject/" + email, true);
  xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.send("Your JSON Data Here");
}

function rejectGameCallback(){
    if (this.readyState == 4 && this.status == 200) {
        var removedGame = JSON.parse(this.responseText)
        console.log('We received :' + removedGame['email'])

        // remove the email address from the list under the received invitations heading
        var rec = document.getElementById('received')
        for (i = 0 ; i < rec.children.length ; i++){
            // get the child
            if (rec.children[i].innerText.indexOf(removedGame['email']) != -1){
                // if it finds a match then remove it - this will remove all from the same email
                rec.removeChild(rec.children[i])
            }
        }
    }
}

function rejectGame(email){
    rejectGameREST(email, rejectGameCallback)
}