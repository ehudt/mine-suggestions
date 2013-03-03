from sys import argv
from urllib2 import Request, urlopen
from urllib import urlencode
import json
import re

SUGGESTION_URL = 'http://suggestqueries.google.com/complete/search' # URI for suggest API
SUGGEST_CLIENT_TYPE = 'firefox' # set reply type to JSON

def get_suggestions(prefix):
	if prefix is None or len(prefix) == 0:
		return []
	req = Request('{0}?{1}'.format(SUGGESTION_URL, urlencode({'q':prefix, 'client':SUGGEST_CLIENT_TYPE})))
	try:
		resp = urlopen(req)
	except URLError, e:
		return []

	# check for request errors that weren't raised by urllib
	if resp.code / 100 >= 4:
		return []

	suggestions = json.loads(resp.read())[1]
	resp.close()
	return suggestions

def search_prefixes(): # temporary
	return ['get', 'how to', 'how can i', 'why']

QUERY_BASE = 'http://www.google.com/search'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'
COUNT_REGEX = 'About ([0-9,]*) results'

def run_query(query_str):
	req = Request('{0}?{1}'.format(QUERY_BASE, urlencode({'q':query_str.replace(' ', '+')})))
	req.add_header('User-Agent', USER_AGENT)
	try:
		resp = urlopen(req)
	except URLError, e:
		return 0, None
	body = resp.read()
	match = re.search(COUNT_REGEX, body)
	if match is None:
		return 0, None
	result_count = int(match.group(1).replace(',',''))
	return result_count, None


def main():
	search_pages = {}
	for prefix in search_prefixes():
		for query_str in get_suggestions(prefix):
			search_pages[query_str], _ = run_query(query_str)
			print '%s : %d results' % (query_str, search_pages[query_str])
	print search_pages


if __name__ == '__main__':
	main()