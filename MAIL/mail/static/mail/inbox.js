document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // when click the submit button, send a post request to server
  document.querySelector('#compose-form').addEventListener('submit', function(event) {
    event.preventDefault();
    fetch('/emails',{
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      alert(result.message);
      load_mailbox('sent');
    })
    .catch(error => {
      alert(error.message);
    });
  });

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}


function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  //when user visits inbox, sent, archive, to display emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach( email => {
      const element = document.createElement('div');
      let email_id = email.id;
      element.innerHTML = `<strong>From: </strong> ${email.sender}
                            <strong>Subject: </strong> ${email.subject}
                            <strong>TimeStamp: </strong> ${email.timestamp}`;
      element.className = 'emails' // to add css for all emails 
       // if email is read, background gray; if unread, background is white
      if (email.read){element.style.backgroundColor = 'rgba(128,128,128,0.3'}
      else{element.style.backgroundColor = 'white'}   
      document.querySelector('#emails-view').append(element);

      // for each email, add eventlistener of click to view email
      element.addEventListener('click', function() {
        fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then( email => {
          const view_email = document.createElement('div');
          view_email.innerHTML = `
                            <strong>From: </strong> ${email.recipients}
                            <strong>Subject: </strong> ${email.subject}
                            <strong>TimeStamp: </strong> ${email.timestamp}
                            <strong>Body: </strong> ${email.body}
                            `;
          view_email.className = 'single_email';
          document.querySelector('#single-email-view').innerHTML = '';
          document.querySelector('#single-email-view').append(view_email);
          document.querySelector('#single-email-view').style.display = 'block';
          document.querySelector('#emails-view').style.display = 'none';

        // when view the inbox email, add a archive button
        let archive = document.createElement('button');
        archive.className = 'btn btn-sm btn-outline-primary';
        archive.innerHTML = email.archived ? 'Unarchive':'Archive';
        document.querySelector('#single-email-view').append(archive);
        archive.addEventListener('click', () => {
          fetch(`/emails/${email_id}`, {
            method:'PUT',
            body: JSON.stringify({archived: !email.archived})
          })
          // load user's inbox after archived/unarchived email
          .then( () => load_mailbox('inbox'));
        }); //ends event Listener arvhive button

        // when view an email add a reply button
        let reply = document.createElement('button');
        reply.className = 'btn btn-sm btn-outline-primary';
        reply.innerHTML = 'Reply';
        document.querySelector('#single-email-view').append(reply);
        reply.addEventListener('click', () => {
          compose_email();
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = email.subject.startsWith('Re:') ? email.subject : `Re: ${email.subject}`; 
          document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}`;
        }); //ends event Listener for click reply button
        });
        // mark the email as read once it is clicked and viewed
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({read: true})
        }) 
        // end fetch 
      });
      // ends eventlistener for view email   
    });
  });
}


