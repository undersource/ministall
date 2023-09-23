from django.shortcuts import render
from shop.monero_rpc import check_monero_rpc
import requests

class MoneroCheck:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        try:
	        check_monero_rpc()
        except requests.exceptions.ConnectionError:
	        return render(request, 'shop/error.html', {'title': 'MiniStall - Error', 'error': '500 - Server error'})

        return self._get_response(request)