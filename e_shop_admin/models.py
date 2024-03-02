from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify
from e_shop_user.models import Category, Product
from django.utils import timezone
# Create your models here.

class Auth_user(AbstractUser):
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False,max_length=100)
    email = models.EmailField()
    image = models.ImageField(upload_to=('images/user-images'))
    phone_no = models.IntegerField()
    password = models.CharField(max_length=128, blank=True)
    forget_password_token = models.CharField(max_length=100,editable=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateField(auto_created=True, auto_now_add=True, editable=False)
    last_login = models.DateField(auto_created=True, auto_now_add=True, editable=False)
    expire_token = models.DateTimeField(blank=True,null=True,default=timezone.now)
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.email)
        super(Auth_user, self).save(*args, **kwargs)


class Image_slider(models.Model):
    title = models.CharField(max_length=30)
    img = models.ImageField(upload_to='images/crousal')
    link_type = models.CharField(choices=[('product', 'product'), ('category', 'category')])
    link_product = models.ForeignKey(Product, max_length=50, blank=True, null=True, on_delete=models.CASCADE)
    link_category = models.ForeignKey(Category, max_length=50, blank=True, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        if self.link_type == 'product' and self.link_product:
            return reverse('pro-det', args=[str(self.link_product.slug)])
        elif self.link_type == 'category' and self.link_category:
            return reverse('cate-pro', args=[str(self.link_category.slug)])


# class Profile_user(models.Model):
#     user = models.ForeignKey(Auth_user, on_delete=models.CASCADE)
#     forget_password_token = models.CharField(max_length=100)
#     # created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

class Contact_Us(models.Model):
    name = models.CharField(max_length=15)
    email = models.EmailField()
    subject = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name