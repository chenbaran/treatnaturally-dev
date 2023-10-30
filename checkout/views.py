from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from treatnaturallystore.settings.prod import webhook_secret
import stripe
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Customer, Membership
from core.models import User

class CreateCheckoutSession(APIView):
    def post(self, request):
        dataDict = dict(request.data)
        product_name = dataDict['product_name']
        print(dataDict['metadata'])
        metadata = dataDict['metadata']

        if 'sub' in dataDict:
          lookup_key = dataDict['lookup_key']

          try:
            prices = stripe.Price.list(
                lookup_keys=[lookup_key],
                expand=['data.product']
            )

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': prices.data[0].id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url='http://localhost:3000/Home?payment=success#isRegistered/',
                cancel_url='https://treatnaturally.co.uk',
                metadata={'username': metadata}
            )
            # Extract the subscription ID and customer ID from the created session
            sub_id = checkout_session.subscription
            customer_id = checkout_session.customer

            # Return both subscription ID and customer ID in the response
            return JsonResponse({"session_id": checkout_session.id, "success": True, "subscription_id": sub_id, "customer_id": customer_id})
          

          except Exception as e:
              print(e)
              return Response({"error": str(e)}, status=400)

        else:
          print(dataDict)
          price = dataDict['price']
          reg = dataDict['freeRegister']
          try:
                checkout_session = stripe.checkout.Session.create(
                    line_items=[{
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': product_name,
                            },
                            'unit_amount': price
                        },
                        'quantity': 1
                    }],
                    mode='payment',
                    success_url= f"http://localhost:3000/checkout?payment=success#ischecked&{reg}",
                    cancel_url='https://treatnaturally.co.uk/',
                )

                return Response({'session_id': checkout_session.id})

          except Exception as e:
                print(e)
                return Response({"error": str(e)}, status=400)
        

class CreatePortalSession(APIView):
    def post(self,request):
      try:
          customer_id = request.data.get('customer_id')
          if not customer_id:
              return JsonResponse({"error": "Customer ID is required."}, status=400)
          
          portal_session = stripe.billing_portal.Session.create(
              customer=customer_id,
              return_url="http://localhost:3000/my-account?isUpdated" # Modify this according to where you want to return the user after they exit the portal.
          )

          return JsonResponse({"url": portal_session.url})

      except Exception as e:
          return JsonResponse({"error": str(e)}, status=400)


class WebHook(APIView):
    def post(self, request):
        event = None
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, webhook_secret
            )
        except ValueError as err:
            # Invalid payload
            raise err
        except stripe.error.SignatureVerificationError as err:
            # Invalid signature
            raise err

        if event.type == 'checkout.session.completed':
            stripe_customer_id = event.data.object.customer
            try:
                stripe.Customer.modify(
                    stripe_customer_id,
                    metadata={
                        'username': event.data.object.metadata.username
                    }
                )
            except Exception as e:
                # If there's an error updating the customer in Stripe, return a 400 so Stripe retries the webhook
                return JsonResponse({"error": f"Failed to update Stripe customer. Error: {str(e)}. Will retry."}, status=400)
            
            # Try to fetch the user based on the metadata provided
            try:
                user = User.objects.get(username=event.data.object.metadata.username)
            except User.DoesNotExist:
                # If user not found, return a 400 so Stripe retries the webhook
                return JsonResponse({"error": "User not found. Will retry."}, status=400)

            # If user is found, then try fetching the customer and updating
            try:
                customer = Customer.objects.get(user=user)
                customer.stripe_customer_id = stripe_customer_id
                customer.save()
            except Customer.DoesNotExist:
                # If customer not found, return a 400 so Stripe retries the webhook
                return JsonResponse({"error": "Customer not found. Will retry."}, status=400)

        elif event.type == 'customer.subscription.created':
            stripe_customer_id = event.data.object.customer
            stripe_customer = stripe.Customer.retrieve(stripe_customer_id) 
            username = stripe_customer.metadata.username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # If user not found, return a 400 so Stripe retries the webhook
                return JsonResponse({"error": "User not found. Will retry."}, status=400)
            customer = Customer.objects.get(user=user)

            try:
                lookup_key = event['data']['object']['items']['data'][0]['price']['lookup_key']
                membership_label = lookup_key.capitalize()
                customer_membership = Membership.objects.get(label=membership_label)
                customer.membership = customer_membership
                customer.save()
            except Customer.DoesNotExist:
                return JsonResponse({"error": "Customer not found. Will retry."}, status=400)

        elif event.type == 'customer.subscription.updated':
            stripe_customer_id = event.data.object.customer
            stripe_customer = stripe.Customer.retrieve(stripe_customer_id) 
            username = stripe_customer.metadata.username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # If user not found, return a 400 so Stripe retries the webhook
                return JsonResponse({"error": "User not found. Will retry."}, status=400)
            customer = Customer.objects.get(user=user)

            try:
                lookup_key = event['data']['object']['items']['data'][0]['price']['lookup_key']
                membership_label = lookup_key.capitalize()
                customer_membership = Membership.objects.get(label=membership_label)
                customer.membership = customer_membership
                customer.save()
            except Customer.DoesNotExist:
                return JsonResponse({"error": "Customer not found. Will retry."}, status=400)

        elif event.type == 'customer.subscription.deleted':
            stripe_customer_id = event.data.object.customer
            stripe_customer = stripe.Customer.retrieve(stripe_customer_id) 
            username = stripe_customer.metadata.username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # If user not found, return a 400 so Stripe retries the webhook
                return JsonResponse({"error": "User not found. Will retry."}, status=400)
            customer = Customer.objects.get(user=user)
            try:
                membership = Membership.objects.get(label='Free')
                customer.membership = membership
                customer.save()
            except e:
                return JsonResponse({"error": e}, status=400)
        

        else:
            print('Unhandled event type {}'.format(event.type))

        return JsonResponse({"success": True}, safe=False)