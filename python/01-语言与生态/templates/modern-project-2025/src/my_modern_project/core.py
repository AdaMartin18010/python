"""
Core functionality module.

This module demonstrates 2025 Python best practices:
- Type annotations (PEP 484, 585, 604)
- Modern syntax (Python 3.12+)
- Docstrings (Google style)
- Clean code principles
"""

from typing import Protocol


def greet(name: str, *, enthusiastic: bool = False) -> str:
    """
    Generate a greeting message.

    Args:
        name: The name of the person to greet
        enthusiastic: Whether to add enthusiasm to the greeting

    Returns:
        A greeting string

    Examples:
        >>> greet("World")
        'Hello, World!'
        >>> greet("Python", enthusiastic=True)
        'Hello, Python!!!'
    """
    greeting = f"Hello, {name}!"
    if enthusiastic:
        greeting += "!!"
    return greeting


class Calculator:
    """
    A simple calculator class demonstrating modern Python patterns.

    This class shows:
    - Type annotations
    - Descriptive method names
    - Clear documentation
    - Error handling

    Examples:
        >>> calc = Calculator()
        >>> calc.add(2, 3)
        5
        >>> calc.divide(10, 2)
        5.0
    """

    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """
        Divide a by b.

        Args:
            a: The dividend
            b: The divisor

        Returns:
            The quotient

        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class DataProcessor(Protocol):
    """
    Protocol for data processors.

    This demonstrates structural subtyping (PEP 544) - a 2025 best practice.
    """

    def process(self, data: str) -> str:
        """Process the input data."""
        ...


class UpperCaseProcessor:
    """Convert data to uppercase."""

    def process(self, data: str) -> str:
        """Process data to uppercase."""
        return data.upper()


class LowerCaseProcessor:
    """Convert data to lowercase."""

    def process(self, data: str) -> str:
        """Process data to lowercase."""
        return data.lower()


def process_data(processor: DataProcessor, data: str) -> str:
    """
    Process data using the given processor.

    This function demonstrates duck typing with Protocol.

    Args:
        processor: An object implementing the DataProcessor protocol
        data: The data to process

    Returns:
        Processed data
    """
    return processor.process(data)

