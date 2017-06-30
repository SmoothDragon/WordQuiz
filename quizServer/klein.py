#!/usr/bin/env python3

from gevent import monkey; monkey.patch_all()
import gevent

import argparse
import bottle
import urllib
import flask


class bottleWrapper(bottle.Bottle):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.response = bottle.response
        self.request = bottle.request
        self.abort = bottle.abort

class Klein:
    '''Deriviative of Bottle that sends all requests to one callback resolver.
    The callback should return
        response        {'info': 'lots of information'}
        content_type    json
        status          200
    TODO: Add WebFramework dependency injection
    '''
    def __init__(self, callback, 
                 framework=bottle.Bottle,
                 response=bottle.response,
                 request=bottle.request,
                 abort=bottle.abort,
                 *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.framework = framework(*args, **kwargs)
        self.callback = callback
        # Send all requests to one function
        self.framework.route('<url:re:.*>', ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], callback=self.processRequest)
        self.response = response
        self.request = request
        self.abort = abort

    def run(self, *args, **kwargs):
        self.framework.run(*args, **kwargs)

    @classmethod
    def parseURL(cls, url):
        '''
        >>> Klein.parseURL('/one/two/three?a=1&b=2&b=3')
        (['one', 'two', 'three'], {'b': ['2', '3'], 'a': ['1']})
        '''
        scheme, netloc, path, queryString, fragment = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(queryString)
        pathList = path.strip('/').split('/')
        return pathList, query

    def getRequestInfo(self):
        pathList, query = self.parseURL(self.request.url)
        json = dict(self.request.json) if self.request.json is not None else {}
        method = self.request.method
        # headers = dict(self.request.body.headers)
        body = self.request.body.readlines()
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
        if status == 404:
            self.abort(404, 'File not found')
        # Set the appropriate references after call is finished
        self.response.content_type = content_type
        self.response.status = status
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
    example = Klein(testCallback)
    example.run(host='0.0.0.0', port=int(args.port), server='gevent')

def main2():
    args = parseArguments()
    example = Klein(testCallback, framework=flask.Flask)
    example.run(host='0.0.0.0', port=int(args.port), server='gevent')

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
