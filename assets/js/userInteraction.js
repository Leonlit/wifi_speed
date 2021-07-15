function add_theme (file, name) {
    var newlink = document.createElement("link");
    newlink.setAttribute("rel", "stylesheet");
    newlink.setAttribute("type", "text/css");
    newlink.setAttribute("href", file);
    newlink.setAttribute("name", name);

    document.getElementsByTagName("head")[0].appendChild(newlink);
}

let defaultTheme = true;
function toggle_theme() {
    if (!defaultTheme) {
        addCSSFile("/css/", "darkTheme")
    }
}