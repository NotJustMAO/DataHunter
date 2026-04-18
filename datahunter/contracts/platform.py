# -*- coding:utf-8 -*-
"""
DataHunterDAO - 主平台整合模块
将 Token、TaskManager、Submission、Reputation 整合为统一平台
同时与底层 BlockChain 对接，将关键事件写入链上
"""
import time
from ..blockchain import BlockChain, Transaction
from .token import DHToken
from .task_manager import TaskManager, TaskType
from .submission import SubmissionContract
from .reputation import ReputationContract


class DataHunterDAO:
    """
    DataHunter DAO 去中心化数据标注平台

    系统角色:
    - Requester (需求方): 发布任务并质押代币
    - Hunter (数据猎手): 领取任务提交答案
    - Validator (验证者): 由共识算法自动担任

    核心流程:
    1. 需求方创建任务 -> 质押代币
    2. 猎手 Commit 答案哈希 -> 质押保证金
    3. 全部提交后进入 Reveal 阶段
    4. 加权多数共识判定 -> 奖惩结算
    5. 结果上链
    """

    def __init__(self, difficulty=2):
        if not isinstance(difficulty, int) or difficulty < 0:
            raise ValueError(f"难度必须是非负整数, 收到: {difficulty}")
        self.blockchain = BlockChain()
        self.blockchain.difficulty = difficulty

        self.token = DHToken()
        self.reputation = ReputationContract()
        self.task_manager = TaskManager(self.token)
        self.submission = SubmissionContract(
            self.task_manager, self.token, self.reputation
        )
        self.platform_log = []

    # ===================== 账户管理 =====================

    def register_requester(self, address, initial_balance=10000):
        """注册需求方并分配初始代币"""
        if initial_balance <= 0:
            raise ValueError(f"初始余额必须大于0, 收到: {initial_balance}")
        self.token.transfer(self.token.treasury, address, initial_balance)
        self._log(f"需求方 {address} 注册成功, 初始余额 {initial_balance} DHT")

    def register_hunter(self, address, initial_balance=500):
        """注册数据猎手并分配初始代币（用于质押）"""
        if initial_balance <= 0:
            raise ValueError(f"初始余额必须大于0, 收到: {initial_balance}")
        self.token.transfer(self.token.treasury, address, initial_balance)
        self.reputation.register(address)
        self._log(f"数据猎手 {address} 注册成功, 初始余额 {initial_balance} DHT")

    # ===================== 任务流程 =====================

    def create_task(self, requester, task_type, description,
                    options=None, reward_per_node=10,
                    required_nodes=3, consensus_threshold=0.5,
                    honeypot_answer=None):
        """需求方发布任务"""
        task = self.task_manager.create_task(
            requester=requester,
            task_type=task_type,
            description=description,
            options=options,
            reward_per_node=reward_per_node,
            required_nodes=required_nodes,
            consensus_threshold=consensus_threshold,
            honeypot_answer=honeypot_answer,
        )
        self._log(f"任务 #{task.task_id} 创建: '{description}' | "
                  f"类型={task_type.value} | 节点数={required_nodes} | "
                  f"每节点奖励={reward_per_node} DHT | 总质押={task.total_stake} DHT")
        return task

    def commit_answer(self, task_id, hunter_address, answer_hash):
        """猎手提交答案哈希（Commit 阶段）"""
        self.submission.commit_answer(task_id, hunter_address, answer_hash)
        self._log(f"猎手 {hunter_address} 对任务 #{task_id} 提交了承诺")

    def reveal_answer(self, task_id, hunter_address, answer, secret):
        """猎手揭示答案（Reveal 阶段）"""
        result = self.submission.reveal_answer(task_id, hunter_address, answer, secret)
        self._log(f"猎手 {hunter_address} 对任务 #{task_id} 揭示了答案")

        if result is not None:
            self._on_consensus_reached(result)

        return result

    def _on_consensus_reached(self, result):
        """共识达成后的回调：记录上链"""
        if result.status == 'CONSENSUS':
            self._log(
                f"=== 任务 #{result.task_id} 共识达成 ===\n"
                f"  最终答案: {result.final_answer}\n"
                f"  共识比率: {result.consensus_ratio:.1%}\n"
                f"  正确节点: {result.correct_nodes}\n"
                f"  错误节点: {result.incorrect_nodes}\n"
                f"  答案分布: {result.answer_distribution}"
            )
            for node in result.correct_nodes:
                task = self.task_manager.get_task(result.task_id)
                self.blockchain.add_transaction(
                    Transaction(self.token.treasury, node, task.reward_per_node)
                )
            self.blockchain.mine_pending_transaction('PLATFORM')
        else:
            self._log(
                f"=== 任务 #{result.task_id} 有争议 ===\n"
                f"  共识比率: {result.consensus_ratio:.1%}\n"
                f"  答案分布: {result.answer_distribution}"
            )

    # ===================== 查询接口 =====================

    def get_balance(self, address):
        return self.token.balance_of(address)

    def get_staked(self, address):
        return self.token.staked_of(address)

    def get_reputation(self, address):
        return self.reputation.get_profile(address).to_dict()

    def get_leaderboard(self, top_n=10):
        return self.reputation.get_leaderboard(top_n)

    def get_open_tasks(self):
        return [t.to_dict() for t in self.task_manager.get_open_tasks()]

    def get_task_result(self, task_id):
        result = self.submission.get_result(task_id)
        return result.to_dict() if result else None

    def verify_chain(self):
        return self.blockchain.verify_blockchain()

    def get_chain_length(self):
        return len(self.blockchain.chain)

    # ===================== 便捷方法 =====================

    @staticmethod
    def compute_commit_hash(answer, secret):
        """供猎手计算承诺哈希"""
        return SubmissionContract.compute_commit_hash(answer, secret)

    def _log(self, message):
        self.platform_log.append({
            'message': message,
            'timestamp': time.time(),
        })
        print(f"[DataHunter] {message}")
