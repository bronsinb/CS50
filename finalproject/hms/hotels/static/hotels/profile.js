document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("addcardmodal").style.display = 'none';

    document.getElementById("close").addEventListener('click', () => {
        document.getElementById("addcardmodal").style.display = 'none';
    });

    document.getElementById("addcard").addEventListener('click', () => {
        document.getElementById("addcardmodal").style.display = 'block';
    });
});