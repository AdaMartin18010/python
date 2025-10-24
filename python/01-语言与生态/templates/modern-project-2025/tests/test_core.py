"""
Tests for core module.

Demonstrates 2025 testing best practices:
- pytest fixtures
- parametrized tests
- Type annotations in tests
- Clear test names
- AAA pattern (Arrange, Act, Assert)
"""

import pytest

from my_modern_project.core import (
    Calculator,
    LowerCaseProcessor,
    UpperCaseProcessor,
    greet,
    process_data,
)


class TestGreet:
    """Tests for the greet function."""

    def test_basic_greeting(self) -> None:
        """Test basic greeting without enthusiasm."""
        # Arrange
        name = "World"

        # Act
        result = greet(name)

        # Assert
        assert result == "Hello, World!"

    def test_enthusiastic_greeting(self) -> None:
        """Test enthusiastic greeting."""
        result = greet("Python", enthusiastic=True)
        assert result == "Hello, Python!!!"

    @pytest.mark.parametrize(
        ("name", "enthusiastic", "expected"),
        [
            ("Alice", False, "Hello, Alice!"),
            ("Bob", True, "Hello, Bob!!!"),
            ("Charlie", False, "Hello, Charlie!"),
        ],
    )
    def test_parametrized_greetings(
        self,
        name: str,
        enthusiastic: bool,
        expected: str,
    ) -> None:
        """Test multiple greeting scenarios."""
        result = greet(name, enthusiastic=enthusiastic)
        assert result == expected


class TestCalculator:
    """Tests for the Calculator class."""

    @pytest.fixture
    def calculator(self) -> Calculator:
        """Fixture providing a Calculator instance."""
        return Calculator()

    def test_add(self, calculator: Calculator) -> None:
        """Test addition."""
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
        assert calculator.add(0, 0) == 0

    def test_subtract(self, calculator: Calculator) -> None:
        """Test subtraction."""
        assert calculator.subtract(5, 3) == 2
        assert calculator.subtract(0, 5) == -5

    def test_multiply(self, calculator: Calculator) -> None:
        """Test multiplication."""
        assert calculator.multiply(2, 3) == 6
        assert calculator.multiply(-2, 3) == -6
        assert calculator.multiply(0, 100) == 0

    def test_divide(self, calculator: Calculator) -> None:
        """Test division."""
        assert calculator.divide(6, 2) == 3
        assert calculator.divide(5, 2) == 2.5

    def test_divide_by_zero(self, calculator: Calculator) -> None:
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)

    @pytest.mark.parametrize(
        ("operation", "a", "b", "expected"),
        [
            ("add", 2, 3, 5),
            ("subtract", 5, 3, 2),
            ("multiply", 4, 3, 12),
            ("divide", 10, 2, 5),
        ],
    )
    def test_all_operations(
        self,
        calculator: Calculator,
        operation: str,
        a: float,
        b: float,
        expected: float,
    ) -> None:
        """Test all calculator operations with parametrize."""
        method = getattr(calculator, operation)
        assert method(a, b) == expected


class TestDataProcessors:
    """Tests for data processors."""

    def test_uppercase_processor(self) -> None:
        """Test uppercase processor."""
        processor = UpperCaseProcessor()
        assert processor.process("hello") == "HELLO"

    def test_lowercase_processor(self) -> None:
        """Test lowercase processor."""
        processor = LowerCaseProcessor()
        assert processor.process("WORLD") == "world"

    def test_process_data_with_uppercase(self) -> None:
        """Test process_data with uppercase processor."""
        processor = UpperCaseProcessor()
        result = process_data(processor, "test")
        assert result == "TEST"

    def test_process_data_with_lowercase(self) -> None:
        """Test process_data with lowercase processor."""
        processor = LowerCaseProcessor()
        result = process_data(processor, "TEST")
        assert result == "test"


# =============================================================================
# 集成测试示例
# =============================================================================
@pytest.mark.integration
class TestIntegration:
    """Integration tests."""

    def test_full_workflow(self) -> None:
        """Test a complete workflow."""
        # Arrange
        calc = Calculator()
        processor = UpperCaseProcessor()

        # Act
        result = calc.add(2, 3)
        message = greet(f"Result is {result}")
        processed = processor.process(message)

        # Assert
        assert processed == "HELLO, RESULT IS 5!"


# =============================================================================
# 慢测试示例
# =============================================================================
@pytest.mark.slow
class TestSlowOperations:
    """Slow running tests."""

    def test_large_calculation(self) -> None:
        """Test with large numbers (marked as slow)."""
        calc = Calculator()
        result = calc.multiply(1_000_000, 1_000_000)
        assert result == 1_000_000_000_000

