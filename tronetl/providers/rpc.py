# The MIT License (MIT)
#
# Copyright (c) 2016 Piper Merriam
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import requests as re
import concurrent
import logging
from web3 import HTTPProvider
from web3._utils.request import make_post_request

from tronetl.misc.retriable_value_error import RetriableValueError

class BatchHTTPProvider(HTTPProvider):

    def make_batch_request(self, text):
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                          self.endpoint_uri, text)
        request_data = text.encode('utf-8')
        raw_response = make_post_request(
            self.endpoint_uri,
            request_data,
            **self.get_request_kwargs()
        )
        response = self.decode_rpc_response(raw_response)
        self.logger.debug("Getting response HTTP. URI: %s, "
                          "Request: %s, Response: %s",
                          self.endpoint_uri, text, response)
        return response
    
    
def make_request(url, method, params=None):
    session = re.Session()
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    if method == "GET":
        response = session.get(url, headers=headers, params=params)
    elif method == "POST":
        response = session.post(url, headers=headers, json=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise RetriableValueError(str(response.status_code))

def make_bundle_request(url_list, method_list, params_list):
    bundle_response = []
    for idx, url in enumerate(url_list):
        method = method_list[idx]
        params = params_list[idx]
        bundle_response.append(make_request(url, method, params))
    return bundle_response

class TronFullNodeBatchProvider():
    def __init__(self, uri, method) -> None:
        self.endpoint_uri = uri
        self.method = method
        self.logger = logging.getLogger("BatchRESTProvider")
    
    def make_batch_request(self, batch_params):
        futures = []
        raw_responses = []
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                self.endpoint_uri, str(batch_params))
        # tron rpc does not support batch request, 
        # the number of threads = batch_size * max_worker should not too large 
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(batch_params)) as executor:
            futures = [executor.submit(
                    make_request,
                    self.endpoint_uri, self.method, params
                ) for params in batch_params]
            for future in concurrent.futures.as_completed(futures):
                if future.done():
                    result = future.result()
                    raw_responses.append(result)
                    self.logger.debug("Getting response HTTP. URI: %s, "
                        ", Response: %s", self.endpoint_uri, str(result))
    
        return raw_responses
    
    
class BatchRESTProvider():
    
    def __init__(self, uri, method) -> None:
        self.endpoint_uri = uri
        self.method = method
        self.logger = logging.getLogger("BatchRESTProvider")

    def make_batch_request(self, batch_params):
        futures = []
        raw_responses = []
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                self.endpoint_uri, str(batch_params))
        # tron rpc does not support batch request, 
        # the number of threads = batch_size * max_worker should not too large 
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(batch_params)) as executor:
            futures = [executor.submit(
                    make_request,
                    self.endpoint_uri, self.method, params
                ) for params in batch_params]
            for future in concurrent.futures.as_completed(futures):
                if future.done():
                    result = future.result()
                    raw_responses.append(result)
                    self.logger.debug("Getting response HTTP. URI: %s, "
                        ", Response: %s", self.endpoint_uri, str(result))
    
        return raw_responses

class BundleBatchRESTProvider():
    
    def __init__(self, uri_list, method_list) -> None:
        self.uri_list = uri_list
        self.method_list = method_list
        self.logger = logging.getLogger("BundleBatchRESTProvider")

    def make_batch_request(self, batch_params):
        futures = []
        raw_responses = []
        self.logger.debug("Making request HTTP. URI: %s, Request: %s",
                str(self.uri_list), str(batch_params))
        # tron rpc does not support batch request, 
        # batch_size * max_worker should not too large 
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(batch_params)) as executor:
            futures = [executor.submit(
                    make_bundle_request,
                    self.uri_list, self.method_list, params
                ) for params in batch_params]
            for future in concurrent.futures.as_completed(futures):
                if future.done():
                    result = future.result()
                    raw_responses.append(result)
                    self.logger.debug("Getting response HTTP. URI: %s, "
                        ", Response: %s", str(self.uri_list), str(result))

        return raw_responses