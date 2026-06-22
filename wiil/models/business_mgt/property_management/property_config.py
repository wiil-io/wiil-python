"""Property management configuration schemas.

This module mirrors
type-ref/business-mgt/property-management/property-config.schema.ts.
"""

from typing import List, Literal, Optional, TypeAlias

from pydantic import Field

from wiil.models.base import BaseModel, EntityModel
from wiil.models.type_definitions.business_definitions import (
    ListingStatus,
    ListingType,
    PropertyCondition,
    PropertySubType,
    PropertyType,
    RentalPeriod,
)
from wiil.models.type_definitions.display_order import (
    CreateDisplayOrderPlacement,
)

LotSizeUnit = Literal["sqft", "acres", "sqm", "hectares"]
BasementType = Literal["none", "unfinished", "partial", "finished"]
BuildOutStatus = Literal["shell", "partial", "turnkey"]
TopographyType = Literal["flat", "sloped", "hilly", "mixed"]
RoadAccessType = Literal["paved", "gravel", "dirt", "none"]
WaterSourceType = Literal["municipal", "well", "none", "unknown"]
SewerType = Literal["municipal", "septic", "none", "unknown"]
MineralRightsType = Literal["included", "excluded", "partial", "unknown"]


class Coordinates(BaseModel):
    """Geographic coordinates for a property address."""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class PropertyCategory(EntityModel):
    """Category used to group properties in catalog listings."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    property_type: PropertyType = Field(..., alias="propertyType")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_default: bool = Field(False, alias="isDefault")


class PropertyAddress(EntityModel):
    """Standalone address record for property locations."""

    street: str = Field(..., min_length=1)
    unit: Optional[str] = None
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    postal_code: Optional[str] = Field(None, alias="postalCode")
    country: str = Field(..., min_length=1)
    coordinates: Optional[Coordinates] = None
    neighborhood: Optional[str] = None
    district: Optional[str] = None
    is_verified: bool = Field(False, alias="isVerified")
    verified_at: Optional[int] = Field(None, alias="verifiedAt")
    primary_user_account_id: Optional[str] = Field(
        None,
        alias="primaryUserAccountId"
    )


class PropertyFeatures(BaseModel):
    """Features shared across all property types."""

    parking_spaces: Optional[int] = Field(None, ge=0, alias="parkingSpaces")
    amenities: List[str] = Field(default_factory=list)
    utilities: List[str] = Field(default_factory=list)


class ResidentialDetails(BaseModel):
    """Residential-specific details."""

    bedrooms: int = Field(..., ge=0)
    bathrooms: float = Field(..., ge=0)
    half_baths: Optional[int] = Field(None, ge=0, alias="halfBaths")
    square_footage: float = Field(..., gt=0, alias="squareFootage")
    lot_size: Optional[float] = Field(None, gt=0, alias="lotSize")
    lot_size_unit: LotSizeUnit = Field("sqft", alias="lotSizeUnit")
    year_built: Optional[int] = Field(
        None,
        ge=1800,
        le=2100,
        alias="yearBuilt"
    )
    floors: Optional[int] = Field(None, gt=0)
    basement_type: Optional[BasementType] = Field(None, alias="basementType")
    attic_finished: Optional[bool] = Field(None, alias="atticFinished")
    heating_type: Optional[str] = Field(None, alias="heatingType")
    cooling_type: Optional[str] = Field(None, alias="coolingType")
    roof_type: Optional[str] = Field(None, alias="roofType")
    exterior_material: Optional[str] = Field(None, alias="exteriorMaterial")
    garage_spaces: Optional[int] = Field(None, ge=0, alias="garageSpaces")
    has_pool: bool = Field(False, alias="hasPool")
    has_fireplace: bool = Field(False, alias="hasFireplace")


class CommercialDetails(BaseModel):
    """Commercial-specific details."""

    square_footage: float = Field(..., gt=0, alias="squareFootage")
    usable_square_footage: Optional[float] = Field(
        None,
        gt=0,
        alias="usableSquareFootage"
    )
    floors: Optional[int] = Field(None, gt=0)
    ceiling_height: Optional[float] = Field(None, gt=0, alias="ceilingHeight")
    loading_docks: Optional[int] = Field(None, ge=0, alias="loadingDocks")
    drive_in_doors: Optional[int] = Field(None, ge=0, alias="driveInDoors")
    freight_elevator: bool = Field(False, alias="freightElevator")
    passenger_elevator: bool = Field(False, alias="passengerElevator")
    zoning_type: str = Field(..., alias="zoningType")
    year_built: Optional[int] = Field(
        None,
        ge=1800,
        le=2100,
        alias="yearBuilt"
    )
    previous_use: Optional[str] = Field(None, alias="previousUse")
    build_out_status: Optional[BuildOutStatus] = Field(
        None,
        alias="buildOutStatus"
    )
    hvac_type: Optional[str] = Field(None, alias="hvacType")
    power_capacity: Optional[str] = Field(None, alias="powerCapacity")
    sprinkler_system: bool = Field(False, alias="sprinklerSystem")


class LandDetails(BaseModel):
    """Land-specific details."""

    lot_size: float = Field(..., gt=0, alias="lotSize")
    lot_size_unit: LotSizeUnit = Field("acres", alias="lotSizeUnit")
    zoning: str
    topography: Optional[TopographyType] = None
    road_frontage: Optional[float] = Field(None, gt=0, alias="roadFrontage")
    road_access: Optional[RoadAccessType] = Field(None, alias="roadAccess")
    utilities_available: List[str] = Field(
        default_factory=list,
        alias="utilitiesAvailable"
    )
    water_source: Optional[WaterSourceType] = Field(None, alias="waterSource")
    sewer_type: Optional[SewerType] = Field(None, alias="sewerType")
    soil_type: Optional[str] = Field(None, alias="soilType")
    flood_zone: bool = Field(False, alias="floodZone")
    flood_zone_designation: Optional[str] = Field(
        None,
        alias="floodZoneDesignation"
    )
    easements: Optional[str] = None
    survey_available: bool = Field(False, alias="surveyAvailable")
    mineral_rights: Optional[MineralRightsType] = Field(
        None,
        alias="mineralRights"
    )
    timber_value: Optional[float] = Field(None, ge=0, alias="timberValue")


class Property(EntityModel):
    """Main property listing schema."""

    category_id: str = Field(..., alias="categoryId")
    category: Optional[PropertyCategory] = None
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    property_type: PropertyType = Field(..., alias="propertyType")
    property_sub_type: PropertySubType = Field(..., alias="propertySubType")
    address_id: str = Field(..., alias="addressId")
    address: Optional[PropertyAddress] = None
    listing_type: ListingType = Field(..., alias="listingType")
    listing_status: ListingStatus = Field(
        ListingStatus.DRAFT,
        alias="listingStatus"
    )
    sale_price: Optional[float] = Field(None, ge=0, alias="salePrice")
    sale_price_currency: str = Field("USD", alias="salePriceCurrency")
    rental_price: Optional[float] = Field(None, ge=0, alias="rentalPrice")
    rental_period: Optional[RentalPeriod] = Field(None, alias="rentalPeriod")
    rental_price_currency: str = Field("USD", alias="rentalPriceCurrency")
    price_negotiable: bool = Field(False, alias="priceNegotiable")
    features: Optional[PropertyFeatures] = None
    condition: Optional[PropertyCondition] = None
    furnished: bool = False
    images: List[str] = Field(default_factory=list)
    virtual_tour_url: Optional[str] = Field(None, alias="virtualTourUrl")
    video_url: Optional[str] = Field(None, alias="videoUrl")
    available_from: Optional[int] = Field(None, alias="availableFrom")
    available_to: Optional[int] = Field(None, alias="availableTo")
    is_active: bool = Field(True, alias="isActive")
    is_featured: bool = Field(False, alias="isFeatured")
    is_verified: bool = Field(False, alias="isVerified")
    external_id: Optional[str] = Field(None, alias="externalId")
    mls_number: Optional[str] = Field(None, alias="mlsNumber")
    residential_details: Optional[ResidentialDetails] = Field(
        None,
        alias="residentialDetails"
    )
    commercial_details: Optional[CommercialDetails] = Field(
        None,
        alias="commercialDetails"
    )
    land_details: Optional[LandDetails] = Field(None, alias="landDetails")


class CreatePropertyCategory(BaseModel):
    """Schema for creating a property category."""

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    property_type: PropertyType = Field(..., alias="propertyType")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_default: bool = Field(False, alias="isDefault")
    placement: Optional[CreateDisplayOrderPlacement] = None


class UpdatePropertyCategory(BaseModel):
    """Schema for updating a property category."""

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[PropertyType] = Field(None, alias="propertyType")
    display_order: Optional[int] = Field(None, alias="displayOrder")
    is_default: Optional[bool] = Field(None, alias="isDefault")
    placement: Optional[CreateDisplayOrderPlacement] = None


class CreatePropertyAddress(BaseModel):
    """Schema for creating a property address."""

    street: str = Field(..., min_length=1)
    unit: Optional[str] = None
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
    postal_code: Optional[str] = Field(None, alias="postalCode")
    country: str = Field(..., min_length=1)
    coordinates: Optional[Coordinates] = None
    neighborhood: Optional[str] = None
    district: Optional[str] = None
    is_verified: bool = Field(False, alias="isVerified")
    primary_user_account_id: Optional[str] = Field(
        None,
        alias="primaryUserAccountId"
    )


class UpdatePropertyAddress(BaseModel):
    """Schema for updating a property address."""

    id: str
    street: Optional[str] = None
    unit: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = Field(None, alias="postalCode")
    country: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    neighborhood: Optional[str] = None
    district: Optional[str] = None
    is_verified: Optional[bool] = Field(None, alias="isVerified")
    primary_user_account_id: Optional[str] = Field(
        None,
        alias="primaryUserAccountId"
    )


class CreateProperty(BaseModel):
    """Schema for creating a property listing."""

    category_id: str = Field(..., alias="categoryId")
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    property_type: PropertyType = Field(..., alias="propertyType")
    property_sub_type: PropertySubType = Field(..., alias="propertySubType")
    address_id: str = Field(..., alias="addressId")
    listing_type: ListingType = Field(..., alias="listingType")
    listing_status: ListingStatus = Field(
        ListingStatus.DRAFT,
        alias="listingStatus"
    )
    sale_price: Optional[float] = Field(None, ge=0, alias="salePrice")
    sale_price_currency: str = Field("USD", alias="salePriceCurrency")
    rental_price: Optional[float] = Field(None, ge=0, alias="rentalPrice")
    rental_period: Optional[RentalPeriod] = Field(None, alias="rentalPeriod")
    rental_price_currency: str = Field("USD", alias="rentalPriceCurrency")
    price_negotiable: bool = Field(False, alias="priceNegotiable")
    features: Optional[PropertyFeatures] = None
    condition: Optional[PropertyCondition] = None
    furnished: bool = False
    images: List[str] = Field(default_factory=list)
    virtual_tour_url: Optional[str] = Field(None, alias="virtualTourUrl")
    video_url: Optional[str] = Field(None, alias="videoUrl")
    available_from: Optional[int] = Field(None, alias="availableFrom")
    available_to: Optional[int] = Field(None, alias="availableTo")
    is_active: bool = Field(True, alias="isActive")
    is_featured: bool = Field(False, alias="isFeatured")
    is_verified: bool = Field(False, alias="isVerified")
    external_id: Optional[str] = Field(None, alias="externalId")
    mls_number: Optional[str] = Field(None, alias="mlsNumber")
    residential_details: Optional[ResidentialDetails] = Field(
        None,
        alias="residentialDetails"
    )
    commercial_details: Optional[CommercialDetails] = Field(
        None,
        alias="commercialDetails"
    )
    land_details: Optional[LandDetails] = Field(None, alias="landDetails")


class UpdateProperty(BaseModel):
    """Schema for updating a property listing."""

    id: str
    category_id: Optional[str] = Field(None, alias="categoryId")
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[PropertyType] = Field(None, alias="propertyType")
    property_sub_type: Optional[PropertySubType] = Field(
        None,
        alias="propertySubType"
    )
    address_id: Optional[str] = Field(None, alias="addressId")
    listing_type: Optional[ListingType] = Field(None, alias="listingType")
    listing_status: Optional[ListingStatus] = Field(
        None,
        alias="listingStatus"
    )
    sale_price: Optional[float] = Field(None, ge=0, alias="salePrice")
    sale_price_currency: Optional[str] = Field(None, alias="salePriceCurrency")
    rental_price: Optional[float] = Field(None, ge=0, alias="rentalPrice")
    rental_period: Optional[RentalPeriod] = Field(None, alias="rentalPeriod")
    rental_price_currency: Optional[str] = Field(
        None,
        alias="rentalPriceCurrency"
    )
    price_negotiable: Optional[bool] = Field(None, alias="priceNegotiable")
    features: Optional[PropertyFeatures] = None
    condition: Optional[PropertyCondition] = None
    furnished: Optional[bool] = None
    images: Optional[List[str]] = None
    virtual_tour_url: Optional[str] = Field(None, alias="virtualTourUrl")
    video_url: Optional[str] = Field(None, alias="videoUrl")
    available_from: Optional[int] = Field(None, alias="availableFrom")
    available_to: Optional[int] = Field(None, alias="availableTo")
    is_active: Optional[bool] = Field(None, alias="isActive")
    is_featured: Optional[bool] = Field(None, alias="isFeatured")
    is_verified: Optional[bool] = Field(None, alias="isVerified")
    external_id: Optional[str] = Field(None, alias="externalId")
    mls_number: Optional[str] = Field(None, alias="mlsNumber")
    residential_details: Optional[ResidentialDetails] = Field(
        None,
        alias="residentialDetails"
    )
    commercial_details: Optional[CommercialDetails] = Field(
        None,
        alias="commercialDetails"
    )
    land_details: Optional[LandDetails] = Field(None, alias="landDetails")


class PropertyCatalog(BaseModel):
    """Category with its property listings."""

    property_category: PropertyCategory = Field(..., alias="propertyCategory")
    items: List[Property] = Field(...)


BusinessPropertyCatalog: TypeAlias = List[PropertyCatalog]
