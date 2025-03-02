# Bloom & Petal - Artificial Flower E-commerce Store

Bloom & Petal is a beautiful e-commerce platform specializing in artificial flowers that last forever. Built with Django and Bootstrap, this application provides a complete shopping experience with user accounts, product management, and order processing.

## Features

- **User-friendly Interface**: Modern, responsive design with Bootstrap
- **Product Catalog**: Browse products by category with search and filter options
- **User Accounts**: Registration, login, profile management
- **Shopping Cart**: Add, update, and remove items
- **Checkout Process**: Secure and streamlined checkout experience
- **Order Management**: View order history and track order status
- **Admin Dashboard**: Manage products, categories, and orders
- **Product Import**: Bulk import products via CSV

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: Django's built-in authentication system
- **Forms**: Django Crispy Forms with Bootstrap 5 template pack

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/bloom-and-petal.git
   cd bloom-and-petal
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. (Optional) Load sample data:
   ```
   python manage.py add_flower_categories
   python manage.py add_sample_products
   ```

## Screenshots

![Homepage](screenshots/homepage.png)
![Product Listing](screenshots/product-listing.png)
![Product Detail](screenshots/product-detail.png)
![Shopping Cart](screenshots/shopping-cart.png)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Bootstrap for the responsive design framework
- Font Awesome for the icons
- Unsplash for sample product images 
