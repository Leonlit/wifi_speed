//when dark theme is toggled, add the dark theme css file into the page
function add_theme (file, name) {
    var newlink = document.createElement("link");
    newlink.setAttribute("rel", "stylesheet");
    newlink.setAttribute("id", "darkmode");
    newlink.setAttribute("type", "text/css");
    newlink.setAttribute("href", file);
    newlink.setAttribute("name", name);

    document.getElementsByTagName("head")[0].appendChild(newlink);
}

//for animating the toggling and changing the state of the theme
function toggle_theme() {
    const toggle = document.getElementById("themeToggle");
    toggle.style.cssText = "";
    if (!darkMode) {
        add_theme("/css/darkTheme.css", "darkTheme")
        toggle.style.left = "84%";
        toggle.style.backgroundColor = "white";
        darkMode = true;
    }else {
        document.getElementById("darkmode").remove();
        toggle.style.left = "0px";
        toggle.style.backgroundColor = "black";
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
