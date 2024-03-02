from django.db import models

# Create your models here.

from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from decimal import Decimal

from task4.settings import AUTH_USER_MODEL


# STATUS_CHOICE = (
#     ("process","processing"),
#     ("shipped","Shipped"),
#     ("deliverd","Deliverd"),
# )

# Create your models here.

class Category(models.Model):
    cname = models.CharField(max_length=50)
    slug = models.SlugField(editable=False,max_length=50)
    cimage = models.ImageField(upload_to='images/categories')

    def __str__(self):
        return self.cname
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.cname)
        super(Category, self).save(*args, **kwargs)

# class Tag(models.Model):
#     pass

class Product(models.Model):
    slug = models.SlugField(editable=False, max_length=150)
    p_name = models.CharField(max_length=150)
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    p_image = models.ImageField(upload_to='images/products',null=True,blank=True)
    p_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    p_description = models.CharField(max_length=500)
    is_offer = models.BooleanField(default=False)
    offer_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,default=0.00)
    # tags = models.ForeignKey(Tag,on_delete=models.CASCADE)
    # product_status = models.CharField()
    def __str__(self):
        return self.p_name   

    def save(self, *args, **kwargs):
        self.slug = slugify(self.p_name)
        super(Product, self).save(*args, **kwargs)

class ProductImageGallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-galleries",default='/static/images/nope-not-here.webp')
    

    def __str__(self):
        return self.product.p_name



class Wishlist_view(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.p_name
