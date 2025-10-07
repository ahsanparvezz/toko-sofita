from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    for product in product_list:
        rating = int(product.rating or 0)
        if rating > 5:  
            rating = 5
        product.filled_stars = range(rating)
        product.empty_stars = range(5 - rating)


    context = {
        'app_name' : 'Toko Sofita',
        'name': request.user.username,
        'npm' : '2406496050',
        'class': 'PBP E',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)


# Membuat produk baru
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form_entry = form.save(commit=False)
        form_entry.user = request.user
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }
    
    return render(request, "create_product.html", context)



# Menampilkan detail produk tertentu
@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    # Panggil fungsi increment_views
    product.increment_views()

    context = {
        'product': product,
    }
    return render(request, "product_detail.html", context)

def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = []

    for product in product_list:
        thumbnail_url = ''
        if getattr(product, 'thumbnail', None) and hasattr(product.thumbnail, 'url'):
            thumbnail_url = product.thumbnail.url

        data.append({
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'rating': product.rating,
            'stock': getattr(product, 'stock', None),
            'category': getattr(product, 'category', None),
            "thumbnail": product.thumbnail,
            'views': getattr(product, 'views', 0),
            'created_at': product.created_at.isoformat() if getattr(product, 'created_at', None) else '',
            'user_id': product.user.id if product.user else None,
            'is_featured': bool(getattr(product, 'is_featured', False)),
        })

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, id):
    try:
        product_item = Product.objects.filter(pk=id)
        if not product_item.exists():
            return HttpResponse(status=404)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, id):
    try:
        product = Product.objects.select_related('user').get(pk=id)

        # pastikan thumbnail bisa diakses
        thumbnail_url = ''
        if getattr(product, 'thumbnail', None) and hasattr(product.thumbnail, 'url'):
            thumbnail_url = product.thumbnail.url

        data = {
            "id": product.id,
            "name": product.name,
            "category": getattr(product, 'category', None),
            "price": product.price,
            "stock": getattr(product, 'stock', None),
            "description": product.description,
            "thumbnail": str(product.thumbnail) if product.thumbnail else "",
            "is_featured": bool(getattr(product, 'is_featured', False)),
            "rating": product.rating,
            "user_id": product.user.id if product.user else None,
            "user_username": product.user.username if product.user else None,
            "views": getattr(product, 'views', 0),
            "created_at": product.created_at.isoformat() if getattr(product, 'created_at', None) else '',
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)



def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@login_required(login_url='/login')
def list_products_ajax(request):
    """Read: Semua produk (atau milik user)"""
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)

    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "thumbnail": p.thumbnail,
            "category": p.category,
            "stock": p.stock,
            "rating": p.rating,
            "is_featured": p.is_featured,
            "views": p.views,
            "user_id": p.user.id if p.user else None,
            "user_username": p.user.username if p.user else None,
        } for p in products
    ]
    return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def get_product_ajax(request, id):
    """Read: Detail product by id"""
    try:
        product = Product.objects.get(pk=id)
        data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "thumbnail": product.thumbnail,
            "category": product.category,
            "stock": product.stock,
            "rating": product.rating,
            "is_featured": product.is_featured,
            "views": product.views,
            "user_id": product.user.id if product.user else None,
            "user_username": product.user.username if product.user else None,
        }
        # increment views setiap detail dibuka
        product.increment_views()
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"detail": "Product not found"}, status=404)

@csrf_exempt
@login_required(login_url='/login')
def create_product_ajax(request):
    """Create product via AJAX"""
    if request.method == "POST":
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data.get("name"),
            price=data.get("price"),
            description=data.get("description", ""),
            thumbnail=data.get("thumbnail", ""),
            category=data.get("category", "shoes"),
            stock=data.get("stock", 0),
            rating=data.get("rating", 0),
            user=request.user
        )
        return JsonResponse({
            "status": "success",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
            }
        })
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def update_product_ajax(request, id):
    """Update product via AJAX"""
    try:
        product = Product.objects.get(pk=id, user=request.user)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

    if request.method == "POST":
        data = json.loads(request.body)
        product.name = data.get("name", product.name)
        product.price = data.get("price", product.price)
        product.description = data.get("description", product.description)
        product.thumbnail = data.get("thumbnail", product.thumbnail)
        product.category = data.get("category", product.category)
        product.stock = data.get("stock", product.stock)
        product.rating = data.get("rating", product.rating)
        product.is_featured = data.get("is_featured", product.is_featured)
        product.save()
        return JsonResponse({
            "status": "success",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
            }
        })
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

@csrf_exempt
@login_required(login_url='/login')
def delete_product_ajax(request, id):
    """Delete product via AJAX"""
    try:
        product = Product.objects.get(pk=id, user=request.user)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

    if request.method == "DELETE":
        product.delete()
        return JsonResponse({"status": "success", "message": "Product deleted successfully"})
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

@csrf_exempt
def login_ajax(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data['username'], password=data['password'])
    if user:
        login(request, user)
        now = datetime.datetime.now().isoformat()
        response = JsonResponse({'status':'success', 'next':'/', 'last_login': now})
        response.set_cookie('last_login', now)
        return response
    return JsonResponse({'status':'error', 'message':'Username atau password salah'})

@csrf_exempt
def register_ajax(request):
    data = json.loads(request.body)
    if User.objects.filter(username=data['username']).exists():
        return JsonResponse({'status':'error', 'message':'Username sudah ada'})
    if data['password1'] != data['password2']:
        return JsonResponse({'status':'error', 'message':'Password tidak sama'})
    user = User.objects.create_user(username=data['username'], password=data['password1'])
    login(request, user)
    return JsonResponse({'status':'success', 'next':'/'})



    


# komentar tambahan tambahan# komentar tambahan tambahan
# komentar tambahan tambahan
