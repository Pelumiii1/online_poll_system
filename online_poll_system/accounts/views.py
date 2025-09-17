from rest_framework.views import APIView
from .serializer import RegisterSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from  drf_spectacular.utils import extend_schema

class RegisterView(APIView):
    # serializer_class = RegisterSerializer
    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: RegisterSerializer
        },
        summary="Register a new user",
        description="Register a new user"
    )
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                "message" : "User registered successfully",
                "user":{
                    "id":user.id,
                    "first_name": user.first_name,
                    "last_name":user.last_name,
                    "email":user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )
    
class LoginView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginSerializer
        },
        summary="Login a user",
        description="Login a user"
    )
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request,email=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user":{
                        "id":user.id,
                        "first_name": user.first_name,
                        "last_name":user.last_name,
                        "email":user.email
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)