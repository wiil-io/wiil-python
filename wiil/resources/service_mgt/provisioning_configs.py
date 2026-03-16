"""Provisioning Configurations resource for managing provisioning configs."""

from typing import Optional, Union

from wiil.client.http_client import HttpClient
from wiil.errors import WiilValidationError
from wiil.models.service_mgt import (
    CreateProvisioningConfig,
    CreateTranslationChainConfig,
    DynamicModelConfiguration,
    DynamicSTTModelConfiguration,
    DynamicTTSModelConfiguration,
    ProvisioningConfigChain,
    TranslationChainConfig,
    UpdateProvisioningConfig,
)
from wiil.types import PaginatedResult, PaginationRequest


class ProvisioningConfigurationsResource:
    """Resource class for managing provisioning configurations.

    Provides methods for creating, retrieving, updating, deleting, and listing
    provisioning configurations. Provisioning configurations define processing
    chains and translation configurations for AI deployments.

    Example:
        >>> client = WiilClient(api_key='your-api-key')
        >>>
        >>> # Create a new provisioning configuration
        >>> config = client.provisioning_configs.create(
        ...     CreateProvisioningConfig(
        ...         chain_name='customer-support-chain',
        ...         stt_config=DynamicSTTModelConfiguration(...),
        ...         processing_config=DynamicModelConfiguration(...),
        ...         tts_config=DynamicTTSModelConfiguration(...),
        ...     )
        ... )
        >>>
        >>> # Get by chain name
        >>> config = client.provisioning_configs.get_by_chain_name('my-chain')
        >>>
        >>> # List provisioning chains
        >>> chains = client.provisioning_configs.list_provisioning_chains()
        >>>
        >>> # List translation chains
        >>> trans = client.provisioning_configs.list_translation_chains()
    """

    def __init__(self, http: HttpClient):
        self._http = http
        self._base_path = '/provisioning-configurations'

    def create(
        self,
        data: CreateProvisioningConfig
    ) -> ProvisioningConfigChain:
        """Create a new provisioning configuration chain.

        Args:
            data: Provisioning configuration creation data

        Returns:
            The created provisioning configuration chain

        Raises:
            WiilValidationError: When validation fails or model not supported
            WiilAPIError: When the API returns an error
        """
        self._validate_model_configurations(
            data.stt_config,
            data.processing_config,
            data.tts_config
        )

        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateProvisioningConfig,
            response_model=ProvisioningConfigChain
        )

    def create_translation(
        self,
        data: CreateTranslationChainConfig
    ) -> TranslationChainConfig:
        """Create a new translation configuration chain.

        Args:
            data: Translation configuration chain data

        Returns:
            The created translation configuration chain

        Raises:
            WiilValidationError: When validation fails or model not supported
            WiilAPIError: When the API returns an error
        """
        self._validate_model_configurations(
            data.stt_config,
            data.processing_config,
            data.tts_config
        )

        return self._http.post(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=CreateTranslationChainConfig,
            response_model=TranslationChainConfig
        )

    def get(
        self,
        config_id: str
    ) -> Union[ProvisioningConfigChain, TranslationChainConfig]:
        """Retrieve a provisioning configuration by ID.

        Args:
            config_id: Provisioning configuration ID

        Returns:
            The provisioning configuration chain or translation chain

        Raises:
            WiilAPIError: When configuration is not found or API error
        """
        return self._http.get(
            f'{self._base_path}/{config_id}',
            response_model=ProvisioningConfigChain
        )

    def get_by_chain_name(
        self,
        chain_name: str
    ) -> Union[ProvisioningConfigChain, TranslationChainConfig]:
        """Retrieve a provisioning configuration by chain name.

        Args:
            chain_name: Chain name

        Returns:
            The provisioning configuration chain or translation chain

        Raises:
            WiilAPIError: When configuration is not found or API error
        """
        return self._http.get(
            f'{self._base_path}/by-chain-name/{chain_name}',
            response_model=ProvisioningConfigChain
        )

    def update(
        self,
        data: UpdateProvisioningConfig
    ) -> ProvisioningConfigChain:
        """Update an existing provisioning configuration.

        Args:
            data: Provisioning configuration update data (must include id)

        Returns:
            The updated provisioning configuration chain

        Raises:
            WiilValidationError: When validation fails or model not supported
            WiilAPIError: When configuration is not found or API error
        """
        self._validate_model_configurations(
            data.stt_config,
            data.processing_config,
            data.tts_config
        )

        return self._http.patch(
            self._base_path,
            data.model_dump(by_alias=True, exclude_none=True),
            schema=UpdateProvisioningConfig,
            response_model=ProvisioningConfigChain
        )

    def delete(self, config_id: str) -> bool:
        """Delete a provisioning configuration.

        Args:
            config_id: Provisioning configuration ID

        Returns:
            True if deletion was successful

        Raises:
            WiilAPIError: When configuration is not found or API error
        """
        return self._http.delete(f'{self._base_path}/{config_id}')

    def list(
        self,
        params: Optional[PaginationRequest] = None,
        include_deleted: Optional[bool] = None
    ) -> PaginatedResult[Union[ProvisioningConfigChain, TranslationChainConfig]]:
        """List all provisioning configurations with pagination.

        Args:
            params: Pagination parameters
            include_deleted: Include deleted configurations

        Returns:
            Paginated list of provisioning configurations
        """
        query_parts = []
        if params:
            if params.page:
                query_parts.append(f'page={params.page}')
            if params.page_size:
                query_parts.append(f'pageSize={params.page_size}')
        if include_deleted is not None:
            query_parts.append(f'includeDeleted={str(include_deleted).lower()}')

        query_string = '?' + '&'.join(query_parts) if query_parts else ''
        return self._http.get(
            f'{self._base_path}{query_string}',
            response_model=PaginatedResult[ProvisioningConfigChain]
        )

    def list_provisioning_chains(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[ProvisioningConfigChain]:
        """List provisioning configuration chains with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of provisioning configuration chains
        """
        query_parts = []
        if params:
            if params.page:
                query_parts.append(f'page={params.page}')
            if params.page_size:
                query_parts.append(f'pageSize={params.page_size}')

        query_string = '?' + '&'.join(query_parts) if query_parts else ''
        return self._http.get(
            f'{self._base_path}/provisioning{query_string}',
            response_model=PaginatedResult[ProvisioningConfigChain]
        )

    def list_translation_chains(
        self,
        params: Optional[PaginationRequest] = None
    ) -> PaginatedResult[TranslationChainConfig]:
        """List translation configuration chains with pagination.

        Args:
            params: Pagination parameters

        Returns:
            Paginated list of translation configuration chains
        """
        query_parts = []
        if params:
            if params.page:
                query_parts.append(f'page={params.page}')
            if params.page_size:
                query_parts.append(f'pageSize={params.page_size}')

        query_string = '?' + '&'.join(query_parts) if query_parts else ''
        return self._http.get(
            f'{self._base_path}/translations{query_string}',
            response_model=PaginatedResult[TranslationChainConfig]
        )

    def _validate_model_configurations(
        self,
        stt_config: Optional[DynamicSTTModelConfiguration],
        processing_config: Optional[DynamicModelConfiguration],
        tts_config: Optional[DynamicTTSModelConfiguration]
    ) -> None:
        """Validate STT, Processing, and TTS model configs."""
        has_stt = (
            stt_config
            and stt_config.provider_type
            and stt_config.provider_model_id
        )
        if has_stt:
            self._validate_model(
                stt_config.provider_type,
                stt_config.provider_model_id,
                'STT'
            )

        has_processing = (
            processing_config
            and processing_config.provider_type
            and processing_config.provider_model_id
        )
        if has_processing:
            self._validate_model(
                processing_config.provider_type,
                processing_config.provider_model_id,
                'Processing'
            )

        has_tts = (
            tts_config
            and tts_config.provider_type
            and tts_config.provider_model_id
        )
        if has_tts:
            self._validate_model(
                tts_config.provider_type,
                tts_config.provider_model_id,
                'TTS'
            )

    def _validate_model(
        self,
        provider_type: str,
        provider_model_id: str,
        model_type: str
    ) -> None:
        """Validate a single model against the support registry."""
        is_supported = self._http.get(
            f'/support-models/supports/{provider_type}/{provider_model_id}',
            response_model=bool
        )

        if not is_supported:
            msg = (
                f'Unsupported {model_type} model: '
                f'{provider_type}/{provider_model_id}. '
                f'Verify the model is available in the support registry.'
            )
            raise WiilValidationError(msg)


__all__ = ['ProvisioningConfigurationsResource']
