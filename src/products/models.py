from django.db import models
from products.utils import Config

c = Config()
# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Category(models.Model):
    main_choices, sub_choices, sub_sub_choices = c.get_categories_choices()
    title = models.PositiveSmallIntegerField( choices=main_choices, default=0)
    sub = models.PositiveSmallIntegerField( choices=sub_choices, default=0)
    sub2 = models.PositiveSmallIntegerField(choices=sub_sub_choices, default=0)

    def __str__(self):
        return "%s/ %s/ %s" % (self.get_title_display(), self.get_sub_display(), self.get_sub2_display())

    def get_category(self):
        return ("%s, %s, %s") % (self.get_title_display(), self.get_sub_display(), self.get_sub2_display())

    def get_title(self):
        return self.get_title_display()
    
    def get_sub(self):
        return self.get_sub_display()
    
    def get_sub2(self):
        return self.get_sub2_display()

    
class Product(models.Model):
    created = models.DateTimeField(auto_now=True)
    # owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, default='')
    brand_choices = c.get_brand_choices()
    item_condition_choices = c.get_item_condition_choices()
    shipping_choices = c.get_shipping_choices()
    item_condition = IntegerRangeField(min_value=1, max_value=5)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null=True, blank=True)
    brand_name = models.PositiveSmallIntegerField(choices=brand_choices, default=0)
    shipping = IntegerRangeField(min_value=0, max_value=1)
    item_description = models.TextField(default='', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.name

    def get_brand(self):
        return self.get_brand_name_display()


