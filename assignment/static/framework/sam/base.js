/**
 * Created by 2000jedi on 2016/12/9.
 */
function postcall(url,params){
    var tempform = document.createElement("form");
    tempform.action = url;
    tempform.method = "post";
    tempform.style.display="none";
    var opt;
    for (var x in params) {
        opt = document.createElement("input");
        opt.name = x;
        opt.setAttribute("value",params[x]);
        tempform.appendChild(opt);
    }

    opt = document.createElement("input");
    opt.type = "submit";
    opt.name = "postsubmit";
    tempform.appendChild(opt);
    document.body.appendChild(tempform);
    tempform.submit();
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=")
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1
            c_end = document.cookie.indexOf(";", c_start)
            if (c_end == -1) c_end = document.cookie.length
            return unescape(document.cookie.substring(c_start, c_end))
        }
    }
    return ""
}

var flag_showApps = false;
function showApps() {
    flag_showApps = !flag_showApps;
    if (flag_showApps) {
        $('#apps-menu-detail').css('display', 'block');
    }
    else {
        $('#apps-menu-detail').css('display', 'none');
    }
}
function showModule(id) {
    window.location.href = "/" + id;
}