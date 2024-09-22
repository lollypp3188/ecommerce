from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import uuid


def cart_summary(request):
  cart = Cart(request)
  context = {'cart': cart}
  return render(request, 'cart/cart-summary.html', context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')

        try:
            product_id = int(product_id)
        except ValueError:
            try:
                product_id = uuid.UUID(product_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid product ID format'}, status=400)

        product_quantity = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, product_qty=product_quantity)

        cart_quantity = cart.__len__()

        response = JsonResponse({
            'qty': cart_quantity
        })
        return response

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_delete(request):
  pass


def cart_update(request):
  pass