const url = (new URL(document.location)).origin

function getJSON(url) {
    var j = []
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) { j = data },
        async: false
    })
    return j
}

function postJSON(url, JSON) {
    var j = []
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        data: JSON,
        success: (data) => { j = data },
        async: false
    })
    return j
}

function timeStampToDate(date) {
    return `${date.getHours()}:${date.getMinutes()} ${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}