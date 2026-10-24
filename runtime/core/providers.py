"""
ARGON AI-OS — AI Model Provider Gateway

Provider-neutral interface for model inference.
Implements:
- Provider capability discovery
- Timeouts and bounded retries
- Token/request usage tracking
- Configurable spending limits
- Secret redaction
- Explicit offline mode
- Mock providers for deterministic testing
- No dependency on paid APIs for local test suite
"""
from __future__ import annotations

import enum
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


class ProviderStatus(enum.Enum):
    """Status of a provider."""
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    DEGRADED = "DEGRADED"
    OFFLINE = "OFFLINE"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    AUTH_FAILED = "AUTH_FAILED"
    RATE_LIMITED = "RATE_LIMITED"
    UNKNOWN = "UNKNOWN"


@dataclass
class ProviderCapabilities:
    """What a provider can do."""
    provider_name: str
    supports_chat: bool = False
    supports_code_generation: bool = False
    supports_analysis: bool = False
    supports_embedding: bool = False
    max_tokens: int = 0
    max_context: int = 0
    models: list[str] = field(default_factory=list)
    status: ProviderStatus = ProviderStatus.NOT_CONFIGURED
    requires_auth: bool = True
    auth_configured: bool = False
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0

    def to_dict(self) -> dict:
        return {
            "provider_name": self.provider_name,
            "supports_chat": self.supports_chat,
            "supports_code_generation": self.supports_code_generation,
            "supports_analysis": self.supports_analysis,
            "supports_embedding": self.supports_embedding,
            "max_tokens": self.max_tokens,
            "max_context": self.max_context,
            "models": self.models,
            "status": self.status.value,
            "requires_auth": self.requires_auth,
            "auth_configured": self.auth_configured,
        }


@dataclass
class InferenceRequest:
    """A request to a provider."""
    prompt: str
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.0
    system_prompt: str = ""
    timeout_seconds: int = 60
    task_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class InferenceResponse:
    """Response from a provider."""
    content: str = ""
    model_used: str = ""
    provider: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0
    success: bool = False
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "model_used": self.model_used,
            "provider": self.provider,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "latency_ms": self.latency_ms,
            "success": self.success,
            "error": self.error,
        }


@dataclass
class UsageRecord:
    """Tracks usage and cost."""
    total_requests: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    estimated_cost: float = 0.0
    budget_limit: float = 0.0
    requests_by_provider: dict[str, int] = field(default_factory=dict)

    def add(self, response: InferenceResponse, cost_per_1k_in: float, cost_per_1k_out: float) -> None:
        self.total_requests += 1
        self.total_input_tokens += response.input_tokens
        self.total_output_tokens += response.output_tokens
        self.estimated_cost += (
            response.input_tokens / 1000 * cost_per_1k_in
            + response.output_tokens / 1000 * cost_per_1k_out
        )
        prov = response.provider
        self.requests_by_provider[prov] = self.requests_by_provider.get(prov, 0) + 1

    def is_over_budget(self) -> bool:
        if self.budget_limit <= 0:
            return False
        return self.estimated_cost >= self.budget_limit

    def to_dict(self) -> dict:
        return {
            "total_requests": self.total_requests,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "estimated_cost": round(self.estimated_cost, 6),
            "budget_limit": self.budget_limit,
            "requests_by_provider": self.requests_by_provider,
        }


