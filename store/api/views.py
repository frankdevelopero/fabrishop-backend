from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from base64 import b64decode
from django.core.files.base import ContentFile
import base64
import six
import uuid
from .serializers import *
from ..models import *


class StoreView(APIView):
    def get(self, request):
        stories = Store.objects.all()
        serializer = StoreSerializer(stories, many=True)
        return Response(data={"stories": serializer.data}, status=status.HTTP_200_OK)


class StoreDetailView(RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreHomeView(APIView):
    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        categories = Category.objects.filter(store=store)
        serializer = CategorySerializer(categories, many=True)

        return Response(data={"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


class HomeView(APIView):
    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        categories = Category.objects.filter(store=store)
        cat_serializer = CategorySerializer(categories, many=True)

        products = Product.objects.filter(store=store)
        prod_serializer = ProductSerializer(products, many=True)

        return Response(
            data={"success": True, "data": {"products": prod_serializer.data, "categories": cat_serializer.data}},
            status=status.HTTP_200_OK)


class StoreDataView(APIView):
    def get(self, request, pk):
        store = Store.objects.get(pk=pk)
        store_serializer = StoreSerializer(store)

        return Response(
            data={"success": True, "data": {"store": store_serializer.data}},
            status=status.HTTP_200_OK)


def decode_base64_file(data):
    def get_file_extension(file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    from django.core.files.base import ContentFile
    import base64
    import six
    import uuid

    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension,)

        return ContentFile(decoded_file, name=complete_file_name)


class ProductAddView(APIView):

    def post(self, request):
        print(request.data)
        name = request.data['name']
        description = request.data['description']
        price = request.data['price']
        category = request.data['category']
        store = request.data['store']
        images = request.data['images']

        category_obj = Category.objects.get(pk=category)
        store_obj = Store.objects.get(pk=store)

        product = Product()
        product.name = name
        product.description = description
        product.price = price
        product.category = category_obj
        product.store = store_obj
        product.image = decode_base64_file(images[0])
        product.save()

        print(product.id)
        print(product.name)
        print(product.image)

        del images[0:1]
        for base_64 in images:
            gallery = Gallery()
            gallery.product = product
            gallery.image = decode_base64_file(base_64)
            gallery.save()

        return Response(data={"success": True, "message": "Producto registrado con éxito"}, status=status.HTTP_200_OK)


class CategoryAddView(APIView):
    def post(self, request):
        print(request.data)
        name = request.data['name']
        description = request.data['description']
        store = request.data['store']
        store_obj = Store.objects.get(pk=store)

        category = Category()
        category.name = name
        category.description = description
        category.store = store_obj
        category.save()
        return Response(data={"success": True, "message": "Categoría agregado con éxito"}, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    def post(self, request):
        print(request.data)
        firstname = request.data['firstname']
        lastname = request.data['lastname']
        fcm = request.data['fcm']
        email = request.data['email']
        password = request.data['password']
        store_name = request.data['store_name']
        store_slug = request.data['store_slug']
        message = "Usuario registrado con éxito."
        user = User.objects.filter(email=email)
        success = True
        bodyres = {}
        if user:
            message = "Este correo ya está en uso. ¡Por favor intenta con otro correo!."
            success = False
        else:
            if firstname and lastname and password and email and store_name and store_slug:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=firstname,
                    last_name=lastname,
                    password=password,
                )
                user_profile = CustomUser()
                user_profile.user = user
                user_profile.fcm = fcm
                user_profile.save()

                store = Store()
                store.name = store_name
                store.slug = store_slug
                store.admin = user_profile
                store.save()

                bodyres = {
                    "user": {
                        "id": user_profile.id,
                        "firstname": firstname,
                        "lastname": lastname,
                        "email": email,
                    },
                    "store": {
                        "id": store.id,
                        "name": store_name,
                        "slug": store.slug,
                    }
                }
            else:
                success = False
                message = "¡Por favor completa el formulario de registro!."
        if success:
            data = {"success": success, "message": message, "data": bodyres}
        else:
            data = {"success": success, "message": message}

        return Response(data=data, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class VerifySlugAPIView(APIView):
    def get(self, request, slug):
        succes = True
        store = Store.objects.filter(slug=slug)
        if store:
            succes = False
        return Response(data={"success": succes}, status=status.HTTP_200_OK)


class ProductAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get(self, request):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(data={"products": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class CategoryAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CategoryCrudSerializer

    def get(self, request):
        category = Category.objects.all()
        serializer = CategoryCrudSerializer(category, many=True)
        return Response(data={"categories": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = CategoryCrudSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
