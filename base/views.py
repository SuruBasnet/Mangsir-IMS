from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from .models import Product,ProductType,Department,Purchase,User
from .serializers import ProductSerializer, ProductTypeSerializer, UserSerializer, PurchaseSerializer, GroupSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,BasePermission,DjangoModelPermissions
from rest_framework.decorators import api_view,permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from dotenv import load_dotenv
import os,random

load_dotenv()

# Create your views here.
class PurchaseApiView(ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def create(self,request): # Email send to all management users(email) - msg(Purchase has been made of {productname}, by {email}.)
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            purchase_obj = serializer.save()
            product_name = purchase_obj.product_id.name
            email = request.user.email
            from_email = os.getenv('EMAIL_HOST_USER')
            management_user = User.objects.filter(groups__name='Management')
            management_user_email = []
            for m_u in management_user:
                management_user_email.append(m_u.email)

            send_mail(subject='Product purchased!',message=f'Purchase has been made of {product_name}, by {email}',from_email=from_email,recipient_list=management_user_email)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        


class ProductApiView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['type_id','department_id']
    search_fields = ['name','description']

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
@permission_classes([IsAuthenticated])
def register_api_view(request):
    if request.user.groups.name == 'Management':
        password = request.data.get('password')
        hash_password = make_password(password)
        data = request.data.copy()
        data['password'] = hash_password
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            while True:
                otp = random.randint(10000,99999)
                try:
                    User.objects.get(otp=otp)
                except:
                    break
            email = request.data.get('email')
            send_mail(subject='OTP for verification!',message=f'Your otp for verification is: {otp}',from_email=os.getenv('EMAIL_HOST_USER'),recipient_list=[email])
            user = serializer.save()
            user.otp = otp
            user.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail':'You do not have permission!'},status=status.HTTP_403_FORBIDDEN)
    
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

@api_view(['GET'])
@permission_classes([])
def group_api_view(request):
    group_objs = Group.objects.all()
    serializer = GroupSerializer(group_objs,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([])
def otp_verify(request):
    otp = request.data.get('otp')
    try:
        user = User.objects.get(otp=otp)
    except:
        return Response({'detail':'Invalid otp!'})
    user.is_active = True
    user.save()
    serializer = UserSerializer(user)
    return Response(serializer.data)
