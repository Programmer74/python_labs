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

function updateFeed() {
    var id = document.getElementById("feed_id").innerHTML;
    document.getElementById("feed_update_prg").style = "visible: block";
    getRq("/feed/update/" + id,
        function (s) {
            setTimeout(function(){
              window.location.reload();
            });
        },
        function (err, s) {
            alert("Error " + err);
        });
}


function addFeed() {
    var id = document.getElementById("new_feed_url").value;
    var url = encodeURIComponent(encodeURIComponent(id));
//    alert(url);
    document.getElementById("new_feed_prg").style = "visible: block";
    getRq("/feed/add/" + url,
        function (s) {
            setTimeout(function(){
              window.location.reload();
            });
        },
        function (err, s) {
            alert("Error " + err);
        });
}