# -*- coding:utf-8 -*-
"""DataHunter DAO 统一测试套件"""
import unittest
import time
import json

from datahunter import (
    Transaction, TransactionEncoder, Block, BlockChain,
    DHToken, TaskManager, TaskType, TaskStatus,
    SubmissionContract, ReputationContract, ReputationTier,
    DataHunterDAO,
)


# ============================================================
#  区块链底层测试
# ============================================================

class TestTransaction(unittest.TestCase):

    def test_init(self):
        tx = Transaction('a', 'b', 50)
        self.assertEqual(tx.from_address, 'a')
        self.assertEqual(tx.to_address, 'b')
        self.assertEqual(tx.amount, 50)

    def test_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            Transaction('a', 'b', 'not_a_number')

    def test_json_encode(self):
        tx = Transaction('a', 'b', 100)
        result = json.loads(json.dumps(tx, cls=TransactionEncoder))
        self.assertEqual(result['amount'], 100)

    def test_json_encode_none_address(self):
        tx = Transaction(None, 'b', 100)
        result = json.loads(json.dumps(tx, cls=TransactionEncoder))
        self.assertIsNone(result['from_address'])


class TestBlock(unittest.TestCase):

    def test_hash_deterministic(self):
        block = Block(1000000, [], 'prev')
        self.assertEqual(block.calculate_hash(), block.calculate_hash())

    def test_different_data_different_hash(self):
        b1 = Block(1000000, [], 'prev')
        b2 = Block(1000001, [], 'prev')
        self.assertNotEqual(b1.hash, b2.hash)

    def test_hash_is_sha256(self):
        block = Block(1000000, [], '')
        self.assertEqual(len(block.hash), 64)

    def test_mine_block(self):
        block = Block(time.time(), [Transaction('a', 'b', 10)], 'prev')
        block.mine_block(2)
        self.assertTrue(block.hash.startswith('00'))

    def test_invalid_timestamp_type(self):
        with self.assertRaises(TypeError):
            Block('not_a_number', [], '')

    def test_invalid_transactions_type(self):
        with self.assertRaises(TypeError):
            Block(time.time(), 'not_a_list', '')

    def test_invalid_difficulty(self):
        block = Block(time.time(), [], '')
        with self.assertRaises(ValueError):
            block.mine_block(-1)


class TestBlockChain(unittest.TestCase):

    def setUp(self):
        self.bc = BlockChain()
        self.bc.difficulty = 2

    def test_genesis_block(self):
        self.assertEqual(len(self.bc.chain), 1)
        self.assertEqual(self.bc.chain[0].previous_hash, '')

    def test_add_invalid_transaction(self):
        with self.assertRaises(TypeError):
            self.bc.add_transaction("not_a_transaction")

    def test_mine_empty_address(self):
        with self.assertRaises(ValueError):
            self.bc.mine_pending_transaction('')

    def test_add_and_mine(self):
        self.bc.add_transaction(Transaction('a', 'b', 50))
        self.bc.mine_pending_transaction('miner')
        self.assertEqual(len(self.bc.chain), 2)

    def test_balance(self):
        self.bc.add_transaction(Transaction('a', 'b', 100))
        self.bc.add_transaction(Transaction('b', 'a', 30))
        self.bc.mine_pending_transaction('miner')
        self.assertEqual(self.bc.get_balance_of_address('a'), -70)
        self.assertEqual(self.bc.get_balance_of_address('b'), 70)

    def test_verify_valid(self):
        self.bc.add_transaction(Transaction('a', 'b', 10))
        self.bc.mine_pending_transaction('miner')
        self.assertTrue(self.bc.verify_blockchain())

    def test_verify_tampered(self):
        self.bc.add_transaction(Transaction('a', 'b', 10))
        self.bc.mine_pending_transaction('miner')
        self.bc.chain[1].transactions = [Transaction('a', 'b', 99999)]
        self.assertFalse(self.bc.verify_blockchain())

    def test_chain_link(self):
        self.bc.add_transaction(Transaction('a', 'b', 10))
        self.bc.mine_pending_transaction('miner')
        self.assertEqual(self.bc.chain[1].previous_hash, self.bc.chain[0].hash)

    def test_multiple_blocks(self):
        for i in range(3):
            self.bc.add_transaction(Transaction('a', 'b', 10))
            self.bc.mine_pending_transaction('miner')
        self.assertEqual(len(self.bc.chain), 4)
        self.assertTrue(self.bc.verify_blockchain())


# ============================================================
#  代币合约测试
# ============================================================

