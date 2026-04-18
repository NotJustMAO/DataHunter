# -*- coding:utf-8 -*-
"""
Submission - 提交与共识合约
处理猎手的答案提交，实现哈希承诺（Commit-Reveal）机制
执行加权多数共识 (Weighted Majority Consensus) 算法
"""
import hashlib
import time
from collections import Counter
from enum import Enum
from .task_manager import TaskStatus


class SubmissionPhase(Enum):
    COMMIT = 'commit'
    REVEAL = 'reveal'
    CLOSED = 'closed'


class ConsensusResult:
    """共识判定结果"""

    def __init__(self, task_id, status, final_answer=None,
                 correct_nodes=None, incorrect_nodes=None,
                 answer_distribution=None, consensus_ratio=0.0):
        self.task_id = task_id
        self.status = status
        self.final_answer = final_answer
        self.correct_nodes = correct_nodes or []
        self.incorrect_nodes = incorrect_nodes or []
        self.answer_distribution = answer_distribution or {}
        self.consensus_ratio = consensus_ratio
        self.timestamp = time.time()

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'status': self.status,
            'final_answer': self.final_answer,
            'correct_nodes': self.correct_nodes,
            'incorrect_nodes': self.incorrect_nodes,
            'answer_distribution': self.answer_distribution,
            'consensus_ratio': round(self.consensus_ratio, 4),
        }


