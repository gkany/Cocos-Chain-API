#-*- coding: utf-8  -*-

import unittest
from utils import *
from config import *
import sys
from websocket import create_connection

class test_network_broadcast_api(websocket_unittest):
    @classmethod
    def setUpClass(self):
        self.ws = create_connection(node_ws_url)
        req_data = {
            "id":1,
            "method":"call",
            "params":[1, "network_broadcast", []]
        }
        self.handle = ws_post(self.ws, req_data)['result']

        req_data = {
            "jsonrpc": "2.0",
            "method": "unlock",
            "params": [wallet_password],
            "id":1
        }
        request_post(req_data, is_wallet_rpc=True)

        req_data = {
            "jsonrpc": "2.0",
            "method": "import_key",
            "params": [test_account, test_account_private_key],
            "id":1
        }
        request_post(req_data, is_wallet_rpc=True)
        print('{} done\n'.format(sys._getframe().f_code.co_name))

    @classmethod
    def tearDownClass(self):
        self.ws.close()
        print('{} done\n'.format(sys._getframe().f_code.co_name))

# (broadcast_transaction)(broadcast_transaction_with_callback)
# (broadcast_transaction_synchronous)(broadcast_block))

    @unittest.skipIf(False, 'test other')
    def test_broadcast_transaction(self):
        req_data = {
            "method": "transfer",
            "params": [test_account, test_witness_account, "0.1", core_asset, ["test broadcast_transaction", 'false'], 'false'],
            "id":1
        }
        result = request_post(req_data, is_wallet_rpc=True)['result']
        # transaction_id = result[0]
        trx = result[1]
        block_num_from = 10
        block_num_to = 48
        req_data = {
            "id":1,
            "method":"call",
            "params":[self.handle, "broadcast_transaction", [trx]]
        }
        self.ws_post(self.ws, req_data)
        print('{} done\n'.format(sys._getframe().f_code.co_name))

# >> transfer ['nicotest', 'init1', '0.1', 'COCOS', ['test broadcast_transaction_with_callback', 'false'], 'false']
# {u'jsonrpc': u'2.0', u'id': 1, u'result': [u'fce1dd11e37a1f5dabb51f85656444965b1bb1a60237743a54d83271d1f70f7e', {u'ref_block_prefix': 1028192142, u'operations': [[0, {u'to': u'1.2.6', u'amount': {u'asset_id': u'1.3.0', u'amount': 10000}, u'from': u'1.2.17', u'memo': [0, u'test broadcast_transaction_with_callback'], u'extensions': []}]], u'signatures': [u'205128e407b696d9ca580e231ac85b9b5ec7e98b783baf52a94289ced3162dc60244c45a541500efe7583eb216c57cefe53b08df49b735826af55b9688ddbd1aae'], u'ref_block_num': 13697, u'extensions': [], u'expiration': u'2019-12-03T09:31:24'}]}

#   void broadcast_transaction_with_callback(confirmation_callback cb, const signed_transaction &trx);
    @unittest.skipIf(True, 'test other')
    def test_broadcast_transaction_with_callback(self):
        req_data = {
            "method": "transfer",
            "params": [test_account, test_witness_account, "0.1", core_asset, ["test broadcast_transaction_with_callback", 'false'], 'false'],
            "id":1
        }
        result = request_post(req_data, is_wallet_rpc=True)['result']
        # transaction_id = result[0]
        trx = result[1]
        block_num_from = 10
        block_num_to = 48
        req_data = {
            "id":1,
            "method":"call",
            "params":[self.handle, "broadcast_transaction_with_callback", [test_callback, trx]]
        }
        self.ws_post(self.ws, req_data)
        print('{} done\n'.format(sys._getframe().f_code.co_name))

    @unittest.skipIf(True, 'test other')
    def test_broadcast_transaction_synchronous(self):
        req_data = {
            "method": "transfer",
            "params": [test_account, test_witness_account, "0.1", core_asset, ["test broadcast_transaction_synchronous", 'false'], 'false'],
            "id":1
        }
        result = request_post(req_data, is_wallet_rpc=True)['result']
        # transaction_id = result[0]
        trx = result[1]
        block_num_from = 10
        block_num_to = 48
        req_data = {
            "id":1,
            "method":"call",
            "params":[self.handle, "broadcast_transaction_synchronous", [trx]]
        }
        self.ws_post(self.ws, req_data)
        print('{} done\n'.format(sys._getframe().f_code.co_name))

    @unittest.skipIf(True, 'test other')
    def test_broadcast_block(self):
        req_data = {
            "method": "info",
            "params": [],
            "id":1
        }
        info = request_post(req_data, is_wallet_rpc=True)['result']
        head_block_num = info['head_block_num']
        req_data = {
            "method": "get_block",
            "params": [head_block_num],
            "id":1
        }
        block = request_post(req_data, is_wallet_rpc=True)['result']
        # print('block: {}'.format(block))
        req_data = {
            "id":1,
            "method":"call",
            "params":[self.handle, "broadcast_block", [block]]
        }
        self.ws_post(self.ws, req_data)
        print('{} done\n'.format(sys._getframe().f_code.co_name))

