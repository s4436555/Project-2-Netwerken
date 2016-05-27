#!/usr/bin/env python2
import unittest
import socket
import sys

import dns.resolver

""" Tests for your DNS resolver and server """

portnr = 5353
server = "localhost"

class TestResolver(unittest.TestCase):

    def setUp(self):
        """ Prepare for testing """


    def tearDown(self):
        """ Clean up after testing """


    def test_valid_fqdn(self):
        """ ... """
        hostname = "www.google.nl."
        resolver = dns.resolver.Resolver(False, 64)
        found_host = resolver.gethostbyname(hostname)
        self.assertNotEqual([], found_host[2])

    def test_invalid_fqdn(self):
        """ Checks if the output is empty if the FQDN does not exist """
        hostname = "www.google.nl.maffia."
        resolver = dns.resolver.Resolver(False, 64)
        found_host = resolver.gethostbyname(hostname)
        self.assertEqual([], found_host[2])


class TestResolverCache(unittest.TestCase):
    
    def setUp(self):
        """ Prepare for testing """


    def tearDown(self):
        """ Clean up after testing """
        
        
    def check_add_to_cache(self):
        """ Checks if the answers are added to the cache """
        pass
        
    def check_existing_cache(self):
        """ Checks if the cache is used when answering queries """
        pass
        
    def check_cache_expiration(self):
        """ Checks if old entries are no longer used after expiring """
        pass

class TestServer(unittest.TestCase):
    
    def setUp(self):
        """ Prepare for testing """
        # TODO
        pass


    def tearDown(self):
        """ Clean up after testing """
        # TODO
        pass
    
    def check_fqdn_direct_authority(self):
        """ Checks if the server is able to solve a query for a FQDN for which 
            the server has direct authority
        """
        pass
    
    def check_fqdn_in_zone(self):
        """ Checks if the server is able to solve a query for a FQDN for which
            the server has no direct authority, but knows a name server in it's 
            zone which does 
        """
        pass
        
    def check_fqdn_outside_zone(self):
        """ Checks if the server is able to solve a query for a FQDN that is 
            outside of it's zone
        """
        pass
        
    def check_parallel_requests(self):
        """ Checks if the server is able to correctly handle parallel requests 
        """
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
