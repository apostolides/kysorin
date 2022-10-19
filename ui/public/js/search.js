let searchBar = document.getElementById("searchBar");
let baseDomain = "http://localhost:8081";
let loadingIntervalId;

function submit(){
    let query = searchBar.value.trim();
    playerIframe.src = "";
    if(query){
        loadingIntervalId = setInterval(loading,1000);
        revealLoadingBar();
        fetch(`${baseDomain}/animix/${query}`)
        .then((response)=> response.json())
        .then((data)=>{
            format(query, data);
        })
        .catch((error)=>{
            console.error(error);
        })
        .finally(()=>{
            clearInterval(loadingIntervalId);
            hideLoadingBar();
        })
    }
}

searchBar.addEventListener("submit", submit);
searchBar.addEventListener("keyup", (e)=>{
    if(e.code == "Enter"){
        submit();
    }
});

function getEpisodes(originalQuery, title, index){
    loadingIntervalId = setInterval(loading,1000);
    revealLoadingBar();
    hideResults()
    fetch(`${baseDomain}/animix/total/${originalQuery}/${index}`)
    .then((response)=> response.json())
    .then((data)=>{
        formatEpisodes(originalQuery, title, index, data);
    })
    .catch((error)=>{
        console.error(error);
    })
    .finally(()=>{
        clearInterval(loadingIntervalId);
        hideLoadingBar();
    })
}

function getStream(title, index, episode){
    console.log(title, index, episode);
    loadingIntervalId = setInterval(loading,1000);
    revealLoadingBar();
    fetch(`${baseDomain}/animix/${title}/${index}/${episode}`)
    .then((response)=> response.json())
    .then((data)=>{
        loadPlayer(data);
    })
    .catch((error)=>{
        console.error(error);
    })
    .finally(()=>{
        clearInterval(loadingIntervalId);
        hideLoadingBar();
    })
}