#!/usr/bin/env python3

from gevent import monkey; monkey.patch_all()
import gevent

import argparse
import bottle
import urllib


class KleinBottle(bottle.Bottle):
    '''Deriviative of Bottle that sends all requests to one callback resolver.
    The callback should return
        response        {'info': 'lots of information'}
        content_type    json
        status          200
    '''
    def __init__(self, callback, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.callback = callback
        # Send all requests to one function
        self.route('<url:re:.*>', ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                   callback=self.processRequest)

    def parseURL(self, url):
        scheme, netloc, path, queryString, fragment = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(queryString)
        pathList = path.strip('/').split('/')
        return pathList, query

    def getRequestInfo(self):
        pathList, query = self.parseURL(bottle.request.url)
        json = dict(bottle.request.json) if bottle.request.json is not None else {}
        method = bottle.request.method
        # headers = dict(bottle.request.body.headers)
        body = bottle.request.body.readlines()
        return dict(
            pathList=pathList,
            query=query,
            json=json,
            method=method,
            body=body,
            )

    def processRequest(self, url):
        requestData = self.getRequestInfo()
        # Send relevant information so resolver can be independent of bottle
        response, content_type, status = self.callback(**requestData)
        # Set the appropriate bottle references after call is finished
        bottle.response.content_type = content_type
        bottle.response.status = status
        return response

#####################################################################
# Testing stuff below
#####################################################################

def parseArguments():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Start advisor service.')
    parser.add_argument('-p', action='store', default='8880',
                        dest='port', help='Port (default 8880)')
    parser.add_argument('-d', action='store_true', default=False,
                        dest='daemon', help='Run as daemon')
    parser.add_argument('-l', action='store_true', default=False,
                        dest='logger', help='Log service activity')
    parser.add_argument('-f', action='store', dest='logfile',
                        default='/var/log/advisor/advisor.log',
                        help='Logfile name')
    parser.add_argument('-t', action='store_true', default=False,
                        dest='testing', help='Run doctests')
    parser.add_argument('--datafile', action='store', dest='datafile',
                        default='/var/lib/advisor/advisor.sqlite3',
                        help='Data directory')
    return parser.parse_args()

def testCallback(**args):
    print(args)
    return args, 'application/json', 200

def main():
    args = parseArguments()
    example = KleinBottle(testCallback)
    example.run(host='0.0.0.0', port=int(args.port), server='gevent')

if __name__ == '__main__':
    main()
