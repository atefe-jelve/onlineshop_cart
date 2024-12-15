from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from .models import BaseUser

class UserRegister(APIView):
    def post(self, request):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            BaseUser.objects.create_user(
                username = ser_data.validated_data['username'],
                phone_number=ser_data.validated_data['phone_number'],
                password=ser_data.validated_data['password'],
            )

            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

