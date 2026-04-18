# -*- coding:utf-8 -*-
"""
DataHunter DAO - 去中心化 AI 数据标注平台
基于区块链的加权多数共识 + Commit-Reveal 机制
"""
from .blockchain import BlockChain, Block, Transaction, TransactionEncoder
from .contracts import (
    DataHunterDAO,
    DHToken,
    TaskManager, TaskType, TaskStatus, Task,
    SubmissionContract, SubmissionPhase, ConsensusResult,
    ReputationContract, ReputationTier, NodeProfile,
)

__version__ = '1.0.0'

__all__ = [
    # Blockchain layer
    'BlockChain', 'Block', 'Transaction', 'TransactionEncoder',
    # Contracts layer
    'DataHunterDAO',
    'DHToken',
    'TaskManager', 'TaskType', 'TaskStatus', 'Task',
    'SubmissionContract', 'SubmissionPhase', 'ConsensusResult',
    'ReputationContract', 'ReputationTier', 'NodeProfile',
]
