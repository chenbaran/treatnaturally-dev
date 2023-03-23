from django.core.mail import send_mail
from django.conf import settings


# Order confirmation mail
def send_order_confirmation_email(order):
    subject = 'Your Order Has Been Recieved!'
    message = f'Hi {order.billing_address.first_name}!\n\n'
    message += f'Your order #{order.id} has been received.\n\n'
    message += f'Order Items:\n\n'
    for item in order.items.all():
        message += f'{item.orderitems.name} - Quantity: {item.orderitems.quantity}\n'
    message += f'Total: ${order.final_price}\n'
    if order.optional_shipping_address:    
        message += f'Shipping Address: {order.optional_shipping_address}\n'
    else:
        message += f'Shipping Address: {order.billing_address}'
    message += '\nThank you for your order!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.billing_address.email]
    send_mail(subject, message, from_email, recipient_list)


def send_order_alert_to_admin(order):
    subject = f'New Order #{order.id} - Treatnaturally'
    message = f'Your order #{order.id} has been received.\n\n'
    message += f'Total: ${order.final_price}\n'
    if order.optional_shipping_address:    
        message += f'Shipping Address: {order.optional_shipping_address}\n'
    else:
        message += f'Shipping Address: {order.billing_address}'
    message += '\nThank you for your order!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ['info@treatnaturally.co.uk']
    send_mail(subject, message, from_email, recipient_list)