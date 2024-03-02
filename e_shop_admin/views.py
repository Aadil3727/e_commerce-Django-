from django.shortcuts import render
from django.http import HttpResponse
# from . forms import Sign_Up , Login_User
from . models import Auth_user, Image_slider 

from . models import *
from django.contrib.auth import login , authenticate, logout
from django.shortcuts import redirect, get_object_or_404
from e_shop_user.models import Category , Product, ProductImageGallery
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.http import QueryDict
# from decimal import Decimal

# Create your views here.


    
def auth_login(request):
    type = 'Logi'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user.is_superuser:
            login(request, user)
            return redirect('index-page')
        else:
            return HttpResponse("User is not superuser or not exist")
            #include message error here

            
            # User is authenticated
    return render(request,'loginadmin.html',{'ty':type})
    
    

@login_required(login_url='loginn')
def index(request):
    users = Auth_user.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request,"index.html",{'us':users,'cs':categories,'ps':products})

def add_catrgory(request):
    type='Add Category'
    if request.method=='POST':
        cname = request.POST.get('cname')
        cimage = request.FILES.get('cimage')
        if Category.objects.filter(cname=cname).first():
            messages.error(request,'Already Exist')
        else:
            data = Category(cname=cname,cimage=cimage)
            data.save()
            return redirect('show-cat')
    return render(request,'add_category.html',{'cate':type})

def add_product(request):
    type='Add Products'
    c = Category.objects.all()
    i = {}
    a = Product.objects.all()
    if request.method == "POST":
        p_name = request.POST.get('p_name')
        p_price = request.POST.get('p_price')
        p_image = request.FILES.getlist('p_image')
        categorid = request.POST.get('p_category')
        offer_price = request.POST.get('offer_price')
        print("HERE",offer_price)
        is_offer = request.POST.get('is_offer') 
        selected_categopry = Category.objects.filter(id=categorid).first()
        p_description = request.POST.get('p_description')
        
        if is_offer == 'on':
            is_offer = True
        else:
            is_offer = False

        if offer_price == "":
            offer_price = None
    
            # print("hello",offer_price)

        if is_offer == True and offer_price is None:
            messages.warning(request, "Enter Offer Price")
            return redirect('add-product')
            # print("Wifi",is_offer)
            # print("Wifi",offer_price)            

        if p_name is None or p_price is None or p_image is None or categorid is None or p_description is None : 
            messages.error(request, "Required")
            return redirect('add-product')

        else:
            data = Product.objects.create(p_name=p_name,p_price=p_price,p_category=selected_categopry,p_description=p_description,p_image=p_image[0],is_offer=is_offer,offer_price=offer_price)
            
            for image in p_image:
            
                ProductImageGallery.objects.create(product=data,image=image).save()
            
            data.save()

            return redirect('show-pro')
           
    return render(request,'add_product.html',{'p':type,'pro':c})


def showcategory(request):
    catgories = Category.objects.all()
    return render(request,'show_category.html',{'categories':catgories})


def del_cat(request,slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('show-cat')

def edit_cat(request,slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        cname = request.POST.get('cname')
        cimage = request.FILES.get('cimage')
        if cimage is None:
            updated = Category.objects.filter(slug=slug).update(cname=cname,cimage=category.cimage)
            return redirect('show-cat')
        else:
            category.cname = cname
            category.cimage = cimage
            category.save()
    
    context = {'cat': category}
    return render(request,'edit_category.html',context)

        
    
def show_product(request):
    product = Product.objects.all()
    return render(request,'show_product.html',{'products':product})


def del_product(request,slug):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    return redirect('show-pro')

def edit_product(request,slug):

    c = Category.objects.all()
    product = get_object_or_404(Product, slug=slug)
    pro = ProductImageGallery.objects.filter(product=product)

    if request.method == "POST":
        p_name=request.POST.get('p_name')
        p_price=request.POST.get('p_price')
        p_image=request.FILES.getlist('p_image')
        p_description=request.POST.get('p_description')
        product.is_offer = True if request.POST.get('is_offer') else False
        offer_price=request.POST.get('offer_price')
        p_category=request.POST.get('p_category')
        cate = Category.objects.filter(id=p_category).first()

        # if is_offer == 'True':
        #         product.is_offer = True
        # else:
        #         product.is_offer = False
        # print("ABC",product.is_offer)
        if p_image is None:
            update = Product.objects.filter(slug=slug).update(p_name=p_name,p_price=p_price,p_description=p_description,p_category=cate,p_image=product.p_image[0],is_offer=product.is_offer,offer_price=offer_price)
            return redirect('show-pro')
        else:
           
            product.p_name=p_name
            product.p_price=p_price
            product.p_description=p_description
            product.p_category=cate
            product.p_image=p_image[0]
            product=product.is_offer
            product.offer_price=offer_price

            for image in p_image:
            
                ProductImageGallery.objects.create(product=product,image=image).save()
            product.save()
            return redirect('show-pro')

    return render(request,'edit_product.html',{'products':product,'pro1':c,'try':pro})
    

def img_crousal(request):
    product = Product.objects.all()
    category = Category.objects.all()
    crousal = Image_slider.objects.all()
    if request.method == 'POST':
        img = request.FILES.get('img')
        title = request.POST.get('title')
        link_type = request.POST.get('link_type')
        link_category = request.POST.get('link_category')
        link_product = request.POST.get('link_product')
        print('category',link_category)
        print('product',link_product)
        cate_id = Category.objects.filter(id=link_category).first()
        pro_id = Product.objects.filter(id=link_product).first()
   
        # if pro_id == 0:
        #     pro_id=None
        # if cate_id == 0:
        #     cate_id=None

        data = Image_slider(img=img,title=title,link_category=cate_id,link_type=link_type,link_product=pro_id)    
        data.save()

    context = {
        'categories' : category ,
        'products' : product ,
        'sliders' : Image_slider._meta.get_field("link_type").choices ,
        'crousal' : crousal
    }
    return render(request,'add_crousal.html',context)

def show_crousal(request):
    c = Image_slider.objects.all()
    return render(request,'show_crousal.html',{'slider':c})


def del_crousal(request,pk):
    crousal = get_object_or_404(Image_slider,id=pk)
    crousal.delete()
    return redirect('all-crousal')


def auth_logout(request):
    logout(request)
    return redirect('loginn')


def delete_img_gallery(request,pk,slug):
    product = Product.objects.filter(slug=slug).first()
    img = get_object_or_404(ProductImageGallery,id=pk,product=product)
    img.delete()
    return redirect("edit-pro",slug=product.slug)

def show_messages(request):
    mess = Contact_Us.objects.all()
    context = {
        "mess":mess
    }
    return render(request,'show_messages.html',context)

def del_mess(request,pk):
    mess = get_object_or_404(Contact_Us,id=pk)
    mess.delete()
    return redirect('message-list')