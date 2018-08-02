import requests
import simplejson as json

page_url = 'http://primedice.com'
r = requests.post(page_url)

print r.text
