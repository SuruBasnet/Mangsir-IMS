from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Product,ProductType,Department
from .serializers import ProductSerializer, ProductTypeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,BasePermission,DjangoModelPermissions
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductTypeApiView(GenericViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def list(self,request):
        product_type_objs = self.get_queryset()
        serializer = self.get_serializer(product_type_objs,many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self,request,pk):
        product_type_obj = self.get_object()
        serializer = self.get_serializer(product_type_obj)
        return Response(serializer.data)

    def update(self,request,pk):
        product_type_obj = self.get_object()
        serializer = self.get_serializer(product_type_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self,request,pk):
        product_type_obj = self.get_object()
        serializer = self.get_serializer(product_type_obj,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self,request,pk):
        product_type_obj = self.get_object()
        product_type_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([])
def register_api_view(request):
    password = request.data.get('password')
    hash_password = make_password(password)
    data = request.data.copy()
    data['password'] = hash_password
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([])
def login_api_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email,password=password)

    if user == None:
        return Response({'detail':'Invalid credentials'},status=status.HTTP_400_BAD_REQUEST)

    token,_ = Token.objects.get_or_create(user=user)

    return Response(token.key)