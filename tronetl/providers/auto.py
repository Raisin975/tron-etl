# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
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


from urllib.parse import urlparse
from web3 import HTTPProvider, IPCProvider
from tronetl.providers.rpc import BatchRESTProvider
from tronetl.providers.rpc import BundleBatchRESTProvider

from tronetl.providers.ipc import BatchIPCProvider
from tronetl.providers.rpc import BatchHTTPProvider


DEFAULT_TIMEOUT = 60

def get_transaction_bundle_web3_provider_from_uri_list(uri_string_list, method_list):
    assert(len(uri_string_list) == len(method_list))
    for uri_string in uri_string_list:
        uri = urlparse(uri_string)
        if uri.scheme != 'http' and uri.scheme != 'https':
            raise ValueError('Unknown uri scheme {}'.format(uri_string))
    return BundleBatchRESTProvider(uri_string_list, method_list)

    
def get_rest_provider_from_uri(uri_string, method):
    uri = urlparse(uri_string)
    if uri.scheme == 'http' or uri.scheme == 'https':
        return BatchRESTProvider(uri_string, method)
    else:
        raise ValueError('Unknown uri scheme {}'.format(uri_string))


def get_json_provider_from_uri(uri_string, timeout=DEFAULT_TIMEOUT, batch=False):
    uri = urlparse(uri_string)
    if uri.scheme == 'file':
        if batch:
            return BatchIPCProvider(uri.path, timeout=timeout)
        else:
            return IPCProvider(uri.path, timeout=timeout)
    elif uri.scheme == 'http' or uri.scheme == 'https':
        request_kwargs = {'timeout': timeout}
        if batch:
            return BatchHTTPProvider(uri_string, request_kwargs=request_kwargs)
        else:
            return HTTPProvider(uri_string, request_kwargs=request_kwargs)
    else:
        raise ValueError('Unknown uri scheme {}'.format(uri_string))