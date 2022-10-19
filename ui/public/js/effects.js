let loadingField = document.getElementById("loadingField");

function loading(){
    loadingField.appendChild(document.createTextNode("."));
}

function revealLoadingBar(){
    loadingField.classList.remove("hidden");
}

function hideLoadingBar(){
    loadingField.innerHTML = '';
}

function hideResults(){
    document.getElementById("mainResultTable").classList.add("hidden");
}

function revealResults(){
    document.getElementById("mainResultTable").classList.remove("hidden");
}