var movieLabelList = new Set();

// ---< Send request to get movie recommendation >---
function submitReq() {
    // Send ajax to designated URL, then render "recommendation-list"
    //    based on the retrieved data
    var csrftoken = getCookie('csrftoken');
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
    var data = genData();
    postData('/api/recommendation/', data)
        .then(data => renderRecommendationList(data))
        .catch(error => console.error(error));
    return false;
}
function getPoster(film, i){
        var parenthesisPos = film.indexOf("(");
        if (parenthesisPos != -1) {
            film = film.substr(0, parenthesisPos);
        }
         if(film == ''){
             // do nothing
         } else {
            $.getJSON("https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=" + film + "&callback=?", function(json) {
               if (json != "Nothing found."){                 
                    console.log(json);
                    $('#poster'+i).html('<div class="movie"> <div class="movie-image"> <a href="https://www.themoviedb.org/search/movie?query='+json.results[0].title+'&language=en" target="_Blank"><img src="http://image.tmdb.org/t/p/w500/' + json.results[0].poster_path+'" alt="movie" /></a></div><label>'+json.results[0].title+'</label></div>');
                    console.log(json.results[0].title);
                }
             });
          }

        return false;
   }
function renderRecommendationList(data) {
    console.log(data);
    var htmlString = "<p style='color:white; font-size:2.5em;'><strong> Recommendations for you </strong></p>";
    var recommendationList = data["data"];
    var i = 1;
    var renderItem = (movieItem) => {
        itemId = 'poster' + (i++);
        htmlString += "<div id=\""
        + itemId + "\" class = \"poster\">" + movieItem + "</div>";
    }
    recommendationList.forEach(renderItem);
    var elemRecommendationList = document.getElementById('recommendation-list');
    // elemRecommendationList.style.display = "block";
    elemRecommendationList.innerHTML = htmlString;
    elemRecommendationList.style.display = 'block';
    i = 1;
    var renderPoster = (movieItem) => {
        getPoster(movieItem, i++);
    }
    recommendationList.forEach(renderPoster);
   // var elemRecommendationList = document.getElementById('recommendation-list');
   // elemRecommendationList.style.display = "block";
   // elemRecommendationList.innerHTML = htmlString;
}

// ---< Construct a json for request >---
function genData() {
    var data = {};
    data['twitterId'] = document.forms[0].twitterId.value;
    var movies = Array.from(movieLabelList);
    data['movies'] = movies;
    return data;
}

// ---< Add a new movie label >---
function addMovieLabel() {
    var elemMovieLabelInput = document.forms[0].MovieLabelInput;
    if (elemMovieLabelInput.value.length == 0)
        return false;
    movieLabelList.add(elemMovieLabelInput.value);
    elemMovieLabelInput.value = "";
    renderMovieLabelList();
    return false;
}

// ---< Re-render the movie label list >---
function renderMovieLabelList() {
    var htmlString = "";
    var f = (item) => {
        htmlString += "<span class=\"label label-info\">" 
        + item +"</span>&nbsp";
    };
    movieLabelList.forEach(f);
    if (htmlString.length == 0)
        return;
    var elemMovieLabelList = document.getElementById("movie-label-list");
    elemMovieLabelList.innerHTML = htmlString;
}

// ---< function to get token for authorization related purposes >---
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