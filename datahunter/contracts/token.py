# -*- coding:utf-8 -*-
"""
DHToken - DataHunter DAO 平台代币
模拟 ERC-20 代币的核心功能：铸造、转账、质押、罚没
"""
import time


class DHToken:
    def __init__(self, name='DataHunter Token', symbol='DHT', total_supply=1_000_000):
        if total_supply < 0:
            raise ValueError("初始发行量不能为负数")
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balances = {}
        self.staked = {}
        self.treasury = 'TREASURY'
        self.balances[self.treasury] = total_supply
        self.tx_log = []

    def _validate_address(self, address):
        if not address or not isinstance(address, str):
            raise ValueError(f"无效地址: {address!r}")

    def _validate_amount(self, amount, label="数量"):
        if not isinstance(amount, (int, float)):
            raise TypeError(f"{label}必须是数字, 收到: {type(amount).__name__}")
        if amount <= 0:
            raise ValueError(f"{label}必须大于0, 收到: {amount}")

    def mint(self, to_address, amount):
        """铸造代币"""
        self._validate_address(to_address)
        self._validate_amount(amount, "铸造数量")
        self.total_supply += amount
        self.balances[self.treasury] = self.balances.get(self.treasury, 0) + amount
        if to_address != self.treasury:
            self._transfer(self.treasury, to_address, amount)
        self._log('MINT', self.treasury, to_address, amount)

    def transfer(self, from_address, to_address, amount):
        """普通转账"""
        self._validate_address(from_address)
        self._validate_address(to_address)
        self._validate_amount(amount, "转账数量")
        if from_address == to_address:
            raise ValueError("不能给自己转账")
        self._transfer(from_address, to_address, amount)
        self._log('TRANSFER', from_address, to_address, amount)

    def balance_of(self, address):
        """查询可用余额（不含质押部分）"""
        return self.balances.get(address, 0)

    def staked_of(self, address):
        """查询已质押余额"""
        return self.staked.get(address, 0)

    def stake(self, address, amount):
        """质押代币：从可用余额转入质押池"""
        self._validate_address(address)
        self._validate_amount(amount, "质押数量")
        if self.balances.get(address, 0) < amount:
            raise ValueError(f"余额不足: 需要 {amount}, 可用 {self.balances.get(address, 0)}")
        self.balances[address] -= amount
        self.staked[address] = self.staked.get(address, 0) + amount
        self._log('STAKE', address, 'STAKE_POOL', amount)

    def unstake(self, address, amount):
        """解除质押：从质押池释放到可用余额"""
        self._validate_address(address)
        self._validate_amount(amount, "解除质押数量")
        if self.staked.get(address, 0) < amount:
            raise ValueError(f"质押余额不足: 需要 {amount}, 已质押 {self.staked.get(address, 0)}")
        self.staked[address] -= amount
        self.balances[address] = self.balances.get(address, 0) + amount
        self._log('UNSTAKE', 'STAKE_POOL', address, amount)

    def slash(self, address, amount):
        """罚没质押金（惩罚恶意节点）"""
        self._validate_address(address)
        self._validate_amount(amount, "罚没数量")
        actual = min(amount, self.staked.get(address, 0))
        if actual == 0:
            return 0
        self.staked[address] -= actual
        self.balances[self.treasury] = self.balances.get(self.treasury, 0) + actual
        self._log('SLASH', address, self.treasury, actual)
        return actual

    def _transfer(self, from_address, to_address, amount):
        if self.balances.get(from_address, 0) < amount:
            raise ValueError(
                f"余额不足: {from_address} 需要 {amount}, 可用 {self.balances.get(from_address, 0)}"
            )
        self.balances[from_address] -= amount
        self.balances[to_address] = self.balances.get(to_address, 0) + amount

    def _log(self, tx_type, from_addr, to_addr, amount):
        self.tx_log.append({
            'type': tx_type,
            'from': from_addr,
            'to': to_addr,
            'amount': amount,
            'timestamp': time.time(),
        })
