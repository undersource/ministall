import requests
from requests.auth import HTTPDigestAuth
import config

rpc_user = config.MONERO_RPC_USER
rpc_password = config.MONERO_RPC_PASS
rpc_endpoint = config.MONERO_RPC_ENDPOINT

headers = {'Content-Type': 'application/json'}
rpc_default = {'jsonrpc': '2.0', 'id': '0'}

def check_monero_rpc():
    return requests.post(rpc_endpoint, headers=headers, auth=HTTPDigestAuth(rpc_user, rpc_password))

def create_account(name):
    rpc_input = {
        **rpc_default,
        'method': 'create_account',
        'params': {
            'label': name
        }
    }

    res = requests.post(rpc_endpoint, json=rpc_input, headers=headers, auth=HTTPDigestAuth(rpc_user, rpc_password))
    account_index = res.json()['result']['account_index']
    address = res.json()['result']['address']
    
    return account_index, address

def get_balance(index):
    rpc_input = {
        **rpc_default,
        'method': 'get_balance',
        'params': {
            'account_index': index
        }
    }

    res = requests.post(rpc_endpoint, json=rpc_input, headers=headers, auth=HTTPDigestAuth(rpc_user, rpc_password))
    balance = res.json()['result']['balance']

    return balance