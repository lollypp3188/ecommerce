from decimal import Decimal
from store.models import Product


class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get('cart')

        if 'cart' not in self.session:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product, product_qty):
        """Add or update product in the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['qty'] += int(product_qty)
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': int(product_qty)}
        self.session.modified = True

    def __len__(self):
        return sum(int(item['qty']) for item in self.cart.values())

    def __iter__(self):
        all_products_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_products_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
