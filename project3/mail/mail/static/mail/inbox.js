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
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Enable Fields disabled by reply
  document.querySelector('#compose-recipients').disabled = false;
  document.querySelector('#compose-subject').disabled = false;

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

      load_mailbox('sent')
  });
}

function load_mailbox(mailbox) {
  // Clear it
  document.querySelector('#emails-view').innerHTML = '';

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      //Display Emails
      emails.forEach(email => add_email_element(email, mailbox));

      if(emails.length == 0){
        add_empty_message(mailbox);
      }
  });
}

function archive_mail(email){
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !email.archived
    })
  }).then((response) => load_mailbox('inbox'));
}

function add_email_element(email, mailbox){
  // Create new email element
  const email_element = document.createElement('div');
  email_element.className = 'email row';

  if (email.read){
    email_element.style.backgroundColor = "lightgray";
  }

  if(mailbox !== 'sent'){
    const button_element = document.createElement('button');
    button_element.className = "col-auto btn archive";

    if (email.archived){
      button_element.innerHTML  = `<i class="fa fa-remove"></i>`;
    } else {
      button_element.innerHTML = `<i class="fa fa-archive"></i>`;
    }

    button_element.addEventListener("click", function() {
      const element = email_element.children[0];
      element.parentElement.style.animationPlayState = 'running';
      element.parentElement.addEventListener('animationend', () =>  {
          archive_mail(email);
      });  
    });

    email_element.append(button_element);
  }

  // Create new email element
  const text_element = document.createElement('div');
  text_element.className = 'col-lg row';

  text_element.innerHTML = `<div class="col vertical-center"><h5>${email.subject}</h5><div>${email.sender}</div></div><div class="vertical-center">${email.timestamp}</div>`;

  text_element.addEventListener('click', () => load_email(email, mailbox));
  email_element.append(text_element);

  // Append It
  document.querySelector('#emails-view').append(email_element);
}

function load_email(email, mailbox){
  

  // Show the email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  const email_view = document.querySelector('#email-view');
  email_view.innerHTML = '';
  
  const email_element = document.createElement('div');
  email_element.className = "card";

  const original_email = document.createElement('div');
  original_email.className = "card-body";

  var html =`<h4 class="card-title">${email.subject}</h4><h6 class="card-subtitle mb-2">${email.sender}</h6><h6 class="card-subtitle mb-2 text-muted">To: `;
  email.recipients.forEach(recipient => html += `${recipient}, `);
  html = html.substring(0, html.length - 2) + `</h6>`;
  html += `<h6 style="font-size: 12px;" class="card-subtitle mb-2 text-muted">${email.timestamp}</h6><hr/>`;
  html += `<p class="card-text">${email.body.split("\n").join("<br>")}</p>`;
  html += `<button class="btn btn-link reply">Reply</button>`;
  if(mailbox !== "sent"){
    html += `<button class="btn btn-link archive">`;
    if(email.archived){
      html += `Unarchive</button>`;
    } else {
      html += `Archive</button>`;
    }
  }

  original_email.innerHTML = html;
  email_element.append(original_email);

  email_view.append(email_element);

  // Click listener
  document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === "btn btn-link reply") {
      compose_email();

      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-recipients').disabled = true;
      if(email.subject.includes("Re: ")){
        document.querySelector('#compose-subject').value = `${email.subject}`;
      } else {
        document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
      }
      document.querySelector('#compose-subject').disabled = true;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n ${email.body} \n.\n.\n.\n`;
    }

    if (element.className === "btn btn-link archive"){
      archive_mail(email);
    }
  });
}

function add_empty_message(mailbox){
  const alert_element = document.createElement('div');
  alert_element.className = "alert alert-dark";
  alert_element.role = "alert";

  alert_element.innerHTML = `${mailbox.toUpperCase()} is Empty!`;

  document.querySelector('#emails-view').append(alert_element);
}