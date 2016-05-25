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
    
    def __init__(self, caching, ttl):
        """ Initialize the resolver
        
        Args:
            caching (bool): caching is enabled if True
            ttl (int): ttl of cache entries (if > 0)
        """
        self.caching = caching
        self.ttl = ttl

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

        nameservers = {"8.8.8.8"}
        resolved = False

        parts = []
        prev = ""

        for part in reversed(hostname.split(".")):
            prev = part + "." + prev
            parts.append(prev)

        resolving = 0
        parts_len = len(parts)

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

        #3. Send them queries until one returns a response.
        while not resolved and resolving < parts_len:
            # Create and send query
            question = dns.message.Question(parts[resolving], Type.A, Class.IN)
            header = dns.message.Header(9001, 0, 1, 0, 0, 0)
            header.qr = 0
            header.opcode = 0
            header.rd = 1
            query = dns.message.Message(header, [question])

            for ns in nameservers:
                sock.sendto(query.to_bytes(), (ns, 53))
                # Receive response
                data = sock.recv(512)
                response = dns.message.Message.from_bytes(data)
                break #TODO: add timeout code

            if resolving != parts_len - 1:
                nameservers = [ans for ans in response.answers if ans.type_ == Type.A]
                for ans in response.answers:
                    print ans
                if (len(nameservers) == 0):
                    print "no answers"
                    break
                print "nameserver: " + nameservers[0]
                resolving += 1
            else:
                # Get data
                for additional in response.additionals:
                    if additional.type_ == Type.CNAME:
                        aliases.append(additional.rdata.data)
                for answer in response.answers:
                    if answer.type_ == Type.A:
                        addresses.append(answer.rdata.data)


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

        return hostname, aliases, addresses
