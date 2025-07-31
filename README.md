# E-commerce Project - StoreAFP

A modern Django-based e-commerce platform with user authentication, product management, shopping cart, order processing, and blog functionality.

## 🏗️ Project Structure

```
ecommerce_project/
├── ecommerce_project/          # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   ├── asgi.py               # ASGI configuration
│   └── context_processors.py # Custom context processors
├── store/                     # User management app
│   ├── models.py             # User and Store models
│   ├── views.py              # Authentication views
│   ├── urls.py               # Store URLs
│   └── admin.py              # Admin configuration
├── products/                  # Product management app
│   ├── models.py             # Product, Cart, Order models
│   ├── views.py              # Product views
│   ├── urls.py               # Product URLs
│   └── admin.py              # Admin configuration
├── blog/                      # Blog functionality app
│   ├── models.py             # Blog post models
│   ├── views.py              # Blog views
│   ├── urls.py               # Blog URLs
│   └── admin.py              # Admin configuration
├── templates/                 # HTML templates
│   ├── index.html            # Base template
│   ├── pages/                # Page templates
│   └── blog/                 # Blog templates
├── static/                    # Static files
│   ├── css/                  # Stylesheets
│   ├── js/                   # JavaScript files
│   └── images/               # Static images
├── photos/                    # Media files (product images)
├── requirements.txt           # Python dependencies
├── manage.py                 # Django management script
└── db.sqlite3               # Database file
```

## 🚀 Features

### Core E-commerce Features
- **Product Management**: Add, edit, delete products with categories
- **Shopping Cart**: Add/remove items, quantity management
- **Order Processing**: Complete order workflow with status tracking
- **User Authentication**: Custom user model with profile management
- **Reviews & Ratings**: Product reviews and rating system
- **Coupons**: Discount code system
- **Notifications**: Real-time notification system

### Additional Features
- **Blog System**: Content management for articles
- **Advertisement System**: Banner management
- **Responsive Design**: Mobile-friendly interface
- **Search & Filter**: Product search and filtering
- **Admin Panel**: Comprehensive admin interface

## 🛠️ Technology Stack

- **Backend**: Django 5.1.6
- **Database**: SQLite (development)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design
- **Image Processing**: Pillow
- **Task Queue**: Celery with Redis
- **API**: Django REST Framework

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ecommerce_project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with the following variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
The project uses SQLite by default. For production, consider using PostgreSQL or MySQL.

## 📱 Usage

### For Customers
1. **Browse Products**: Visit the home page to see featured products
2. **Search & Filter**: Use the search functionality to find specific products
3. **Add to Cart**: Click on products to add them to your shopping cart
4. **Checkout**: Complete the purchase process with shipping information
5. **Track Orders**: Monitor order status in your account

### For Administrators
1. **Product Management**: Add/edit products through the admin panel
2. **Order Management**: Process and update order status
3. **User Management**: Manage customer accounts
4. **Content Management**: Create blog posts and advertisements

## 🎨 Design Features

### Modern UI/UX
- **Responsive Design**: Works on all device sizes
- **Smooth Animations**: CSS transitions and animations
- **Accessibility**: ARIA labels and semantic HTML
- **Loading States**: Visual feedback for user actions
- **Real-time Updates**: Live notification system

### Color Scheme
- **Primary**: #218eaf (Blue)
- **Secondary**: #eaf6fa (Light Blue)
- **Accent**: #007bff (Bootstrap Blue)
- **Background**: Gradient from #e0e7ff to #f4f6fb

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **User Authentication**: Secure login/logout system
- **Input Validation**: Form validation and sanitization
- **File Upload Security**: Secure image upload handling
- **SQL Injection Protection**: Django ORM protection

## 📊 Performance Optimizations

- **Image Optimization**: Automatic image resizing
- **Database Indexing**: Optimized database queries
- **Static File Caching**: Efficient static file serving
- **Lazy Loading**: Images load as needed
- **Minified CSS/JS**: Optimized frontend assets

## 🧪 Testing

Run tests to ensure everything works correctly:
```bash
python manage.py test
```

## 📈 Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in settings
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure media file storage
- [ ] Set up SSL certificate
- [ ] Configure email settings
- [ ] Set up monitoring and logging

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud infrastructure
- **Vercel**: Frontend deployment option

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## 🔄 Version History

- **v1.0.0**: Initial release with core e-commerce features
- **v1.1.0**: Added blog system and notifications
- **v1.2.0**: Enhanced UI/UX and performance optimizations

---

**Built with ❤️ using Django** 