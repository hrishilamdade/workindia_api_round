import json
import random
from rest_framework import serializers,exceptions
from rest_framework.validators import UniqueValidator

from .models import *



class UserRegistrationSerializer(serializers.ModelSerializer):
    
    # sub= SubSerializer(required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('email','username','first_name','last_name' ,'dob','aadhar_number', 'pancard_number','address','user_type')
        extra_kwargs = {'password': {'write_only': True}}


    def validate(self, data):
        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("Email already registered")
        elif User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError("Username already registered")
        # elif form.clean_password()==False:
        #     messages.error(request, form.errors)
        #     return HttpResponseRedirect(reverse('show_company_dash'))
        return data
    
    def create(self, validated_data):
        print(validated_data)
        data = {}
        data['email'] = validated_data['email']
        data['username'] = validated_data['email']
        data['first_name'] = validated_data['first_name']
        data['last_name'] = validated_data['last_name']
        data['dob'] = validated_data["dob"]
        data['aadhar_number']  = validated_data["aadhar_number"]
        data['pancard_number']  = validated_data["pancard_number"]
        data['address']  = validated_data["address"]
        data['user_type']  = validated_data["user_type"]
        pin = str(random.randint(999, 9999))
        data['password'] = pin

        user = User.objects.create_user(**data)
        user.save()
        account = Account.objects.create(user = user)
        resp_data = {"account_no":account.account_no,"pin":pin}
        return resp_data


class UserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','username','first_name','last_name' )


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class TokenObtainPairSerializer(serializers.Serializer):

    default_error_messages = {
        'no_active_account': 'No active account found with the given credentials',
        'user_not_active': 'Please check your email box to activate your account.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        
        username = attrs['username']
        password = attrs['password']
        try:
            self.user = User.objects.get(username=username)
            if self.user.check_password(password):
                if self.user is None :
                    raise exceptions.AuthenticationFailed(
                        self.error_messages['no_active_account'],
                        'no_active_account',
                    )
                elif not self.user.is_active:
                    raise exceptions.AuthenticationFailed(
                        self.error_messages['user_not_active'],
                        'user_not_active',
                    )
            else:
                raise serializers.ValidationError("Incorrect username or Password")
                
        except User.DoesNotExist:
            raise serializers.ValidationError("Incorrect username or Password")
        
        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')

class CustomTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ("account_no","user","balance","account_state","last_transaction_timestamp")
