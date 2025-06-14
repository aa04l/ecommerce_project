from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login
from django.contrib.auth.forms import AuthenticationForm
from .models import Store
from django.contrib import messages  # لإضافة الرسائل
from .models import Userstore
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'pages/home.html', {'store': Store.objects.first()})
def about(request):
    return render(request, 'pages/about.html', {'store': Store.objects.first()})
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # تسجيل الدخول
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')  # استبدل 'home' بصفحتك الرئيسية
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # تحقق إذا كان اسم المستخدم أو الإيميل مستخدمًا مسبقًا
        if Userstore.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if Userstore.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # إنشاء مستخدم جديد
        user = Userstore.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username,
            password=password,
            email=email,
            phone_number=phone_number,
            address=address,
            gender=gender
        )
        user.save()

        # رسائل النجاح
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('login')  # استبدل 'login' برابط صفحة تسجيل الدخول

    return render(request, 'pages/register.html')


@login_required
def profile(request):
    user = request.user

    if request.method == "POST":
        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.phone_number = request.POST.get("phone_number", "")
        user.address = request.POST.get("address", "")
        user.gender = request.POST.get("gender", "")

        try:
            user.save()
            messages.success(request, "save successfully")
            return redirect('profile')  # مهم جدًا إعادة التوجيه بعد الحفظ
        except Exception as e:
            messages.error(request, f"error  {e}")

    return render(request, "pages/profile.html", {"user": user})
@login_required
def profile_view(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'pages/profile.html', {'user': user})
    else:
        messages.error(request, 'You need to be logged in to view your profile.')
        return redirect('login')  # استبدل 'login' برابط صفحة تسجيل الدخول