 $(function() {
      $(document).ready(function () {
        var todaysDate = new Date();
        var year = todaysDate.getFullYear();
        var month = ("0" + (todaysDate.getMonth() + 1)).slice(-2);
        var day = ("0" + (todaysDate.getDate()+1)).slice(-2);
        var maxDate = (year +"-"+ month +"-"+ day);
        $('.min').attr('min',maxDate);
      });
});

function startDate(){

    if($('.min').val()!=""){
         $('.end-date').attr('min',$('.min').val());
         $('.end-date').val($('.min').val());
    }
}

$("#submit").click(function(event){
    $('span').text('')
    event.preventDefault();
    $("#submit").attr("disabled", true);
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var formdata = new FormData();
    formdata.append('leave_start_date',$('#start-date').val());
    formdata.append('leave_end_date',$('#end-date').val());
    formdata.append('leave_type',$('#leave-type').val());

    makeAuthAjaxRequest('POST', csrfToken, "http://127.0.0.1:8000/add-leave/api/", formdata, function(response) {
        if (response.message) {
            $('#form')[0].reset();
            alert('leave successfully added');
            $("#submit").attr("disabled", false);
        }
        else {
            alert("error");
        }
    })
    Callback();
});