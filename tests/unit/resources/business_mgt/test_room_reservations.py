"""Tests for Room Reservations resource."""

import responses

from wiil import WiilClient
from wiil.models.business_mgt import (
    CreateRoomReservation,
    RoomRatePerNight,
    UpdateRoomReservation,
)
from wiil.models.type_definitions.business_definitions import ReservationStatus
from wiil.types import PaginationRequest

BASE_URL = "https://api.wiil.io/v1"
API_KEY = "test-api-key"


class TestRoomReservationsResource:
    """Test suite for RoomReservationsResource."""

    def _reservation(self, reservation_id: str = "room_rsv_123") -> dict:
        return {
            "id": reservation_id,
            "resourceId": "room_101",
            "guestId": "guest_123",
            "personsNumber": 2,
            "checkIn": 1234567890,
            "checkOut": 1234654290,
            "nights": 1,
            "source": None,
            "ratePerNight": [{"date": "2026-01-01", "amount": 120.0}],
            "totalWithTax": 120.0,
            "deposit": 20.0,
            "paymentStatus": "pending",
            "status": "confirmed",
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
            f"{BASE_URL}/room-reservations",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/room-reservations/room_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/room-reservations/by-guest/"
                "guest_123?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/room-reservations/by-resource/"
                "room_101?page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.GET,
            (
                f"{BASE_URL}/room-reservations/by-check-in-range?"
                "checkInStart=1234500000&"
                "checkInEnd=1234700000&page=1&pageSize=10"
            ),
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )
        mock_api.add(
            responses.PATCH,
            f"{BASE_URL}/room-reservations/room_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.POST,
            f"{BASE_URL}/room-reservations/room_rsv_123/cancel",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(reservation),
            status=200,
        )
        mock_api.add(
            responses.DELETE,
            f"{BASE_URL}/room-reservations/room_rsv_123",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(True),
            status=200,
        )
        mock_api.add(
            responses.GET,
            f"{BASE_URL}/room-reservations?page=1&pageSize=10",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        create_result = client.room_reservations.create(
            CreateRoomReservation(
                resource_id="room_101",
                guest_id="guest_123",
                persons_number=2,
                check_in=1234567890,
                check_out=1234654290,
                nights=1,
                rate_per_night=[
                    RoomRatePerNight(date="2026-01-01", amount=120.0)
                ],
                total_with_tax=120.0,
                deposit=20.0,
                status=ReservationStatus.CONFIRMED,
            )
        )
        get_result = client.room_reservations.get("room_rsv_123")
        by_guest = client.room_reservations.get_by_guest(
            "guest_123",
            PaginationRequest(page=1, page_size=10),
        )
        by_resource = client.room_reservations.get_by_resource(
            "room_101",
            PaginationRequest(page=1, page_size=10),
        )
        by_check_in = client.room_reservations.get_by_check_in_range(
            1234500000,
            1234700000,
            PaginationRequest(page=1, page_size=10),
        )
        update_result = client.room_reservations.update(
            "room_rsv_123",
            UpdateRoomReservation(id="room_rsv_123", persons_number=3),
        )
        cancel_result = client.room_reservations.cancel(
            "room_rsv_123",
            reason="Plan changed",
        )
        delete_result = client.room_reservations.delete("room_rsv_123")
        list_result = client.room_reservations.list(
            PaginationRequest(page=1, page_size=10)
        )

        assert create_result.id == "room_rsv_123"
        assert get_result.id == "room_rsv_123"
        assert by_guest.meta.total_count == 1
        assert by_resource.meta.total_count == 1
        assert by_check_in.meta.total_count == 1
        assert update_result.id == "room_rsv_123"
        assert cancel_result.id == "room_rsv_123"
        assert delete_result is True
        assert list_result.meta.total_count == 1

    def test_create_batch(self, client: WiilClient, mock_api, api_response):
        reservation = self._reservation("room_rsv_1")
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
            f"{BASE_URL}/room-reservations/batch",
            headers={"X-Wiil-Api-Key": API_KEY},
            json=api_response(paged),
            status=200,
        )

        result = client.room_reservations.create_batch(
            [
                CreateRoomReservation(
                    resource_id="room_101",
                    guest_id="guest_123",
                    persons_number=2,
                    check_in=1234567890,
                    check_out=1234654290,
                    nights=1,
                    rate_per_night=[
                        RoomRatePerNight(
                            date="2026-01-01",
                            amount=120.0,
                        )
                    ],
                    total_with_tax=120.0,
                )
            ]
        )

        assert len(result.data) == 1
