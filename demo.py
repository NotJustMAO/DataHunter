# -*- coding:utf-8 -*-
"""
DataHunter DAO - 完整演示脚本
模拟从任务发布到共识结算的全流程

演示场景:
  场景1: 猫狗分类任务 - 3个猎手一致回答"猫" -> 共识达成
  场景2: 多选项分类  - 5个猎手存在分歧 -> 多数决共识
  场景3: 蜜罐检测    - 混入已知答案的测试题，识别恶意节点
  场景4: 争议处理    - 没有任何答案超过阈值
"""
from datahunter import DataHunterDAO, TaskType


def print_separator(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_balances(dao, addresses, label=""):
    if label:
        print(f"\n--- {label} ---")
    for addr in addresses:
        balance = dao.get_balance(addr)
        staked = dao.get_staked(addr)
        print(f"  {addr}: 可用={balance} DHT, 质押={staked} DHT")


def scenario_1_basic_consensus(dao):
    """场景1: 基本共识 - 3个猎手全部回答"猫"，100%共识"""
    print_separator("场景1: 猫狗分类 - 全票共识")

    # 创建任务: 识别一张图片是猫还是狗
    task = dao.create_task(
        requester='company_A',
        task_type=TaskType.CLASSIFICATION,
        description='请判断这张图片中的动物是猫还是狗？(IPFS: QmXxx...)',
        options=['猫', '狗'],
        reward_per_node=20,
        required_nodes=3,
        consensus_threshold=0.5,
    )

    hunters = ['hunter_1', 'hunter_2', 'hunter_3']
    correct_answer = '猫'

    # Commit 阶段: 每个猎手提交答案哈希
    print("\n[Commit 阶段]")
    secrets = {}
    for hunter in hunters:
        secret = f"secret_{hunter}_{task.task_id}"
        secrets[hunter] = secret
        commit_hash = dao.compute_commit_hash(correct_answer, secret)
        dao.commit_answer(task.task_id, hunter, commit_hash)

    # Reveal 阶段: 每个猎手揭示答案
    print("\n[Reveal 阶段]")
    for hunter in hunters:
        result = dao.reveal_answer(
            task.task_id, hunter, correct_answer, secrets[hunter]
        )
        if result:
            print(f"\n  共识结果: {result.to_dict()}")

    print_balances(dao, ['company_A'] + hunters, "结算后余额")


def scenario_2_majority_consensus(dao):
    """场景2: 多数决共识 - 5个猎手中3个回答A，2个回答B"""
    print_separator("场景2: 多数决共识 (3/5 = 60%)")

    task = dao.create_task(
        requester='company_A',
        task_type=TaskType.QA,
        description='地球上最大的哺乳动物是什么？',
        options=['蓝鲸', '大象', '长颈鹿'],
        reward_per_node=15,
        required_nodes=5,
        consensus_threshold=0.5,
    )

    # 模拟: 3个猎手回答"蓝鲸"，2个回答"大象"
    answers = {
        'hunter_4': '蓝鲸',
        'hunter_5': '蓝鲸',
        'hunter_6': '蓝鲸',
        'hunter_7': '大象',
        'hunter_8': '大象',
    }

    # Commit
    print("\n[Commit 阶段]")
    secrets = {}
    for hunter, answer in answers.items():
        secret = f"s2_{hunter}"
        secrets[hunter] = secret
        commit_hash = dao.compute_commit_hash(answer, secret)
        dao.commit_answer(task.task_id, hunter, commit_hash)

    # Reveal
    print("\n[Reveal 阶段]")
    for hunter, answer in answers.items():
        result = dao.reveal_answer(task.task_id, hunter, answer, secrets[hunter])
        if result:
            print(f"\n  共识结果: {result.to_dict()}")

    all_hunters = list(answers.keys())
    print_balances(dao, all_hunters, "结算后余额")


def scenario_3_honeypot(dao):
    """场景3: 蜜罐检测 - 已知答案题目，检测恶意节点"""
    print_separator("场景3: 蜜罐检测 - 识别恶意节点")

    # 蜜罐任务: 已知答案是"红色"
    task = dao.create_task(
        requester='company_A',
        task_type=TaskType.CLASSIFICATION,
        description='[蜜罐题] 这个交通灯是什么颜色？(已知答案用于检测)',
        options=['红色', '绿色', '黄色'],
        reward_per_node=10,
        required_nodes=3,
        consensus_threshold=0.5,
        honeypot_answer='红色',
    )

    # 模拟: 2个猎手回答正确，1个恶意猎手乱填
    answers = {
        'hunter_1': '红色',    # 正确
        'hunter_2': '红色',    # 正确
        'hunter_3': '绿色',    # 恶意/错误
    }

    secrets = {}
    print("\n[Commit 阶段]")
    for hunter, answer in answers.items():
        secret = f"s3_{hunter}"
        secrets[hunter] = secret
        commit_hash = dao.compute_commit_hash(answer, secret)
        dao.commit_answer(task.task_id, hunter, commit_hash)

    print("\n[Reveal 阶段]")
    for hunter, answer in answers.items():
        result = dao.reveal_answer(task.task_id, hunter, answer, secrets[hunter])
        if result:
            print(f"\n  蜜罐检测结果: {result.to_dict()}")

    # 展示 hunter_3 被惩罚
    print("\n--- 蜜罐检测后信誉 ---")
    for hunter in answers:
        rep = dao.get_reputation(hunter)
        print(f"  {hunter}: 信誉分={rep['reputation_score']}, "
              f"正确={rep['correct_tasks']}, 错误={rep['incorrect_tasks']}")


def scenario_4_dispute(dao):
    """场景4: 争议处理 - 没有答案超过阈值"""
    print_separator("场景4: 争议处理 - 无法达成共识")

    task = dao.create_task(
        requester='company_A',
        task_type=TaskType.QA,
        description='这段文本的情感倾向是？',
        options=['正面', '负面', '中性'],
        reward_per_node=10,
        required_nodes=3,
        consensus_threshold=0.5,
    )

    # 3个猎手给出3个不同答案
    answers = {
        'hunter_4': '正面',
        'hunter_5': '负面',
        'hunter_6': '中性',
    }

    secrets = {}
    print("\n[Commit 阶段]")
    for hunter, answer in answers.items():
        secret = f"s4_{hunter}"
        secrets[hunter] = secret
        commit_hash = dao.compute_commit_hash(answer, secret)
        dao.commit_answer(task.task_id, hunter, commit_hash)

    print("\n[Reveal 阶段]")
    for hunter, answer in answers.items():
        result = dao.reveal_answer(task.task_id, hunter, answer, secrets[hunter])
        if result:
            print(f"\n  争议结果: {result.to_dict()}")


def main():
    print("=" * 60)
    print("   DataHunter DAO - 去中心化数据标注平台演示")
    print("   基于加权多数共识 + 哈希承诺机制")
    print("=" * 60)

    # 初始化平台（difficulty=2 加快演示速度）
    dao = DataHunterDAO(difficulty=2)

    # 注册参与者
    print_separator("初始化: 注册参与者")
    dao.register_requester('company_A', initial_balance=10000)
    for i in range(1, 9):
        dao.register_hunter(f'hunter_{i}', initial_balance=500)

    print_balances(dao, ['company_A'], "需求方余额")

    # 运行 4 个演示场景
    scenario_1_basic_consensus(dao)
    scenario_2_majority_consensus(dao)
    scenario_3_honeypot(dao)
    scenario_4_dispute(dao)

    # 最终状态汇总
    print_separator("最终状态汇总")

    print("\n--- 区块链状态 ---")
    print(f"  链上区块数: {dao.get_chain_length()}")
    print(f"  链完整性: {'有效' if dao.verify_chain() else '无效'}")

    print("\n--- 信誉排行榜 ---")
    leaderboard = dao.get_leaderboard(top_n=5)
    for i, profile in enumerate(leaderboard, 1):
        print(f"  #{i} {profile['address']}: "
              f"信誉={profile['reputation_score']}, "
              f"准确率={profile['accuracy']:.0%}, "
              f"等级={profile['tier']}, "
              f"徽章={profile['badges'] or '无'}")

    print("\n--- 所有任务结果 ---")
    for task_id in range(1, dao.task_manager.task_counter + 1):
        task = dao.task_manager.get_task(task_id)
        result = dao.get_task_result(task_id)
        status = result['status'] if result else task.status.value
        answer = result['final_answer'] if result and result.get('final_answer') else 'N/A'
        print(f"  任务 #{task_id}: {task.description[:30]}... | "
              f"状态={status} | 答案={answer}")


if __name__ == '__main__':
    main()
