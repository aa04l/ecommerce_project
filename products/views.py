from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Product, Purchase, Advertisement, Cart, Order, OrderItem, 
    Review, Coupon, Notification
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from decimal import Decimal

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
    
    # Get product reviews
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Check if user has reviewed this product
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'user_review': user_review,
    }
    return render(request, 'pages/product.html', context)

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


# Cart Views
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)


@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'pages/cart.html', context)


@login_required
def update_cart(request, cart_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


# Order Views
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('products')
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        phone_number = request.POST.get('phone_number')
        coupon_code = request.POST.get('coupon_code')
        
        if not shipping_address or not phone_number:
            messages.error(request, 'Please provide shipping address and phone number.')
            return render(request, 'pages/checkout.html', {'cart_items': cart_items})
        
        # Calculate total
        subtotal = sum(item.total_price for item in cart_items)
        discount = 0
        
        # Apply coupon if valid
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    discount = (subtotal * coupon.discount_percentage) / 100
                    coupon.used_count += 1
                    coupon.save()
                else:
                    messages.error(request, 'Invalid or expired coupon code.')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.')
        
        total_amount = subtotal - discount
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address=shipping_address,
            phone_number=phone_number,
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )
        
        # Clear cart
        cart_items.delete()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            title='Order Placed Successfully',
            message=f'Your order #{order.order_number} has been placed successfully.',
            notification_type='order_status',
        )
        
        messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'cart_items': cart_items,
        'subtotal': sum(item.total_price for item in cart_items),
    }
    return render(request, 'pages/checkout.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'pages/orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'pages/order_detail.html', {'order': order})


# Review Views
@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        
        review, created = Review.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
        
        messages.success(request, 'Review submitted successfully!')
        return redirect('product_detail', product_id=product_id)
    
    return redirect('product_detail', product_id=product_id)


# Notification Views
@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'pages/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return JsonResponse({'success': True})


@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'success': True})


@login_required
def clear_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'success': True})


@login_required
def check_new_notifications(request):
    """Check for new notifications (for real-time updates)"""
    from django.utils import timezone
    from datetime import timedelta
    
    # Get notifications from the last 30 seconds
    recent_time = timezone.now() - timedelta(seconds=30)
    new_notifications = Notification.objects.filter(
        user=request.user,
        created_at__gte=recent_time,
        is_read=False
    ).values('id', 'title', 'message', 'notification_type')
    
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    return JsonResponse({
        'new_notifications': list(new_notifications),
        'unread_count': unread_count
    })
