from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Purchase, Advertisement
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# عرض المنتجات مع دعم البحث والفلاتر
def product_list(request):
    query = request.GET.get('q', '').strip()
    price_filter = request.GET.get('price', 'all')
    category_filter = request.GET.get('category', 'all')

    # تصفية المنتجات
    products = Product.objects.filter(active=True)
    if query:
        products = products.filter(name__icontains=query)
    if price_filter == 'low':
        products = products.filter(price__lt=50)
    elif price_filter == 'medium':
        products = products.filter(price__gte=50, price__lte=100)
    elif price_filter == 'high':
        products = products.filter(price__gt=100)
    if category_filter != 'all':
        products = products.filter(category=category_filter)

    # جلب الفئات بدون تكرار باستخدام distinct
    categories = list(set(products.values_list('category', flat=True)))

    context = {
        'pro': products,
        'categories': categories,
    }
    return render(request, 'pages/products.html', context)

# عرض تفاصيل منتج معين
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'pages/product.html', {'product': product})

# الصفحة الرئيسية
def home(request):
    products = Product.objects.filter(active=True).order_by('name')
    ads = Advertisement.objects.filter(is_active=True)

    return render(request, 'pages/home.html', {'ads':ads,'pro': products})

# شراء منتج معين
@login_required
def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        buyer_name = request.POST.get('buyer_name', '').strip()

        # التحقق من إدخال اسم المشتري
        if not buyer_name:
            messages.error(request, "Please provide your name.")
            return render(request, 'pages/product.html', {'product': product})

        # التحقق من اكتمال الملف الشخصي
        user = request.user
        if not user.address or not user.phone_number:
            messages.error(request, "Please complete your profile information (address and phone number).")
            return redirect('/profile/')  # رابط تحديث الملف الشخصي

        # إنشاء عملية الشراء
        Purchase.objects.create(
            user=user,
            product_name=product.name,
            price=product.price,
            buyer_name=buyer_name,
        )
        messages.success(request, "Purchase completed successfully!")
        return redirect('product_detail', product_id=product.id)

    return render(request, 'pages/product.html', {'product': product})
