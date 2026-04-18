# -*- coding:utf-8 -*-
import hashlib
import json
import time
from .transaction import TransactionEncoder


class Block:

    def __init__(self, timestamp, transactions, previous_hash=''):
        if not isinstance(timestamp, (int, float)):
            raise TypeError(f"时间戳必须是数字, 收到: {type(timestamp).__name__}")
        if not isinstance(transactions, list):
            raise TypeError(f"交易列表必须是 list, 收到: {type(transactions).__name__}")
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        raw_str = (self.previous_hash
                   + str(self.timestamp)
                   + json.dumps(self.transactions, ensure_ascii=False, cls=TransactionEncoder)
                   + str(self.nonce))
        return hashlib.sha256(raw_str.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        if not isinstance(difficulty, int) or difficulty < 0:
            raise ValueError(f"难度必须是非负整数, 收到: {difficulty}")
        time_start = time.perf_counter()
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        elapsed = time.perf_counter() - time_start
        print(f"挖到区块:{self.hash}, 耗时: {elapsed:.6f}秒")
