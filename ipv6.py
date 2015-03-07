import threading
import socket
import urllib2
import json
import dns


# These four lines are a complete hack to force urllib2 to use IPv6
# We change the default socket info to use the AF_INET6 family
origGetAddrInfo = socket.getaddrinfo

def getAddrInfoWrapper(host, port, family=0, socktype=0, proto=0, flags=0):
	return origGetAddrInfo(host, port, socket.AF_INET6, socktype, proto, flags)

socket.getaddrinfo = getAddrInfoWrapper


class myCheck6(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.results = {}
    
    def run(self):

        # Open socket and try to connect to it, store results in dictionary
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        try:
            self.sock.connect(("theverge.com",80))
        except socket.error:
            pass
        self.results['address'] = self.sock.getsockname()[0]
        self.sock.close()
        self.loadPage()
        self.DNSTest()
        return

    def loadPage(self):
        self.pageLoaded = True
        try:
            urllib2.urlopen("http://www.facebook.com/").read(100)
        except urllib2.URLError:
            self.pageLoaded = False

        self.results['pageLoaded'] = str(self.pageLoaded) # str() Just in case

    def DNSTest(self):
        import dns.message
        import dns.query
        
        domain = "www.google.com"
        self.DNSSuccess = True

        request = dns.message.make_query(domain, dns.rdatatype.AAAA) #IPv6 record

        try:
            response = dns.query.udp(request, "2001:4860:4860::8888", 5)
        except dns.exception.Timeout:
            self.DNSSuccess = False

        # Just to make sure it actually works
        #answers = response.answer 
        #print([answer.to_text() for answer in answers])

        self.results['DNSSuccess'] = str(self.DNSSuccess)
        #print(json.dumps(self.results))
