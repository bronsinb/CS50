document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Get Compose Form
  const compose_form = document.querySelector("#compose-form");

  // Add Submit listener
  compose_form.addEventListener('submit', send_email);
}

function send_email(event) {
  event.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      //Display Emails
      emails.forEach(add_email_element);
  });

  // If hide button is clicked, delete the post
  document.addEventListener('click', event => {
      const element = event.target;
      if (element.className === "btn btn-secondary archive") {
          element.parentElement.style.animationPlayState = 'running';
          element.parentElement.addEventListener('animationend', () =>  {
              element.parentElement.remove();
              archive_mail(element.dataset.id)
          });
      }
  });
}
function archive_mail(email_num){
  fetch(`/emails/${email_num}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
}

function add_email_element(email){
  // Create new email element
  const email_element = document.createElement('div');
  email_element.className = 'email';
  email_element.innerHTML = `<button data-id="${email.id}" class="btn btn-secondary archive"><i class="fa fa-archive"></i></button> ${email.sender} ${email.subject}`;

  // Append It
  document.querySelector('#emails-view').append(email_element);
}