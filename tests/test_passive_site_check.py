import unittest
from unittest.mock import patch
import importlib.util, pathlib, sys
p = pathlib.Path(__file__).parents[1] / "scripts" / "passive_site_check.py"
spec = importlib.util.spec_from_file_location("siteguard_checker", p)
m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m; spec.loader.exec_module(m)

class URLTests(unittest.TestCase):
    def test_adds_https(self): self.assertEqual(m.validate_url("Example.com").scheme, "https")
    def test_rejects_file_scheme(self):
        with self.assertRaises(ValueError): m.validate_url("file:///etc/passwd")
    def test_rejects_credentials(self):
        with self.assertRaises(ValueError): m.validate_url("https://u:p@example.com")
    def test_rejects_query(self):
        with self.assertRaises(ValueError): m.validate_url("https://example.com/?token=x")
    def test_rejects_private_ip(self):
        with self.assertRaises(ValueError): m.validate_url("http://127.0.0.1")
    def test_rejects_nonstandard_port(self):
        with self.assertRaises(ValueError): m.validate_url("https://example.com:8443")

class DNSTests(unittest.TestCase):
    @patch("socket.getaddrinfo")
    def test_rejects_private_dns(self, mock):
        mock.return_value = [(None,None,None,None,("10.0.0.1",443))]
        with self.assertRaises(ValueError): m.resolve_public("example.com",443)
    @patch("socket.getaddrinfo")
    def test_accepts_public_dns(self, mock):
        mock.return_value = [(None,None,None,None,("93.184.216.34",443))]
        self.assertEqual(m.resolve_public("example.com",443),"93.184.216.34")

if __name__ == "__main__": unittest.main()
