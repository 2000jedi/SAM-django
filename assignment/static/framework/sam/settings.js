/* Settings Module */
function changePassword(){
    var oldPass = $('#oldPass').val();
    var newPass1 = $('#newPass1').val();
    var newPass2 = $('#newPass2').val();
    var csrf = getCookie('csrftoken');

    if (newPass1 != newPass2){
        alert("Two passwords do not match.");
    }else if (newPass1.length < 6){
        alert("The new password is too short.");
    }else{
        postcall("/settings/password", {oldPass: oldPass, newPass: newPass1, csrfmiddlewaretoken: csrf});
    }
}
function changeEmail(){
    function validateEmail(email){
        var re = /\S+@\S+\.\S+/;
        return re.test(email);
    }
    var email = $('#newEmail').val();
    if (!validateEmail(email)){
        alert("Not a valid email.");
    }else{
        var csrf = getCookie('csrftoken');
        postcall("/settings/email",{email: email, csrfmiddlewaretoken: csrf});
    }
}
