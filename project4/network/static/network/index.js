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
});