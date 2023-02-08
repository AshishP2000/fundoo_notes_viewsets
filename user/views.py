import logging

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

import user
from fundoo_notes import settings
from user.models import User
from user.serializers import UserSerializer
from user.utils import JWT

logging.basicConfig(filename='fundoo_notes.log', level=logging.INFO)


# Create your views here.


class UserRegister(viewsets.ViewSet):

    def create(self, request):
        """
        register: getting user_name,email,password and phone from user and saving in the database
        request: data from user
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWT().encode({'user_id': serializer.data.get('id')})
            send_mail(
                'fundoo notes',
                settings.BASE_URL + reverse('verify', kwargs={'token': token}),
                settings.EMAIL_HOST_USER,
                [serializer.data.get('email')]
            )
            return Response({'message': 'user is registered', 'status': 201, 'data': serializer.data},
                            status=status.HTTP_201_CREATED)
        except TypeError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(viewsets.ViewSet):
    def list(self, request):
        """
        login: getting user_name and password from user and logging
        request: data from user
        """
        try:
            user = authenticate(email=request.data.get('email'), password=request.data.get('password'))
            if user is not None:
                token = JWT().encode({'user_id': user.id})
                return Response({'INFO': "LOGIN SUCCESSFUL", 'status': 202, 'token': token},
                                status=status.HTTP_202_ACCEPTED)
            return Response({'INFO': "LOGIN UNSUCCESSFUL", 'status': 401}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({'message': str(ex)})


class IsVerify(viewsets.ViewSet):
    def list(self, request, token):
        try:
            decode = JWT().decode(token=token)
            user = User.objects.get(id=decode.get('user_id'))
            if user:
                user.is_verify = True
                user.save()
                return Response({'INFO': "Verified"})
        except KeyError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except NameError as ex:
            logging.exception(ex)
            return Response({'message': str(ex), 'status': 400, 'data': {}}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logging.exception(ex)
            return Response({'message': str(ex)})
