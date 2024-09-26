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
    cart = Cart(request)
    if request.POST.get('action') == 'delete':
        product_id = request.POST.get('product_id')

        if product_id:
            cart.delete(product=product_id)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()

            return JsonResponse({
                'qty': cart_quantity,
                'cart_total': cart_total
            })

        return JsonResponse({'error': 'Product ID is missing'}, status=400)

    return JsonResponse({'error': 'Invalid action'}, status=400)



def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') != 'post':
        return JsonResponse({'error': 'Invalid action'}, status=400)
    product_id = request.POST.get('product_id')
    if not product_id:
        return JsonResponse({'error': 'Product ID is missing'}, status=400)

    product_quantity = request.POST.get('product_quantity')
    if not product_quantity or not product_quantity.isdigit():
        return JsonResponse({'error': 'Invalid product quantity'}, status=400)

    product_quantity = int(product_quantity)
    if product_quantity <= 0:
        return JsonResponse({'error': 'Product quantity must be greater than zero'}, status=400)

    cart.update(product=product_id, qty=product_quantity)

    cart_quantity = cart.__len__()
    cart_total = cart.get_total()

    return JsonResponse({
        'qty': cart_quantity,
        'cart_total': cart_total
    })

