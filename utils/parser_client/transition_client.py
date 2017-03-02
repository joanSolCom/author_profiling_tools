#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib2, urllib
import conll

EN_PARSER = "http://services-taln.s.upf.edu:8080/transition/en/parse"
ES_PARSER = "http://multisensor-taln.s.upf.edu:8080/transition/es/parse"
FR_PARSER = "http://multisensor-taln.s.upf.edu:8080/transition/fr/parse"
DE_PARSER = "http://multisensor-taln.s.upf.edu:8080/transition/de/parse"


class TransitionClient(object):

    def __init__(self, parser_url):
        self.parser_url = parser_url
        
    def parse_text(self, text):
        
        params = u"text=%s" % (urllib.quote(text))
        request = urllib2.urlopen(self.parser_url, params)
        response = json.loads(request.read())

        if "error" in response:
            raise Exception(response["error"])

        return conll.ConllStruct(response["output"].encode('utf8'))

if __name__ == "__main__":
    
    text = "My horse's car. Nananana song in the &&& world. This is ññññ `+ `+ `+ ` * + ++ just a tribute."

    parser_en = TransitionClient(EN_PARSER)
    output = parser_en.parse_text(text)
    print output

    print '\n\n\n'

    text = "El coche de mi caballo. Nananana canción en el &&& mundo. Esto es ññññ `+ `+ `+ ` * + ++ solo un tributo."

    parser_es = TransitionClient(ES_PARSER)
    output = parser_es.parse_text(text)
    print output
	
