function makeAuthAjaxRequest(methodType, csrfToken, url, data, callback)
{
    $.ajax({
        method: methodType,
        headers: {
            'X-CSRFToken': csrfToken
        },
        url: url,
        data: data,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

    });
}

function makeAuthAjaxGet(methodType, url, callback) {
    $.ajax({
        method: methodType,
        url: url,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },

    });
}


function makeAjaxRequest(methodType, csrfToken, url, data, callback)
{
    const headers = { 'X-CSRFToken': csrfToken, 'Authorization': 'Token ' + localStorage.getItem("access_token"), 'content-type': 'multipart/form-data' };
    $.ajax({
        method: methodType,
        headers: headers,
        url: url,
        data: data,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

    });
}

function ajaxGet(methodType, url, callback) {
    const headers = {'Authorization': 'Token ' + localStorage.getItem("access_token"), 'content-type': 'multipart/form-data' };
    $.ajax({
        method: methodType,
        headers: headers,
        url: url,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function(data){
            if(data.status == 401)
            {
                window.location.href= '/login/';
            }
        }
    });
}

function userAjaxRequest(methodType, csrfToken, url, data, callback)
{
    const headers = { 'X-CSRFToken': csrfToken, 'Authorization': 'Token ' + localStorage.getItem("access_token")};
    $.ajax({
        method: methodType,
         headers: headers,
        url: url,
        data: data,
        processData: false,
        contentType: false,
        success: function (data) {
            if (callback) {
                callback(data)
            }
        },
        error: function (data) {
             if (callback) {
                callback(data)
            }
        },

    });
}
