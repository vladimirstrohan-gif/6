from django.core.management.base import BaseCommand
from store.models import Category, Product, Order

class Command(BaseCommand):
    help = "Заповнює базу даних тестовими даними"

    def handle(self, *args, **kwargs):
        # Очистка старих даних
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Категорії
        electronics = Category.objects.create(
            name="Електроніка", slug="electronics"
        )
        clothing = Category.objects.create(
            name="Одяг", slug="clothing"
        )
        books = Category.objects.create(
            name="Книги", slug="books"
        )

        # Товари
        products = [
            Product(category=electronics, name="Ноутбук Lenovo",
                description="Потужний ноутбук для роботи і навчання",
                price=32000, stock=5, slug="noutbuk-lenovo"),
            Product(category=electronics, name="Смартфон Samsung",
                description="Флагманський смартфон з чудовою камерою",
                price=18000, stock=0, is_available=False, slug="smartfon-samsung"),
            Product(category=electronics, name="Навушники Sony",
                description="Бездротові навушники з шумозаглушенням",
                price=4500, stock=12, slug="navushnyky-sony"),
            Product(category=clothing, name="Футболка Nike",
                description="Спортивна футболка з дихаючого матеріалу",
                price=800, stock=30, slug="futbolka-nike"),
            Product(category=clothing, name="Джинси Levi's",
                description="Класичні джинси прямого крою",
                price=2200, stock=8, slug="dzhynsy-levis"),
            Product(category=books, name="Книга 'Clean Code'",
                description="Роберт Мартін про чистий код",
                price=650, stock=15, slug="knyha-clean-code"),
            Product(category=books, name="Книга 'Django для початківців'",
                description="Практичний посібник з Django",
                price=480, stock=3, slug="knyha-django-dlya-pochatkivciv"),
        ]
        Product.objects.bulk_create(products)

        # Замовлення (беремо товари по slug)
        p1 = Product.objects.get(slug="noutbuk-lenovo")
        p2 = Product.objects.get(slug="knyha-django-dlya-pochatkivciv")
        p3 = Product.objects.get(slug="navushnyky-sony")

        Order.objects.create(
            product_id=p1.id,
            product_name=p1.name,
            quantity=2,
            total_price=p1.price * 2,
            customer_name="Іван",
            phone="+380501234567"
        )
        Order.objects.create(
            product_id=p2.id,
            product_name=p2.name,
            quantity=1,
            total_price=p2.price,
            customer_name="Олена",
            phone="+380671234567"
        )
        Order.objects.create(
            product_id=p3.id,
            product_name=p3.name,
            quantity=3,
            total_price=p3.price * 3,
            customer_name="Петро",
            phone="+380931234567"
        )

        self.stdout.write(self.style.SUCCESS(
            f"Створено {Category.objects.count()} категорій, "
            f"{Product.objects.count()} товарів і {Order.objects.count()} замовлень"
        ))
