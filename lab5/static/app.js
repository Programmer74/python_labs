function getRq(url, callback, error) {
    console.log("Requesting url " + url);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState === 4) {
            if (xmlHttp.status === 200) {
                callback(xmlHttp.responseText);
            } else {
                error(xmlHttp.status, xmlHttp.responseText)
            }
        }
    };
    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.send(null);
}

function getRandomName(objectId) {
    document.getElementById(objectId).innerHTML = "loading";
    getRq("/randomname",
        function (s) {
            document.getElementById(objectId).innerHTML = s;
        },
        function (err, s) {
            document.getElementById(setTextTo).innerHTML = "Error " + err;
        });
}

function getGuessResult(objectIdForId, objectIdForName, objectIdForResult) {
    document.getElementById(objectIdForResult).innerHTML = "loading";
    var id = document.getElementById(objectIdForId).innerHTML;
    var name = document.getElementById(objectIdForName).value;
    getRq("/guess/" + id + "/"  + name,
        function (s) {
            document.getElementById(objectIdForResult).innerHTML = s;
        },
        function (err, s) {
            document.getElementById(objectIdForResult).innerHTML = "Error " + err;
        });
}