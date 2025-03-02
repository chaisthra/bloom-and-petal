import os
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files import File
from store.models import Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Updates images for existing products'

    def handle(self, *args, **kwargs):
        # Sample product data with new images
        product_images = {
            'Rose Bouquet': 'https://images.pexels.com/photos/931177/pexels-photo-931177.jpeg?auto=compress&cs=tinysrgb&w=800',
            'Tulip Arrangement': 'https://images.pexels.com/photos/1083822/pexels-photo-1083822.jpeg?auto=compress&cs=tinysrgb&w=800',
            'Orchid Plant': 'https://images.pexels.com/photos/4751970/pexels-photo-4751970.jpeg?auto=compress&cs=tinysrgb&w=800',
            'Sunflower Bunch': 'https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg?auto=compress&cs=tinysrgb&w=800',
            'Lavender Bouquet': 'https://images.pexels.com/photos/4197491/pexels-photo-4197491.jpeg?auto=compress&cs=tinysrgb&w=800',
            'Peony Arrangement': 'https://images.pexels.com/photos/1233414/pexels-photo-1233414.jpeg?auto=compress&cs=tinysrgb&w=800',
        }
        
        # Create media directory if it doesn't exist
        media_root = settings.MEDIA_ROOT
        products_dir = os.path.join(media_root, 'products')
        if not os.path.exists(media_root):
            os.makedirs(media_root)
        if not os.path.exists(products_dir):
            os.makedirs(products_dir)
        
        # Update product images
        for product_name, image_url in product_images.items():
            try:
                product = Product.objects.get(name=product_name)
                
                # Download and save the image
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        image_name = f"{product_name.lower().replace(' ', '_')}.jpg"
                        product.image.save(
                            image_name,
                            File(BytesIO(response.content)),
                            save=True
                        )
                        self.stdout.write(self.style.SUCCESS(f"Updated image for: {product.name}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Failed to download image for {product.name}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error updating image for {product.name}: {str(e)}"))
            except Product.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Product not found: {product_name}"))
        
        self.stdout.write(self.style.SUCCESS('Product images updated successfully!')) 