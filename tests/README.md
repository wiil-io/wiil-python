# WIIL Python SDK - Test Suite

Comprehensive test suite for the WIIL Python SDK covering all resources, error handling, and edge cases.

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── README.md                      # This file
├── unit/                          # Unit tests
│   ├── __init__.py
│   └── resources/                 # Resource tests
│       ├── __init__.py
│       ├── account/               # Account resource tests
│       │   ├── __init__.py
│       │   ├── test_organizations.py
│       │   └── test_projects.py
│       ├── business_mgt/          # Business management resource tests
│       │   ├── __init__.py
│       │   ├── test_customers.py
│       │   ├── test_menus.py
│       │   ├── test_products.py
│       │   ├── test_menu_orders.py
│       │   ├── test_product_orders.py
│       │   ├── test_reservations.py
│       │   ├── test_reservation_resources.py
│       │   ├── test_service_appointments.py
│       │   └── test_business_services.py
│       └── service_mgt/           # Service management resource tests
│           ├── __init__.py
│           ├── test_agent_configs.py
│           ├── test_deployment_configs.py
│           ├── test_deployment_channels.py
│           ├── test_instruction_configs.py
│           ├── test_phone_configs.py
│           ├── test_provisioning_configs.py
│           ├── test_conversation_configs.py
│           ├── test_translation_sessions.py
│           └── test_knowledge_sources.py
└── integration/                   # Integration tests (future)
    └── __init__.py
```

## Prerequisites

### Install Dependencies

```bash
# Install package with dev dependencies
pip install -e ".[dev]"

# Or install test dependencies directly
pip install pytest pytest-asyncio pytest-cov respx httpx
```

### Dependencies Used

- **pytest**: Test framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Code coverage reporting
- **respx**: HTTP mocking (Python equivalent of nock)
- **httpx**: HTTP client used by the SDK

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/unit/resources/service_mgt/test_agent_configs.py
```

### Run Specific Test Class

```bash
pytest tests/unit/resources/service_mgt/test_agent_configs.py::TestAgentConfigurationsResource
```

### Run Specific Test Method

```bash
pytest tests/unit/resources/service_mgt/test_agent_configs.py::TestAgentConfigurationsResource::test_create_agent_configuration
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Output Capture Disabled

```bash
pytest -s
```

### Run Tests Matching Pattern

```bash
# Run all customer tests
pytest -k customers

# Run all create tests
pytest -k create

# Run all tests except slow ones
pytest -m "not slow"
```

## Code Coverage

### Generate Coverage Report

```bash
# Terminal report
pytest --cov=wiil --cov-report=term-missing

# HTML report
pytest --cov=wiil --cov-report=html

# Open HTML report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov\index.html  # Windows
```

### Coverage Goals

- **Target Coverage**: 90%+
- **Critical Modules**: 95%+ (client, errors, resources)
- **Models**: 80%+ (validated through Pydantic)

## Test Fixtures

### Available Fixtures

Defined in `conftest.py`:

#### `client`
Returns a configured `WiilClient` instance for testing.

```python
def test_example(client):
    result = client.customers.get("cust_123")
```

#### `mock_api`
Enables respx HTTP mocking context.

```python
def test_example(client, mock_api):
    mock_api.get("https://api.wiil.io/v1/customers/123").mock(
        return_value=Response(200, json={...})
    )
```

#### `api_response`
Helper function to create standardized API responses.

```python
def test_example(client, mock_api, api_response):
    mock_response = {"id": "123", "name": "Test"}
    mock_api.get(...).mock(
        return_value=Response(200, json=api_response(mock_response))
    )
```

#### `error_response`
Helper function to create standardized error responses.

```python
def test_example(client, mock_api, error_response):
    mock_api.get(...).mock(
        return_value=Response(
            404,
            json=error_response("NOT_FOUND", "Resource not found")
        )
    )
```

## Test Patterns

### Standard Resource Test Pattern

Each resource test file follows this pattern:

```python
"""Tests for [Resource Name] resource."""

