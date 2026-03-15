"""Property configuration schema definitions for real estate management.

This module mirrors src/core/business-mgt/property-config.schema.ts
"""

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, Field, HttpUrl

from wiil.models.base import BaseModel
from wiil.models.type_definitions.business_definitions import (
    ListingStatus,
    ListingType,
    PropertyCondition,
    PropertySubType,
    PropertyType,
    RentalPeriod,
)


class Coordinates(PydanticBaseModel):
    """Geographic coordinates."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")


class PropertyCategory(BaseModel):
    """Property category for organizing property listings.

    Attributes:
        id: Unique identifier
        name: Category name (e.g., Luxury Homes, Commercial Offices)
        description: Category description
        property_type: Type of property (residential, commercial, land)
        display_order: Display order in listing
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        category = PropertyCategory(
            id="cat-123",
            name="Luxury Homes",
            description="High-end residential properties",
            property_type=PropertyType.RESIDENTIAL,
            display_order=1
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., min_length=1, description="Category name")
    description: Optional[str] = Field(None, description="Category description")
    property_type: PropertyType = Field(
        ...,
        description="Type of property (residential, commercial, land)",
        alias="propertyType"
    )
    display_order: Optional[int] = Field(
        None,
        description="Display order in listing",
        alias="displayOrder"
    )


class PropertyAddress(BaseModel):
    """Property address (standalone entity).

    Attributes:
        id: Unique identifier
        street: Street address
        unit: Unit or apartment number
        city: City name
        state: State or province
        postal_code: Postal or ZIP code
        country: Country
        coordinates: Geographic coordinates
        neighborhood: Neighborhood or district name
        district: Administrative district
        is_verified: Whether address has been verified
        verified_at: Timestamp when address was verified
        primary_user_account_id: User account managing the property
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        address = PropertyAddress(
            id="addr-123",
            street="123 Main St",
            city="San Francisco",
            state="CA",
            postal_code="94102",
            country="USA",
            is_verified=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    street: str = Field(..., min_length=1, description="Street address")
    unit: Optional[str] = Field(None, description="Unit or apartment number")
    city: str = Field(..., min_length=1, description="City name")
    state: str = Field(..., min_length=1, description="State or province")
    postal_code: Optional[str] = Field(
        None,
        description="Postal or ZIP code",
        alias="postalCode"
    )
    country: str = Field(..., min_length=1, description="Country")
    coordinates: Optional[Coordinates] = Field(
        None,
        description="Geographic coordinates"
    )
    neighborhood: Optional[str] = Field(
        None,
        description="Neighborhood or district name"
    )
    district: Optional[str] = Field(None, description="Administrative district")
    is_verified: bool = Field(
        False,
        description="Whether address has been verified",
        alias="isVerified"
    )
    verified_at: Optional[int] = Field(
        None,
        description="Timestamp when address was verified",
        alias="verifiedAt"
    )
    primary_user_account_id: Optional[str] = Field(
        None,
        description="User account managing the property at this address",
        alias="primaryUserAccountId"
    )


class PropertyFeatures(PydanticBaseModel):
    """Property features schema."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
    )

    bedrooms: Optional[int] = Field(None, ge=0, description="Number of bedrooms")
    bathrooms: Optional[float] = Field(None, ge=0, description="Number of bathrooms")
    parking_spaces: Optional[int] = Field(
        None,
        ge=0,
        description="Number of parking spaces",
        alias="parkingSpaces"
    )
    square_footage: Optional[float] = Field(
        None,
        gt=0,
        description="Total square footage",
        alias="squareFootage"
    )
    lot_size: Optional[float] = Field(
        None,
        gt=0,
        description="Lot size",
        alias="lotSize"
    )
    lot_size_unit: Literal["sqft", "acres", "sqm", "hectares"] = Field(
        "sqft",
        description="Unit for lot size",
        alias="lotSizeUnit"
    )
    year_built: Optional[int] = Field(
        None,
        ge=1800,
        le=2100,
        description="Year the property was built",
        alias="yearBuilt"
    )
    floors: Optional[int] = Field(None, gt=0, description="Number of floors")
    amenities: List[str] = Field(
        default_factory=list,
        description="List of amenities (pool, gym, etc.)"
    )
    utilities: List[str] = Field(
        default_factory=list,
        description="Available utilities (gas, electric, water, etc.)"
    )


