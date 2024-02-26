document.addEventListener('DOMContentLoaded', function() {
    var themeToggle = document.getElementById('theme-toggle');
    var body = document.body;
    var savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
    }
    if (savedTheme === 'dark-theme') {
        themeToggle.src = "/static/icon/sun.svg";
    } else {
        themeToggle.src = "/static/icon/moon.svg";
    }
    themeToggle.addEventListener('click', function() {
        var isDarkTheme = body.classList.contains('dark-theme');
        if (isDarkTheme) {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
            localStorage.setItem('theme', 'light-theme');
            themeToggle.src = "/static/icon/moon.svg";
        } else { 
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark-theme');
            themeToggle.src = "/static/icon/sun.svg";
        }
    });
});