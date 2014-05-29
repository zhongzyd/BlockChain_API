#################################################
#在python3.4环境下可以正确运行
#调用get_days_needed_to_redo_the_block_chain()即可得到在当前算力下，重做整个区块链所需的天数
#在算力上升的情况下，得出的天数会偏高，在算力下降的情况下，得出的天数会偏低
#需要联网，因为需要调用blockchain.info的API来取得区块的数据，
#请耐心等待，需要几分钟时间才能运行完


import json
import requests
from http import client

def get_difficulty_from_bits(bits):
    e = bits >> 24
    b = bits & ( (1 << 24) - 1 )
    return (0xffff * (256 ** (0x1d - 3))) / (b * (256 ** (e - 3)))

def get_block(block_height):
        block_height = str(block_height)
        conn = client.HTTPConnection("blockchain.info", timeout=10)
        url = "/block-height/%s?format=json" % block_height
        conn.request("GET", url)
        response = conn.getresponse().read().decode('utf-8')
        data = json.loads(response)
        conn.close()
        return data

def get_block_difficulty(block_height):
        block_height = int(block_height)
        while True:
            try:
                block = get_block(block_height)
                bits = block["blocks"][0]["bits"]
            except:
                print("get_block fail, retry.")
                continue
            break
        return get_difficulty_from_bits( bits )

def get_blockchain_difficulty(block_height):
        block_height = int(block_height)
        total_difficulty = 0;
        n = 0
        while n <= block_height - 2016:
                total_difficulty += get_block_difficulty(n) * 2016
                n += 2016
        total_difficulty += get_block_difficulty(n) * (block_height - n + 1)
        return total_difficulty

def get_latest_block_height():
        conn = client.HTTPConnection("blockchain.info", timeout=10)
        url = "/latestblock"
        conn.request("GET", url)
        response = conn.getresponse().read().decode('utf-8')
        data = json.loads(response)
        conn.close()
        return data["height"]

def get_days_needed_to_redo_the_block_chain():
        latest_block_height = get_latest_block_height()
        blockchain_difficulty = get_blockchain_difficulty(latest_block_height)
        latest_block_difficult = get_block_difficulty(latest_block_height)
        needed_minutes = (blockchain_difficulty / latest_block_difficult) * 10
        needed_days = needed_minutes / 60 / 24        
        return needed_days
