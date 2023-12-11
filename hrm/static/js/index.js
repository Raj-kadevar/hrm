var bool = true
$(".add").click(function(event){
    event.preventDefault();
    if (bool == true){
        $(".testbox").show();
        $(".add").text("Cancel");
        bool = false
    }else{
        bool = true
        $(".testbox").hide();
        $('#form')[0].reset();
        $('.span').text('')
        $(".add").text("Add user");
    }
});

$("#submit").click(function(event){
    $(this).attr("disabled", true);
    $('span').text('')
    event.preventDefault();
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = $("#login_form").serialize();


});

$("#register").click(function(event){
    $('.span').text('')
    event.preventDefault();
    $("#register").attr("disabled", true);
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = new FormData();
    formdata.append('username',$('#username').val());
    formdata.append('email',$('#email').val());
    formdata.append('password',$('#password').val());
    formdata.append('password2',$('#password2').val());
    formdata.append('roles',$('#roles').val());
    formdata.append('profile', $('input[type=file]')[0].files[0]);

    userAjaxRequest('POST', csrfToken, "http://127.0.0.1:8000/registration/api/", formdata, function(response) {
        if (response.message) {
            $('#form')[0].reset();
            alert('user successfully added');
            $("#register").attr("disabled", false);
        }
        else {
           response = JSON.parse(response.responseText)
           $('.name').text(response['username'])
           $('.email').text(response['email'])
           $('.password').text(response['password'])
           $('.password2').text(response['password2'])
           $('.role').text(response['roles'])
           $('.profile').text(response['profile'])
           $("#register").attr("disabled", false);

        }
    })
    Callback();
});


var key_counter = 0;
$(document).on('keypress','.select2-search__field', function () {
   if(event.which != 32){
        key_counter++;
   }else{

   }
   if (key_counter == 3){
        key_counter = 0;
        url = new URL("http://127.0.0.1:8000/get-device/api");
        url.searchParams.set("search", $.trim($(".select2-search__field").val()));
        ajaxGet('GET', url, function(response) {
        if (response) {
            for (let result=0; result < response.results.length; result++) {
                $('.js-example-basic-single').append('<option value="' + response.results[result]['name'] + '">' + response.results[result]['name'] + '</option>');
            }
        }
        else {
            alert(response.responseText);
        }
    })
   }
});

function select(){
    $('.js-example-basic-single option').each(function() {
    if ( $(this).val() !=  $('.js-example-basic-single').val()) {
        $(this).remove();
    }
});
}