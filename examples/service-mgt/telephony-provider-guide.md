# Telephony Provider Guide

This guide covers accessing telephony provider services using the WIIL Platform Python SDK. The telephony provider resource allows you to discover available phone numbers, check pricing, and purchase phone numbers for AI deployments.

## Quick Start

```python
import os
from wiil import WiilClient

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

# Get available phone numbers
numbers = client.telephony_provider.get_phone_numbers()

print('Available numbers:', len(numbers))
for num in numbers:
    print(f'- {num.phone_number} ({num.friendly_name})')
```

## Architecture Overview

The telephony provider resource provides:

- **Phone Number Discovery**: Search for available phone numbers by area code, region, or capabilities
- **Pricing Information**: Get current pricing for different phone number types
- **Phone Number Purchase**: Acquire phone numbers for use in call/SMS deployments
- **Purchase Status Tracking**: Monitor the status of phone number purchases

## Phone Number Search Options

| Field | Type | Description |
|-------|------|-------------|
| area_code | str | Area code filter (e.g., '206', '415') |
| contains | str | Number pattern to search for |
| postal_code | str | Postal code filter |

## Operations

### Get Available Phone Numbers

```python
# Get all available numbers
numbers = client.telephony_provider.get_phone_numbers()

print('Found', len(numbers), 'available phone numbers')

for num in numbers:
    print(f'{num.phone_number}:')
    print(f'  Friendly Name: {num.friendly_name}')
    if num.capabilities:
        print(f'  Capabilities: {", ".join(num.capabilities)}')
```

### Filter Phone Numbers by Area Code

```python
numbers = client.telephony_provider.get_phone_numbers(
    area_code='206'
)

print('Seattle area numbers:', len(numbers))
for num in numbers:
    print(f'- {num.phone_number}')
```

### Filter by Pattern (Contains)

```python
numbers = client.telephony_provider.get_phone_numbers(
    contains='555'
)

print('Numbers containing 555:', len(numbers))
```

### Filter by Postal Code

```python
numbers = client.telephony_provider.get_phone_numbers(
    postal_code='98101'
)

print('Numbers in postal code 98101:', len(numbers))
```

### Get Pricing Information

```python
pricing = client.telephony_provider.get_pricing()

print('Phone number pricing:')
for price in pricing:
    print(f'  {price.number_type}: ${price.price}')
```

### Purchase a Phone Number

```python
from wiil.models.service_mgt import PurchasePhoneNumber

# Search for available numbers
numbers = client.telephony_provider.get_phone_numbers(
    area_code='415'
)

if len(numbers) == 0:
    raise Exception('No numbers available in this area')

# Purchase the first available number
purchase = client.telephony_provider.purchase(
    PurchasePhoneNumber(
        phone_number=numbers[0].phone_number,
        friendly_name='Customer Support Line'
    )
)

print('Purchase initiated:')
print('  Phone Number:', purchase.phone_number)
print('  Purchase ID:', purchase.id)
print('  Status:', purchase.status)
```

### Check Purchase Status

```python
# The purchase() method automatically polls until completion
# But you can also manually check status:

status = client.telephony_provider.get_purchase_status('purchase_123')

print('Purchase Status:')
print('  ID:', status.id)
print('  Phone Number:', status.phone_number)
print('  Status:', status.status)
```

## Phone Purchase Status Values

```python
from wiil.models.service_mgt import PhonePurchaseStatus

# Available values:
PhonePurchaseStatus.PENDING      # 'pending' - Purchase initiated
PhonePurchaseStatus.PROCESSING   # 'processing' - Being processed by provider
PhonePurchaseStatus.COMPLETED    # 'completed' - Successfully purchased
PhonePurchaseStatus.FAILED       # 'failed' - Purchase failed
PhonePurchaseStatus.CANCELLED    # 'cancelled' - Purchase cancelled
```

## Complete Example

```python
import os
from wiil import WiilClient
from wiil.models.service_mgt import PhonePurchaseStatus, PurchasePhoneNumber

client = WiilClient(
    api_key=os.environ['WIIL_API_KEY']
)

def explore_telephony_provider():
    # 1. Get pricing information
    print('Fetching pricing information...')
    pricing = client.telephony_provider.get_pricing()

    print('\nPhone number pricing:')
    for p in pricing:
        print(f'  {p.number_type}: ${p.price}')

    # 2. Search for available numbers
    print('\nSearching for available phone numbers...')
    numbers = client.telephony_provider.get_phone_numbers()

    print(f'Found {len(numbers)} available numbers')

    if len(numbers) == 0:
        print('No numbers available')
        return

    # Display first 5 numbers
    print('\nFirst 5 available numbers:')
    for num in numbers[:5]:
        print(f'  {num.phone_number} - {num.friendly_name}')

    # 3. Search with area code filter
    print('\nSearching for 206 area code numbers...')
    seattle_numbers = client.telephony_provider.get_phone_numbers(
        area_code='206'
    )

    print(f'Found {len(seattle_numbers)} numbers in 206 area code')

    # 4. Example purchase (commented out to prevent actual purchases)
    """
    print('\nPurchasing phone number...')
    purchase = client.telephony_provider.purchase(
        PurchasePhoneNumber(
            phone_number=numbers[0].phone_number,
            friendly_name='Test Support Line'
        )
    )

    print('Purchase result:')
    print('  ID:', purchase.id)
    print('  Number:', purchase.phone_number)
    print('  Status:', purchase.status)

    if purchase.status == PhonePurchaseStatus.COMPLETED:
        print('Phone number successfully purchased!')
    """

if __name__ == '__main__':
    explore_telephony_provider()
```

## Best Practices

1. **Check availability before purchasing** - Always search for available numbers first and select from the results.

2. **Use area codes strategically** - Filter by area code to get numbers that match your target audience's location.

3. **Set meaningful friendly names** - Use descriptive friendly names to identify phone numbers in your admin console.

4. **Handle purchase polling** - The `purchase()` method automatically polls until completion. The default timeout is 2 minutes.

5. **Plan for failures** - Phone number purchases can fail due to carrier issues. Always handle the FAILED status gracefully.

## Troubleshooting

### No Numbers Available

**Error:**

```text
No phone numbers available
```

**Solution:**
Try different filter criteria or check with a different area code:

```python
# Try multiple area codes
area_codes = ['206', '415', '212', '310']

for area_code in area_codes:
    numbers = client.telephony_provider.get_phone_numbers(area_code=area_code)
    if len(numbers) > 0:
        print(f'Found {len(numbers)} numbers in area code {area_code}')
        break
```

### Purchase Timeout

**Error:**

```text
Error: Phone number purchase timed out after 120000ms
```

**Solution:**
The purchase is still processing on the provider side. Check the status manually:

```python
# If you have the purchase ID, check status
status = client.telephony_provider.get_purchase_status(purchase_id)

if status.status == PhonePurchaseStatus.PROCESSING:
    print('Purchase still processing, please wait...')
elif status.status == PhonePurchaseStatus.COMPLETED:
    print('Purchase completed:', status.phone_number)
```

### Invalid Phone Number Format

**Error:**

```text
WiilValidationError: Phone number must be in E.164 format
```

**Solution:**
Ensure phone numbers are in E.164 format (+1XXXXXXXXXX for US numbers):

```python
# Always use the phone_number value returned from get_phone_numbers()
numbers = client.telephony_provider.get_phone_numbers()
phone_number = numbers[0].phone_number  # Already in correct format

purchase = client.telephony_provider.purchase(
    PurchasePhoneNumber(
        phone_number=phone_number,  # Use as-is
        friendly_name='Support Line'
    )
)
```
