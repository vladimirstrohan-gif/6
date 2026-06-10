from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .data import PRODUCTS, ORDERS, VALID_CATEGORIES,CATEGORY_NAMES
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

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
  totalProducts = len(PRODUCTS)
  context ={
     'totalProducts':totalProducts,
     'heading':'My Store'
  }

  return render(request,"store/home.html",context)
 

def product_list(request):
  sort = request.GET.get("sort","")
  in_stock = request.GET.get("in_stock")=="1"

  products = apply_filters(PRODUCTS, sort=sort, in_stock=in_stock)

  return JsonResponse({
    "filters":{
      "sort":sort or None,
      "in_stock": in_stock,
    },
    "count": len(products),
    "products": products,
  },json_dumps_params={"ensure_ascii":False,"indent":2})

def product_detail(request, product_id):
  product = PRODUCTS.get(product_id)
  if  product is None:
    return JsonResponse({"error":"Товар не знайдено"}, status=404, json_dumps_params={"ensure_ascii":False,"indent":2})

  return JsonResponse(product_to_dict(product_id, product), json_dumps_params={"ensure_ascii":False,"indent":2})


def order_list(request):
  if not ORDERS:
    return JsonResponse( 
       {"message": "Замовлень поки немає", "orders": []}, 
       json_dumps_params={"ensure_ascii":False,"indent":2})
  return JsonResponse({
     "count": len(ORDERS),
     "orders": ORDERS
     }, json_dumps_params={"ensure_ascii":False,"indent":2})
  
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
def search_view(request):
    
    query = request.GET.get("q", "").lower()
    if not query:
        return JsonResponse({"error": "Параметр 'q' є обов'язковим"}, status=400, json_dumps_params={"ensure_ascii": False, "indent": 2})

    matched_products = [
        product_to_dict(pid, p)
        for pid, p in PRODUCTS.items()
        if query in p["name"].lower()
    ]

    return JsonResponse({
        "query": query,
        "count": len(matched_products),
        "products": matched_products,
        }, 
        json_dumps_params={"ensure_ascii": False, "indent": 2})

# Завдання 7
# http://127.0.0.1:8000/store/order/1/
# http://127.0.0.1:8000/store/orders


@csrf_exempt
def order_views(request,product_id):
  product = PRODUCTS.get(product_id)

  if  product is None:
    return JsonResponse({"error":"Товар не знайдено"}, status=404, json_dumps_params={"ensure_ascii":False,"indent":2})

  if request.method == "GET":
     return HttpResponse(f"""
                      <h1>Оформлення замовлення для {product["name"]}</h1>
                      <form method="POST">
                        <input type="text" name="name" placeholder="Ім'я"> <br>
                        <input type="text" name="phone" placeholder="Телефон"> <br>
                        <input type="text" name="quantity" placeholder="Кількість"> <br>
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
    
    if product["stock"] == 0:
      return JsonResponse({"error":"Товар відсутній на складі"}, status=400, json_dumps_params={"ensure_ascii":False,"indent":2})
    order ={
            "order_id": len(ORDERS) + 1,
            "product_id": product_id,
            "product_name": product["name"],
            "quantity": request.POST.get("quantity"),
            "total_price": int(request.POST.get("quantity")) * product["price"],
            "customer_name": request.POST.get("name"),
            "phone": request.POST.get("phone"),
            }
    ORDERS.append(order)
    return redirect ("order_list")
  
# Завдання 9
# http://127.0.0.1:8000/store/old-catalog/
def old_catalog(request):
    response = redirect('product_list', permanent=True)
    response['X-Redirect-Reason'] = 'page-deprecated'
    return response