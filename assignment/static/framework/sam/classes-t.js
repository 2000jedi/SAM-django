/**
 * Created by jedi on 16-12-11.
 */
function manageClass(class_id){
    window.location.href = '/classes/' + class_id.toString();
}

function addStudentPanel(class_id){
    var csrf = getCookie("csrftoken");
    postcall('/classes', {class_id: class_id, csrfmiddlewaretoken: csrf, type: "student"})
}

function updateMembers(class_id){
    var query = {class_id: class_id};
    var csrf = getCookie("csrftoken");
    var forms = $('.check-student');

    for (var i=0; i<forms.length; i++){
        query[forms[i].id] = forms[i].checked;
    }
    query['csrfmiddlewaretoken'] = csrf;
    postcall('/classes/updateStudent', query);
}

function newAssignment(class_id){
    var csrf = getCookie("csrftoken");
    postcall('/classes', {class_id: class_id, csrfmiddlewaretoken: csrf, type: "assignment", assignment_id:-1})
}

function submitAssignment(class_id){

}