document.addEventListener("DOMContentLoaded", function () {
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const button = form.querySelector('button[type="submit"], button:not(.btn-close)');
            if (button && form.checkValidity()) {
                button.disabled = true;
                if (!button.dataset.originalText) {
                    button.dataset.originalText = button.innerText;
                }
                button.innerText = "Processing...";
            }
        });
    });
});
