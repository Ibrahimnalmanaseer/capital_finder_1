
from http.server import BaseHTTPRequestHandler
from urllib import parse
from webbrowser import get
import requests

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        '''
        display the country name or a capital details depends on user query
        
        '''
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        
        api_path=self.path
        url_components=parse.urlsplit(api_path)
        query=parse.parse_qsl(url_components.query)
        dic_set=dict(query)
        country=dic_set.get('country')
        capital=dic_set.get('capital')

        if not country and not capital:
            self.send_response(404)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(str('Invalid entry, please try again').encode())

            return 
        if country:

            url='https://restcountries.com/v3.1/name/'
            country=dic_set['country']

            r = requests.get(url + country)
            data = r.json()
            capital=data[0]['capital'][0]

            display=f"The capital of {country} is {capital}"
            self.wfile.write(str(display).encode())

        elif capital:
            url='https://restcountries.com/v3.1/capital/'
            capital=dic_set['capital']
            r = requests.get(url + capital)
            data = r.json()
            country= data[0]['name']['common']
            display=f"{capital} is the capital of {country}."
            self.wfile.write(str(display).encode())
        

        

        return