"""Tests for Property Inquiry resource."""

import pytest
import responses

from wiil import WiilClient
from wiil.errors import WiilAPIError
from wiil.models.business_mgt import (
    CreatePropertyInquiry,
    UpdatePropertyInquiry,
    UpdatePropertyInquiryStatus,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestPropertyInquiryResource:
    """Test suite for PropertyInquiryResource."""

    def test_create(self, client: WiilClient, mock_api, api_response):
        """Test creating a new property inquiry."""
        mock_response = {
            "id": "inq_123",
            "propertyId": "prop_123",
            "customerId": "cust_123",
            "customer": None,
            "inquiryType": "general",
            "message": "I'm interested in viewing this property",
            "source": "website",
            "status": "new",
            "preferredViewingDate": 1234567890,
            "preferredViewingTime": "10:00 AM",
            "scheduledViewingDate": None,
            "viewingCompleted": False,
            "viewingNotes": None,
            "followUpDate": None,
            "followUpNotes": None,
            "assignedAgentId": None,
            "convertedToTransaction": False,
            "transactionId": None,
            "transactionType": None,
            "interestedInBuying": True,
            "interestedInRenting": False,
            "budgetMin": 300000,
            "budgetMax": 500000,
            "notes": None,
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-inquiries",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.create(CreatePropertyInquiry(
            property_id="prop_123",
            customer_id="cust_123",
            inquiry_type="general",
            message="I'm interested in viewing this property",
            source="website",
            preferred_viewing_date=1234567890,
            preferred_viewing_time="10:00 AM",
            interested_in_buying=True,
            budget_min=300000,
            budget_max=500000
        ))

        assert result.id == "inq_123"
        assert result.property_id == "prop_123"

    def test_get(self, client: WiilClient, mock_api, api_response):
        """Test retrieving a property inquiry by ID."""
        mock_response = {
            "id": "inq_123",
            "propertyId": "prop_123",
            "customerId": "cust_123",
            "customer": None,
            "inquiryType": "viewing",
            "message": None,
            "source": "direct",
            "status": "contacted",
            "preferredViewingDate": None,
            "preferredViewingTime": None,
            "scheduledViewingDate": 1234567890,
            "viewingCompleted": False,
            "viewingNotes": None,
            "followUpDate": None,
            "followUpNotes": None,
            "assignedAgentId": "agent_123",
            "convertedToTransaction": False,
            "transactionId": None,
            "transactionType": None,
            "interestedInBuying": False,
            "interestedInRenting": True,
            "budgetMin": None,
            "budgetMax": None,
            "notes": None,
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-inquiries/inq_123",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.get("inq_123")

        assert result.id == "inq_123"
        assert result.status == "contacted"

    def test_get_by_property(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving property inquiries by property ID."""
        mock_inquiries = [
            {
                "id": "inq_1",
                "propertyId": "prop_123",
                "customerId": "cust_123",
                "customer": None,
                "inquiryType": "general",
                "message": None,
                "source": "website",
                "status": "new",
                "preferredViewingDate": None,
                "preferredViewingTime": None,
                "scheduledViewingDate": None,
                "viewingCompleted": False,
                "viewingNotes": None,
                "followUpDate": None,
                "followUpNotes": None,
                "assignedAgentId": None,
                "convertedToTransaction": False,
                "transactionId": None,
                "transactionType": None,
                "interestedInBuying": True,
                "interestedInRenting": False,
                "budgetMin": None,
                "budgetMax": None,
                "notes": None,
                "assignedUserAccountId": None,
                "calendarId": None,
                "calendarEventId": None,
                "calendarProvider": None,
                "cancelReason": None,
                "serviceConversationConfigId": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_inquiries,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-inquiries/by-property/prop_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.get_by_property(
            "prop_123",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].property_id == "prop_123"

    def test_get_by_customer(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test retrieving property inquiries by customer ID."""
        mock_inquiries = [
            {
                "id": "inq_1",
                "propertyId": "prop_123",
                "customerId": "cust_123",
                "customer": None,
                "inquiryType": "viewing",
                "message": None,
                "source": "direct",
                "status": "qualified",
                "preferredViewingDate": None,
                "preferredViewingTime": None,
                "scheduledViewingDate": None,
                "viewingCompleted": True,
                "viewingNotes": "Very interested",
                "followUpDate": 1234567891,
                "followUpNotes": "Send more listings",
                "assignedAgentId": "agent_123",
                "convertedToTransaction": False,
                "transactionId": None,
                "transactionType": None,
                "interestedInBuying": True,
                "interestedInRenting": False,
                "budgetMin": 400000,
                "budgetMax": 600000,
                "notes": None,
                "assignedUserAccountId": None,
                "calendarId": None,
                "calendarEventId": None,
                "calendarProvider": None,
                "cancelReason": None,
                "serviceConversationConfigId": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_inquiries,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-inquiries/by-customer/cust_123?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.data[0].customer_id == "cust_123"

    def test_update(self, client: WiilClient, mock_api, api_response):
        """Test updating a property inquiry."""
        mock_response = {
            "id": "inq_123",
            "propertyId": "prop_123",
            "customerId": "cust_123",
            "customer": None,
            "inquiryType": "viewing",
            "message": "Updated message",
            "source": "direct",
            "status": "contacted",
            "preferredViewingDate": None,
            "preferredViewingTime": None,
            "scheduledViewingDate": 1234567891,
            "viewingCompleted": False,
            "viewingNotes": None,
            "followUpDate": 1234567892,
            "followUpNotes": "Call to confirm",
            "assignedAgentId": "agent_123",
            "convertedToTransaction": False,
            "transactionId": None,
            "transactionType": None,
            "interestedInBuying": True,
            "interestedInRenting": False,
            "budgetMin": 350000,
            "budgetMax": 550000,
            "notes": "Serious buyer",
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567891,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/property-inquiries",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.update(UpdatePropertyInquiry(
            id="inq_123",
            message="Updated message",
            status="contacted",
            assigned_agent_id="agent_123",
            scheduled_viewing_date=1234567891,
            follow_up_date=1234567892,
            follow_up_notes="Call to confirm",
            budget_min=350000,
            budget_max=550000,
            notes="Serious buyer"
        ))

        assert result.status == "contacted"
        assert result.assigned_agent_id == "agent_123"

    def test_update_status(
        self, client: WiilClient, mock_api, api_response
    ):
        """Test updating property inquiry status."""
        mock_response = {
            "id": "inq_123",
            "propertyId": "prop_123",
            "customerId": "cust_123",
            "customer": None,
            "inquiryType": "viewing",
            "message": None,
            "source": "direct",
            "status": "converted",
            "preferredViewingDate": None,
            "preferredViewingTime": None,
            "scheduledViewingDate": 1234567890,
            "viewingCompleted": True,
            "viewingNotes": "Great viewing, client made an offer",
            "followUpDate": None,
            "followUpNotes": None,
            "assignedAgentId": "agent_123",
            "convertedToTransaction": True,
            "transactionId": "trans_123",
            "transactionType": "purchase",
            "interestedInBuying": True,
            "interestedInRenting": False,
            "budgetMin": 400000,
            "budgetMax": 500000,
            "notes": None,
            "assignedUserAccountId": None,
            "calendarId": None,
            "calendarEventId": None,
            "calendarProvider": None,
            "cancelReason": None,
            "serviceConversationConfigId": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567892,
        }

        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/property-inquiries/inq_123/status",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.update_status(
            "inq_123",
            UpdatePropertyInquiryStatus(
                id="inq_123",
                status="converted",
                viewing_completed=True,
                viewing_notes="Great viewing, client made an offer"
            )
        )

        assert result.status == "converted"
        assert result.viewing_completed is True

    def test_delete(self, client: WiilClient, mock_api, api_response):
        """Test deleting a property inquiry."""
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/property-inquiries/inq_123",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(True),
            status=200,
        )

        result = client.property_inquiry.delete("inq_123")

        assert result is True

    def test_list(self, client: WiilClient, mock_api, api_response):
        """Test listing property inquiries with pagination."""
        mock_inquiries = [
            {
                "id": "inq_1",
                "propertyId": "prop_123",
                "customerId": "cust_123",
                "customer": None,
                "inquiryType": "general",
                "message": None,
                "source": "website",
                "status": "new",
                "preferredViewingDate": None,
                "preferredViewingTime": None,
                "scheduledViewingDate": None,
                "viewingCompleted": False,
                "viewingNotes": None,
                "followUpDate": None,
                "followUpNotes": None,
                "assignedAgentId": None,
                "convertedToTransaction": False,
                "transactionId": None,
                "transactionType": None,
                "interestedInBuying": False,
                "interestedInRenting": False,
                "budgetMin": None,
                "budgetMax": None,
                "notes": None,
                "assignedUserAccountId": None,
                "calendarId": None,
                "calendarEventId": None,
                "calendarProvider": None,
                "cancelReason": None,
                "serviceConversationConfigId": None,
                "createdAt": 1234567890,
                "updatedAt": 1234567890,
            },
        ]

        mock_response = {
            "data": mock_inquiries,
            "meta": {
                "page": 1,
                "pageSize": 20,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-inquiries?page=1&pageSize=10",
            headers={"X-WIIL-API-Key": API_KEY},
            json=api_response(mock_response),
            status=200,
        )

        result = client.property_inquiry.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert len(result.data) == 1
        assert result.meta.total_count == 1

    # =============== Error Handling Tests ===============

    def test_create_api_error(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test create inquiry handles API errors."""
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/property-inquiries",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response("VALIDATION_ERROR", "Property ID required"),
            status=400,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.property_inquiry.create(CreatePropertyInquiry(
                property_id="",
                customer_id="cust_123",
                inquiry_type="general"
            ))

        assert exc_info.value.code == "VALIDATION_ERROR"

    def test_get_not_found(
        self, client: WiilClient, mock_api, error_response
    ):
        """Test get inquiry handles not found errors."""
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/property-inquiries/nonexistent",
            headers={"X-WIIL-API-Key": API_KEY},
            json=error_response("NOT_FOUND", "Inquiry not found"),
            status=404,
        )

        with pytest.raises(WiilAPIError) as exc_info:
            client.property_inquiry.get("nonexistent")

        assert exc_info.value.code == "NOT_FOUND"
