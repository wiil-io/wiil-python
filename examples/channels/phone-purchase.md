# Phone Number Purchase Guide

Use this guide to discover numbers with the Python SDK, then map purchased numbers to WIIL channels.

## Important SDK Note

The current Python SDK exposes telephony discovery endpoints:

- `client.telephony_provider.get_phone_numbers(...)`
- `client.telephony_provider.get_pricing(...)`

If your account uses a separate purchase workflow, complete purchase outside this SDK, then use `client.phone_configs` to retrieve channel IDs.

## Discover Regions and Numbers

```python
from wiil import WiilClient
from wiil.types import ProviderType

client = WiilClient(api_key="YOUR_API_KEY")

numbers = client.telephony_provider.get_phone_numbers(
    ProviderType.SIGNALWIRE,
    "US",
    area_code="212",
    contains="555",
)

for number in numbers[:10]:
    print(number.phone_number, number.country_code, number.number_type)
```

## Check Pricing

```python
from wiil import WiilClient
from wiil.types import ProviderType

client = WiilClient(api_key="YOUR_API_KEY")

pricing = client.telephony_provider.get_pricing(ProviderType.SIGNALWIRE, "US")
for p in pricing:
    print(p.number_type, p.current_price)
```

## Retrieve Channel IDs After Purchase

Once a number is purchased and provisioned in your environment, fetch the generated channel IDs:

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

phone_config = client.phone_configs.get_by_phone_number("+12125551234")
print("status:", phone_config.status)
print("voice_channel_id:", phone_config.voice_channel_id)
print("sms_channel_id:", phone_config.sms_channel_id)
```

## Optional Lookup by Request ID

If your purchase workflow returns a request ID:

```python
from wiil import WiilClient

client = WiilClient(api_key="YOUR_API_KEY")

phone_config = client.phone_configs.get_by_request_id("YOUR_REQUEST_ID")
print(phone_config.phone_number, phone_config.status)
```

[Back to channels home](./README.md)