class Property(BaseModel):
    """Main property schema for real estate listings.

    Attributes:
        id: Unique identifier
        category_id: ID of the category this property belongs to
        category: Property category (populated)
        title: Property listing title
        description: Detailed property description
        property_type: Type of property
        property_sub_type: Subtype of property
        address_id: ID of the property address
        address: Property address (populated)
        listing_type: Type of listing (sale, rent, or both)
        listing_status: Current listing status
        sale_price: Sale price
        sale_price_currency: Currency for sale price
        rental_price: Rental price
        rental_period: Rental period
        rental_price_currency: Currency for rental price
        price_negotiable: Whether price is negotiable
        features: Property features
        condition: Property condition
        furnished: Whether property is furnished
        images: Array of image URLs
        virtual_tour_url: Virtual tour URL
        video_url: Video tour URL
        available_from: Available from date (timestamp)
        available_to: Available until date (timestamp)
        is_active: Whether property is active in listings
        is_featured: Whether property is featured
        is_verified: Whether property has been verified
        external_id: External system reference ID
        mls_number: MLS listing number
        created_at: Timestamp when created
        updated_at: Timestamp when last updated

    Example:
        ```python
        property = Property(
            id="prop-123",
            category_id="cat-456",
            title="Beautiful 3BR Home",
            property_type=PropertyType.RESIDENTIAL,
            property_sub_type=PropertySubType.HOUSE,
            address_id="addr-789",
            listing_type=ListingType.SALE,
            listing_status=ListingStatus.ACTIVE,
            sale_price=450000,
            is_active=True
        )
        ```
    """

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    category_id: str = Field(..., description="ID of the category", alias="categoryId")
    category: Optional[PropertyCategory] = Field(
        None,
        description="Property category (populated)"
    )

    # Basic Info
    title: str = Field(..., min_length=1, description="Property listing title")
    description: Optional[str] = Field(None, description="Detailed description")
    property_type: PropertyType = Field(
        ...,
        description="Type of property",
        alias="propertyType"
    )
    property_sub_type: PropertySubType = Field(
        ...,
        description="Subtype of property",
        alias="propertySubType"
    )

    # Location
    address_id: str = Field(..., description="ID of the property address", alias="addressId")
    address: Optional[PropertyAddress] = Field(
        None,
        description="Property address (populated)"
    )

    # Listing Info
    listing_type: ListingType = Field(
        ...,
        description="Type of listing (sale, rent, or both)",
        alias="listingType"
    )
    listing_status: ListingStatus = Field(
        ListingStatus.DRAFT,
        description="Current listing status",
        alias="listingStatus"
    )

    # Sale Pricing
    sale_price: Optional[float] = Field(
        None,
        ge=0,
        description="Sale price",
        alias="salePrice"
    )
    sale_price_currency: str = Field(
        "USD",
        description="Currency for sale price",
        alias="salePriceCurrency"
    )

    # Rental Pricing
    rental_price: Optional[float] = Field(
        None,
        ge=0,
        description="Rental price",
        alias="rentalPrice"
    )
    rental_period: Optional[RentalPeriod] = Field(
        None,
        description="Rental period (daily, weekly, monthly, yearly)",
        alias="rentalPeriod"
    )
    rental_price_currency: str = Field(
        "USD",
        description="Currency for rental price",
        alias="rentalPriceCurrency"
    )

    # Pricing Options
    price_negotiable: bool = Field(
        False,
        description="Whether price is negotiable",
        alias="priceNegotiable"
    )

    # Features
    features: Optional[PropertyFeatures] = Field(None, description="Property features")

    # Condition
    condition: Optional[PropertyCondition] = Field(None, description="Property condition")
    furnished: bool = Field(False, description="Whether property is furnished")

    # Media
    images: List[str] = Field(default_factory=list, description="Array of image URLs")
    virtual_tour_url: Optional[str] = Field(
        None,
        description="Virtual tour URL",
        alias="virtualTourUrl"
    )
    video_url: Optional[str] = Field(
        None,
        description="Video tour URL",
        alias="videoUrl"
    )

    # Availability
    available_from: Optional[int] = Field(
        None,
        description="Available from date (timestamp)",
        alias="availableFrom"
    )
    available_to: Optional[int] = Field(
        None,
        description="Available until date (timestamp)",
        alias="availableTo"
    )

    # Flags
    is_active: bool = Field(
        True,
        description="Whether property is active in listings",
        alias="isActive"
    )
    is_featured: bool = Field(
        False,
        description="Whether property is featured",
        alias="isFeatured"
    )
    is_verified: bool = Field(
        False,
        description="Whether property has been verified",
        alias="isVerified"
    )

    # Reference
    external_id: Optional[str] = Field(
        None,
        description="External system reference ID",
        alias="externalId"
    )
    mls_number: Optional[str] = Field(
        None,
        description="MLS listing number",
        alias="mlsNumber"
    )


