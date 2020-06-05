import re
import random
from dfh.models import *
from dfh.serializers import *
from rest_framework import status
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# for custom mails use: '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$' 
p = 23
g = 5


class GetKeyViewSet(ModelViewSet):
    queryset =  Key.objects.all()
    serializer_class = KeySerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        errors = []
        # sanity check whether email is present or not
        if 'email' in request.GET:
            email = request.GET.get('email')
            # Check for valid email
            if not re.search(regex,email):
                errors.append("Please send a valid email.")
        else:
            errors.append("Please send the email")

        # generate a random number
        alice_secret = random.randint(4,1000)

        # Public key to send
        send_bob = (g**a) % p

        # save the instance or update
        obj, created = Key.objects.update_or_create(email=email,
                                                    defaults={
                                                        'p': p,
                                                        'g': g,
                                                        'a': alice_secret,
                                                        'key': send_bob,
                                                    })

        if bool(errors):
            return Response({'fixes': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'pk': send_bob}, status=status.HTTP_200_OK)


class SubmitKeyViewSet(ModelViewSet):
    queryset =  Key.objects.all()
    serializer_class = KeySerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        errors = []
        email = request.GET.get('email', None)
        bob_key = request.GET.get('B_public', None)
        shared_secret = request.GET.get('solution', None)

        if email is None:
            errors.append("email not sended")
        elif bob_key is None:
            errors.append("bob key not sended")
        elif isinstance(int, bob_key):
            errors.append("bob key is not integer")
        elif shared_secret is None:
            errors.append("shared secret not sended")
        elif isinstance(int, shared_secret):
            errors.append("shared secret is not integer")
        else:
            obj = self.get_queryset().filter(email=email)
            if not obj.first():
                errors.append("email not found")

        if bool(errors):
            return Response({'fixes': errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Go forward
            alice_secret = obj.first().a
            cal_alice_secret = (shared_secret ** alice_secret) % p
            if cal_alice_secret == alice_secret:
                return Response({'status': 'Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Failed'}, status=status.HTTP_401_UNAUTHORIZED)
            
        