# -*- coding:utf-8 -*-
import time
from .block import Block
from .transaction import Transaction


class BlockChain:
    def __init__(self):
        self.chain = [self._create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []
        self.mining_reward = 100

    @staticmethod
    def _create_genesis_block():
        timestamp = time.mktime(time.strptime('2018-06-11 00:00:00', '%Y-%m-%d %H:%M:%S'))
        return Block(timestamp, [], '')

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError(f"必须传入 Transaction 实例, 收到: {type(transaction).__name__}")
        self.pending_transactions.append(transaction)

    def mine_pending_transaction(self, mining_reward_address):
        if not mining_reward_address:
            raise ValueError("挖矿奖励地址不能为空")
        block = Block(time.time(), self.pending_transactions, self.chain[-1].hash)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.pending_transactions = [
            Transaction(None, mining_reward_address, self.mining_reward)
        ]

    def get_balance_of_address(self, address):
        balance = 0
        for block in self.chain:
            for trans in block.transactions:
                if trans.from_address == address:
                    balance -= trans.amount
                if trans.to_address == address:
                    balance += trans.amount
        return balance

    def verify_blockchain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.calculate_hash():
                return False
        return True
