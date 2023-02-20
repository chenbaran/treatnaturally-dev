from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from store.models import BillingAddress, Customer, OptionalShippingAddress

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    if kwargs['created']:
      Customer.objects.create(user=kwargs['instance'])


@receiver(post_save, sender=BillingAddress)
def update_customer_billing_address(sender, instance, created, **kwargs):
    if created:
        instance.customer.billing_address_id = instance.id
        instance.customer.save()


@receiver(post_delete, sender=BillingAddress)
def delete_customer_billing_address(sender, instance, **kwargs):
    instance.customer.billing_address_id = None
    instance.customer.save()



@receiver(post_save, sender=OptionalShippingAddress)
def update_customer_optional_shipping_address(sender, instance, created, **kwargs):
    if created:
        instance.customer.optional_shipping_address_id = instance.id
        instance.customer.save()


@receiver(post_delete, sender=OptionalShippingAddress)
def delete_customer_optional_shipping_address(sender, instance, **kwargs):
    instance.customer.optional_shipping_address_id = None
    instance.customer.save()