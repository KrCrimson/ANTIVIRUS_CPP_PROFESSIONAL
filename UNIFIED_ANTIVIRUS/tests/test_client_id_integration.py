import unittest
import shutil
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import logging

# Add project root to path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web_system.integration.client_identity import ClientIdentity
from web_system.integration.web_log_handler import WebLogHandler

class TestClientIdentity(unittest.TestCase):
    def setUp(self):
        self.test_config_dir = "test_config_identity"
        if os.path.exists(self.test_config_dir):
            shutil.rmtree(self.test_config_dir)
            
    def tearDown(self):
        if os.path.exists(self.test_config_dir):
            shutil.rmtree(self.test_config_dir)

    def test_identity_generation(self):
        # First run - should create identity
        identity = ClientIdentity(config_dir=self.test_config_dir)
        instance_id = identity.instance_id
        
        self.assertIsNotNone(instance_id)
        self.assertTrue(os.path.exists(os.path.join(self.test_config_dir, "client_identity.json")))
        
        # Second run - should load same identity
        identity2 = ClientIdentity(config_dir=self.test_config_dir)
        self.assertEqual(identity2.instance_id, instance_id)

class TestWebLogHandlerIntegration(unittest.TestCase):
    def setUp(self):
        self.test_config_dir = "test_config_handler"
        if os.path.exists(self.test_config_dir):
            shutil.rmtree(self.test_config_dir)
            
    def tearDown(self):
        if os.path.exists(self.test_config_dir):
            shutil.rmtree(self.test_config_dir)

    @patch('web_system.integration.web_log_handler.ClientIdentity')
    @patch('requests.post')
    @patch('requests.get')
    def test_log_payload_contains_instance_id(self, mock_get, mock_post, mock_identity_cls):
        # Mock ClientIdentity
        mock_identity = MagicMock()
        mock_identity.instance_id = "test-uuid-12345"
        mock_identity.hostname = "test-host"
        mock_identity.get_metadata.return_value = {"os_info": "TestOS", "version": "1.0"}
        mock_identity_cls.return_value = mock_identity
        
        # Mock connection check
        mock_get.return_value.status_code = 200
        
        # Initialize handler
        handler = WebLogHandler(
            api_url="http://localhost:8000/api",
            api_key="test-key",
            batch_size=1,
            flush_interval=0.1
        )
        
        # Create a log record
        record = logging.LogRecord(
            name="test_component",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        # Format record
        log_data = handler._format_log_record(record)
        
        # Verify instance_id is in payload
        self.assertEqual(log_data['instance_id'], "test-uuid-12345")
        
        # Verify registration was called
        # The handler calls _register_instance in __init__ -> _test_connection
        # We need to check if requests.post was called with registration data
        
        # Filter calls to find the registration call
        registration_call = None
        for call in mock_post.call_args_list:
            if '/instances' in call[0][0]:
                registration_call = call
                break
                
        self.assertIsNotNone(registration_call, "Registration endpoint was not called")
        self.assertEqual(registration_call[1]['json']['id'], "test-uuid-12345")

if __name__ == '__main__':
    unittest.main()
