from products.models import Product, Category
from .serializers import CategorySerializer, ProductSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

from django.http.response import JsonResponse
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from algo.Predictor import prediction
from products.utils import Config


# @api_view(['POST'])
# @permission_classes([AllowAny, ])
# class create_or_update_product(request):
#     if request.method == 'POST':

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permissions_classes = (permissions.AllowAny,)

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def get_price(request, pk, format=None):
    try:
        product = Product.objects.get(pk=pk)
        name = product.name
        item_condition = product.item_condition
        category_main = product.category.get_title()
        category_sub = product.category.get_sub()
        category_sub2 = product.category.get_sub2()
        brand_name = product.get_brand_name_display()
        shipping = product.shipping
        item_description = product.item_description
        price = prediction(name, item_condition, category_main, category_sub, category_sub2, brand_name, shipping, item_description)
        final_price = round(price.predicted_price()[0], 2)
        product.price = final_price
        product.save()
        data = {
            'name': name,
            'item_condition': item_condition,
            'category': {
                'title':product.category.title,
                'sub':product.category.sub,
                'sub2':product.category.sub
            },
            'brand_name': product.brand_name,
            'shipping': shipping,
            'item_description': item_description,
            'price': final_price
        }
        resp = {'message': 'Success', 'status_code': 1, 'data': {'price': final_price}}
        return JsonResponse(resp, status=200)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# def get_brand_list(request):
#     brands = c.get_brand()


    
    # print(product.get_brand_name_display())
    # print(category_main)
    # print(product.category)
    # price = prediction(name, item_condition, category_main, category_sub, category_sub2, brand_name, shipping, item_description)
    # final_price = round(price.predicted_price()[0], 2)
    # print('Price', final_price)
    # product.price = final_price
    # product.save()
    # data = {
    #     'name': name,
    #     'item_condition': item_condition,
    #     'category': {
    #         'title':product.category.title,
    #         'sub':product.category.sub,
    #         'sub2':product.category.sub
    #     },
    #     'brand_name': product.brand_name,
    #     'shipping': shipping,
    #     'item_description': item_description,
    #     'price': final_price

    # }
    # # serializer = ProductSerializer(product, data=data)
    # # serializer.is_valid(raise_exception=True)
    # # serializer.save()

    # return Response(product)