function get_theme_by_session () {
    const isDarkTheme = get_theme_session();
    if (isDarkTheme !== null) {
        toggle_theme();
    }
}

function get_theme_session () {
    return localStorage.getItem("dark_theme");
}

function remove_theme_session () {
    localStorage.clear();
}

function set_theme_session () {
    localStorage.setItem("dark_theme", "true");
}