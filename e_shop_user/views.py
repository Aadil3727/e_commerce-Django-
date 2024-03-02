from django.forms import ValidationError
from django.shortcuts import render
from e_shop_admin.models import Auth_user, Contact_Us
from django.contrib.auth.hashers import make_password
from . import models
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login , authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Product, ProductImageGallery,Wishlist_view
from e_shop_admin.models import Image_slider 
from carton.cart import Cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from .helpers import send_forget_password_mail
from django.contrib import messages
# Create your views here.
import datetime  
from datetime import timedelta
from django.utils import timezone


# def your_view(request):
#     # Your logic to generate messages
#     messages.success(request, 'Your success message.')
#     messages.error(request, 'Your error message.')
#     # Pass messages to the template context
#     return render(request, 'base/base.html', {'messages': messages.get_messages(request)})


def reg(request):
    type = 'Registration'
    if request.method == "POST":
       username = request.POST.get('username')
       email = request.POST.get('email')
       image = request.FILES.get('image')
       phone_no = request.POST.get('phone_no')
       password = make_password(request.POST['password'])

       if Auth_user.objects.filter(username=username).first():
            return HttpResponse("Username already exists")
       else:
            f1 = Auth_user(
                username=username,
                email=email,
                image=image,
                phone_no=phone_no,
                password=password
            )
            f1.save() 
            return redirect('home-page')
    
    return render(request, 'registration.html', {'type': type})

def user_login(request):
    type = 'loginn'
    if request.user.is_authenticated:
        messages.warning(request," Hey Your are Already Logged In")
        return redirect('home-page')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request,f"Welcome {username}")
            return redirect('home-page')
        else:   
            messages.warning(request, f"'{username}' user is not exist")
            #include message error here

            
            # User is authenticated
    return render(request,'registration.html',{'ty':type})




def home(request):
    # auth = get_object_or_404(Auth_user,slug=slug)
    category = Category.objects.order_by('cname')[0:8]
    product = Product.objects.order_by('p_name')[0:6]
    
    crousal = Image_slider.objects.all()
    context = {
        'category': category,
        'products': product,
        'crousal' : crousal,
        # 'name1':auth
    }
    return render(request,'main.html',context)

@login_required(login_url='login-user')
def product_details(request,slug):
    # wishlist_items = Wishlist_view.objects.filter(user=request.user)
    product = get_object_or_404(Product,slug=slug)
    pro = ProductImageGallery.objects.filter(product=product)

    return render(request,'product_section/product_detail.html',{'product':product,'p':pro})

@login_required(login_url='login-user')
def user_logout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('login-user')

@login_required(login_url='login-user')
def cart_view(request):
    cart = Cart(request.session)

    return render(request,'cart/cart_view.html',{'cart':cart})

def add_to_cart(request, slug):
    cart = Cart(request.session)
    quantity1 = request.POST.get('quantity')
    print('Your quantity is :', quantity1)
    product = Product.objects.filter(slug=slug).first()
    print("Your Product",product)
    price = 0
    if product.is_offer:
        price = product.offer_price
    else:
        price = product.p_price
        if quantity1:
            cart.add(product=product, price=price, quantity=quantity1)
            print("LOL",quantity1)
    cart.add(product=product, price=price, quantity=1)
    return redirect('cart-view')

def del_cart_item(request, slug):
    cart = Cart(request.session)
    product = Product.objects.filter(slug=slug).first()
    cart.remove_single(product=product)
    return redirect('cart-view')


def add_cart_item(request, slug):
    cart = Cart(request.session)

    product = Product.objects.filter(slug=slug).first()
    price = 0
    if product.is_offer:
        price = product.offer_price
    else:
        price = product.p_price
    cart.add(product=product, price=price, quantity=1)
    
    return redirect('cart-view')


def del_all_cart(request, slug):
    cart = Cart(request.session)
    product = Product.objects.filter(slug=slug).first()
    cart.remove(product=product)
    return redirect('cart-view')


class PostsView(ListView):
    model = Product
    paginate_by = 2 # number of posts will load
    context_object_name = 'posts'
    template_name = 'product_section/all_products.html'
    ordering = ['-p_name']

