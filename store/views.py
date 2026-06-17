from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .data import PRODUCTS, ORDERS, VALID_CATEGORIES,CATEGORY_NAMES
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Product,Order

#Допоміжні функції

def product_to_dict(product_id, product):
    """Перетворює товар у словник для JSON-відповіді."""
    return {
        "id": product_id,
        "name": product["name"],
        "price": product["price"],
        "category": product["category"],
        "stock": product["stock"],
        "available": product["stock"] > 0,
    }
 
 
def apply_filters(products_dict, sort=None, in_stock=False):
    """Застосовує фільтри та сортування до словника товарів."""
    items = [product_to_dict(pid, p) for pid, p in products_dict.items()]
 
    if in_stock:
        items = [p for p in items if p["available"]]
 
    if sort == "price_asc":
        items.sort(key=lambda p: p["price"])
    elif sort == "price_desc":
        items.sort(key=lambda p: p["price"], reverse=True)
    elif sort == "name":
        items.sort(key=lambda p: p["name"])
 
    return items

# Views функції

def home(request):
    latest_products = Product.objects.order_by('-id')[:5]
    return render(request, 'store/home.html', {
        'heading': "Головна сторінка",
        'totalProducts': Product.objects.count(),
        'available_products': Product.objects.filter(is_available=True).count(),
        'latest_products': latest_products
    })
 

def product_list(request):
  sort = request.GET.get("sort","")
  in_stock = request.GET.get("in_stock")=="1"
  price_min = request.GET.get("price_min")
  price_max = request.GET.get("price_max")
  categories = request.GET.getlist("category")

  price_min = int(price_min) if price_min else None
  price_max = int(price_max) if price_max else None

  

  products = apply_filters(
      PRODUCTS, 
      sort=sort, 
      in_stock=in_stock,
      price_min=price_min,
      price_max=price_max,
      categories=categories
      )

  return render(request,"store/product_list.html",{
      "products":products,
      "sort":sort,
      "in_stock":in_stock,
      "price_min": price_min,
      "price_max": price_max,
      "categories": categories,
      "all_categories": CATEGORY_NAMES.items()
  })

def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({"error": "Товар не знайдено"}, status=404)

    data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price),
        "sale_price": float(product.sale_rpice) if product.sale_rpice else None,
        "stock": product.stock,
        "available": product.available,
        "category": product.category.name if product.category else None,
    }

    return JsonResponse(data, json_dumps_params={"ensure_ascii": False, "indent": 2})


def order_list(request):
    orders = Order.objects.all()
    if not orders.exists():
        return JsonResponse({"message": "Замовлень поки немає", "orders": []}, json_dumps_params={"ensure_ascii": False, "indent": 2})

    data = [
        {
            "order_id": o.id,
            "product_name": o.product_name,
            "quantity": o.quantity,
            "total_price": float(o.total_price),
            "customer_name": o.customer_name,
            "phone": o.phone
        }
        for o in orders
    ]
    return JsonResponse({"count": len(data), "orders": data}, json_dumps_params={"ensure_ascii": False, "indent": 2})
  
# Завдання 5 
# http://127.0.0.1:8000/store/category/electronics/
def category_view(request, category):
    if category not in VALID_CATEGORIES:
        return JsonResponse({"error": "Невідома категорія"}, status=400, json_dumps_params={"ensure_ascii": False, "indent": 2})

    filtered_products = [
        product_to_dict(pid, p)
        for pid, p in PRODUCTS.items()
        if p["category"] == category
    ]

    return JsonResponse({
        "category": category,
        "category_name": CATEGORY_NAMES[category],
        "count": len(filtered_products),
        "products": filtered_products,
        }, 
        json_dumps_params={"ensure_ascii": False, "indent": 2})     

# Завдання 6 
# http://127.0.0.1:8000/store/search/?q=Книга
# http://127.0.0.1:8000/store/search/?q=test
def search(request):
    is_ajax = request.headers.get("X-Requested-With")=="XMLHttpRequest"
    query = request.GET.get("q", "").lower().strip()
    products = []

    if query:
     products = [
        product_to_dict(pid, p)
        for pid, p in PRODUCTS.items()
        if query in p["name"].lower().strip()
    ]
     
    if is_ajax:
       return JsonResponse(
          {"products":products},
          json_dumps_params={"ensure_ascii":False}
       )

    return render(request,"store/search.html",{
        "query": query,
        "count": len(products),
        "products": products
        })

# Завдання 7
# http://127.0.0.1:8000/store/order/1/
# http://127.0.0.1:8000/store/orders


@csrf_exempt
def order_views(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({"error": "Товар не знайдено"}, status=404)

    if request.method == "GET":
        return HttpResponse(f"""
            <h1>Оформлення замовлення для {product.name}</h1>
            <form method="POST">
              <input type="text" name="name" placeholder="Ім'я"> <br>
              <input type="text" name="phone" placeholder="Телефон"> <br>
              <input type="number" name="quantity" placeholder="Кількість" min="1"> <br>
              <button>Оформити замовлення</button>
            </form>
        """)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        quantity = request.POST.get("quantity", "").strip()

        errors = {}
        if not name:
            errors["name"] = "Ім'я є обов'язковим полем"
        if not phone:
            errors["phone"] = "Телефон є обов'язковим полем"
        if not quantity:
            errors["quantity"] = "Кількість є обов'язковим полем"

        if errors:
            return JsonResponse({"errors": errors}, status=400, json_dumps_params={"ensure_ascii": False, "indent": 2})

        quantity = int(quantity)
        if product.stock == 0:
            return JsonResponse({"error": "Товар відсутній на складі"}, status=400, json_dumps_params={"ensure_ascii": False, "indent": 2})

        total_price = product.price * quantity

        Order.objects.create(
            product_id=product.id,
            product_name=product.name,
            quantity=quantity,
            total_price=total_price,
            customer_name=name,
            phone=phone
        )

        return redirect("order_list")
  
# Завдання 9
# http://127.0.0.1:8000/store/old-catalog/
def old_catalog(request):
    response = redirect('product_list', permanent=True)
    response['X-Redirect-Reason'] = 'page-deprecated'
    return response


def apply_filters(products_dict, sort=None, in_stock=False, price_min=None, price_max=None, categories=None):
   
    items = [product_to_dict(pid, p) for pid, p in products_dict.items()]

    if in_stock:
        items = [p for p in items if p["available"]]

    if price_min:
        items = [p for p in items if p["price"] >= price_min]
    if price_max:
        items = [p for p in items if p["price"] <= price_max]

    if categories:
        items = [p for p in items if p["category"] in categories]

    if sort == "price_asc":
        items.sort(key=lambda p: p["price"])
    elif sort == "price_desc":
        items.sort(key=lambda p: p["price"], reverse=True)
    elif sort == "name":
        items.sort(key=lambda p: p["name"])

    return items