class TestDHToken(unittest.TestCase):

    def setUp(self):
        self.token = DHToken(total_supply=100_000)

    def test_initial_supply(self):
        self.assertEqual(self.token.balance_of('TREASURY'), 100_000)

    def test_transfer(self):
        self.token.transfer('TREASURY', 'alice', 1000)
        self.assertEqual(self.token.balance_of('alice'), 1000)

    def test_transfer_insufficient(self):
        with self.assertRaises(ValueError):
            self.token.transfer('alice', 'bob', 100)

    def test_transfer_to_self(self):
        self.token.transfer('TREASURY', 'alice', 100)
        with self.assertRaises(ValueError):
            self.token.transfer('alice', 'alice', 10)

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            self.token.transfer('', 'bob', 100)

    def test_invalid_amount_type(self):
        with self.assertRaises(TypeError):
            self.token.transfer('TREASURY', 'bob', 'abc')

    def test_stake_and_unstake(self):
        self.token.transfer('TREASURY', 'alice', 100)
        self.token.stake('alice', 30)
        self.assertEqual(self.token.balance_of('alice'), 70)
        self.assertEqual(self.token.staked_of('alice'), 30)
        self.token.unstake('alice', 20)
        self.assertEqual(self.token.balance_of('alice'), 90)

    def test_stake_insufficient(self):
        self.token.transfer('TREASURY', 'alice', 10)
        with self.assertRaises(ValueError):
            self.token.stake('alice', 20)

    def test_slash(self):
        self.token.transfer('TREASURY', 'alice', 100)
        self.token.stake('alice', 50)
        slashed = self.token.slash('alice', 30)
        self.assertEqual(slashed, 30)
        self.assertEqual(self.token.staked_of('alice'), 20)

    def test_slash_more_than_staked(self):
        self.token.transfer('TREASURY', 'alice', 50)
        self.token.stake('alice', 20)
        slashed = self.token.slash('alice', 100)
        self.assertEqual(slashed, 20)

    def test_mint(self):
        self.token.mint('bob', 500)
        self.assertEqual(self.token.balance_of('bob'), 500)
        self.assertEqual(self.token.total_supply, 100_500)

    def test_negative_supply(self):
        with self.assertRaises(ValueError):
            DHToken(total_supply=-1)


# ============================================================
#  任务管理合约测试
# ============================================================

class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.token = DHToken(total_supply=100_000)
        self.token.transfer('TREASURY', 'req', 5000)
        self.tm = TaskManager(self.token)

    def test_create_task(self):
        task = self.tm.create_task('req', TaskType.CLASSIFICATION, '分类', reward_per_node=10, required_nodes=3)
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.status, TaskStatus.OPEN)
        self.assertEqual(task.total_stake, 30)

    def test_create_task_insufficient(self):
        self.token.transfer('TREASURY', 'poor', 10)
        with self.assertRaises(ValueError):
            self.tm.create_task('poor', TaskType.QA, 'test', reward_per_node=100, required_nodes=5)

    def test_invalid_task_type(self):
        with self.assertRaises(TypeError):
            self.tm.create_task('req', 'not_enum', 'test')

    def test_invalid_description(self):
        with self.assertRaises(ValueError):
            self.tm.create_task('req', TaskType.QA, '', reward_per_node=10, required_nodes=3)

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            self.tm.create_task('req', TaskType.QA, 'test', consensus_threshold=0.0)

    def test_cancel_task(self):
        task = self.tm.create_task('req', TaskType.QA, 'test', reward_per_node=10, required_nodes=3)
        before = self.token.balance_of('req')
        self.tm.cancel_task(task.task_id, 'req')
        self.assertEqual(task.status, TaskStatus.CANCELLED)
        self.assertEqual(self.token.balance_of('req'), before + 30)

    def test_cancel_by_non_owner(self):
        task = self.tm.create_task('req', TaskType.QA, 'test', reward_per_node=10, required_nodes=3)
        with self.assertRaises(PermissionError):
            self.tm.cancel_task(task.task_id, 'stranger')

    def test_get_open_tasks(self):
        self.tm.create_task('req', TaskType.QA, 'q1', reward_per_node=5, required_nodes=3)
        self.tm.create_task('req', TaskType.QA, 'q2', reward_per_node=5, required_nodes=3)
        self.assertEqual(len(self.tm.get_open_tasks()), 2)


# ============================================================
#  信誉合约测试
# ============================================================

