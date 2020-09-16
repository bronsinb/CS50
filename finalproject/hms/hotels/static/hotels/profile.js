function add(){
    
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("addcardmodal").style.display = 'none';

    document.getElementById("close").addEventListener('click', () => {
        document.getElementById("addcardmodal").style.display = 'none';
    });

    if(document.getElementById("addcard") != null){
        document.getElementById("addcard").addEventListener('click', () => {
            document.getElementById("addcardmodal").style.display = 'block';
        });
        
        document.querySelector(".btn.btn-success.addcard").addEventListener('click', () => {
            fetch("card", {
                method: "PUT",
                body: JSON.stringify({
                    name: document.getElementById("name").value,
                    cardnum: document.getElementById("cardnum").value,
                    cvv: document.getElementById("cvv").value,
                    expire: document.getElementById("expire").value
                })
            })
            .then(response => {
                console.log("add");
                const num = document.createElement('label');
                num.className = "col-form-label col-auto";

                const strong = document.createElement('strong');
                strong.innerHTML = "Card: ";

                num.append(strong);
                num.innerHTML += "************" + document.getElementById("cardnum").value.substring(12);

                document.getElementById("top").innerHTML = "";

                const remove = document.createElement('button');
                remove.type = "button";
                remove.className = "btn btn-danger";
                remove.id = "removecard";
                remove.innerHTML = "Remove Card";

                document.getElementById("top").append(num);
                document.getElementById("top").append(remove);

                location.reload();
            })
        });
    } else {
        document.getElementById("removecard").addEventListener('click', () => {
            fetch("card", {
                method: "PUT"
            })
            .then(response => {
                console.log("removed")

                document.getElementById("top").innerHTML = "";

                const add = document.createElement('button');
                add.type = "button";
                add.className = "btn btn-success";
                add.id = "removecard";
                add.innerHTML = "Add Card";

                document.getElementById("top").append(add);

                location.reload();
            })
        });
    }
});