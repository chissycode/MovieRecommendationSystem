function submitReq() {
    var csrftoken = getCookie('csrftoken');

    var form = document.forms[0];
    var aliasElem = form.elements.alias;
    var desElem = form.elements.des;

    const postData = (url, data) => {
        return fetch(url, {
            method: "POST", 
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        })
        .then(response => response.json()); 
    };
    postData('/haha/some_api/', {alias: aliasElem.value, des: desElem.value})
        .then(data => renderDataContainer(data))
        .catch(error => console.error(error));
    return false;
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function renderDataContainer(data) {
    var elem = document.getElementById("data-container");
    var htmlString = "";
    elem.style.display = "block";
    for (var key in data) {
        htmlString += "<h2>" + key + ": " + data[key] + "</h2>";
    }
    elem.innerHTML = htmlString;
}

// function postData(url = '', data = {}) {
//   // Default options are marked with *
//     return fetch(url, {
//         method: "POST", 
//         headers: {
//             "Content-Type": "application/json",
//             // "Content-Type": "application/x-www-form-urlencoded",
//         },
//         body: JSON.stringify(data), // body data type must match "Content-Type" header
//     })
//     .then(response => response.json()); // parses JSON response into native Javascript objects 
// }