class TestReputationContract(unittest.TestCase):

    def setUp(self):
        self.rep = ReputationContract()

    def test_register(self):
        self.rep.register('node_a')
        p = self.rep.get_profile('node_a')
        self.assertEqual(p.reputation_score, 100)
        self.assertEqual(p.tier, ReputationTier.NOVICE)

    def test_invalid_address(self):
        with self.assertRaises(ValueError):
            self.rep.register('')

    def test_correct_increases_score(self):
        self.rep.register('node_a')
        before = self.rep.get_profile('node_a').reputation_score
        self.rep.record_correct('node_a')
        self.assertGreater(self.rep.get_profile('node_a').reputation_score, before)

    def test_incorrect_decreases_score(self):
        self.rep.register('node_a')
        before = self.rep.get_profile('node_a').reputation_score
        self.rep.record_incorrect('node_a')
        self.assertLess(self.rep.get_profile('node_a').reputation_score, before)

    def test_accuracy(self):
        self.rep.register('node_a')
        for _ in range(7):
            self.rep.record_correct('node_a')
        for _ in range(3):
            self.rep.record_incorrect('node_a')
        self.assertAlmostEqual(self.rep.get_profile('node_a').accuracy, 0.7)

    def test_auto_register(self):
        profile = self.rep.get_profile('new')
        self.assertEqual(profile.reputation_score, 100)

    def test_leaderboard(self):
        for name in ['a', 'b', 'c']:
            self.rep.register(name)
        self.rep.record_correct('a')
        self.rep.record_correct('a')
        self.rep.record_correct('b')
        board = self.rep.get_leaderboard(top_n=2)
        self.assertEqual(len(board), 2)
        self.assertEqual(board[0]['address'], 'a')

    def test_badge_minting(self):
        self.rep.register('grinder')
        for _ in range(10):
            self.rep.record_correct('grinder')
        self.assertIn('初级数据猎手', self.rep.get_profile('grinder').badges)


# ============================================================
#  提交与共识合约测试
# ============================================================

