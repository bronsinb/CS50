document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#new-post').style.display = 'none';

    document.querySelector('#new-post-button').addEventListener('click', () => {
        if(document.querySelector('#new-post').style.display === 'none'){
            document.querySelector('#new-post').style.display = 'block';
            document.querySelector('#new-post-button').innerHTML = "Close";
            document.querySelector('#new-post-button').className = "btn btn-danger";
        } else {
            document.querySelector('#new-post').style.display = 'none';
            document.querySelector('#new-post-button').innerHTML = "New Post";
            document.querySelector('#new-post-button').className = "btn btn-primary";
        }
    });

    document.querySelector('#new-post-textarea').addEventListener("keyup", () => {
        var count = document.querySelector('#new-post-textarea').value.length;
        if(count > 280){
            document.querySelector('#new-post-textarea').value = document.querySelector('#new-post-textarea').value.substring(0, 280);
            count = 280;
        }
        document.querySelector('#counter').innerHTML = `${count}/280`;
    });
});