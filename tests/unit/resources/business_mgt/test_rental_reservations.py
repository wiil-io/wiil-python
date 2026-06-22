"""Tests for Rental Reservations resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateRentalReservation,
    RentalReservationPayment,
    UpdateRentalReservation,
)
from wiil.models.type_definitions.business_definitions import DepositStatus
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestRentalReservationsResource:
    """Test suite for RentalReservationsResource."""

    def _reservation(self, reservation_id: str = "rent_rsv_123") -> dict:
        return {
            "id": reservation_id,
            "customerId": "cust_123",
            "resourceId": "rental_1",
            "tierId": "tier_basic",
            "startAt": 1234567890,
            "endAt": 1234571490,
            "actualReturnAt": None,
            "status": "upcoming",
            "payment": {
                "rentalCharge": 45.0,
                "securityDeposit": 100.0,
                "depositStatus": "pending",
            },
            "checklistCompletions": [],
            "waiver": None,
            "idVerification": None,
            "notes": None,
            "externalRef": None,
            "createdAt": 1234567890,
            "updatedAt": 1234567890,
        }

    def test_crud_and_queries(
        self,
        client: WiilClient,
        mock_api,
        api_response,
    ):
        reservation = self._reservation()
        paged = {
            "data": [reservation],
            "meta": {
                "page": 1,
                "pageSize": 10,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/rental-reservations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/rental-reservations/rent_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/rental-reservations/by-customer/"
                "cust_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/rental-reservations/by-resource/"
                "rental_1?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/rental-reservations/by-tier/"
                "tier_basic?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/rental-reservations/by-date-range?"
                "startAt=1234567000&endAt=1234573000&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/rental-reservations/rent_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/rental-reservations/rent_rsv_123/return",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/rental-reservations/rent_rsv_123/cancel",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/rental-reservations/rent_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/rental-reservations?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.rental_reservations.create(
            CreateRentalReservation(
                customer_id="cust_123",
                resource_id="rental_1",
                tier_id="tier_basic",
                start_at=1234567890,
                end_at=1234571490,
                payment=RentalReservationPayment(
                    rental_charge=45.0,
                    security_deposit=100.0,
                    deposit_status=DepositStatus.PENDING,
                ),
            )
        )
        get_result = client.rental_reservations.get("rent_rsv_123")
        by_customer = client.rental_reservations.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10),
        )
        by_resource = client.rental_reservations.get_by_resource(
            "rental_1",
            PaginationRequest(page=1, page_size=10),
        )
        by_tier = client.rental_reservations.get_by_tier(
            "tier_basic",
            PaginationRequest(page=1, page_size=10),
        )
        by_date = client.rental_reservations.get_by_date_range(
            1234567000,
            1234573000,
            PaginationRequest(page=1, page_size=10),
        )
        update_result = client.rental_reservations.update(
            "rent_rsv_123",
            UpdateRentalReservation(id="rent_rsv_123", notes="Updated"),
        )
        return_result = client.rental_reservations.record_return(
            "rent_rsv_123",
            actual_return_at=1234571490,
        )
        cancel_result = client.rental_reservations.cancel(
            "rent_rsv_123",
            reason="Customer request",
        )
        delete_result = client.rental_reservations.delete("rent_rsv_123")
        list_result = client.rental_reservations.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "rent_rsv_123"
        assert get_result.id == "rent_rsv_123"
        assert by_customer.meta.total_count == 1
        assert by_resource.meta.total_count == 1
        assert by_tier.meta.total_count == 1
        assert by_date.meta.total_count == 1
        assert update_result.id == "rent_rsv_123"
        assert return_result.id == "rent_rsv_123"
        assert cancel_result.id == "rent_rsv_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        reservation = self._reservation("rent_rsv_1")
        paged = {
            "data": [reservation],
            "meta": {
                "page": 1,
                "pageSize": 1,
                "totalCount": 1,
                "totalPages": 1,
                "hasNextPage": False,
                "hasPreviousPage": False,
            },
        }

        mock_api.add(
            responses.POST,
            f"{BASE_URL}/rental-reservations/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.rental_reservations.create_batch(
            [
                CreateRentalReservation(
                    customer_id="cust_123",
                    resource_id="rental_1",
                    tier_id="tier_basic",
                    start_at=1234567890,
                    end_at=1234571490,
                    payment=RentalReservationPayment(
                        rental_charge=45.0,
                        security_deposit=100.0,
                        deposit_status=DepositStatus.PENDING,
                    ),
                )
            ]
        )

        assert len(result.data) == 1
