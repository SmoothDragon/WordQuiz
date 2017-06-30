#!/usr/bin/env python3

# from gevent import monkey; monkey.patch_all()
# import gevent

import argparse
import bottle
import urllib
import flask
import sys
import time

class Request:
    __slots__ = 'url method json'.split()

class bottleWrapper(bottle.Bottle):
    def __init__(self, routeAll, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.routeAll(routeAll)

    def routeAll(self, callback):
        # Send all requests to one function
        self.route('<url:re:.*>', ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], callback=callback)

    def getRequestInfo(self):
        request = Request()
        request.url = bottle.request.url
        request.method = bottle.request.method
        if bottle.request.json is None:
            request.json = {}
        else:
            request.json = dict(bottle.request.json)
        return request

    def setResponseInfo(self,
                   status=200,
                   content_type='application/html',
                   ):
        if status == 404:
            bottle.abort(404, 'File not found')
        bottle.response.status = status
        bottle.response.content_type = content_type


class flaskWrapper(flask.Flask):
    def __init__(self, routeAll, *args, **kwargs):
        super(self.__class__, self).__init__(__name__, *args, **kwargs)
        self.routeAll(routeAll)

    def routeAll(self, callback):
        # Send all requests to one function
        self.add_url_rule('/', view_func=callback, defaults={'path': ''})
        self.add_url_rule('/<path:path>', view_func=callback)
        print("Added rules!")

    def getRequestInfo(self):
        request = Request()
        request.url = flask.request.url
        print(request.url, file=sys.stderr)
        request.method = flask.request.method
        request.json = flask.request.json
        return request

    def setResponseInfo(self,
                   status=200,
                   content_type='application/html',
                   ):
        return


class mockWrapper:
    def __init__(self, routeAll, *args, **kwargs):
        self.routeAll(routeAll)

    def routeAll(self, callback):
        # Send all requests to one function
        self.callback = callback

    def getRequestInfo(self):
        request = Request()
        request.url = 'http://localhost:8880/one/two/three?a=1&b=2&b=3'
        request.method = 'GET'
        request.json = {}
        return request

    def setResponseInfo(self,
                   status=200,
                   content_type='application/html',
                   ):
        return

    def run(self, delay=5, *args, **kwargs):
        while True:
            self.callback('Unused URL')
            time.sleep(delay)


class Klein:
    '''Deriviative of Web Framework that sends all requests to one callback resolver.
    The callback should return
        response        {'info': 'lots of information'}
        content_type    json
        status          200
    TODO: Add WebFramework dependency injection
    '''
    def __init__(self, callback,
                 framework=bottleWrapper,
                 *args, **kwargs):
        self.framework = framework(routeAll=self.processRequest, *args, **kwargs)
        self.callback = callback

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
        request = self.framework.getRequestInfo()
        pathList, query = self.parseURL(request.url)
        # headers = dict(self.request.body.headers)
        # body = self.framework.request.body.readlines()
        return dict(
            pathList=pathList,
            query=query,
            json=request.json,
            method=request.method,
            )

    def processRequest(self, url):
        print('Request initaited', file=sys.stderr)
        requestData = self.getRequestInfo()
        # Send relevant information so resolver can be independent of bottle
        response, content_type, status = self.callback(**requestData)
        self.framework.setResponseInfo(status=status, content_type=content_type)
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
    # example = Klein(testCallback)
    # example = Klein(testCallback, framework=flaskWrapper)
    example = Klein(testCallback, framework=mockWrapper)
    example.run(host='0.0.0.0', port=int(args.port))

def main2():
    args = parseArguments()
    app = flask.Flask(__name__)
    def hello(path):
        print('path: %s' % path)
        print('method: %s' % flask.request.method)
        print('json: %s' % flask.request.json)
        print('url: %s' % flask.request.url)
        # print(flask.path)
        return 'path chosen: %s' % path
    app.add_url_rule('/', view_func=hello, defaults={'path': ''})
    app.add_url_rule('/<path:path>', view_func=hello)
    app.run(host='0.0.0.0', port=int(args.port))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
