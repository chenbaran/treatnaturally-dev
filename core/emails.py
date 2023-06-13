from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

# User Registration Mail
def send_user_registration_mail(user):
    subject = 'Welcome To TreatNaturally!'
    message = f'<h3>Hi {user.first_name}!</h3>'
    message += f'<h4>Welcome to TreatNaturally - Your one-stop-shop for natural & organic health supplements.</h4>'
    message += f'<h4>Your registration has been completed successfully and you may continue shopping on our website.</h4>'
    message += f'<a style="color: white; background-color: #04aa6d; padding: 5px 10px; font-weight: bold;" href="staging.treatnaturally.co.uk">Shop Now</a>'
    message += '<br><br>Thank you for shopping at <a href="https://treatnaturally.co.uk">TreatNaturally!</a>'
    message += '<br><br>Business address goes here'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    html_message = f'<html><body style="font-family: Roboto">{message}</body></html>'
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

def send_contact_form_entry_alert_mail(contactentry):
    subject = f'New Contact Form Entry #{contactentry.id}'
    message = f'<h3>New contact form entry:</h3>'
    message += f'<h4>Name: {contactentry.name}</h4>'
    message += f'<h4>Email: {contactentry.email}</h4>'
    message += f'<h4>Subject: {contactentry.subject}</h4>'
    message += f'<h4>Message: {contactentry.message}</h4>'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['info@treatnaturally.co.uk']
    html_message = f'<html><body style="font-family: Roboto">{message}</body></html>'
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)