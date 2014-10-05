from kivy.network.urlrequest import UrlRequest
import json

headers = {'Content-type': 'application/json',
		'Accept': 'application/json; charset=UTF-8'}


 
class KivyConnNeo(object):
	def __init__(self,base_url="http://127.0.0.1:7474"):
		self.base_url = base_url
		self.results = []
		
	def post_query(self,req,result):
		#print json.dumps(result,indent=4, sort_keys=True)
		if result:
			for key, value in result.iteritems():
				if key == 'errors':
					for s in value:
						print s['message']
				elif key == 'results':
					for s in value:
						for t in s['data']:
							for e in t['row']:
								self.results.append(e)

		
	def print_error(self,req,error):
		print type(error)
		print error

	def cypher(self, query):
		self.query = query
		self.params = json.dumps({
		"statements" : [ {
		"statement" : ""+self.query+"",
		"resultDataContents" : [ "row", "graph" ]
		} ]
		})

		self.req = UrlRequest(self.base_url + '/db/data/transaction/commit',
			on_success=self.post_query ,req_headers=headers, on_error=self.print_error, req_body = self.params , debug = True, method = 'POST')

		self.req.wait(delay=0.5)
