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
  });

  // Click listener
  document.addEventListener('click', event => {
      const element = event.target;
      if (element.className === "btn archive") {
        element.parentElement.style.animationPlayState = 'running';
        element.parentElement.addEventListener('animationend', () =>  {
            element.parentElement.remove();
            console.log(element.dataset.archive);
            if (element.dataset.archive == "true"){
              archive_mail(element.dataset.id, false);
            } else {
              archive_mail(element.dataset.id, true)
            }
        });
      }
  });
}

function archive_mail(email_num, action){
  console.log(action);
  fetch(`/emails/${email_num}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: action
    })
  });
}

function add_email_element(email, mailbox){
  // Create new email element
  const email_element = document.createElement('div');
  email_element.className = 'email row';
  email_element.onclick = () => {
    load_email(email);
  };
  var html = '';
  if(mailbox !== 'sent'){
    html = `<button data-mailbox="${mailbox}" data-archive="${email.archived}" data-id="${email.id}" class="btn archive">`;
    if (email.archived){
      html += `<i class="fa fa-remove"></i></button> `;
    } else {
      html += `<i class="fa fa-archive"></i></button> `;
    }
  }
  html += `<div class="col vertical-center">`
  if (email.read){
    html += `<h5>${email.subject}</h5>`;
  } else {
    html += `<h5><strong>${email.subject}</strong></h5>`;
  }

  html += `<div>${email.sender}</div></div><div class="vertical-center">${email.timestamp}</div>`;
  

  email_element.innerHTML = html;

  // Append It
  document.querySelector('#emails-view').append(email_element);
}

function load_email(email){
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
  html = html.substring(0, html.length - 2) + `</h6><hr/>`;
  html += `<p class="card-text">${email.body}</p>`;
  html += `<button class="card-link reply" data-sender="${email.sender}" data-timestamp="${email.timestamp}" data-subject="${email.subject}" data-body="${email.body}">Reply</button>`;
  original_email.innerHTML = html;
  email_element.append(original_email);

  // Click listener
  document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === "card-link reply") {
      compose_email();
      console.log(element.dataset.email);

      document.querySelector('#compose-recipients').value = element.dataset.sender;
      document.querySelector('#compose-subject').value = `Re: ${element.dataset.subject}`;
      document.querySelector('#compose-body').value = `On ${element.dataset.timestamp} ${element.dataset.sender} wrote: ${element.dataset.body} \n.\n.\n.\n`;
    }
  });

  email_view.append(email_element);
}