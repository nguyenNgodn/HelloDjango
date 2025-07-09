from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Profile, Account
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import check_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['age', 'address']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash password
        return super().create(validated_data)

class UserCreateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    account = AccountSerializer()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'profile', 'account']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        account_data = validated_data.pop('account')

        # Tạo user trước
        user = User.objects.create(**validated_data)

        # Tạo profile gắn với user
        Profile.objects.create(user=user, **profile_data)

        # Hash và tạo account gắn với user
        account_data['user'] = user
        account_data['password'] = make_password(account_data['password'])
        Account.objects.create(**account_data)

        return user

class LoginAccountSerializer(serializers.Serializer):
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)
        def validate(self, data):
            username = data.get('username')
            password = data.get('password')

            try:
                account = Account.objects.select_related('user').get(username=username)
            except Account.DoesNotExist:
                raise serializers.ValidationError("Tài khoản không tồn tại")

            if not check_password(password, account.password):
                raise serializers.ValidationError("Mật khẩu không đúng")

            user = account.user

            refresh = RefreshToken.for_user(user)
    
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id,
                'username': account.username,
            }
