let resultsDiv = document.getElementById("results");
let episodesDiv= document.getElementById("episodes");
let playerIframe = document.getElementById("player");
playerIframe.src = "";

let tablehmtl = `
<table id="mainResultTable" class="table table-dark">
<thead>
  <tr>
    <th scope="col">#</th>
    <th scope="col">Name</th>
    <th scope="col">Link</th>
    <th scope="col">Stream</th>
  </tr>
</thead>
<tbody id="resultsBody">
</tbody>
</table>
`;

function format(query, data){
    let results = data.results;
    if(results.length > 0){
        resultsDiv.innerHTML = tablehmtl;
    }
    
    let tableBody = document.getElementById("resultsBody");

    for(let i = 0; i < results.length;i++){
        console.log(results[i]);
        let entry = `
        <tr>
        <th scope="row">${i+1}</th>
        <td>${results[i]["name"]}</td>
        <td>${results[i]["url"]}</td>
        <td><button type="button" id="playStream${i}" originalquery="${query}" onClick="getEpisodes(this.getAttribute('originalquery'), this.getAttribute('animename'), this.getAttribute('animeindex'))" animename="${results[i]["name"]}" animeindex="${i}" class="btn btn-dark">&#9658;</button></td>
        </tr>
        `;
        tableBody.innerHTML += entry;
    } 

    episodesDiv.innerHTML = '';
}

function formatEpisodes(originalQuery, title, index, data){
    let total = data["total"];
    episodesDiv.innerHTML = "<h2 class='text-white'>" + title + "</h2>";
    episodesDiv.innerHTML += "<p>"
    episodesDiv.innerHTML += "<h3 class='text-white'> Total Episodes: " + total + "</h3>";
    
    let flexbox = document.createElement("div");
    flexbox.classList.add("box");

    for(let i=1;i<total+1;i++){
      flexbox.innerHTML += `<button animename="${originalQuery}" animeepisode="${i}" animeindex="${index}" type="button" class="btn btn-dark" onClick="getStream(this.getAttribute('animename'), this.getAttribute('animeindex'), this.getAttribute('animeepisode'))">${i}</button>`;
    }

    episodesDiv.appendChild(flexbox);
}

function loadPlayer(data){
  let streamSrc = data["stream"];
  playerIframe.src = streamSrc;
}