from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import ProductForm, CategoryForm, ProductImportForm
import csv
import io

def home(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    return render(request, 'store/product_detail.html', {'product': product})

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, available=True)
    categories = Category.objects.all()
    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
        'category': category
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('product_detail', product_id=product_id)

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    return render(request, 'store/cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.product.name} removed from your cart.")
    return redirect('view_cart')

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.warning(request, "Your cart is empty.")
            return redirect('view_cart')
            
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty.")
        return redirect('home')
    
    if request.method == 'POST':
        # Process the order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            total_price=cart.total
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
        
        # Clear the cart
        cart.delete()
        
        messages.success(request, "Your order has been placed successfully!")
        return redirect('home')
    
    return render(request, 'store/checkout.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@staff_member_required
def manage_products(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    products = Product.objects.all()
    
    # Filter by category if provided
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            products = products.filter(category=category)
        except (Category.DoesNotExist, ValueError):
            pass
    
    # Filter by search query if provided
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all().order_by('name')
    
    # Order products by creation date (newest first)
    products = products.order_by('-created')
    
    return render(request, 'store/manage_products.html', {
        'products': products,
        'categories': categories,
        'current_category_id': category_id,
        'search_query': search_query
    })

@staff_member_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' added successfully!")
            return redirect('manage_products')
    else:
        form = ProductForm()
    
    return render(request, 'store/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })

@staff_member_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'store/product_form.html', {
        'form': form,
        'product': product,
        'title': 'Edit Product'
    })

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f"Product '{product_name}' deleted successfully!")
        return redirect('manage_products')
    
    return render(request, 'store/delete_product.html', {
        'product': product
    })

@staff_member_required
def manage_categories(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'store/manage_categories.html', {
        'categories': categories
    })

@staff_member_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f"Category '{category.name}' added successfully!")
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    
    return render(request, 'store/category_form.html', {
        'form': form,
        'title': 'Add Category'
    })

@staff_member_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated successfully!")
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'store/category_form.html', {
        'form': form,
        'category': category,
        'title': 'Edit Category'
    })

@staff_member_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        # Check if category has products
        if category.products.exists():
            messages.error(request, f"Cannot delete category '{category.name}' because it has products. Please reassign or delete the products first.")
            return redirect('manage_categories')
        
        category_name = category.name
        category.delete()
        messages.success(request, f"Category '{category_name}' deleted successfully!")
        return redirect('manage_categories')
    
    return render(request, 'store/delete_category.html', {
        'category': category,
        'has_products': category.products.exists()
    })

@staff_member_required
def import_products(request):
    if request.method == 'POST':
        form = ProductImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            # Check if it's a CSV file
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a CSV file.')
                return redirect('import_products')
            
            # Process the CSV file
            try:
                # Read the CSV file
                csv_data = csv_file.read().decode('utf-8')
                csv_reader = csv.DictReader(io.StringIO(csv_data))
                
                # Track import statistics
                products_created = 0
                products_skipped = 0
                errors = []
                
                # Process each row
                for row in csv_reader:
                    try:
                        # Get or create the category
                        category_name = row.get('category', '').strip()
                        if not category_name:
                            errors.append(f"Row {csv_reader.line_num}: Missing category")
                            continue
                        
                        category, _ = Category.objects.get_or_create(name=category_name)
                        
                        # Check if product already exists
                        product_name = row.get('name', '').strip()
                        if not product_name:
                            errors.append(f"Row {csv_reader.line_num}: Missing product name")
                            continue
                        
                        if Product.objects.filter(name=product_name).exists():
                            products_skipped += 1
                            continue
                        
                        # Parse price
                        try:
                            price = float(row.get('price', 0))
                        except ValueError:
                            errors.append(f"Row {csv_reader.line_num}: Invalid price format")
                            continue
                        
                        # Parse stock
                        try:
                            stock = int(row.get('stock', 0))
                        except ValueError:
                            errors.append(f"Row {csv_reader.line_num}: Invalid stock format")
                            continue
                        
                        # Parse available
                        available_str = row.get('available', 'true').lower()
                        available = available_str in ['true', 'yes', '1', 'y']
                        
                        # Create the product
                        Product.objects.create(
                            name=product_name,
                            description=row.get('description', ''),
                            price=price,
                            category=category,
                            stock=stock,
                            available=available
                        )
                        
                        products_created += 1
                        
                    except Exception as e:
                        errors.append(f"Row {csv_reader.line_num}: {str(e)}")
                
                # Show import results
                if products_created > 0:
                    messages.success(request, f"Successfully imported {products_created} products.")
                
                if products_skipped > 0:
                    messages.warning(request, f"Skipped {products_skipped} products that already exist.")
                
                if errors:
                    for error in errors[:5]:  # Show first 5 errors
                        messages.error(request, error)
                    
                    if len(errors) > 5:
                        messages.error(request, f"... and {len(errors) - 5} more errors.")
                
                return redirect('manage_products')
                
            except Exception as e:
                messages.error(request, f"Error processing CSV file: {str(e)}")
                return redirect('import_products')
    else:
        form = ProductImportForm()
    
    return render(request, 'store/import_products.html', {
        'form': form
    })

@login_required
def my_account(request):
    if request.method == 'POST':
        # Update user profile
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('my_account')
    
    return render(request, 'store/my_account.html')

@login_required
def my_orders(request):
    # Get all orders for the current user
    orders_list = Order.objects.filter(user=request.user).order_by('-created')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status and status != 'all':
        orders_list = orders_list.filter(status=status)
    
    # Paginate the orders
    paginator = Paginator(orders_list, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    
    return render(request, 'store/my_orders.html', {
        'orders': orders
    })

@login_required
def order_detail(request, order_id):
    # Get the order for the current user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    return render(request, 'store/order_detail.html', {
        'order': order
    })