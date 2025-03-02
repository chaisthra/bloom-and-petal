from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Adds various artificial flower categories to the database'

    def handle(self, *args, **kwargs):
        # Sample category data
        categories = [
            {
                'name': 'Artificial Roses',
                'description': 'Beautiful artificial roses in various colors and arrangements. Perfect for home decor, weddings, and special occasions.'
            },
            {
                'name': 'Artificial Tulips',
                'description': 'Colorful artificial tulips that bring the beauty of spring into your home all year round.'
            },
            {
                'name': 'Artificial Orchids',
                'description': 'Elegant artificial orchids that add a touch of sophistication to any space without the maintenance.'
            },
            {
                'name': 'Artificial Sunflowers',
                'description': 'Bright and cheerful artificial sunflowers that bring warmth and happiness to any room.'
            },
            {
                'name': 'Artificial Lavender',
                'description': 'Fragrant-looking artificial lavender that adds a touch of Provence to your home decor.'
            },
            {
                'name': 'Artificial Peonies',
                'description': 'Luxurious artificial peonies that add elegance and beauty to any arrangement or display.'
            },
            {
                'name': 'Artificial Lilies',
                'description': 'Stunning artificial lilies that make a bold statement in any floral arrangement or home decor.'
            },
            {
                'name': 'Artificial Daisies',
                'description': 'Cheerful artificial daisies that bring a fresh, country feel to your home or event decor.'
            },
            {
                'name': 'Artificial Hydrangeas',
                'description': 'Full and lush artificial hydrangeas that create a dramatic and beautiful display in any setting.'
            },
        ]
        
        # Add categories to the database
        for category_data in categories:
            # Check if category already exists
            if Category.objects.filter(name=category_data['name']).exists():
                self.stdout.write(self.style.WARNING(f"Category already exists: {category_data['name']}"))
                continue
            
            # Create the category
            category = Category.objects.create(
                name=category_data['name'],
                description=category_data['description']
            )
            
            self.stdout.write(self.style.SUCCESS(f"Added category: {category.name}"))
        
        self.stdout.write(self.style.SUCCESS('Flower categories added successfully!')) 