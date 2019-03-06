from django.shortcuts import render
from app.serializers import LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pyrebase
# Create your views here.

# FCM credentials
config = {
    "apiKey" : "<api_key>",
    "authDomain" : "<auth_Domain>",
    "databaseURL" : "<database_URL>",
    "projectId" : "<project_Id>",
    "storageBucket" : "<storage_Bucket>",
    "messagingSenderId" : "<messaging_SenderId>"
  }


# firebase = pyrebase.initialize_app(config)
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()

database = firebase.database()



class LoginView(APIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']

            user = authe.sign_in_with_email_and_password(email,password)
            if user:
                content = {'message':'user exists'}
                return Response(content,status=status.HTTP_200_OK)
            else:
                content = {'message':'user not exists'}
                return Response(content,status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)        