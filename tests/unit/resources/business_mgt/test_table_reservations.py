"""Tests for Table Reservations resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateTableReservation,
    UpdateTableReservation,
)
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestTableReservationsResource:
    """Test suite for TableReservationsResource."""

    def _reservation(self, reservation_id: str = "tbl_rsv_123") -> dict:
        return {
            "id": reservation_id,
            "customerId": "cust_123",
            "resourceId": "table_1",
            "time": 1234567890,
            "duration": 3600,
            "personsNumber": 4,
            "status": "pending",
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
            f"{BASE_URL}/table-reservations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/table-reservations/tbl_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/table-reservations/by-customer/"
                "cust_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/table-reservations/by-resource/"
                "table_1?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/table-reservations/by-date-range?"
                "startTime=1234567000&endTime=1234569999&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/table-reservations/tbl_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/table-reservations/tbl_rsv_123/cancel",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/table-reservations/tbl_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/table-reservations?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.table_reservations.create(
            CreateTableReservation(
                customer_id="cust_123",
                resource_id="table_1",
                time=1234567890,
                duration=3600,
                persons_number=4,
            )
        )
        get_result = client.table_reservations.get("tbl_rsv_123")
        by_customer = client.table_reservations.get_by_customer(
            "cust_123",
            PaginationRequest(page=1, page_size=10),
        )
        by_resource = client.table_reservations.get_by_resource(
            "table_1",
            PaginationRequest(page=1, page_size=10),
        )
        by_date = client.table_reservations.get_by_date_range(
            1234567000,
            1234569999,
            PaginationRequest(page=1, page_size=10),
        )
        update_result = client.table_reservations.update(
            "tbl_rsv_123",
            UpdateTableReservation(id="tbl_rsv_123", persons_number=5),
        )
        cancel_result = client.table_reservations.cancel(
            "tbl_rsv_123",
            reason="Customer request",
        )
        delete_result = client.table_reservations.delete("tbl_rsv_123")
        list_result = client.table_reservations.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "tbl_rsv_123"
        assert get_result.id == "tbl_rsv_123"
        assert by_customer.meta.total_count == 1
        assert by_resource.meta.total_count == 1
        assert by_date.meta.total_count == 1
        assert update_result.id == "tbl_rsv_123"
        assert cancel_result.id == "tbl_rsv_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        reservation = self._reservation("tbl_rsv_1")
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
            f"{BASE_URL}/table-reservations/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.table_reservations.create_batch(
            [
                CreateTableReservation(
                    customer_id="cust_123",
                    resource_id="table_1",
                    time=1234567890,
                    duration=3600,
                    persons_number=4,
                )
            ]
        )

        assert len(result.data) == 1
