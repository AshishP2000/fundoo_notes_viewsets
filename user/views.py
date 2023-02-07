import logging

from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.response import Response

from user.serializers import UserSerializer
from user.utils import JWT

logging.basicConfig(filename='fundoo_notes.log', level=logging.INFO)


# Create your views here.


class UserRegister(viewsets.ViewSet):

    def list(self, request):
        """
        register: getting user_name,email,password and phone from user and saving in the database
        request: data from user
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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

