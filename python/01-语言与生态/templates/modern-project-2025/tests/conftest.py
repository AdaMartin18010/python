"""
Pytest configuration and shared fixtures.

This file demonstrates 2025 testing best practices:
- Centralized fixtures
- Test configuration
- Hooks for test customization
"""

import pytest


@pytest.fixture(scope="session")
def sample_data() -> dict[str, str]:
    """
    Provide sample data for tests.

    This fixture has session scope, meaning it's created once
    for the entire test session.
    """
    return {
        "name": "Test User",
        "email": "test@example.com",
        "role": "admin",
    }


@pytest.fixture(scope="function")
def temp_config() -> dict[str, bool]:
    """
    Provide temporary configuration.

    This fixture has function scope (default), meaning it's created
    for each test function.
    """
    return {
        "debug": True,
        "testing": True,
        "verbose": False,
    }


# Hooks for test customization
def pytest_configure(config: pytest.Config) -> None:
    """
    Configure pytest with custom markers.

    Args:
        config: pytest configuration object
    """
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    )
    config.addinivalue_line(
        "markers",
        "integration: marks tests as integration tests",
    )
    config.addinivalue_line(
        "markers",
        "unit: marks tests as unit tests",
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """
    Modify test collection.

    Args:
        config: pytest configuration object
        items: list of collected test items
    """
    # Add 'unit' marker to all tests by default if no marker is present
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)

