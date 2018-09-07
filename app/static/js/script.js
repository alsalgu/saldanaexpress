$(document).ready(function () {

    var current_page = ""
    var page_cat = ""

    if (window.location.pathname != "/") {
        var pathname = window.location.pathname.substring(1);
        pathname = pathname.replace(/\//g, '-');
        current_page = "#" + pathname;
        page_cat = window.location.pathname.split('/')
    } else {
        current_page = "#home";
    }

    $(current_page).addClass('active');
    $("#" + page_cat[1]).addClass('active');
});