if __name__ == '__main__':
    unittest.main()


'''
  File "/usr/lib/python2.7/json/encoder.py", line 184, in default
    raise TypeError(repr(o) + " is not JSON serializable")
TypeError: <function test_callback at 0x7fab41f35140> is not JSON serializable

回调函数json序列化问题
'''
'''
dev@ubuntu:~/data/mrepo/Cocos-chain-api$ python3 t04_network_broadcast_api.py 
>> call [1, 'network_broadcast', []]
{'jsonrpc': '2.0', 'result': 2, 'id': 1}

>> unlock ['123456']
{'jsonrpc': '2.0', 'result': None, 'id': 1}

>> import_key ['nicotest', '5J2SChqa9QxrCkdMor9VC2k9NT4R4ctRrJA6odQCPkb3yL89vxo']
{'jsonrpc': '2.0', 'result': True, 'id': 1}

setUpClass done

s>> transfer ['nicotest', 'init1', '0.1', 'COCOS', ['test broadcast_transaction', 'false'], 'false']
{'jsonrpc': '2.0', 'result': ['84e6e8f0e00876bcec396cb57d2c8d47d848502bba25555f9019b65e843ef166', {'extensions': [], 'ref_block_num': 11704, 'expiration': '2020-08-05T09:00:22', 'ref_block_prefix': 669180122, 'operations': [[0, {'to': '1.2.6', 'amount': {'amount': 10000, 'asset_id': '1.3.0'}, 'extensions': [], 'memo': [0, 'test broadcast_transaction'], 'from': '1.2.16'}]], 'signatures': ['20155fb6f99c2498448a5b63425536fa207210d78a5441c26fa6440a92af093e191ddb728503781c496e81532ad33d50593747f01b017cf20c0607ad107eb4b94d']}], 'id': 1}

>> call [2, 'broadcast_transaction', [{'extensions': [], 'ref_block_num': 11704, 'expiration': '2020-08-05T09:00:22', 'ref_block_prefix': 669180122, 'operations': [[0, {'to': '1.2.6', 'amount': {'amount': 10000, 'asset_id': '1.3.0'}, 'extensions': [], 'memo': [0, 'test broadcast_transaction'], 'from': '1.2.16'}]], 'signatures': ['20155fb6f99c2498448a5b63425536fa207210d78a5441c26fa6440a92af093e191ddb728503781c496e81532ad33d50593747f01b017cf20c0607ad107eb4b94d']}]]
{'jsonrpc': '2.0', 'result': '84e6e8f0e00876bcec396cb57d2c8d47d848502bba25555f9019b65e843ef166', 'id': 1}

test_broadcast_transaction done

.sstearDownClass done


----------------------------------------------------------------------
Ran 4 tests in 0.025s

OK (skipped=3)

######################## 根据broadcast_transaction api返回的transaction_id，链上交易查询结果如下：
unlocked >>> get_transaction_in_block_info 84e6e8f0e00876bcec396cb57d2c8d47d848502bba25555f9019b65e843ef166 
get_transaction_in_block_info 84e6e8f0e00876bcec396cb57d2c8d47d848502bba25555f9019b65e843ef166 
{
  "id": "3.1.1265",
  "block_num": 11713,
  "trx_in_block": 0,
  "trx_hash": "84e6e8f0e00876bcec396cb57d2c8d47d848502bba25555f9019b65e843ef166"
}
unlocked >>> get_block 11713
get_block 11713
{
  "previous": "00002dc0b2dcff5248e30fa7de5a5740f0fb1e66",
  "timestamp": "2020-08-05T08:39:54",
  "witness": "1.6.1",
  "transaction_merkle_root": "851e5c946306adb09f43ab6d4521bfd7883ebe7b",
  "witness_signature": "2008e4324d8db04074b6a697ac642ee78731a30264bcced1bf5ce56c1f8ab370fb1feb8af5783b70bbeed4f4f667ee7ec05dec78f7520929a887d4533afa2dda18",
  "block_id": "00002dc1999e0b3ca5d0ecfce5a143383603f2c6",
  "transactions": [[
      "84e6e8f0e00876bcec396cb57d2c8d47d848502bba25555f9019b65e843ef166",{
        "ref_block_num": 11704,
        "ref_block_prefix": 669180122,
        "expiration": "2020-08-05T09:00:22",
        "operations": [[
            0,{
              "from": "1.2.16",
              "to": "1.2.6",
              "amount": {
                "amount": 10000,
                "asset_id": "1.3.0"
              },
              "memo": [
                0,
                "test broadcast_transaction"
              ],
              "extensions": []
            }
          ]
        ],
        "extensions": [],
        "signatures": [
          "20155fb6f99c2498448a5b63425536fa207210d78a5441c26fa6440a92af093e191ddb728503781c496e81532ad33d50593747f01b017cf20c0607ad107eb4b94d"
        ],
        "operation_results": [[
            1,{
              "fees": [{
                  "amount": 2028320,
                  "asset_id": "1.3.0"
                }
              ],
              "real_running_time": 109
            }
          ]
        ]
      }
    ]
  ]
}
unlocked >>> 
'''

