# urHotel: Hotel Management System Final Project
## Description
urHotel is a Hotel Management System where administrators have the ability to add hotels and rooms to the database for users to book them based on availability. Users can view hotels from the Rooms page or from each hotel page, search for rooms based on query, check-in date, and check-out date, add their preferred card to their account for future bookings, and cancel their current reservations.
## Static Files
#### styles.css
CSS file for minor styling on top of Bootstrap.
#### index.js
JavaScript file for front-end operations for the index.html file. This file handles fetching rooms using an API call that gets available rooms from the database using search query, check-in date and check-out date. This file also handles the booking modal view.
#### profile.js
JavaScript file for front-end operations for the profile.html file. This file handles adding card modal view, and the logic behind adding and removing credit/debit card using an API call.
## Templates Folder
#### layout.html
HTML file for the overall structure of the website including the navigation bar.
#### login.html and register.html
HTML files for registering and logging in the user.
#### hotels.html
HTML file for displaying the hotels that are present in the database. Here users are able to view rooms from a single hotel using index.html file and can also get directions to the hotel using Google Maps.
#### index.html
HTML file for the initial page where available hotel rooms are displayed. Here users are able to search for rooms based on query, check-in date and check-out date, and book rooms that are available. This file is also used in conjunction with hotels.html to display rooms from a single hotel.
#### profile.html
HTML file for user's profile information. Here users are able to add and credit/debit card, and view and cancel their room reservations.
## Python Files
#### views.py
Python file that includes code for the API and the backend for processing and rendering each page/view of the application.
#### models.py
Python file that includes all the models used to store data in the database.
#### admins.py
Python file that registers all models from model.py file for easy data manipulation from Django's administrator page.
