from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
# from rest_framework_social_oauth2.authentication import SocialAuthentication
from django.core.files.storage import FileSystemStorage
from django.core.files import File as FileClass
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # print(self)
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        resp = {
            "status": 'success',
            "username": self.user.username,
            "status_code": 200,
            "access": str(refresh.access_token)
        }
        return resp

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserRegistrationView(CreateAPIView):
    
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.save()   
            status_code = status.HTTP_201_CREATED
            response = {
                "status": "Account successfully created",
                "status_code": 201,
                "json_data": data
            }
            return Response(response, status=status_code)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountView(GenericAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)

    def get(self,request,account_no):

        account = Account.objects.get(account_no=account_no)
        
        data = self.serializer_class(account).data

        return Response(data,status=status.HTTP_200_OK)


class TransactionView(GenericAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)


    def get(self,request):
        username = request.GET.get("username")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        sort = request.GET.get("sort")

        user = User.objects.get(username=username)

        transactions = self.serializer_class(user.transactions,many=True).data

        print(transactions)

        return Response(transactions)


    def post(self,request):
        data = request.data
        beneficiary_name = data["beneficiary_name"]
        amount = data["amount"]
        transaction_type = data["type"]

        user = User.objects.get(id = self.request.user)
        transaction = Transaction.objects.create(user = user,transaction_type=transaction_type,beneficiary_name=beneficiary_name,sender_name=user.first_name+user.last_name,amount=amount)
        transaction.save()
        
        print(user)

        return Response({"adad":"eafwe"})



class AddMoney(GenericAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTTokenUserAuthentication,)


    def post(self,request):
        data = request.data
        account_no = data["account_no"]
        amount = data["amount"]
        transaction_mode = data["transaction_mode"]