def all_cate(request):
    cate = Category.objects.all()
    return render(request,'category_section/all_categories.html', {'cates':cate})

#Products by category
def cate_pro(request,slug):
    cat = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(p_category=cat).order_by("p_name")
    return render(request,'category_section/category_wise_products.html',{"prod":products,"cat":cat})


# def posts_view(request):
#     queryset = Product.objects.all().order_by('-p_name')

#     paginator = Paginator(queryset, 2)
#     page = request.POST.get('page')

#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)

#     context = {
#         'posts': posts,
#     }

#     return render(request, 'product_section/all_products.html', context)



import uuid
@login_required(login_url='login-user')
def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not Auth_user.objects.filter(username=username).first():
            messages.warning(request,"Email is not registerd!")
            # raise ValidationError("Email is not registerd!")
            # return redirect('reset-pass')
        else:
            user_obj = Auth_user.objects.get(username = username)
            # print("AAA",user_obj)
            token = str(uuid.uuid4())
            #For Token exipre
            expiration_time = timezone.now() + timezone.timedelta(hours=1) 
            user_obj.expire_token=expiration_time
            user_obj.forget_password_token = token
            user_obj.save()
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('reset-pass')
    return render(request,'forgotpassword.html')    
        
@login_required(login_url='login-user')
def change_password(request,token):
    profile_obj = Auth_user.objects.filter(forget_password_token = token).first()
    # print("LLL",profile_obj)
    context = {'user_id' : profile_obj.id}
    if request.method == 'POST':
            new_password = request.POST.get('new_password')
            # print("POP",new_password)
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')
            # print("IDDDDDDDDD",user_id)
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = Auth_user.objects.get(id = user_id)
            # print('Hello',user_obj)
            hash_pass = make_password(new_password)
            user_obj.password=hash_pass
            user_obj.save()
            return redirect('login-user')
    return render(request, 'change-password.html',context)


@login_required(login_url='login-user')
def wish_list(request):
    
    # wishlist1 = Wishlist_view.objects.all()
    # product = get_object_or_404(Product,slug=slug)
    # # pro = ProductImageGallery.objects.filter(product=product)
    
    wishlist_items = Wishlist_view.objects.filter(user=request.user)
    # if user.is_authenticated:
    #     messages.warning(request,"Please! Login first")
    context = {
        "wish" : wishlist_items,
        "total": len(wishlist_items),
        # "p":product
    }
    return render(request,'wishlist/wishlist.html',context)

@login_required(login_url='login-user')
def add_to_wishlist(request,pk):
    user = Auth_user.objects.filter(id=pk)
    # user = Auth_user.objects.all()
    product1 = get_object_or_404(Product,id=pk)
    # if request.method == "POST":
    if request.user.is_authenticated:
        if Wishlist_view.objects.filter(product=product1,user=request.user).exists():
           messages.warning(request,"Already in your wishlist")
        else:
            Wishlist_view.objects.create(product=product1,user=request.user)
            messages.info(request,"Added to your Wishlist")
    else:
        messages.warning(request,"Please login first")
    return redirect('allproducts')

@login_required(login_url='login-user')
def del_wishlist(request,pk):
    wishlist = get_object_or_404(Wishlist_view,id=pk)
    wishlist.delete()
    return redirect('wish-lists')

@login_required(login_url='login-user')
def user_profile(request,slug):
    auth = get_object_or_404(Auth_user,slug=slug)
    if request.method == 'POST':
        username = request.POST.get('username')
        phone_no = request.POST.get('phone_no')
        image = request.FILES.get('image')
        if image is None:
            updated = Auth_user.objects.filter(slug=slug).update(username=username,image=auth.image,phone_no=phone_no)
            return redirect('user-profile')
        else:
            auth.username = username
            auth.phone_no = phone_no
            auth.image = image
            auth.save()
       
    return render(request,'profile/user_profile.html')

def page_not_found(request,exception):
    return render(request,'404/404.html')

def contact_us(request):
    return render(request,'contact_us\contact_us.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        add = Contact_Us(name=name,email=email,subject=subject,message=message)
        add.save()
        messages.info(request,"Your message has been sent")

    return render(request,'contact_us/contact_us.html')