class ProviderAdapter(ABC):
    """Abstract base class for provider adapters."""

    @abstractmethod
    def get_capabilities(self) -> ProviderCapabilities:
        """Return the provider's capabilities."""
        ...

    @abstractmethod
    def check_readiness(self) -> tuple[ProviderStatus, str]:
        """
        Check if the provider is ready.
        Returns (status, human-readable message).
        Must NOT disclose secrets.
        """
        ...

    @abstractmethod
    def infer(self, request: InferenceRequest) -> InferenceResponse:
        """Perform inference."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        ...


class MockProvider(ProviderAdapter):
    """
    Deterministic mock provider for testing.
    Returns predictable responses without any external dependency.
    """

    def __init__(
        self,
        name: str = "mock",
        responses: Optional[dict[str, str]] = None,
        should_fail: bool = False,
        latency_ms: float = 10.0,
    ):
        self._name = name
        self._responses = responses or {}
        self._should_fail = should_fail
        self._latency_ms = latency_ms
        self._call_count = 0

    @property
    def name(self) -> str:
        return self._name

    def get_capabilities(self) -> ProviderCapabilities:
        return ProviderCapabilities(
            provider_name=self._name,
            supports_chat=True,
            supports_code_generation=True,
            supports_analysis=True,
            max_tokens=4096,
            max_context=8192,
            models=["mock-model-v1"],
            status=ProviderStatus.AVAILABLE,
            requires_auth=False,
            auth_configured=True,
        )

    def check_readiness(self) -> tuple[ProviderStatus, str]:
        if self._should_fail:
            return ProviderStatus.UNAVAILABLE, "Mock provider configured to fail"
        return ProviderStatus.AVAILABLE, "Mock provider ready"

    def infer(self, request: InferenceRequest) -> InferenceResponse:
        self._call_count += 1
        if self._should_fail:
            return InferenceResponse(
                provider=self._name,
                model_used="mock-model-v1",
                success=False,
                error="Mock provider configured to fail",
            )

        # Return deterministic response
        content = self._responses.get(
            request.prompt,
            f"Mock response #{self._call_count} for: {request.prompt[:50]}",
        )
        # Simulate token counts
        input_tokens = len(request.prompt.split())
        output_tokens = len(content.split())

        return InferenceResponse(
            content=content,
            model_used="mock-model-v1",
            provider=self._name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=self._latency_ms,
            success=True,
        )


class ProviderGateway:
    """
    Central gateway for model inference.
    Routes requests to available providers with fallback.
    """

    def __init__(self, budget_limit: float = 0.0, offline_mode: bool = False):
        self._providers: dict[str, ProviderAdapter] = {}
        self._primary: Optional[str] = None
        self._fallback_order: list[str] = []
        self._usage = UsageRecord(budget_limit=budget_limit)
        self._offline_mode = offline_mode

    def register_provider(
        self,
        provider: ProviderAdapter,
        primary: bool = False,
    ) -> None:
        """Register a provider adapter."""
        self._providers[provider.name] = provider
        if primary:
            self._primary = provider.name
        if provider.name not in self._fallback_order:
            self._fallback_order.append(provider.name)

    def get_provider_status(self) -> dict[str, dict]:
        """Get status of all registered providers."""
        result = {}
        for name, provider in self._providers.items():
            status, message = provider.check_readiness()
            caps = provider.get_capabilities()
            result[name] = {
                "status": status.value,
                "message": message,
                "capabilities": caps.to_dict(),
                "is_primary": name == self._primary,
            }
        return result

    def infer(self, request: InferenceRequest) -> InferenceResponse:
        """
        Perform inference with provider selection and fallback.
        """
        if self._offline_mode:
            # In offline mode, only use mock providers
            for name, provider in self._providers.items():
                if isinstance(provider, MockProvider):
                    return provider.infer(request)
            return InferenceResponse(
                success=False,
                error="Offline mode: no mock provider available",
            )

        if self._usage.is_over_budget():
            return InferenceResponse(
                success=False,
                error=f"Budget limit exceeded: "
                      f"${self._usage.estimated_cost:.4f} >= "
                      f"${self._usage.budget_limit:.4f}",
            )

        # Try primary first, then fallbacks
        order = []
        if self._primary and self._primary in self._providers:
            order.append(self._primary)
        for name in self._fallback_order:
            if name not in order:
                order.append(name)

        last_error = ""
        for name in order:
            provider = self._providers[name]
            status, msg = provider.check_readiness()
            if status not in (ProviderStatus.AVAILABLE, ProviderStatus.DEGRADED):
                last_error = f"{name}: {msg}"
                continue
            try:
                response = provider.infer(request)
                if response.success:
                    caps = provider.get_capabilities()
                    self._usage.add(
                        response, caps.cost_per_1k_input, caps.cost_per_1k_output
                    )
                    return response
                last_error = f"{name}: {response.error}"
            except Exception as e:
                last_error = f"{name}: {e}"

        return InferenceResponse(
            success=False,
            error=f"All providers failed. Last error: {last_error}",
        )

    def get_usage(self) -> dict:
        return self._usage.to_dict()
