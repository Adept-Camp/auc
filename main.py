from dotmap import DotMap
from brownie import *
from brownie.network.gas.strategies import GasNowStrategy
import json
from dotenv import load_dotenv
import os
import requests
from rich.status import Status
from brownie.network import gas_price

load_dotenv()
wallet = os.getenv( 'wallet' )
brownie = os.getenv( 'network' )

network.connect( brownie )
me = accounts.default = accounts.load( wallet )

strategy = GasNowStrategy( speed='rapid' )
gas_price( strategy )

with open( 'accounts_.json', 'r' ) as f:
    accounts = DotMap( json.load( f ) )

c = Contract.from_explorer( '0xA39d1e9CBecdb17901bFa87a5B306D67f15A2391' )


def claim(r):
    d = DotMap()
    d.id = r['id']
    d.account = r['account']
    d.amount = int( '0' + r['amount'] )
    d.r = int( '0' + r['r'] )
    d.s = int( '0' + r['s'] )
    d.v = int( '0' + r['v'] )

    c.claim( d.id, d.account, d.amount, d.v, d.r, d.s )


with Status( 'API not updated..' ):
    while True:
        url = f'https://cu3pxr9ydi.execute-api.us-east-1.amazonaws.com/prod/distributor' \
              f'/{accounts.main}'
        r = requests.get( url ).json()[0]
        if r['id'] != '':
            claim( r )
            for a in accounts.others:
                url = f'https://cu3pxr9ydi.execute-api.us-east-1.amazonaws.com/prod/distributor' \
                      f'/{a}'
            r = requests.get( url ).json()[0]
            claim( r )
