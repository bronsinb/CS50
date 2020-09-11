document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("book").style.display = 'none';

    document.getElementById("close").addEventListener('click', () => {
        document.getElementById("book").style.display = 'none';
    });

    document.querySelectorAll(".btn.btn-success.book").forEach((element) => {
        element.addEventListener('click', () => {
            document.getElementById("book").style.display = 'block';
        });
    });
});