let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})

$(document).ready(function() {
    ajaxGet('GET',"http://127.0.0.1:8000/index/api/",function(response) {
        if (response.responseText) {
            alert("error");
        }
    })
});

$(document).ready(function() {
$('.js-example-basic-single').select2({
        dropdownParent: $('#exampleModal')
});
});



