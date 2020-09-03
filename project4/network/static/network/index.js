document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#new-post').style.display = 'none';

    function hide_post_area(){
        document.querySelector('#new-post').style.display = 'none';
        document.querySelector('#new-post-button').innerHTML = "New Post";
        document.querySelector('#new-post-button').className = "btn btn-primary";
        document.querySelector('#new-post').children[0].children[0].children[1].innerHTML = "New Post"
        document.querySelector('#new-post-textarea').value = '';
        document.querySelector('#counter').innerHTML = `0/280`;
    }

    if(document.getElementById('new-post-button') != null){
        document.querySelector('#new-post-button').addEventListener('click', () => {
            const hidden_element = document.createElement('input');
            hidden_element.name = 'posttype';
            hidden_element.type = 'hidden';
            hidden_element.value = 'post';
            document.querySelector('#new-post').children[0].children[0].append(hidden_element);
            if(document.querySelector('#new-post').style.display === 'none'){
                document.querySelector('#new-post').style.display = 'block';
                document.querySelector('#new-post-button').innerHTML = "Close";
                document.querySelector('#new-post-button').className = "btn btn-danger";
            } else {
                hide_post_area();
            }
        });
    }

    if(document.getElementById('follow') != null){
        document.getElementById('follow').addEventListener('click', () => {
            const element = document.getElementById('follow');
            fetch(`/follow/${element.dataset.userid}`)
            .then(response => response.json())
            .then(json => {
                if(json["follow"]){
                    element.innerHTML = "Unfollow";  
                    element.className = "btn btn-danger";
                } else {
                    element.innerHTML = "Follow";  
                    element.className = "btn btn-outline-success";
                }
                document.getElementById('followers').innerHTML = `${json['amount']} Followers`;
            })
        });
    }

    document.querySelectorAll('.btn.edit').forEach((element) => element.addEventListener('click', () => {
        const hidden_element = document.createElement('input');
        hidden_element.name = 'posttype';
        hidden_element.type = 'hidden';
        hidden_element.value = element.dataset.postid;
        document.querySelector('#new-post').children[0].children[0].append(hidden_element);
        document.querySelector('#new-post').children[0].children[0].children[1].innerHTML = "Edit Post"
        document.querySelector('#new-post').style.display = 'block';
        document.querySelector('#new-post-button').innerHTML = "Close";
        document.querySelector('#new-post-button').className = "btn btn-danger";
        document.querySelector('#new-post-textarea').value = element.dataset.post;
        document.querySelector(".btn.btn-primary.post").innerHTML = "Save";
        document.querySelector("#new-post-form").addEventListener('submit', (event) => edit_post(event, element));
        document.querySelector('#counter').innerHTML = `${document.querySelector('#new-post-textarea').value.length}/280`;
    }));

    function edit_post(event, element){
        event.preventDefault();
        fetch(`edit/${element.dataset.postid}`, {
            method: 'PUT',
            body: JSON.stringify({
                edited: document.querySelector("#new-post-form").children[2].value
            })
        }).then((response) => {
            element.parentElement.children[3].innerHTML = document.querySelector("#new-post-form").children[2].value;
            document.querySelector("#new-post-form").removeEventListener('submit', (event) => edit_post(event, element));
            hide_post_area();
        })
    }

    document.querySelector('#new-post-textarea').addEventListener("keyup", () => {
        var count = document.querySelector('#new-post-textarea').value.length;
        if(count > 280){
            document.querySelector('#new-post-textarea').value = document.querySelector('#new-post-textarea').value.substring(0, 280);
            count = 280;
        }
        document.querySelector('#counter').innerHTML = `${count}/280`;
    });

    document.querySelectorAll('.btn.like').forEach((element) => element.addEventListener('click', () => {
        fetch(`/like/${element.dataset.postid}`)
        .then(response => response.json())
        .then(json => {
            if(json["like"]){
                element.children[0].style.color = "red";  
            } else {
                element.children[0].style.color = "black";  
            }
            const tmp = element.children[0];
            element.innerHTML = "";
            element.append(tmp)
            element.append(` ${json["amount"]}`)
        })
    }));
});