# Create schemas
class CreatePropertyCategory(PydanticBaseModel):
    """Schema for creating a new property category."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    property_type: PropertyType = Field(..., alias="propertyType")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class UpdatePropertyCategory(PydanticBaseModel):
    """Schema for updating a property category."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[PropertyType] = Field(None, alias="propertyType")
    display_order: Optional[int] = Field(None, alias="displayOrder")


class CreatePropertyAddress(PydanticBaseModel):
    """Schema for creating a new property address."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

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
    primary_user_account_id: Optional[str] = Field(None, alias="primaryUserAccountId")


class UpdatePropertyAddress(PydanticBaseModel):
    """Schema for updating a property address."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

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
    primary_user_account_id: Optional[str] = Field(None, alias="primaryUserAccountId")


class CreateProperty(PydanticBaseModel):
    """Schema for creating a new property listing."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    category_id: str = Field(..., alias="categoryId")
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    property_type: PropertyType = Field(..., alias="propertyType")
    property_sub_type: PropertySubType = Field(..., alias="propertySubType")
    address_id: str = Field(..., alias="addressId")
    listing_type: ListingType = Field(..., alias="listingType")
    listing_status: ListingStatus = Field(ListingStatus.DRAFT, alias="listingStatus")
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


class UpdateProperty(PydanticBaseModel):
    """Schema for updating a property listing."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    id: str
    category_id: Optional[str] = Field(None, alias="categoryId")
    title: Optional[str] = None
    description: Optional[str] = None
    property_type: Optional[PropertyType] = Field(None, alias="propertyType")
    property_sub_type: Optional[PropertySubType] = Field(None, alias="propertySubType")
    address_id: Optional[str] = Field(None, alias="addressId")
    listing_type: Optional[ListingType] = Field(None, alias="listingType")
    listing_status: Optional[ListingStatus] = Field(None, alias="listingStatus")
    sale_price: Optional[float] = Field(None, alias="salePrice")
    sale_price_currency: Optional[str] = Field(None, alias="salePriceCurrency")
    rental_price: Optional[float] = Field(None, alias="rentalPrice")
    rental_period: Optional[RentalPeriod] = Field(None, alias="rentalPeriod")
    rental_price_currency: Optional[str] = Field(None, alias="rentalPriceCurrency")
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


# Catalog schemas
class PropertyCatalog(PydanticBaseModel):
    """Schema representing a property category and its listings."""

    model_config = ConfigDict(
        validate_by_name=True,
        validate_by_alias=True,
        use_enum_values=True,
    )

    property_category: PropertyCategory = Field(..., alias="propertyCategory")
    items: List[Property] = Field(
        default_factory=list,
        description="List of properties in this category"
    )


# Type alias for business property catalog
BusinessPropertyCatalog = List[PropertyCatalog]
