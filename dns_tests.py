#!/usr/bin/env python2
import unittest
import socket
import sys

import dns.resolver

""" Tests for your DNS resolver and server """

portnr = 5353
server = "localhost"

class TestResolver(unittest.TestCase):
    """Test cases for GET requests"""

    def setUp(self):
        """Prepare for testing"""


    def tearDown(self):
        """Clean up after testing"""


    def test_not_empty_valid(self):
        """..."""
        hostname = "www.google.nl."
        resolver = dns.resolver.Resolver(False, 64)
        found_host = resolver.gethostbyname(hostname)
        self.assertNotEqual([], found_host[2])

    def test_empty_valid(self):
        """..."""
        hostname = "www.google.nl.maffia."
        resolver = dns.resolver.Resolver(False, 64)
        found_host = resolver.gethostbyname(hostname)
        self.assertEqual([], found_host[2])


class TestResolverCache(unittest.TestCase):
    pass


class TestServer(unittest.TestCase):
    pass


if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="HTTP Tests")
    parser.add_argument("-s", "--server", type=str, default="localhost")
    parser.add_argument("-p", "--port", type=int, default=5001)
    args, extra = parser.parse_known_args()
    portnr = args.port
    server = args.server
    
    # Pass the extra arguments to unittest
    sys.argv[1:] = extra

    # Start test suite
    unittest.main()
