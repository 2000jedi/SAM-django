/**
 * Created by 2000jedi on 2016/12/9.
 */
function updatePercentage(perc) { // draw assignment percentage circle
    perc = parseFloat(perc);
    em = Number(getComputedStyle(document.body, null).fontSize.replace(/[^\d]/g, ''));

    var canvas = document.getElementById("percentage");
    var ctx = canvas.getContext("2d");
    var text = parseInt(perc * 100) + '%';

    canvas.width = 40 * em;
    canvas.height = 40 * em;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.lineWidth = 25;

    if (perc == 1.0) {
        ctx.beginPath();
        ctx.arc(20 * em, 20 * em, 12 * em, 0, 2 * Math.PI);
        ctx.strokeStyle = 'rgba(81,157,217,1)';
        ctx.stroke();
    }

    if (perc == 0.0) {
        ctx.beginPath();
        ctx.arc(20 * em, 20 * em, 12 * em, 0, 2 * Math.PI);
        ctx.strokeStyle = 'rgba(240,124,120,1)';
        ctx.stroke();
    }

    if ((perc < 1) && (perc > 0)) {
        ctx.beginPath();
        ctx.arc(20 * em, 20 * em, 12 * em, (1.0125 - perc) * 2 * Math.PI, 2 * Math.PI - 0.075);
        ctx.strokeStyle = 'rgba(81,157,217,1)';
        ctx.stroke();

        ctx.beginPath();
        ctx.strokeStyle = 'rgba(240,124,120,1)';
        ctx.arc(20 * em, 20 * em, 12 * em, -0.9875 * 2 * Math.PI, -(perc + 0.0125) * 2 * Math.PI);
        ctx.stroke();
    }

    ctx.font = 8 * em + "px Arial";
    ctx.fillStyle = 'rgba(133,189,234,1)';
    ctx.fillText(text, (canvas.width - text.length*em*4)/2 - 25, (canvas.height + 4*em)/2);
}

function markComplete(assignment_id){
    var csrf = getCookie("csrftoken");
    postcall("/dashboard/mark_as_complete", {assignment_id: assignment_id, csrfmiddlewaretoken: csrf});
}

function markUnComplete(assignment_id){
    var csrf = getCookie("csrftoken");
    postcall("/dashboard/mark_as_uncomplete", {assignment_id: assignment_id, csrfmiddlewaretoken: csrf});
}