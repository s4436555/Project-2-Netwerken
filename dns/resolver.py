#!/usr/bin/env python2

""" DNS Resolver

This module contains a class for resolving hostnames. You will have to implement
things in this module. This resolver will be both used by the DNS client and the
DNS server, but with a different list of servers.
"""

import socket

from dns.classes import Class
from dns.types import Type

import dns.cache
import dns.message
import dns.rcodes

class Resolver(object):
    """ DNS resolver """
    
#    root_servers = {
#        "localhost"
#    }
    
    root_servers = {
        "198.41.0.4",       #A.ROOT-SERVERS.NET.
        "192.228.79.201",   #B.ROOT-SERVERS.NET.
        "192.33.4.12",      #C.ROOT-SERVERS.NET.
        "199.7.91.13",      #D.ROOT-SERVERS.NET.
        "192.203.230.10",   #E.ROOT-SERVERS.NET.
        "192.5.5.241",      #F.ROOT-SERVERS.NET.
        "192.112.36.4",     #G.ROOT-SERVERS.NET.
        "198.97.190.53",    #H.ROOT-SERVERS.NET.
        "192.36.148.17",    #I.ROOT-SERVERS.NET.
        "192.58.128.30",    #J.ROOT-SERVERS.NET.
        "193.0.14.129",     #K.ROOT-SERVERS.NET.
        "199.7.83.42",      #L.ROOT-SERVERS.NET.
        "202.12.27.33"      #M.ROOT-SERVERS.NET.
    }
    
    def __init__(self, caching, ttl):
        """ Initialize the resolver
        
        Args:
            caching (bool): caching is enabled if True
            ttl (int): ttl of cache entries (if > 0)
        """
        self.caching = caching
        self.ttl = ttl
    
    def _get_response(self, sock, nameservers, query):
        for ns in nameservers:
            try:
                sock.sendto(query.to_bytes(), (ns, 53))
                # Receive response
                data = sock.recv(512)
                response = dns.message.Message.from_bytes(data)
                
                return response
            except socket.timeout:
                pass
        return None
        
    def _get_single_A(self, sock, nameservers, hostname):
        question = dns.message.Question(hostname, Type.A, Class.IN)
        header = dns.message.Header(9001, 0, 1, 0, 0, 0)
        header.qr = 0
        header.opcode = 0
        header.rd = 1
        query = dns.message.Message(header, [question])
        
        return self._get_response(sock, nameservers, query)
    
    def _cache_get_ns_ip(self, hostname):
        print ("_cache_get_ns_ip")
        nameservers = []
        
        while nameservers == []:
            split = hostname.split(".", 1)
            if (len(split) > 1):
                hostname = split[1]
            else:
                return self.root_servers
            addresses = self.cache.lookup(hostname, Type.NS, Class.IN)
            if addresses != []:
                for address in p_addresses:
                    nameservers.append(address.rdata.data)
        
        return nameservers
    
    def get_ns(self, sock, nameservers, authorities):
        NS_answers = [ans for ans in authorities if ans.type_ == Type.NS]
        for answer in NS_answers:
            response = self._get_single_A(sock, nameservers, answer.rdata.data)
            
            for answer2 in [ans for ans in response.answers + response.additionals if ans.type_ == Type.A]:
                if answer2.name == answer.name:
                    yield answer.rdata.data
    
    def extract_ip(self, authorities, additionals, hostname):
        """ Mandatory function to get NS ip addresses from the additionals when
            asking the root server for information.
        """
        addresses = []
        remaining = []
        for ns in [ans for ans in authorities if ans.type_ == Type.NS]:
            #TODO check if this ns could be useful
            ns_name = ns.rdata.data
            found = False
            for answer in [ans for ans in additionals if ans.type_ == Type.A]:
                if answer.name == ns_name:
                    addresses.append(answer.rdata.data)
            if not found:
                remaining.append(ns)
        return addresses, remaining
        
    def get_hostname_helper(self, sock, nameservers, hostname):
        """ Will break down as soon as something like xxx.nl. -> yyy.com. 
            happens.
        """
        hostname = hostname.rstrip(".") #framework can't handle "" or anything ending with a dot

        aliases = []
        addresses = []

        #1. See if the answer is in local information, and if so return it to the client.
        if self.caching:
            for alias in self.cache.lookup(hostname, Type.CNAME, Class.IN):
                aliases.append(alias.rdata.data)
            for address in self.cache.lookup(hostname, Type.A, Class.IN):
                addresses.append(address.rdata.data)
            
            if aliases != []:
                return hostname, aliases, addresses

        #3. Send them queries until one returns a response.
        # Create and send query
        
        while True:
            response = self._get_single_A(sock, nameservers, hostname)
            
            if response == None:
                break
            
            for answer in [ans for ans in response.answers + response.additionals if ans.type_ == Type.A and ans.name == hostname]:
                addresses.append(answer.rdata.data)
            for additional in [ans for ans in response.additionals if ans.type_ == Type.CNAME and ans.name == hostname]:
                aliases.append(additional.rdata.data)
            if addresses != []:
                break
            
            ns2 = nameservers
            nameservers, remaining = self.extract_ip(response.authorities, response.additionals, hostname)
            if nameservers == []:
                nameservers = self.get_ns(sock, ns2, remaining)
        return hostname, aliases, addresses
    
    
    def gethostbyname(self, hostname):
        """ Translate a host name to IPv4 address.

        Currently this method contains an example. You will have to replace
        this example with the algorithm described in section
        5.3.3 in RFC 1034.

        Args:
            hostname (str): the hostname to resolve

        Returns:
            (str, [str], [str]): (hostname, aliaslist, ipaddrlist)
        """
        
        timeout = 2 # the time waited for a response
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        
        hostname = hostname.rstrip(".") #framework can't handle "" or anything ending with a dot

        aliases = []
        addresses = []

        #1. See if the answer is in local information, and if so return it to the client.
        if self.caching:
            for alias in self.cache.lookup(hostname, Type.CNAME, Class.IN):
                aliases.append(alias.rdata.data)
            for address in self.cache.lookup(hostname, Type.A, Class.IN):
                addresses.append(address.rdata.data)
            
            if aliases != []:
                return hostname, aliases, addresses
        
        #2. Find the best servers to ask.
        if self.caching:
            nameservers = _cache_get_ns_ip(hostname)
        else:
            nameservers = self.root_servers

        #3. Send them queries until one returns a response.
        # Create and send query

        #4. Analyze the response, either:

        #     a. if the response answers the question or contains a name
        #        error, cache the data as well as returning it back to
        #        the client.

        #     b. if the response contains a better delegation to other
        #        servers, cache the delegation information, and go to
        #        step 2.

        #     c. if the response shows a CNAME and that is not the
        #        answer itself, cache the CNAME, change the SNAME to the
        #        canonical name in the CNAME RR and go to step 1.

        #     d. if the response shows a servers failure or other
        #        bizarre contents, delete the server from the SLIST and
        #        go back to step 3.
    
        return self.get_hostname_helper(sock, nameservers, hostname)
        
