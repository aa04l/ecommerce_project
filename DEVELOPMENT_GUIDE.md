# E-commerce Development Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Initial Setup
```bash
# Clone the repository
git clone <repository-url>
cd ecommerce_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp env_example.txt .env

# Edit environment variables
# Edit .env file with your settings

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 📁 Project Structure Overview

### Apps Organization
```
ecommerce_project/
├── store/          # User management & authentication
├── products/       # Product catalog & shopping
├── blog/           # Blog system
└── ecommerce_project/  # Main project settings
```

### Key Files
- `settings.py`: Main Django configuration
- `config.py`: Centralized configuration
- `urls.py`: URL routing
- `models.py`: Database models
- `views.py`: Business logic
- `templates/`: HTML templates
- `static/`: CSS, JS, images

## 🛠️ Development Workflow

### 1. Adding New Features

#### Step 1: Create Models
```python
# In products/models.py
class NewFeature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'New Feature'
        verbose_name_plural = 'New Features'
    
    def __str__(self):
        return self.name
```

#### Step 2: Create Views
```python
# In products/views.py
from django.shortcuts import render, get_object_or_404
from .models import NewFeature

def new_feature_list(request):
    features = NewFeature.objects.all()
    return render(request, 'products/new_feature_list.html', {
        'features': features
    })

def new_feature_detail(request, pk):
    feature = get_object_or_404(NewFeature, pk=pk)
    return render(request, 'products/new_feature_detail.html', {
        'feature': feature
    })
```

#### Step 3: Add URLs
```python
# In products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... existing URLs
    path('new-features/', views.new_feature_list, name='new_feature_list'),
    path('new-features/<int:pk>/', views.new_feature_detail, name='new_feature_detail'),
]
```

#### Step 4: Create Templates
```html
<!-- templates/products/new_feature_list.html -->
{% extends "index.html" %}
{% load static %}

{% block title %}New Features{% endblock %}

{% block content %}
<div class="container">
    <h1>New Features</h1>
    <div class="feature-grid">
        {% for feature in features %}
        <div class="feature-card">
            <h3>{{ feature.name }}</h3>
            <p>{{ feature.description }}</p>
            <a href="{% url 'new_feature_detail' feature.pk %}" class="btn btn-primary">View Details</a>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

#### Step 5: Add Admin Configuration
```python
# In products/admin.py
from django.contrib import admin
from .models import NewFeature

@admin.register(NewFeature)
class NewFeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
```

### 2. Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

### 3. Static Files Management

#### Adding CSS
```css
/* static/css/components.css */
.new-feature-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    transition: transform 0.3s ease;
}

.new-feature-card:hover {
    transform: translateY(-4px);
}
```

#### Adding JavaScript
```javascript
// static/js/main.js
function initializeNewFeature() {
    const featureCards = document.querySelectorAll('.new-feature-card');
    
    featureCards.forEach(card => {
        card.addEventListener('click', () => {
            // Handle click events
        });
    });
}

// Add to initializeApp function
function initializeApp() {
    // ... existing code
    initializeNewFeature();
}
```

## 🎨 Frontend Development

### CSS Organization

#### 1. Main Styles (`style.css`)
- Global styles
- Layout components
- Typography
- Animations

#### 2. Component Styles (`components.css`)
- Reusable components
- Button styles
- Form components
- Modal components

#### 3. Page-Specific Styles
- Inline styles in templates
- Page-specific CSS classes

### JavaScript Organization

#### 1. Main JavaScript (`main.js`)
- Application initialization
- Global event listeners
- Utility functions
- Common functionality

#### 2. Component-Specific JavaScript
- Inline scripts in templates
- Component-specific functionality

### Responsive Design

#### Breakpoints
```css
/* Mobile First Approach */
@media (max-width: 480px) {
    /* Mobile styles */
}

@media (max-width: 768px) {
    /* Tablet styles */
}

@media (max-width: 1024px) {
    /* Desktop styles */
}
```

#### CSS Grid & Flexbox
```css
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.flex-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

## 🔧 Configuration Management

### Environment Variables
```bash
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development
DATABASE_URL=sqlite:///db.sqlite3
```

### Settings Organization
```python
# config.py
from .config import *

# Development settings
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Production settings
if ENVIRONMENT == 'production':
    DEBUG = False
    SECURE_SSL_REDIRECT = True
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test products
python manage.py test store
python manage.py test blog

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Writing Tests
```python
# products/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Product

class ProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            price=99.99,
            content="Test description"
        )
    
    def test_product_list_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
    
    def test_product_detail_view(self):
        response = self.client.get(
            reverse('product_detail', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
```

## 🔒 Security Best Practices

### 1. Input Validation
```python
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
```

### 2. CSRF Protection
```python
# In views.py
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def secure_view(request):
    # Your view logic
    pass
```

### 3. File Upload Security
```python
# In models.py
def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("File size too large")

class Product(models.Model):
    image = models.ImageField(
        upload_to='products/',
        validators=[validate_file_size]
    )
```

## 📊 Database Optimization

### 1. Indexing
```python
class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'created_at']),
        ]
```

### 2. Query Optimization
```python
# Use select_related for foreign keys
products = Product.objects.select_related('category').all()

# Use prefetch_related for many-to-many
orders = Order.objects.prefetch_related('items__product').all()

# Use only() to select specific fields
products = Product.objects.only('name', 'price').all()
```

## 🚀 Performance Optimization

### 1. Caching
```python
from django.core.cache import cache

def get_products():
    products = cache.get('products')
    if products is None:
        products = Product.objects.all()
        cache.set('products', products, 300)  # Cache for 5 minutes
    return products
```

### 2. Static Files
```python
# settings.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Collect static files
python manage.py collectstatic
```

### 3. Database Optimization
```python
# Use bulk operations
Product.objects.bulk_create([
    Product(name="Product 1", price=10.00),
    Product(name="Product 2", price=20.00),
])

# Use update() for bulk updates
Product.objects.filter(category='electronics').update(active=True)
```

## 🔍 Debugging

### 1. Django Debug Toolbar
```bash
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ... other middleware
]
```

### 2. Logging
```python
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.info('Processing request')
    try:
        # Your logic
        pass
    except Exception as e:
        logger.error(f'Error occurred: {e}')
        raise
```

### 3. Print Debugging
```python
# Use print for quick debugging
print(f"Debug: {variable}")

# Use pdb for interactive debugging
import pdb; pdb.set_trace()
```

## 📦 Deployment

### 1. Production Settings
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Environment Variables
```bash
# Production .env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 3. Static Files
```bash
# Collect static files
python manage.py collectstatic

# Serve with nginx or CDN
```

## 📈 Monitoring

### 1. Error Tracking
```python
# Install Sentry
pip install sentry-sdk

# Configure in settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### 2. Performance Monitoring
```python
# Use Django Silk for profiling
pip install django-silk

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'silk',
]

# Add to MIDDLEWARE
MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
    # ... other middleware
]
```

## 🔄 Version Control

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
# Merge to main branch
```

### Commit Messages
```
feat: add new product feature
fix: resolve cart calculation bug
docs: update README with new instructions
style: improve button styling
refactor: reorganize product models
test: add unit tests for cart functionality
```

## 📚 Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

### Tools
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Django Silk](https://github.com/jazzband/django-silk)
- [Django Extensions](https://django-extensions.readthedocs.io/)

### Best Practices
- [Django Best Practices](https://djangoproject.com/community/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Performance](https://docs.djangoproject.com/en/stable/topics/performance/)

This development guide provides a comprehensive overview of how to work with the organized e-commerce project structure, ensuring maintainable and scalable code development. 