import pytest
from unittest.mock import patch, MagicMock

from app.models.auto_translate import auto_translate, context


class MockResponse:
    def __init__(self, text):
        self.text = text


@pytest.fixture
def mock_messages():
    """Create mock messages for testing."""
    return ["This is a test message to translate."]


@pytest.fixture
def mock_env_vars():
    """Mock environment variables."""
    return {'claude_api_key': 'fake_api_key'}


def test_auto_translate(mock_messages, mock_env_vars):
    """Test the auto_translate function with mocked API response."""
    # Mock the get_env_vars function
    with patch('app.models.auto_translate.get_env_vars', return_value=mock_env_vars):
        # Mock the prepare_messages_for_translate function
        with patch('app.models.auto_translate.prepare_messages_for_translate', return_value=mock_messages):
            # Mock the translate_with_claude function
            mock_response = [MockResponse("Translated text")]
            with patch('app.models.auto_translate.translate_with_claude', return_value=mock_response):
                # Call the function
                result = auto_translate(mock_messages)
                
                # Check the result
                assert result == "Translated text"


def test_auto_translate_with_custom_context(mock_messages, mock_env_vars):
    """Test the auto_translate function with a custom context."""
    custom_context = {
        "role": "system",
        "content": {
            "role_description": "Custom translator",
            "job": "Translate text",
            "output_format": {
                "structure": "JSON",
                "required_sections": ["Translation"],
                "style_guide": ["Be accurate"]
            }
        }
    }
    
    # Mock the get_env_vars function
    with patch('app.models.auto_translate.get_env_vars', return_value=mock_env_vars):
        # Mock the prepare_messages_for_translate function
        with patch('app.models.auto_translate.prepare_messages_for_translate', return_value=mock_messages):
            # Mock the translate_with_claude function
            mock_response = [MockResponse("Custom translated text")]
            with patch('app.models.auto_translate.translate_with_claude', return_value=mock_response):
                # Call the function with custom context
                result = auto_translate(mock_messages, context=custom_context)
                
                # Check the result
                assert result == "Custom translated text"


def test_auto_translate_api_parameters(mock_messages, mock_env_vars):
    """Test that the auto_translate function passes the correct parameters to the API."""
    # Mock the get_env_vars function
    with patch('app.models.auto_translate.get_env_vars', return_value=mock_env_vars) as mock_get_env_vars:
        # Mock the prepare_messages_for_translate function
        with patch('app.models.auto_translate.prepare_messages_for_translate', return_value=mock_messages) as mock_prepare:
            # Mock the translate_with_claude function
            mock_translate = MagicMock(return_value=[MockResponse("Translated text")])
            with patch('app.models.auto_translate.translate_with_claude', mock_translate):
                # Call the function
                auto_translate(mock_messages)
                
                # Check that the functions were called with the correct parameters
                mock_get_env_vars.assert_called_once_with(
                    keys=['claude_api_key'],
                    file_name='.env',
                    relative_to_pwd='../../../'
                )
                mock_prepare.assert_called_once_with(mock_messages)
                
                # Check that translate_with_claude was called with the correct parameters
                mock_translate.assert_called_once()
                args, kwargs = mock_translate.call_args
                assert args[0] == 'fake_api_key'  # API key
                assert isinstance(args[1], str)  # System prompt
                assert args[2] == mock_messages  # Messages
                assert kwargs['max_tokens'] == 10000
                assert kwargs['model'] == "claude-3-7-sonnet-20250219" 