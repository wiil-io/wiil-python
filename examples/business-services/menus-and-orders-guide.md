# Menu Management Guide (Python)

This guide covers managing restaurant menus and food service orders using the WIIL Python SDK.

## Quick Start

```python
from time import time

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateBusinessMenuItem,
    CreateMenuCategory,
    CreateMenuOrder,
    MenuOrderItemBase,
    OrderPricing,
)

client = WiilClient(api_key="your-api-key")
now_ms = int(time() * 1000)

category = client.menus.create_category(
    CreateMenuCategory(name="Main Courses", description="Signature entrees", display_order=1)
)

menu_item = client.menus.create_item(
    CreateBusinessMenuItem(
        name="Cheeseburger",
        description="Angus beef with aged cheddar",
        price=12.99,
        category_id=category.id,
        ingredients=["beef", "cheese", "lettuce", "tomato", "bun"],
        allergens=["gluten", "dairy"],
        is_available=True,
        preparation_time=15,
        is_active=True,
    )
)

order = client.menu_orders.create(
    CreateMenuOrder(
        type="takeout",
        items=[
            MenuOrderItemBase(
                menu_item_id=menu_item.id,
                item_name=menu_item.name,
                quantity=2,
                unit_price=menu_item.price,
                total_price=menu_item.price * 2,
            )
        ],
        customer_id="cust_123",
        pricing=OrderPricing(subtotal=25.98, tax=2.60, tip=5.00, total=33.58, currency="USD"),
        order_date=now_ms,
        source="web",
    )
)

print("Created menu item:", menu_item.id)
print("Created menu order:", order.id)
```

## Menu Categories

```python
from wiil.models.business_mgt import CreateMenuCategory, UpdateMenuCategory

category = client.menus.create_category(
    CreateMenuCategory(name="Appetizers", description="Start your meal right", display_order=1)
)

loaded = client.menus.get_category(category.id)
categories = client.menus.list_categories()

updated = client.menus.update_category(
    UpdateMenuCategory(id=category.id, name="Premium Appetizers", display_order=2)
)

deleted = client.menus.delete_category(updated.id)
print(loaded.name, len(categories), deleted)
```

## Menu Items

```python
from wiil.models.business_mgt import CreateBusinessMenuItem, UpdateBusinessMenuItem
from wiil.types import PaginationRequest

item = client.menus.create_item(
    CreateBusinessMenuItem(
        name="Caesar Salad",
        description="Fresh romaine with house-made dressing",
        price=9.99,
        category_id="cat_123",
        preparation_time=10,
        is_available=True,
    )
)

fetched = client.menus.get_item(item.id)
all_items = client.menus.list_items(PaginationRequest(page=1, page_size=50), include_deleted=False)
by_category = client.menus.get_items_by_category("cat_123", include_unavailable=False)
popular = client.menus.get_popular_items(limit=10)

updated = client.menus.update_item(
    UpdateBusinessMenuItem(id=item.id, price=10.99, is_available=True)
)

deleted = client.menus.delete_item(updated.id)
print(fetched.name, len(all_items.data), len(by_category), len(popular), deleted)
```

## Menu Orders

```python
from wiil.models.business_mgt import CreateMenuOrder, MenuOrderItemBase, OrderPricing
from wiil.types import PaginationRequest

order = client.menu_orders.create(
    CreateMenuOrder(
        type="delivery",
        items=[
            MenuOrderItemBase(
                menu_item_id="item_123",
                item_name="Cheeseburger",
                quantity=2,
                unit_price=12.99,
                total_price=25.98,
                special_instructions="No onions",
            )
        ],
        customer_id="cust_456",
        pricing=OrderPricing(subtotal=25.98, tax=2.60, tip=5.00, total=33.58),
        order_date=int(time() * 1000),
        source="web",
    )
)

loaded = client.menu_orders.get(order.id)
customer_orders = client.menu_orders.get_by_customer(
    "cust_456", PaginationRequest(page=1, page_size=20)
)

updated_status = client.menu_orders.update_status(order.id, "confirmed")
cancelled = client.menu_orders.cancel(order.id, reason="Customer requested cancellation")

print(loaded.id, customer_orders.meta.total_count, updated_status.status, cancelled.status)
```
