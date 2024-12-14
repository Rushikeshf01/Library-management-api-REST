from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Book, Member, Loan

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = authenticate(request = self.context["request"], email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid email or password")
        
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "id": user.id,
            "email": user.email
        }

        return data
    
class MemberSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, required=True, write_only=True)

    confirm_password = serializers.CharField(style={'input_type': 'password', 'placeholder': 'Password'}, required=True, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError('password not matched')
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # hashing password manually because create method not hash it by itself
        # another way -- creat_user method of manager(which hashes password by itself)

        password = validated_data.get('password')
        hashed_password = make_password(password)

        user = Member.objects.create(
            email=validated_data['email'],
            password=hashed_password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            address=validated_data.get('address', ''),
        )
        return user
    
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone', 'address','password', 'confirm_password']

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'desc', 'author', 'genere', 'isbn', 'total_copies', 'available_copies']

    def validate(self, attrs):
        if attrs.get('available_copies') > attrs.get('total_copies'):
            raise serializers.ValidationError('available copies cannot be greater than total copies')
        
        return super().validate(attrs)
    
class LoanSerializer(serializers.ModelSerializer):
    fine = serializers.DecimalField(max_digits=6, decimal_places=2, read_only = True)
    class Meta:
        model = Loan
        fields = ['book', 'member', 'borrow_date', 'due_date', 'fine']
    

    def validate(self, attrs):
        book = attrs['book']

        if book.available_copies <= 0:
            raise serializers.ValidationError(f"'{book.title}' has no available copies.")
        return super().validate(attrs)
    
class BookReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = ['book', 'return_date']