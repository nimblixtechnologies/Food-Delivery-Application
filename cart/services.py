from .models import MenuItem, PromoCode


def calculate_total(data):
    items = data.get("items", [])
    promo_code_value = data.get("promo_code")

    subtotal = 0
    total_tax = 0
    delivery_charge = 0
    discount = 0

    if not items:
        return {"error": "No items provided"}

    for item in items:
        menu_item_id = item.get("menu_item_id")
        quantity = item.get("quantity", 1)

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            return {"error": f"Menu item {menu_item_id} not found"}

        item_total = menu_item.price * quantity
        item_tax = (item_total * menu_item.tax_percentage) / 100

        subtotal += item_total
        total_tax += item_tax

        # Delivery charge from restaurant
        delivery_charge = menu_item.restaurant.delivery_charge

    # Apply promo code if exists
    if promo_code_value:
        try:
            promo = PromoCode.objects.get(code=promo_code_value, is_active=True)
            discount = (subtotal * promo.discount_percentage) / 100
        except PromoCode.DoesNotExist:
            pass

    final_amount = subtotal + total_tax + delivery_charge - discount

    return {
        "subtotal": subtotal,
        "tax": total_tax,
        "delivery_charge": delivery_charge,
        "discount": discount,
        "final_amount": final_amount
    }
