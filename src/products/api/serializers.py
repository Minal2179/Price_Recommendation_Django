from rest_framework import serializers
from django.contrib.auth.models import User

from products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'sub', 'sub2')


class ProductSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')
    category = CategorySerializer()
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'item_condition', 'category', 'brand_name', 'shipping', 'item_description', 'price') 

    def create(self, validated_data):
        cat_instance = validated_data.pop('category')
        cat_elem = dict(cat_instance)
        cat_exist = Category.objects.filter(title=cat_elem['title'], sub=cat_elem['sub'], sub2=cat_elem['sub2'])
        
        print(validated_data ,validated_data['name'], validated_data['item_condition'], cat_elem['title'], validated_data['brand_name'], validated_data['shipping'], validated_data['item_description'])
        # brand = Category.get_category()
        # print(brand)
        # price = prediction(validated_data['name'], validated_data['item_condition_id'], category_name, validated_data['brand_name'], shipping, item_description)
        if len(cat_exist) == 0:
            new_cat = Category.objects.create(**cat_elem)
            product = Product.objects.create(**validated_data, category=new_cat)
        else:
            new_cat = Category.objects.get(**cat_elem)
            product = Product.objects.create(**validated_data, category=new_cat)
        return product


class UserSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'products')