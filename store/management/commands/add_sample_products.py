import os
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Category, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Adds sample artificial flower products to the database'

    def handle(self, *args, **kwargs):
        # Create or get the Artificial Flowers category
        category, created = Category.objects.get_or_create(
            name='Artificial Flowers',
            defaults={'description': 'Beautiful artificial flowers that never wilt or fade'}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Category already exists: {category.name}'))
        
        # Sample product data
        products = [
            {
                'name': 'Rose Bouquet',
                'description': 'A beautiful bouquet of artificial roses that look just like the real thing. Perfect for home decor or as a gift that will never wilt.',
                'price': 29.99,
                'stock': 50,
                'image_url': 'https://i.pinimg.com/736x/12/cb/d8/12cbd89ddf379b2fee810b0e4d232845.jpg',
            },
            {
                'name': 'Tulip Arrangement',
                'description': 'Colorful artificial tulips arranged in a decorative vase. Brings spring into your home all year round.',
                'price': 34.99,
                'stock': 30,
                'image_url': 'https://i.pinimg.com/736x/d6/0c/32/d60c326d139e0d0f1689addb23441d34.jpg',
            },
            {
                'name': 'Orchid Plant',
                'description': 'Elegant artificial orchid plant in a ceramic pot. Looks incredibly realistic and requires zero maintenance.',
                'price': 45.99,
                'stock': 25,
                'image_url': 'https://i.pinimg.com/736x/5b/12/d6/5b12d60f05dceee050455c5054fc4346.jpg',
            },
            {
                'name': 'Sunflower Bunch',
                'description': 'Bright and cheerful artificial sunflowers that bring warmth to any room. Perfect for summer decor.',
                'price': 27.99,
                'stock': 40,
                'image_url': 'https://i.pinimg.com/736x/dd/b7/4a/ddb74a8967eb335b581e2f15cf505438.jpg',
            },
            {
                'name': 'Lavender Bouquet',
                'description': 'Fragrant-looking artificial lavender bouquet, perfect for adding a touch of Provence to your home.',
                'price': 22.99,
                'stock': 35,
                'image_url': 'https://i.pinimg.com/736x/71/c9/2b/71c92b94cdb9d4cb75d3356c30dfb8f2.jpg',
            },
            {
                'name': 'Peony Arrangement',
                'description': 'Luxurious artificial peonies in a glass vase. These stunning flowers add elegance to any space.',
                'price': 39.99,
                'stock': 20,
                'image_url': 'https://i.pinimg.com/736x/52/51/9b/52519b1fe8e5f79becdb5fa1dc01bf8b.jpg',
            },
        ]
        
        # Create media directory if it doesn't exist
        media_root = settings.MEDIA_ROOT
        products_dir = os.path.join(media_root, 'products')
        if not os.path.exists(media_root):
            os.makedirs(media_root)
        if not os.path.exists(products_dir):
            os.makedirs(products_dir)
        
        # Add products to the database
        for product_data in products:
            # Check if product already exists
            if Product.objects.filter(name=product_data['name']).exists():
                self.stdout.write(self.style.WARNING(f"Product already exists: {product_data['name']}"))
                continue
            
            # Create the product without image first
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=category,
                stock=product_data['stock'],
                available=True
            )
            
            # Download and save the image
            try:
                response = requests.get(product_data['image_url'])
                if response.status_code == 200:
                    image_name = f"{product_data['name'].lower().replace(' ', '_')}.jpg"
                    product.image.save(
                        image_name,
                        File(BytesIO(response.content))
                    )
                    self.stdout.write(self.style.SUCCESS(f"Added product with image: {product.name}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to download image for {product.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error adding image for {product.name}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS('Sample products added successfully!')) 