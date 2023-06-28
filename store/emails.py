from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse


# Order confirmation mail
def send_order_confirmation_email(order):
    items_table = '<table style="font-family: Arial; border-collapse: collapse; border: 1px solid #ddd; margin-top:10px margin-bottom: 10px;">'
    items_table += '<thead style="color: white; background-color: #04aa6d;"><tr><th style="text-align: left; padding: 8px;">Product</th><th style="text-align: left; padding: 8px;">Quantity</th><th style="text-align: left; padding: 8px;">Final Price</th></tr></thead>'
    items_table += '<tbody>'
    for item in order.items.all():
        items_table += f'<tr><td style="padding: 8px; border: 1px solid #ddd;">{item.product.name}</td><td style="padding: 8px; border: 1px solid #ddd;">{item.quantity}</td><td style="padding: 8px; border: 1px solid #ddd;">${item.final_price_after_discount}</td></tr>'
    items_table += '</tbody></table>'

    subject = 'Your Order Has Been Received!'
    message = f'<h3>Hi {order.billing_address.first_name}!</h3>'
    message += f'<h4>Your order #{order.id} has been received.</h4>'
    message += f'<h4>Order Items:</h4>'
    message += f'{items_table}'
    message += f'<h4>Total: £{order.final_price}</h4>'
    if order.optional_shipping_address:
        message += f'Shipping Address:<br>{order.optional_shipping_address}'
    else:
        message += f'Shipping Address: {order.billing_address}'
    message += '<br><br>Thank you for shopping at <a href="https://treatnaturally.co.uk">TreatNaturally!</a>'
    message += '<br><br>IPURE NUTRITION <br>311 HALE ROAD, HALE BARNS, WA15 8SS'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.billing_address.email]
    html_message = f'<html><body style="font-family: Arial">{message}</body></html>'
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)



def send_order_alert_to_admin(order):
    items_table = '<table style="font-family: Arial; border-collapse: collapse; border: 1px solid #ddd; margin-top:10px margin-bottom: 10px;">'
    items_table += '<thead style="color: white; background-color: #04aa6d"><tr><th style="text-align: left; padding: 8px;">Product</th><th style="text-align: left; padding: 8px;">Quantity</th><th style="text-align: left; padding: 8px;">Final Price</th></tr></thead>'
    items_table += '<tbody>'
    for item in order.items.all():
        items_table += f'<tr><td style="padding: 8px; border: 1px solid #ddd;">{item.product.name}</td><td style="padding: 8px; border: 1px solid #ddd;">{item.quantity}</td><td style="padding: 8px; border: 1px solid #ddd;">${item.final_price_after_discount}</td></tr>'
    items_table += '</tbody></table>'

    subject = f'New Order #{order.id} - treatnaturally.co.uk'
    message = f'<h3>New order from customer {order.billing_address.first_name} {order.billing_address.last_name}!</h3>'
    message += f'<h4>Order #{order.id}</h4>'
    message += f'<h4>Order Items:</h4>'
    message += f'{items_table}'
    message += f'<h4>Total: £{order.final_price}</h4><br><br>'
    if order.optional_shipping_address:
        message += f'Shipping Address:<br>{order.optional_shipping_address}'
    else:
        message += f'Shipping Address:<br>{order.billing_address}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['info@treatnaturally.co.uk']
    html_message = f'<html><body style="font-family: Arial;">{message}</body></html>'
    send_mail(subject, message, from_email, recipient_list, html_message=html_message)