document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("book").style.display = 'none';

    document.getElementById("close").addEventListener('click', () => {
        document.getElementById("book").style.display = 'none';
    });

    const today = (new Date());
    
    document.getElementById("start").min = today.toISOString().split("T")[0];
    document.getElementById("start").value = today.toISOString().split("T")[0];

    today.setDate(today.getDate() + 1);
    document.getElementById("end").min = today.toISOString().split("T")[0];
    document.getElementById("end").value = today.toISOString().split("T")[0];

    document.querySelectorAll(".btn.btn-success.book").forEach((element) => {
        element.addEventListener('click', () => {
            document.getElementById("book").style.display = 'block';
            document.getElementById("hotel-name").innerHTML = element.dataset.hotel;
            document.getElementById("hotel-address").innerHTML = element.dataset.address;
            
            document.getElementById("room-type").innerHTML = "";
            const roomtype = document.createElement('strong');
            roomtype.innerHTML = "Type: ";
            document.getElementById("room-type").append(roomtype);
            document.getElementById("room-type").innerHTML += element.dataset.roomtype;
            
            document.getElementById("room-number").innerHTML = "";
            const number = document.createElement('strong');
            number.innerHTML = "Room Number: ";
            document.getElementById("room-number").append(number);
            document.getElementById("room-number").innerHTML += element.dataset.number;

            document.getElementById("room-price").innerHTML = "";
            const price = document.createElement('strong');
            price.innerHTML = `$${element.dataset.price}`;
            document.getElementById("room-price").append(price);
            document.getElementById("room-price").innerHTML += " per Night";

            document.getElementById("room-img").src = element.dataset.img;
            document.getElementById("hotel-img").src = element.dataset.hotelimg;
        });
    });
});