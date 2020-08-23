
function getBaseUrl(prefix){
    // prefix : e.g. "/game/number" or "/"
    // find the last occurance of it
    var path = window.location.pathname

    // check where it is
    lastIndex = path.lastIndexOf(prefix)

    // take the substring
    var base = path.substring(0, lastIndex)

    return base
}