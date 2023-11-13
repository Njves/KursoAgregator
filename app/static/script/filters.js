document.addEventListener('DOMContentLoaded', function () {
    var toggleForms = document.querySelectorAll('.img_button');

    toggleForms.forEach(function (toggleForm) {
        toggleForm.addEventListener('click', function () {
            var index = toggleForm.getAttribute('data-index');
            var container = document.querySelector('.filter-container[data-index="' + index + '"]');

            container.style.display = (container.style.display === 'none' || container.style.display === '') ? 'block' : 'none';

            toggleForm.src = container.style.display === 'none' ?
                "/static/icon/chevron-up.svg" :
                "/static/icon/chevron-down.svg";
        });
    });
});
