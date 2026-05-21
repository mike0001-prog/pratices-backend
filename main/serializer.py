from rest_framework import serializers
from .models import TodoList,TodoListItem,Message,Room
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = "__all__"

class TodoListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoListItem
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ["content","sender","created_at"]

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = ["email","password","username","password2"]
    def validate_username (self,value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError({"username":"Username must be unique"})
        return value
    
    def validate_email(self,value):
        value = value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is in use")
        return value
    
    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2":"passwords do not match"}) 
        
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password":list(e.messages)})
        return data 
    
    def create(self, validated_data):
        # validated_data.pop("password2")
        user   = User.objects.create_user(username=validated_data["username"],
                                          email=validated_data["email"],
                                          password=validated_data["password"])
        return user
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","id"]

class RoomSerializer(serializers.ModelSerializer):
    user_one_name = serializers.StringRelatedField(source = "user_one",read_only=True)
    user_two_name = serializers.StringRelatedField(source = "user_two",read_only=True)
    # user_one_name = ser
    class Meta:
        model = Room 
        fields = ["uuid","user_one","user_two","user_one_name","user_two_name"]
class TokenSerializer(serializers.ModelSerializer):
    user_name = serializers.StringRelatedField(source="user",read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Token
        fields = ["user_name","user","key"]
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True )
    password = serializers.CharField(write_only=True)

class UpdateUsernameSerializer(serializers.Serializer):
    # new_username = serializers.CharField(max_length =20 )
    username = serializers.CharField( )

class ChangePasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

# class UserProfileSerializer(serializers.ModelSerializer):
#     rooms = serializers.PrimaryKeyRelatedField()
#     class Meta:
#         model = User
#         fields = ["username"]
# class UserProfileSerializer(serializers.Serializer):
#     user = 