class SubmissionContract:
    """提交与共识合约"""

    def __init__(self, task_manager, token, reputation):
        if any(x is None for x in (task_manager, token, reputation)):
            raise ValueError("task_manager / token / reputation 不能为 None")
        self.task_manager = task_manager
        self.token = token
        self.reputation = reputation
        self.commits = {}
        self.reveals = {}
        self.phases = {}
        self.participants = {}
        self.results = {}
        self.event_log = []

    # ===================== Commit 阶段 =====================

    def commit_answer(self, task_id, node_address, answer_hash):
        """承诺阶段：节点提交答案的哈希值 sha256(answer:secret)"""
        if not node_address or not isinstance(node_address, str):
            raise ValueError(f"无效的节点地址: {node_address!r}")
        if not answer_hash or not isinstance(answer_hash, str):
            raise ValueError("answer_hash 必须是非空字符串")

        task = self.task_manager.get_task(task_id)

        if task.status not in (TaskStatus.OPEN, TaskStatus.IN_PROGRESS):
            raise ValueError(f"任务 {task_id} 不接受提交，当前状态: {task.status.value}")

        if task_id not in self.commits:
            self.commits[task_id] = {}
            self.reveals[task_id] = {}
            self.phases[task_id] = SubmissionPhase.COMMIT
            self.participants[task_id] = set()

        if self.phases[task_id] != SubmissionPhase.COMMIT:
            raise ValueError(f"任务 {task_id} 不在承诺阶段")

        if node_address in self.commits[task_id]:
            raise ValueError(f"节点 {node_address} 已提交过承诺")

        stake_amount = max(1, task.reward_per_node // 5)
        self.token.stake(node_address, stake_amount)

        self.commits[task_id][node_address] = answer_hash
        self.participants[task_id].add(node_address)

        if task.status == TaskStatus.OPEN:
            task.status = TaskStatus.IN_PROGRESS

        self._emit('AnswerCommitted', {
            'task_id': task_id,
            'node': node_address,
            'staked': stake_amount,
        })

        if len(self.commits[task_id]) >= task.required_nodes:
            self.phases[task_id] = SubmissionPhase.REVEAL
            self._emit('PhaseChanged', {
                'task_id': task_id,
                'new_phase': 'REVEAL',
            })

    # ===================== Reveal 阶段 =====================

    def reveal_answer(self, task_id, node_address, answer, secret):
        """揭示阶段：节点提交明文答案和 secret，系统验证哈希"""
        if not node_address or not isinstance(node_address, str):
            raise ValueError(f"无效的节点地址: {node_address!r}")
        if answer is None:
            raise ValueError("答案不能为 None")
        if not secret:
            raise ValueError("secret 不能为空")

        self.task_manager.get_task(task_id)  # 确保任务存在

        if task_id not in self.phases or self.phases[task_id] != SubmissionPhase.REVEAL:
            raise ValueError(f"任务 {task_id} 不在揭示阶段")

        if node_address not in self.commits.get(task_id, {}):
            raise ValueError(f"节点 {node_address} 没有提交过承诺")

        if node_address in self.reveals[task_id]:
            raise ValueError(f"节点 {node_address} 已揭示过答案")

        expected_hash = self._compute_commit_hash(answer, secret)
        actual_hash = self.commits[task_id][node_address]

        if expected_hash != actual_hash:
            raise ValueError(
                f"哈希验证失败: 明文答案与承诺不匹配 "
                f"(expected={expected_hash[:16]}..., got={actual_hash[:16]}...)"
            )

        self.reveals[task_id][node_address] = answer
        self._emit('AnswerRevealed', {
            'task_id': task_id,
            'node': node_address,
        })

        if len(self.reveals[task_id]) >= len(self.commits[task_id]):
            return self._verify_consensus(task_id)

        return None

    # ===================== 共识验证 =====================

    def _verify_consensus(self, task_id):
        """加权多数共识算法"""
        task = self.task_manager.get_task(task_id)
        answers = self.reveals[task_id]

        # ---- 蜜罐检测 ----
        honeypot_cheaters = set()
        if task.honeypot_answer is not None:
            for node, ans in answers.items():
                if ans != task.honeypot_answer:
                    honeypot_cheaters.add(node)

        # ---- 加权投票统计 ----
        weighted_votes = Counter()
        total_weight = 0

        for node, ans in answers.items():
            if node in honeypot_cheaters:
                continue
            weight = self.reputation.get_weight(node)
            weighted_votes[ans] += weight
            total_weight += weight

        # ---- 判定共识 ----
        if total_weight == 0:
            result = ConsensusResult(
                task_id=task_id,
                status='DISPUTED',
                answer_distribution=dict(Counter(answers.values())),
            )
        else:
            mode_answer, mode_weight = weighted_votes.most_common(1)[0]
            consensus_ratio = mode_weight / total_weight

            if consensus_ratio >= task.consensus_threshold:
                correct_nodes = [n for n, a in answers.items()
                                 if a == mode_answer and n not in honeypot_cheaters]
                incorrect_nodes = [n for n, a in answers.items()
                                   if a != mode_answer or n in honeypot_cheaters]
                result = ConsensusResult(
                    task_id=task_id,
                    status='CONSENSUS',
                    final_answer=mode_answer,
                    correct_nodes=correct_nodes,
                    incorrect_nodes=incorrect_nodes,
                    answer_distribution=dict(Counter(answers.values())),
                    consensus_ratio=consensus_ratio,
                )
                task.status = TaskStatus.CONSENSUS
            else:
                result = ConsensusResult(
                    task_id=task_id,
                    status='DISPUTED',
                    answer_distribution=dict(Counter(answers.values())),
                    consensus_ratio=consensus_ratio,
                )
                task.status = TaskStatus.DISPUTED

        self.results[task_id] = result
        self.phases[task_id] = SubmissionPhase.CLOSED

        self._execute_payouts(task, result, honeypot_cheaters)
        self._emit('ConsensusReached', result.to_dict())
        return result

    def _execute_payouts(self, task, result, honeypot_cheaters):
        """执行奖惩结算"""
        stake_amount = max(1, task.reward_per_node // 5)

        if result.status == 'CONSENSUS':
            for node in result.correct_nodes:
                self.token.unstake(node, stake_amount)
                self.token.transfer(self.token.treasury, node, task.reward_per_node)
                self.reputation.record_correct(node)

            for node in result.incorrect_nodes:
                self.token.slash(node, stake_amount)
                self.reputation.record_incorrect(node)

            task.status = TaskStatus.COMPLETED

        elif result.status == 'DISPUTED':
            for node in self.participants.get(task.task_id, set()):
                current_stake = self.token.staked_of(node)
                if current_stake >= stake_amount:
                    self.token.unstake(node, stake_amount)

            for node in honeypot_cheaters:
                self.token.slash(node, stake_amount)
                self.reputation.record_incorrect(node)

    # ===================== 工具方法 =====================

    @staticmethod
    def _compute_commit_hash(answer, secret):
        raw = f"{answer}:{secret}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    @staticmethod
    def compute_commit_hash(answer, secret):
        """公开方法供节点计算承诺哈希"""
        raw = f"{answer}:{secret}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def get_result(self, task_id):
        return self.results.get(task_id)

    def _emit(self, event_name, data):
        self.event_log.append({
            'event': event_name,
            'data': data,
            'timestamp': time.time(),
        })
