# -*- coding:utf-8 -*-
"""
TaskManager - 任务管理合约
需求方发布任务、定义数据类型、单价、所需共识节点数
接收需求方质押的代币，锁定资金直到任务完成
"""
import hashlib
import time
from enum import Enum


class TaskType(Enum):
    CLASSIFICATION = 'classification'
    QA = 'qa'
    OCR = 'ocr'
    LABELING = 'labeling'


class TaskStatus(Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    CONSENSUS = 'consensus'
    DISPUTED = 'disputed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Task:
    """单个任务"""

    def __init__(self, task_id, requester, task_type, description,
                 options, reward_per_node, required_nodes,
                 consensus_threshold=0.5, honeypot_answer=None):
        if not description or not isinstance(description, str):
            raise ValueError("任务描述不能为空")
        if not isinstance(task_type, TaskType):
            raise TypeError(f"task_type 必须是 TaskType 枚举, 收到: {type(task_type).__name__}")
        if reward_per_node <= 0:
            raise ValueError(f"每节点奖励必须大于0, 收到: {reward_per_node}")
        if required_nodes < 1:
            raise ValueError(f"所需节点数必须 >= 1, 收到: {required_nodes}")
        if not (0.0 < consensus_threshold <= 1.0):
            raise ValueError(f"共识阈值必须在 (0, 1] 之间, 收到: {consensus_threshold}")

        self.task_id = task_id
        self.requester = requester
        self.task_type = task_type
        self.description = description
        self.options = options
        self.reward_per_node = reward_per_node
        self.required_nodes = required_nodes
        self.consensus_threshold = consensus_threshold
        self.honeypot_answer = honeypot_answer
        self.status = TaskStatus.OPEN
        self.created_at = time.time()
        self.total_stake = reward_per_node * required_nodes
        self.data_hash = self._compute_data_hash()

    def _compute_data_hash(self):
        raw = f"{self.task_id}:{self.requester}:{self.description}:{self.created_at}"
        return hashlib.sha256(raw.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'requester': self.requester,
            'type': self.task_type.value,
            'description': self.description,
            'options': self.options,
            'reward_per_node': self.reward_per_node,
            'required_nodes': self.required_nodes,
            'consensus_threshold': self.consensus_threshold,
            'status': self.status.value,
            'total_stake': self.total_stake,
            'data_hash': self.data_hash,
            'is_honeypot': self.honeypot_answer is not None,
        }


class TaskManager:
    """任务管理器"""

    def __init__(self, token):
        if token is None:
            raise ValueError("token 实例不能为 None")
        self.token = token
        self.tasks = {}
        self.task_counter = 0
        self.event_log = []

    def create_task(self, requester, task_type, description, options=None,
                    reward_per_node=10, required_nodes=5,
                    consensus_threshold=0.5, honeypot_answer=None):
        """需求方创建任务，自动质押代币"""
        self.task_counter += 1
        task_id = self.task_counter

        task = Task(
            task_id=task_id,
            requester=requester,
            task_type=task_type,
            description=description,
            options=options,
            reward_per_node=reward_per_node,
            required_nodes=required_nodes,
            consensus_threshold=consensus_threshold,
            honeypot_answer=honeypot_answer,
        )

        self.token.transfer(requester, self.token.treasury, task.total_stake)
        self.tasks[task_id] = task
        self._emit('TaskCreated', {
            'task_id': task_id,
            'requester': requester,
            'total_stake': task.total_stake,
        })
        return task

    def cancel_task(self, task_id, caller):
        """需求方取消任务（仅限 OPEN 状态）"""
        task = self._get_task(task_id)
        if task.requester != caller:
            raise PermissionError("只有需求方可以取消任务")
        if task.status != TaskStatus.OPEN:
            raise ValueError(f"任务状态 {task.status.value} 不允许取消")
        self.token.transfer(self.token.treasury, task.requester, task.total_stake)
        task.status = TaskStatus.CANCELLED
        self._emit('TaskCancelled', {'task_id': task_id})

    def get_open_tasks(self):
        return [t for t in self.tasks.values() if t.status == TaskStatus.OPEN]

    def get_task(self, task_id):
        return self._get_task(task_id)

    def _get_task(self, task_id):
        if task_id not in self.tasks:
            raise KeyError(f"任务 {task_id} 不存在")
        return self.tasks[task_id]

    def _emit(self, event_name, data):
        self.event_log.append({
            'event': event_name,
            'data': data,
            'timestamp': time.time(),
        })
