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
        set_theme_session();
    }else {
        document.getElementById("darkmode").remove();
        toggle.style.left = "0px";
        toggle.style.backgroundColor = "black";
        darkMode = false;
        remove_theme_session();
    }
    update_chart_theme();
}

function close_nav () {
    const nav = document.getElementsByTagName("nav")[0];
    nav.style.top = `-100%`;
    console.log(nav.style.top);
}

function open_nav () {
    const nav = document.getElementsByTagName("nav")[0];
    nav.style.top = "0";
}

function set_up_table_list (data, ip_addr) {
    const selection = document.getElementById("ip_filter");
    data.forEach(name => {
        newOption = document.createElement("option");
        console.log(name, ip_addr);
        if (name == ip_addr) {
            newOption.selected = true;
        }
        name = get_back_ip_addr(name);
        newOption.setAttribute("value", name);
        newOption.innerText = name;
        selection.appendChild(newOption);
    });
}

function get_back_ip_addr(ip) {
    return ip.replaceAll("_", ".")
}