class TestSubmissionContract(unittest.TestCase):

    def _setup(self, required_nodes=3, consensus_threshold=0.5, honeypot_answer=None):
        token = DHToken(total_supply=1_000_000)
        rep = ReputationContract()
        tm = TaskManager(token)
        sub = SubmissionContract(tm, token, rep)

        token.transfer('TREASURY', 'req', 10000)
        hunters = [f'h{i}' for i in range(required_nodes)]
        for h in hunters:
            token.transfer('TREASURY', h, 500)
            rep.register(h)

        task = tm.create_task(
            'req', TaskType.CLASSIFICATION, 'test task',
            options=['A', 'B', 'C'],
            reward_per_node=10, required_nodes=required_nodes,
            consensus_threshold=consensus_threshold,
            honeypot_answer=honeypot_answer,
        )
        return token, rep, tm, sub, task, hunters

    def test_full_consensus(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        secrets = {}
        for h in hunters:
            s = f"s_{h}"
            secrets[h] = s
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash('A', s))

        result = None
        for h in hunters:
            result = sub.reveal_answer(task.task_id, h, 'A', secrets[h])

        self.assertEqual(result.status, 'CONSENSUS')
        self.assertEqual(result.final_answer, 'A')
        self.assertAlmostEqual(result.consensus_ratio, 1.0)

    def test_majority_consensus(self):
        token, rep, tm, sub, task, hunters = self._setup(5)
        answers = {hunters[0]: 'A', hunters[1]: 'A', hunters[2]: 'A',
                   hunters[3]: 'B', hunters[4]: 'B'}
        secrets = {}
        for h, ans in answers.items():
            s = f"s_{h}"
            secrets[h] = s
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash(ans, s))

        result = None
        for h, ans in answers.items():
            result = sub.reveal_answer(task.task_id, h, ans, secrets[h])

        self.assertEqual(result.status, 'CONSENSUS')
        self.assertEqual(result.final_answer, 'A')
        self.assertEqual(len(result.correct_nodes), 3)
        self.assertEqual(len(result.incorrect_nodes), 2)

    def test_dispute(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        answers = {hunters[0]: 'A', hunters[1]: 'B', hunters[2]: 'C'}
        secrets = {}
        for h, ans in answers.items():
            s = f"s_{h}"
            secrets[h] = s
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash(ans, s))

        result = None
        for h, ans in answers.items():
            result = sub.reveal_answer(task.task_id, h, ans, secrets[h])

        self.assertEqual(result.status, 'DISPUTED')

    def test_hash_verification_failure(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        for h in hunters:
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash('A', f"s_{h}"))
        with self.assertRaises(ValueError):
            sub.reveal_answer(task.task_id, hunters[0], 'A', 'wrong_secret')

    def test_duplicate_commit(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        commit = sub.compute_commit_hash('A', 'sec')
        sub.commit_answer(task.task_id, hunters[0], commit)
        with self.assertRaises(ValueError):
            sub.commit_answer(task.task_id, hunters[0], commit)

    def test_invalid_node_address(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        with self.assertRaises(ValueError):
            sub.commit_answer(task.task_id, '', 'hash')

    def test_honeypot(self):
        token, rep, tm, sub, task, hunters = self._setup(3, honeypot_answer='A')
        answers = {hunters[0]: 'A', hunters[1]: 'A', hunters[2]: 'B'}
        secrets = {}
        for h, ans in answers.items():
            s = f"s_{h}"
            secrets[h] = s
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash(ans, s))

        result = None
        for h, ans in answers.items():
            result = sub.reveal_answer(task.task_id, h, ans, secrets[h])

        self.assertEqual(result.status, 'CONSENSUS')
        self.assertIn(hunters[2], result.incorrect_nodes)

    def test_rewards_distributed(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        before = token.balance_of(hunters[0])
        secrets = {}
        for h in hunters:
            s = f"s_{h}"
            secrets[h] = s
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash('A', s))
        for h in hunters:
            sub.reveal_answer(task.task_id, h, 'A', secrets[h])
        after = token.balance_of(hunters[0])
        self.assertEqual(after, before - 2 + 2 + 10)

    def test_incorrect_node_slashed(self):
        token, rep, tm, sub, task, hunters = self._setup(3)
        initial = token.balance_of(hunters[2])
        answers = {hunters[0]: 'A', hunters[1]: 'A', hunters[2]: 'B'}
        secrets = {}
        for h, ans in answers.items():
            s = f"s_{h}"
            secrets[h] = s
            sub.commit_answer(task.task_id, h, sub.compute_commit_hash(ans, s))
        for h, ans in answers.items():
            sub.reveal_answer(task.task_id, h, ans, secrets[h])
        self.assertEqual(token.balance_of(hunters[2]), initial - 2)
        self.assertEqual(token.staked_of(hunters[2]), 0)


# ============================================================
#  主平台集成测试
# ============================================================

class TestDataHunterDAO(unittest.TestCase):

    def setUp(self):
        self.dao = DataHunterDAO(difficulty=2)
        self.dao.register_requester('company', initial_balance=10000)
        for i in range(1, 4):
            self.dao.register_hunter(f'h{i}', initial_balance=500)

    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            DataHunterDAO(difficulty=-1)

    def test_end_to_end(self):
        task = self.dao.create_task(
            'company', TaskType.CLASSIFICATION, '猫狗分类',
            options=['猫', '狗'], reward_per_node=10, required_nodes=3,
        )
        secrets = {}
        for i in range(1, 4):
            h = f'h{i}'
            s = f"s_{h}"
            secrets[h] = s
            self.dao.commit_answer(task.task_id, h, self.dao.compute_commit_hash('猫', s))
        result = None
        for i in range(1, 4):
            h = f'h{i}'
            result = self.dao.reveal_answer(task.task_id, h, '猫', secrets[h])

        self.assertEqual(result.status, 'CONSENSUS')
        self.assertEqual(result.final_answer, '猫')

    def test_blockchain_integrity(self):
        task = self.dao.create_task(
            'company', TaskType.QA, 'test', reward_per_node=10, required_nodes=3,
        )
        secrets = {}
        for i in range(1, 4):
            h = f'h{i}'
            s = f"s_{h}"
            secrets[h] = s
            self.dao.commit_answer(task.task_id, h, self.dao.compute_commit_hash('X', s))
        for i in range(1, 4):
            h = f'h{i}'
            self.dao.reveal_answer(task.task_id, h, 'X', secrets[h])

        self.assertTrue(self.dao.verify_chain())
        self.assertGreater(self.dao.get_chain_length(), 1)

    def test_reputation_updated(self):
        task = self.dao.create_task(
            'company', TaskType.QA, 'test', reward_per_node=10, required_nodes=3,
        )
        answers = {'h1': 'A', 'h2': 'A', 'h3': 'B'}
        secrets = {}
        for h, ans in answers.items():
            s = f"s_{h}"
            secrets[h] = s
            self.dao.commit_answer(task.task_id, h, self.dao.compute_commit_hash(ans, s))
        for h, ans in answers.items():
            self.dao.reveal_answer(task.task_id, h, ans, secrets[h])

        self.assertEqual(self.dao.get_reputation('h1')['correct_tasks'], 1)
        self.assertEqual(self.dao.get_reputation('h3')['incorrect_tasks'], 1)

    def test_leaderboard(self):
        board = self.dao.get_leaderboard()
        self.assertIsInstance(board, list)


if __name__ == '__main__':
    unittest.main()
