# -*- coding:utf-8 -*-
"""
Reputation - 信誉合约
链上信誉系统，记录每个地址的历史准确率
高信誉节点获得更高投票权重，可解锁高难度任务
对应 Soulbound Token (SBT) 概念中的 "数字简历"
"""
import time


class ReputationTier:
    """信誉等级"""
    NOVICE = 'novice'
    SKILLED = 'skilled'
    EXPERT = 'expert'
    MASTER = 'master'


class NodeProfile:
    """节点信誉档案"""

    def __init__(self, address):
        if not address or not isinstance(address, str):
            raise ValueError(f"无效的节点地址: {address!r}")
        self.address = address
        self.total_tasks = 0
        self.correct_tasks = 0
        self.incorrect_tasks = 0
        self.reputation_score = 100
        self.created_at = time.time()
        self.badges = []

    @property
    def accuracy(self):
        if self.total_tasks == 0:
            return 0.0
        return self.correct_tasks / self.total_tasks

    @property
    def tier(self):
        if self.total_tasks >= 100 and self.accuracy >= 0.9:
            return ReputationTier.MASTER
        elif self.total_tasks >= 50 and self.accuracy >= 0.8:
            return ReputationTier.EXPERT
        elif self.total_tasks >= 20 and self.accuracy >= 0.7:
            return ReputationTier.SKILLED
        return ReputationTier.NOVICE

    def to_dict(self):
        return {
            'address': self.address,
            'total_tasks': self.total_tasks,
            'correct_tasks': self.correct_tasks,
            'incorrect_tasks': self.incorrect_tasks,
            'accuracy': round(self.accuracy, 4),
            'reputation_score': self.reputation_score,
            'tier': self.tier,
            'badges': list(self.badges),
        }


class ReputationContract:
    """信誉管理合约"""

    TIER_WEIGHTS = {
        ReputationTier.NOVICE: 1.0,
        ReputationTier.SKILLED: 1.5,
        ReputationTier.EXPERT: 2.0,
        ReputationTier.MASTER: 3.0,
    }

    CORRECT_REWARD = 5
    INCORRECT_PENALTY = 10

    BADGE_RULES = [
        (10, '初级数据猎手'),
        (50, '资深数据猎手'),
        (100, '数据标注专家'),
        (500, '传奇数据大师'),
    ]

    def __init__(self):
        self.profiles = {}
        self.event_log = []

    def register(self, address):
        """注册新节点"""
        if not address or not isinstance(address, str):
            raise ValueError(f"无效的节点地址: {address!r}")
        if address not in self.profiles:
            self.profiles[address] = NodeProfile(address)
            self._emit('NodeRegistered', {'address': address})

    def get_profile(self, address):
        self._ensure_registered(address)
        return self.profiles[address]

    def get_weight(self, address):
        """获取节点的投票权重（基于信誉等级）"""
        self._ensure_registered(address)
        profile = self.profiles[address]
        return self.TIER_WEIGHTS.get(profile.tier, 1.0)

    def record_correct(self, address):
        """记录一次正确回答"""
        self._ensure_registered(address)
        profile = self.profiles[address]
        profile.total_tasks += 1
        profile.correct_tasks += 1
        profile.reputation_score = min(1000, profile.reputation_score + self.CORRECT_REWARD)
        self._check_badges(profile)
        self._emit('ReputationUpdated', {
            'address': address,
            'action': 'correct',
            'new_score': profile.reputation_score,
        })

    def record_incorrect(self, address):
        """记录一次错误回答"""
        self._ensure_registered(address)
        profile = self.profiles[address]
        profile.total_tasks += 1
        profile.incorrect_tasks += 1
        profile.reputation_score = max(0, profile.reputation_score - self.INCORRECT_PENALTY)
        self._emit('ReputationUpdated', {
            'address': address,
            'action': 'incorrect',
            'new_score': profile.reputation_score,
        })

    def get_leaderboard(self, top_n=10):
        if top_n < 1:
            raise ValueError(f"top_n 必须 >= 1, 收到: {top_n}")
        sorted_profiles = sorted(
            self.profiles.values(),
            key=lambda p: (p.reputation_score, p.accuracy),
            reverse=True,
        )
        return [p.to_dict() for p in sorted_profiles[:top_n]]

    def _check_badges(self, profile):
        for threshold, badge_name in self.BADGE_RULES:
            if profile.correct_tasks >= threshold and badge_name not in profile.badges:
                profile.badges.append(badge_name)
                self._emit('BadgeMinted', {
                    'address': profile.address,
                    'badge': badge_name,
                    'type': 'SBT',
                })

    def _ensure_registered(self, address):
        if address not in self.profiles:
            self.register(address)

    def _emit(self, event_name, data):
        self.event_log.append({
            'event': event_name,
            'data': data,
            'timestamp': time.time(),
        })
