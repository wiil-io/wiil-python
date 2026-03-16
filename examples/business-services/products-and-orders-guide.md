# Product Management Guide (Python)

This guide covers managing product catalogs and retail orders using the WIIL Python SDK.

## Quick Start

```python
from time import time

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateBusinessProduct,
    CreateProductCategory,
    CreateProductOrder,
    OrderAddress,
    OrderPricing,
    ProductOrderItemBase,
)

client = WiilClient(api_key="your-api-key")
now_ms = int(time() * 1000)

category = client.products.create_category(
    CreateProductCategory(
        name="Electronics",
        description="Electronic devices and accessories",
        display_order=1,
    )
)

product = client.products.create(
    CreateBusinessProduct(
        name="Wireless Mouse",
        description="Ergonomic wireless mouse with 6 buttons",
        price=29.99,
        sku="WM-2024-BLK",
        barcode="123456789012",
        category_id=category.id,
        brand="TechBrand",
        track_inventory=True,
        stock_quantity=150,
        low_stock_threshold=20,
        weight=0.25,
        is_active=True,
    )
)

order = client.product_orders.create(
    CreateProductOrder(
        items=[
            ProductOrderItemBase(
                product_id=product.id,
                item_name=product.name,
                sku=product.sku,
                quantity=2,
                unit_price=product.price,
                total_price=product.price * 2,
            )
        ],
        customer_id="cust_123",
        pricing=OrderPricing(
            subtotal=59.98,
            tax=4.80,
            shipping_amount=9.99,
            total=74.77,
            currency="USD",
        ),
        order_date=now_ms,
        shipping_address=OrderAddress(
            street="123 Main St",
            city="New York",
            state="NY",
            postal_code="10001",
            country="US",
        ),
        source="web",
    )
)

print("Created product:", product.id)
print("Created order:", order.id)
```

## Product Categories

```python
from wiil.models.business_mgt import CreateProductCategory, UpdateProductCategory
from wiil.types import PaginationRequest

# Create
category = client.products.create_category(
    CreateProductCategory(name="Accessories", description="Add-ons")
)

# Get
category = client.products.get_category(category.id)

# List
categories = client.products.list_categories(PaginationRequest(page=1, page_size=20))
print(categories.meta.total_count)

# Update
updated = client.products.update_category(
    UpdateProductCategory(id=category.id, name="Premium Accessories")
)

# Delete
deleted = client.products.delete_category(updated.id)
print("Deleted:", deleted)
```

## Products

```python
from wiil.models.business_mgt import CreateBusinessProduct, UpdateBusinessProduct
from wiil.types import PaginationRequest

product = client.products.create(
    CreateBusinessProduct(
        name="Wireless Headphones",
        description="Premium noise-canceling wireless headphones",
        price=199.99,
        category_id="category_electronics",
        sku="WH-2024-BLK",
        track_inventory=True,
        stock_quantity=75,
        is_active=True,
    )
)

by_id = client.products.get(product.id)
by_sku = client.products.get_by_sku("WH-2024-BLK")

results = client.products.list(
    params=PaginationRequest(page=1, page_size=50),
    include_deleted=False,
)

updated = client.products.update(
    UpdateBusinessProduct(id=product.id, price=179.99, stock_quantity=100)
)

deleted = client.products.delete(updated.id)
print(by_id.name, by_sku.name, len(results.data), deleted)
```

## Product Orders

```python
from wiil.models.business_mgt import CreateProductOrder, OrderPricing, ProductOrderItemBase
from wiil.types import PaginationRequest

order = client.product_orders.create(
    CreateProductOrder(
        items=[
            ProductOrderItemBase(
                product_id="prod_123",
                item_name="Wireless Headphones",
                sku="WH-2024-BLK",
                quantity=2,
                unit_price=79.99,
                total_price=159.98,
            )
        ],
        customer_id="cust_789",
        pricing=OrderPricing(subtotal=159.98, tax=14.40, shipping_amount=9.99, total=184.37),
        order_date=int(time() * 1000),
        shipping_method="Standard",
        source="web",
    )
)

order_details = client.product_orders.get(order.id)
customer_orders = client.product_orders.get_by_customer(
    "cust_789", PaginationRequest(page=1, page_size=20)
)

print(order_details.status, customer_orders.meta.total_count)
```

## Batch Operations

Create multiple product categories and products efficiently.

### Create Categories in Batch

```python
from wiil.models.business_mgt import CreateProductCategory

categories = client.products.create_category_batch([
    CreateProductCategory(name="Electronics", display_order=1),
    CreateProductCategory(name="Clothing", display_order=2),
    CreateProductCategory(name="Accessories", display_order=3),
])

print(f"Created {len(categories.data)} categories")
for category in categories.data:
    print(f"  - {category.name}")
```

**Limits:** Maximum 50 categories per batch

### Create Products in Batch

```python
from wiil.models.business_mgt import CreateBusinessProduct

products = client.products.create_batch([
    CreateBusinessProduct(
        name="Wireless Earbuds",
        description="Bluetooth 5.0 earbuds",
        price=79.99,
        sku="ELEC-001",
        category_id="cat_electronics",
        is_active=True,
    ),
    CreateBusinessProduct(
        name="Cotton T-Shirt",
        description="100% cotton, various sizes",
        price=24.99,
        sku="CLTH-001",
        category_id="cat_clothing",
        is_active=True,
    ),
    CreateBusinessProduct(
        name="Leather Wallet",
        description="Genuine leather bifold",
        price=49.99,
        sku="ACCS-001",
        category_id="cat_accessories",
        is_active=True,
    ),
])

print(f"Created {len(products.data)} products")
for product in products.data:
    print(f"  - {product.name}: ${product.price}")
```

**Limits:** Maximum 100 products per batch

### Handling Batch Errors

Batch operations validate each item and report errors with index information:

```python
from wiil.errors import WiilValidationError
from wiil.models.business_mgt import CreateBusinessProduct

try:
    products = client.products.create_batch([
        CreateBusinessProduct(name="Valid Product", price=10.00, sku="SKU-001"),
        CreateBusinessProduct(name="", price=10.00, sku="SKU-002"),  # Invalid: empty name
    ])
except WiilValidationError as e:
    print(f"Validation error: {e.message}")
    for detail in e.details:
        print(f"  - {detail}")
```