import pytest
import respx
from httpx import Response

from wiil import WiilClient
from wiil.errors import WiilAPIError


BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class Test[ResourceName]Resource:
    """Test suite for [ResourceName]Resource."""

    def test_create(self, client, mock_api, api_response):
        """Test creating a new resource."""
        # Arrange
        input_data = {...}
        mock_response = {...}
        mock_api.post(...).mock(return_value=Response(200, json=api_response(mock_response)))

        # Act
        result = client.resource.create(**input_data)

        # Assert
        assert result.id == "expected_id"

    def test_get(self, client, mock_api, api_response):
        """Test retrieving a resource by ID."""
        # ...

    def test_get_not_found(self, client, mock_api, error_response):
        """Test API error when resource not found."""
        # ...

    def test_update(self, client, mock_api, api_response):
        """Test updating a resource."""
        # ...

    def test_delete(self, client, mock_api, api_response):
        """Test deleting a resource."""
        # ...

    def test_list(self, client, mock_api, api_response):
        """Test listing resources with pagination."""
        # ...

    def test_list_with_pagination(self, client, mock_api, api_response):
        """Test listing resources with custom pagination."""
        # ...
```

### Testing HTTP Methods

#### POST Requests

```python
def test_create(self, client, mock_api, api_response):
    mock_api.post(
        f"{BASE_URL}/resources",
        headers={"X-WIIL-API-Key": API_KEY}
    ).mock(return_value=Response(200, json=api_response({...})))

    result = client.resources.create(name="Test")
```

#### GET Requests

```python
def test_get(self, client, mock_api, api_response):
    mock_api.get(
        f"{BASE_URL}/resources/123",
        headers={"X-WIIL-API-Key": API_KEY}
    ).mock(return_value=Response(200, json=api_response({...})))

    result = client.resources.get("123")
```

#### PATCH Requests

```python
def test_update(self, client, mock_api, api_response):
    mock_api.patch(
        f"{BASE_URL}/resources",
        headers={"X-WIIL-API-Key": API_KEY}
    ).mock(return_value=Response(200, json=api_response({...})))

    result = client.resources.update(id="123", name="Updated")
```

#### DELETE Requests

```python
def test_delete(self, client, mock_api, api_response):
    mock_api.delete(
        f"{BASE_URL}/resources/123",
        headers={"X-WIIL-API-Key": API_KEY}
    ).mock(return_value=Response(200, json=api_response(True)))

    result = client.resources.delete("123")
```

### Testing Error Handling

```python
def test_not_found_error(self, client, mock_api, error_response):
    mock_api.get(
        f"{BASE_URL}/resources/invalid",
        headers={"X-WIIL-API-Key": API_KEY}
    ).mock(return_value=Response(
        404,
        json=error_response("NOT_FOUND", "Resource not found")
    ))

    with pytest.raises(WiilAPIError) as exc_info:
        client.resources.get("invalid")

    assert exc_info.value.status_code == 404
    assert exc_info.value.code == "NOT_FOUND"
    assert "not found" in exc_info.value.message.lower()
```

### Testing Pagination

```python
def test_list_with_pagination(self, client, mock_api, api_response):
    mock_response = {
        "data": [...],
        "meta": {
            "page": 2,
            "pageSize": 50,
            "totalCount": 100,
            "totalPages": 2,
            "hasNextPage": False,
            "hasPreviousPage": True,
        },
    }

    mock_api.get(
        f"{BASE_URL}/resources?page=2&pageSize=50",
        headers={"X-WIIL-API-Key": API_KEY}
    ).mock(return_value=Response(200, json=api_response(mock_response)))

    result = client.resources.list(page=2, page_size=50)

    assert result.meta.page == 2
    assert result.meta.page_size == 50
    assert result.meta.has_previous_page is True
