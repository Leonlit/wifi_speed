function add_theme (file, name) {
    var newlink = document.createElement("link");
    newlink.setAttribute("rel", "stylesheet");
    newlink.setAttribute("id", "darkmode");
    newlink.setAttribute("type", "text/css");
    newlink.setAttribute("href", file);
    newlink.setAttribute("name", name);

    document.getElementsByTagName("head")[0].appendChild(newlink);
}

function toggle_theme() {
    if (!darkMode) {
        addCSSFile("/css/", "darkTheme")
        darkMode = true;
    }else {
        document.getElementById("darkmode").remove();
        darkMode = false;
    }
    update_chart_theme();
}

function close_nav () {
    const nav = document.getElementsByTagName("nav")[0];
    nav.style.top = "-60%";
}

function open_nav () {
    const nav = document.getElementsByTagName("nav")[0];
    nav.style.top = "0";
}