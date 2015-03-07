#!/usr/bin/python
import threading
import dns, dns.message, dns.query
import csv
import json

class AlexaDNS(threading.Thread):
	def __init__(self, domain, nameServer):
		threading.Thread.__init__(self)
		self.domain = domain
		self.nameServer = nameServer

	def run(self):
		self.results = {}
		self.results['nameServer'] = self.nameServer
		self.results['domain'] = self.domain
		self.failed = True

		request = dns.message.make_query(self.domain, dns.rdatatype.AAAA)

		try:
			response = dns.query.udp(request, self.nameServer, 5)
			answers = response.answer
			self.response = response
			self.results['response'] = [answer.to_text for answer in answers]
			self.failed = False
		except dns.exception.Timeout:
			self.failed = True
		except Exception as e:
			self.results['err'] = e

		self.results['failed'] = self.failed

		with open('AlexaResults.csv', 'ab') as writeFile:
			fieldnames = ['domain', 'failed', 'response', 'nameServer', 'err']
			writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
			writer.writerow(self.results)



def main():

	with open('AlexaResults.csv', 'wb') as writeFile:
		fieldnames = ['domain', 'failed', 'response', 'nameServer', 'err']
		writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
		writer.writeheader()

	nameServer = "2001:4860:4860::8888"
	with open('top-1m.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		lines = list(reader)
		for line in lines[:1000]:
			domain = line[1] # 2 columns in CSV, get domain
			AlexaDNSLookup = AlexaDNS(domain, nameServer)
			AlexaDNSLookup.run()

if __name__ == '__main__':
	main()




				

			