```

## Test Coverage by Resource

### Service Management Resources (9 resources)

| Resource | Test File | Status |
|----------|-----------|--------|
| Agent Configurations | `test_agent_configs.py` | ✅ Implemented |
| Deployment Configurations | `test_deployment_configs.py` | 📝 Template Ready |
| Deployment Channels | `test_deployment_channels.py` | 📝 Template Ready |
| Instruction Configurations | `test_instruction_configs.py` | 📝 Template Ready |
| Phone Configurations | `test_phone_configs.py` | 📝 Template Ready |
| Provisioning Configurations | `test_provisioning_configs.py` | 📝 Template Ready |
| Conversation Configurations | `test_conversation_configs.py` | 📝 Template Ready |
| Translation Sessions | `test_translation_sessions.py` | 📝 Template Ready |
| Knowledge Sources | `test_knowledge_sources.py` | 📝 Template Ready |

### Business Management Resources (9 resources)

| Resource | Test File | Status |
|----------|-----------|--------|
| Customers | `test_customers.py` | ✅ Implemented |
| Menus | `test_menus.py` | 📝 Template Ready |
| Menu Orders | `test_menu_orders.py` | 📝 Template Ready |
| Products | `test_products.py` | 📝 Template Ready |
| Product Orders | `test_product_orders.py` | 📝 Template Ready |
| Reservations | `test_reservations.py` | 📝 Template Ready |
| Reservation Resources | `test_reservation_resources.py` | 📝 Template Ready |
| Service Appointments | `test_service_appointments.py` | 📝 Template Ready |
| Business Services | `test_business_services.py` | 📝 Template Ready |

### Account Resources (2 resources)

| Resource | Test File | Status |
|----------|-----------|--------|
| Organizations | `test_organizations.py` | 📝 Template Ready |
| Projects | `test_projects.py` | 📝 Template Ready |

## Continuous Integration

### GitHub Actions (Example)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Run tests with coverage
      run: |
        pytest --cov=wiil --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

## Best Practices

### 1. Test Naming

- Use descriptive test names: `test_create_customer_with_valid_data`
- Follow pattern: `test_<action>_<scenario>_<expected_result>`

### 2. Test Independence

- Each test should be independent
- Don't rely on test execution order
- Use fixtures to set up test data

### 3. Arrange-Act-Assert Pattern

```python
def test_example(self, client, mock_api, api_response):
    # Arrange - Set up test data and mocks
    input_data = {...}
    mock_response = {...}
    mock_api.post(...).mock(...)

    # Act - Execute the code being tested
    result = client.resource.create(**input_data)

    # Assert - Verify the results
    assert result.id == "expected_id"
    assert result.name == "expected_name"
```

### 4. Error Testing

Always test both success and error cases:

```python
def test_success_case(self, client, mock_api, api_response):
    # Test successful operation
    pass

def test_not_found_error(self, client, mock_api, error_response):
    # Test 404 error
    pass

def test_validation_error(self, client, mock_api, error_response):
    # Test 400 validation error
    pass
```

### 5. Mock External Dependencies

- Mock all HTTP calls using respx
- Don't make real API calls in unit tests
- Use fixtures for reusable mock data

## Troubleshooting

### respx Not Mocking Requests

Ensure you're using the `mock_api` fixture:

```python
def test_example(self, client, mock_api):  # ✅ Correct
    mock_api.get(...).mock(...)
```

### Import Errors

Ensure the package is installed in development mode:

```bash
pip install -e ".[dev]"
```

### Coverage Not Working

Check pytest configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=wiil",
    "--cov-report=term-missing",
]
```

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Use the standard test pattern
3. Include both success and error cases
4. Add docstrings to test methods
5. Ensure tests pass before committing
6. Maintain high code coverage (90%+)

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [respx Documentation](https://lundberg.github.io/respx/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [WIIL API Documentation](https://docs.wiil.io)

## Support

For questions or issues with tests:
- GitHub Issues: https://github.com/wiil-io/wiil-python/issues
- Documentation: https://docs.wiil.io
