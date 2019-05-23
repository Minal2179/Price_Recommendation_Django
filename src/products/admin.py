from django.contrib import admin
from products.models import Product, Category

# Register your models here.
# class CategoryAdmin(admin.TabularInline):
#     model = Category

# class ProductAdmin(admin.ModelAdmin):
#     model = Product
#     fields = ('name', 'item_condition', 'main_category', 'sub_category', 'sub_category2', 'brand_name', 'shipping', 'item_description')
    
#     def main_category(self, obj):
#         return obj.category.title

#     def sub_category(self, obj):
#         return obj.category.sub

#     def sub_category2(self, obj):
#         return obj.category.sub_sub
    

admin.site.register(Product)
admin.site.register(Category)
