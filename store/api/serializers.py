from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField, IntegerField

from store.models import *


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryCrudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    # products = serializers.StringRelatedField(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']
        # depth = 1


class UserLoginSerializer(serializers.ModelSerializer):
    fcm = CharField(allow_blank=True, read_only=True)
    email = EmailField(label="Correo electrónico", required=True, allow_blank=False)
    store_id = IntegerField(read_only=True)
    store_name = CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'fcm',
            'email',
            'password',
            'first_name',
            'last_name',
            'store_id',
            'store_name',
            'id',
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "store_id": {"read_only": True},
            "store_name": {"read_only": True},
            "id": {"read_only": True},

        }

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if not email:
            raise ValidationError("Ingresa tu correo electrónico para ingresa.")
        user = User.objects.filter(
            Q(email=email)
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError('Este correo electrónico no está registrado.')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Correo electrónico o contraseña incorrecta. ¡Intenta de nuevo!.")

        customuser = CustomUser.objects.get(user=user_obj)
        store = Store.objects.filter(admin=customuser).first()
        data["id"] = customuser.id
        data["fcm"] = "TOKEN RANDOM"  # generar token y enviar
        data["first_name"] = user_obj.first_name
        data["last_name"] = user_obj.last_name
        data["store_id"] = store.id
        data["store_name"] = store.name
        return data
