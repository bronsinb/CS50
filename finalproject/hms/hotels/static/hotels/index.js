function populate_rooms(search, start, end){
    fetch("api/rooms", {
        method: "POST",
        body: JSON.stringify({
            start: start,
            end: end,
            hotel: document.getElementById("hotel").innerHTML,
            search: search
        })
    })
    .then(response => response.json())
    .then(rooms => {
        const rooms_area = document.getElementById("roomsarea");
        rooms_area.innerHTML = "";
        console.log(search);
        if(rooms.length == 0){
            const alert = document.createElement('div');
            alert.className = "alert alert-warning";
            alert.role = "alert";
            alert.innerHTML = "No Rooms Available!";

            rooms_area.append(alert);
        }
        rooms.forEach((room) => {
            const card = document.createElement('div');
            card.className = "card room";

            const img = document.createElement('img');
            img.className = "card-img-top image";
            img.src = room.image;
            card.append(img);

            const top_body = document.createElement('div');
            top_body.className = "card-body";

            const title = document.createElement('h5');
            title.className = "card-title";
            title.innerHTML = room.hotel.name;
            top_body.append(title)

            const subtitle = document.createElement('p');
            subtitle.className = "card-subtitle";
            subtitle.style = style="font-size:small;";
            subtitle.innerHTML = room.hotel.address;
            top_body.append(subtitle);

            card.append(top_body);

            const mid_body = document.createElement('ul');
            mid_body.className = "list-group list-group-flush";
            
            const roomtype = document.createElement('li');
            roomtype.className = "list-group-item";

            const type_text = document.createElement('strong');
            type_text.innerHTML = "Type:";

            roomtype.append(type_text);
            roomtype.innerHTML += ` ${room.room_type}`;
            mid_body.append(roomtype);

            const roomnumber = document.createElement('li');
            roomnumber.className = "list-group-item";

            const number_text = document.createElement('strong');
            number_text.innerHTML = "Room Number:";

            roomnumber.append(number_text);
            roomnumber.innerHTML += ` ${room.number}`;
            mid_body.append(roomnumber);

            const roomprice = document.createElement('li');
            roomprice.className = "list-group-item";

            const price_text = document.createElement('strong');
            price_text.innerHTML = `$${room.price}`;

            roomprice.append(price_text);
            roomprice.innerHTML += " per Night";
            mid_body.append(roomprice);

            card.append(mid_body);

            const bottom_body = document.createElement('div');
            bottom_body.className = "card-body text-center";

            const choose = document.createElement('button');
            choose.className = "btn btn-success book";
            choose.dataset.roomid = room.id;
            choose.dataset.hotel = room.hotel.name;
            choose.dataset.address = room.hotel.address;
            choose.dataset.price = room.price;
            choose.dataset.img = room.image;
            choose.dataset.hotelimg = room.hotel.image;
            choose.dataset.number = room.number;
            choose.dataset.roomtype = room.room_type;
            choose.innerHTML = "Choose";

            bottom_body.append(choose);

            card.append(bottom_body);

            rooms_area.append(card);
        });
    })
    .then(() => {
        document.querySelectorAll(".btn.btn-success.book").forEach((element) => {
            element.addEventListener('click', () => {
                document.getElementById("roomid").value = element.dataset.roomid
                document.getElementById("hidden-start").value = document.getElementById("start").value
                document.getElementById("hidden-end").value = document.getElementById("end").value

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

                document.getElementById("startdate").innerHTML = "";
                const checkin = document.createElement('strong');
                checkin.innerHTML = "Check In: ";
                document.getElementById("startdate").append(checkin);
                document.getElementById("startdate").innerHTML += document.getElementById("start").value;

                document.getElementById("enddate").innerHTML = "";
                const checkout = document.createElement('strong');
                checkout.innerHTML = "Check Out: ";
                document.getElementById("enddate").append(checkout);
                document.getElementById("enddate").innerHTML += document.getElementById("end").value;
    
                document.getElementById("room-img").src = element.dataset.img;
                document.getElementById("hotel-img").src = element.dataset.hotelimg;
            });
        });
    })
}


document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const nextday = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);
    
    document.getElementById("start").min = today.toISOString().split("T")[0];
    document.getElementById("start").value = today.toISOString().split("T")[0];
    
    document.getElementById("end").min = nextday.toISOString().split("T")[0];
    document.getElementById("end").value = nextday.toISOString().split("T")[0];

    populate_rooms(null, today.toISOString().split("T")[0], nextday.toISOString().split("T")[0]);

    document.getElementById("book").style.display = 'none';

    document.querySelector(".btn.btn-outline-success.search").addEventListener("click", () => {
        search = document.getElementById("search").value;
        start = document.getElementById("start").value;
        end = document.getElementById("end").value;
        populate_rooms(search, start, end);
    });

    document.getElementById("close").addEventListener('click', () => {
        document.getElementById("book").style.display = 'none';
    });
});