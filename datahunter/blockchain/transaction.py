# -*- coding:utf-8 -*-
import json


class Transaction:
    def __init__(self, from_address, to_address, amount):
        if amount is not None and not isinstance(amount, (int, float)):
            raise TypeError(f"交易金额必须是数字, 收到: {type(amount).__name__}")
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount


class TransactionEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction):
            return o.__dict__
        return super().default(o)
