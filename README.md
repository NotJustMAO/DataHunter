<div align="center">

# DataHunter DAO

**Decentralized AI Data Labeling Platform / 去中心化 AI 数据标注平台**

[![Python](https://img.shields.io/badge/Python-%3E%3D3.8-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-62%20passed-brightgreen)](tests/)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

> **English** | [中文](#中文文档)

## Table of Contents

- [Design Philosophy](#design-philosophy)
- [Architecture Overview](#architecture-overview)
- [Core Mechanisms](#core-mechanisms)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Python Demo Guide](#python-demo-guide)
- [Frontend Demo Guide](#frontend-demo-guide)
- [Contract Module Reference](#contract-module-reference)
- [Testing](#testing)

---

## Design Philosophy

The rapid advancement of large AI models has created an insatiable demand for high-quality labeled data. Traditional centralized labeling platforms suffer from three critical problems:

| Problem | Description |
|---------|-------------|
| **Trust Deficit** | Centralized platforms can tamper with results, withhold payments, or misattribute work |
| **Quality Opacity** | No transparent mechanism to verify labeling accuracy or worker competence |
| **Incentive Misalignment** | Workers lack motivation for precision when pay is purely per-task with no quality feedback loop |

**DataHunter DAO** addresses these problems by transforming data labeling into an on-chain, consensus-driven process:

- **"Data labeling" becomes "on-chain tasks"** — task requirements, staking, and deadlines are immutably recorded
- **"Manual review" becomes "consensus verification"** — multiple independent workers reach agreement through weighted voting, eliminating single-point-of-failure reviews
- **"Flat compensation" becomes "stake-weighted rewards"** — workers put skin in the game (staking), and correct answers earn rewards while incorrect ones face slashing

The system achieves **decentralized trust** without requiring any central authority to adjudicate quality.

---

## Architecture Overview

DataHunter DAO uses a **dual-layer architecture**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer (contracts/)                │
│                                                                 │
│   DHToken          TaskManager       Submission      Reputation │
│   (ERC-20)         (Task CRUD)       (Commit-Reveal) (SBT)     │
│   mint/transfer    create/cancel     commit/reveal   score/tier │
│   stake/slash      lifecycle mgmt    consensus vote   badges    │
│                                                                 │
│                     DataHunterDAO (Unified Platform)            │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │  Settlement transactions
┌────────────────────────────▼────────────────────────────────────┐
│                    Blockchain Layer (blockchain/)                │
│                                                                 │
│   Transaction ──→ Block (SHA-256 + PoW) ──→ BlockChain          │
│                                              (immutable ledger) │
└─────────────────────────────────────────────────────────────────┘
```

**Key design decision**: Only final settlement results (reward payouts) are written to the blockchain. The high-frequency Commit/Reveal/Voting operations remain in the application layer for performance — a pattern analogous to Layer 2 scaling solutions.

---

## Core Mechanisms

### 1. Commit-Reveal Scheme (Hash Commitment)

Prevents answer-copying attacks where a later node could simply replicate an earlier node's answer.

```
Phase 1 — Commit:  hunter submits hash = sha256("answer:secret")
Phase 2 — Reveal:  hunter reveals plaintext "answer" + "secret"
                    system verifies sha256("answer:secret") == committed hash
```

During the Commit phase, all answers are hidden behind cryptographic hashes. No node can see another's answer until all commits are collected. During Reveal, the system verifies integrity — any hash mismatch is immediately rejected.

### 2. Weighted Majority Consensus

Not all votes are equal. Reputation-weighted voting gives experienced, accurate workers more influence:

| Tier | Min Score | Min Tasks | Min Accuracy | Voting Weight |
|------|-----------|-----------|--------------|---------------|
| MASTER | 800 | 100 | 90% | **3.0x** |
| EXPERT | 600 | 50 | 80% | **2.0x** |
| SKILLED | 300 | 20 | 70% | **1.5x** |
| NOVICE | 0 | 0 | — | **1.0x** |

The consensus algorithm:
1. Filter out honeypot cheaters
2. Tally weighted votes per answer
3. If the top answer exceeds the threshold (default 50%), consensus is reached
4. Otherwise, the task is marked as **DISPUTED**

### 3. Staking & Slashing Economics

```
Task creation:   Requester stakes (reward_per_node × required_nodes) DHT into Treasury
Answer commit:   Each hunter stakes 20% of reward_per_node as anti-spam deposit

On CONSENSUS:
  ✅ Correct hunters:   unstake deposit + receive full reward + reputation +5
  ❌ Incorrect hunters: deposit slashed (burned) + reputation -10

On DISPUTE:
  All honest hunters:  deposits returned
  Honeypot cheaters:   still slashed
```

### 4. Honeypot Detection

Known-answer questions (honeypots) are mixed into task pools. Any node answering a honeypot incorrectly is:
- Excluded from the consensus vote (preventing vote pollution)
- Slashed regardless of the final consensus outcome
- Penalized in reputation score

### 5. Soulbound Token (SBT) Reputation

Each hunter has a non-transferable on-chain profile (analogous to Soulbound Tokens):
- **Reputation Score** (0–1000): increases on correct answers, decreases on incorrect
- **Tier**: auto-calculated from score + task count + accuracy
- **Badges**: NFT-like achievements minted at milestones (10, 50, 100, 500 correct tasks)

---

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Blockchain Layer | Python (hashlib, SHA-256) | Block hashing, Proof-of-Work mining, chain verification |
| Smart Contracts | Python (pure, no frameworks) | Token, task management, consensus, reputation |
| Testing | Python unittest (62 test cases) | Full coverage of all contract logic |
| Frontend Demo | React 18 + TypeScript + Vite | Roadshow-ready visual dashboard |
| Styling | Tailwind CSS + shadcn/ui | Dark-theme design system with cyan/purple accents |

**Zero third-party Python dependencies** — the entire backend uses only the Python standard library.

---

## Project Structure

```
project_demo/
├── datahunter/                           # Core Python package
│   ├── __init__.py                       # Package entry, exports all public APIs
│   ├── blockchain/                       # Blockchain layer
│   │   ├── block.py                      # Block: SHA-256 hashing, PoW mining
│   │   ├── chain.py                      # BlockChain: chain integrity, balance query
│   │   └── transaction.py                # Transaction: data model, JSON encoding
│   └── contracts/                        # Smart contract layer
│       ├── token.py                      # DHToken: ERC-20 simulation (mint/transfer/stake/slash)
│       ├── task_manager.py               # TaskManager: task lifecycle, requester staking
│       ├── submission.py                 # SubmissionContract: commit-reveal + consensus engine
│       ├── reputation.py                 # ReputationContract: scoring, tiers, SBT badges
│       └── platform.py                   # DataHunterDAO: unified integration + on-chain logging
│
├── tests/
│   └── test_datahunter.py                # 62 unit tests across 8 test classes
│
├── demo.py                               # CLI demo: 4 scenarios end-to-end
│
├── frontend/                             # React presentation demo
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Overview.tsx              # Dashboard: stats, flow diagram, activity feed
│   │   │   ├── LiveDemo.tsx              # Interactive 5-step task lifecycle walkthrough
│   │   │   ├── BlockExplorer.tsx         # Visual blockchain with block/txn details
│   │   │   └── Leaderboard.tsx           # Reputation rankings with tier system
│   │   ├── components/                   # Sidebar, StatCard, shadcn ui components
│   │   ├── lib/mock-data.ts              # Simulated platform data
│   │   └── index.css                     # Design system tokens
│   ├── package.json
│   └── tailwind.config.ts
│
├── requirements.txt
└── README.md                             # This file
```

---

## Quick Start

### Python Backend

```bash
# No installation required — uses only the Python standard library
# Requires Python >= 3.8

# Run the full demo (4 scenarios)
python demo.py

# Run all unit tests
python -m pytest tests/ -v
# or
python -m unittest discover -s tests -v
```

### Frontend Demo

```bash
cd frontend

# Install dependencies (requires Node.js >= 18)
npm install

# Start development server
npm run dev
# Open http://localhost:5173

# Production build
npm run build
```

---

## Python Demo Guide

`demo.py` executes 4 end-to-end scenarios demonstrating the complete task lifecycle:

### Scenario 1: Unanimous Consensus (100%)

```
Task:    "Is this a cat or dog?" (Classification)
Hunters: 3 hunters all answer "Cat"
Result:  100% consensus → all rewarded 20 DHT each
```

- Demonstrates the basic happy-path flow: Create → Commit → Reveal → Consensus → Settle
- All 3 hunters receive their staked deposit back + full reward
- Reputation scores increase by +5 each

### Scenario 2: Majority Decision (60%)

```
Task:    "Largest mammal on Earth?" (QA)
Hunters: 3/5 answer "Blue Whale", 2/5 answer "Elephant"
Result:  60% > 50% threshold → consensus on "Blue Whale"
```

- Demonstrates weighted majority voting with partial disagreement
- 3 correct hunters: rewarded
- 2 incorrect hunters: deposits slashed, reputation penalized

### Scenario 3: Honeypot Detection

```
Task:    "What color is this traffic light?" (Honeypot, known answer: "Red")
Hunters: 2 answer "Red" (correct), 1 answers "Green" (malicious)
Result:  Honeypot catches the malicious node
```

- The malicious node is excluded from voting, preventing vote pollution
- Malicious node's deposit is slashed
- Honest nodes still reach consensus and receive rewards

### Scenario 4: Dispute Handling

```
Task:    "Sentiment of this text?" (QA)
Hunters: 3 hunters give 3 different answers ("Positive", "Negative", "Neutral")
Result:  No answer > 50% threshold → DISPUTED
```

- Demonstrates the dispute path when no consensus is possible
- All honest hunters receive their deposits back (no slashing on dispute)
- Task is marked as DISPUTED for manual review or re-assignment

### Sample Output

```
============================================================
  Scenario 1: Cat/Dog Classification — Unanimous Consensus
============================================================
[DataHunter] Task #1 created: 'Is this a cat or dog?' | type=classification | ...
[DataHunter] hunter_1 committed answer to Task #1
[DataHunter] hunter_2 committed answer to Task #1
[DataHunter] hunter_3 committed answer to Task #1
[DataHunter] hunter_1 revealed answer to Task #1
[DataHunter] hunter_2 revealed answer to Task #1
[DataHunter] hunter_3 revealed answer to Task #1
[DataHunter] === Task #1 Consensus Reached ===
  Final Answer: Cat
  Consensus Ratio: 100.0%
  Correct Nodes: ['hunter_1', 'hunter_2', 'hunter_3']
```

---

## Frontend Demo Guide

The frontend is a **presentation-ready React dashboard** designed for roadshows and project pitches. It uses simulated data to visualize the platform's capabilities.

### Page Overview

| Page | Description | Key Features |
|------|-------------|--------------|
| **Overview** | Platform dashboard | 6 KPI stat cards, 5-step architecture flow, recent task list, live activity feed |
| **Live Demo** | Interactive walkthrough | Step-by-step visualization: Create → Commit → Reveal → Consensus → Settle, with animated transitions |
| **Blockchain** | Block explorer | Clickable chain of blocks, block metadata panel, transaction list per block |
| **Rankings** | Reputation leaderboard | 4-tier system legend, 8 hunter profiles with reputation bars, accuracy stats, SBT badges |

### Live Demo Walkthrough

The **Live Demo** page is the centerpiece for presentations. Click "Next Step" to walk through:

| Step | Phase | What You See |
|------|-------|-------------|
| 1 | **Create Task** | Task card appears; tokens flow from Requester → Treasury (60 DHT staked) |
| 2 | **Commit Phase** | 3 hunter cards submit `sha256(answer:secret)` hashes; each stakes 4 DHT |
| 3 | **Reveal Phase** | Hashes transform into plaintext "Cat"; green checkmarks confirm hash verification |
| 4 | **Weighted Consensus** | Bar chart fills to 100%; MASTER(3x) + EXPERT(2x) + SKILLED(1.5x) vote tallied |
| 5 | **Settlement** | Correct hunters receive +4 DHT (unstake) + 20 DHT (reward) + reputation +30 |

### Design System

The frontend uses a custom dark-theme design system optimized for large-screen projection:

- **Color palette**: Navy background (`hsl(225, 50%, 4%)`), cyan primary (`hsl(192, 91%, 50%)`), purple secondary (`hsl(268, 60%, 58%)`)
- **Design tokens**: Defined in `src/index.css` (CSS variables) and `tailwind.config.ts` (extended Tailwind)
- **Effects**: Glassmorphism cards, glow borders, fade-in animations, grid background pattern

### Note on Frontend–Backend Integration

The Python backend and React frontend are **intentionally independent**:

- **Python** (`demo.py` + `tests/`): Proves algorithmic correctness with real computation
- **React** (`frontend/`): Provides visual impact for presentations with simulated data

This dual-mode design serves the project's purpose: the backend demonstrates that the consensus algorithms genuinely work, while the frontend creates the visual storytelling needed for pitches.

---

## Contract Module Reference

### DHToken (`token.py`)

ERC-20 style token simulation with staking capabilities.

| Method | Description |
|--------|-------------|
| `transfer(from, to, amount)` | Transfer DHT between addresses |
| `mint(address, amount)` | Mint new tokens to an address |
| `stake(address, amount)` | Lock tokens as staking deposit |
| `unstake(address, amount)` | Release staked tokens back to balance |
| `slash(address, amount)` | Burn staked tokens as penalty |
| `balance_of(address)` | Query available balance |
| `staked_of(address)` | Query staked amount |

### TaskManager (`task_manager.py`)

Task lifecycle management with automatic requester staking.

| Method | Description |
|--------|-------------|
| `create_task(requester, type, desc, ...)` | Create task + auto-stake `reward × nodes` DHT |
| `cancel_task(task_id, caller)` | Cancel OPEN task + refund stake (owner only) |
| `get_task(task_id)` | Retrieve task by ID |
| `get_open_tasks()` | List all tasks with OPEN status |

Task types: `CLASSIFICATION`, `QA`, `OCR`, `LABELING`

### SubmissionContract (`submission.py`)

Commit-Reveal scheme + Weighted Majority Consensus engine.

| Method | Description |
|--------|-------------|
| `commit_answer(task_id, node, hash)` | Submit answer hash + auto-stake 20% of reward |
| `reveal_answer(task_id, node, answer, secret)` | Reveal plaintext + verify hash match |
| `compute_commit_hash(answer, secret)` | Utility: compute `sha256("answer:secret")` |
| `get_result(task_id)` | Retrieve consensus result |

### ReputationContract (`reputation.py`)

On-chain reputation system with Soulbound Token (SBT) badges.

| Method | Description |
|--------|-------------|
| `register(address)` | Register new node with initial score 100 |
| `record_correct(address)` | +5 reputation, increment correct count, check badges |
| `record_incorrect(address)` | -10 reputation, increment incorrect count |
| `get_weight(address)` | Get voting weight based on current tier |
| `get_profile(address)` | Get full node profile |
| `get_leaderboard(top_n)` | Top N nodes sorted by reputation + accuracy |

Badge milestones: 10 / 50 / 100 / 500 correct tasks.

### DataHunterDAO (`platform.py`)

Unified platform integrating all contracts with the blockchain layer.

| Method | Description |
|--------|-------------|
| `register_requester(addr, balance)` | Register requester + allocate initial DHT |
| `register_hunter(addr, balance)` | Register hunter + allocate DHT + init reputation |
| `create_task(...)` | Publish task (delegates to TaskManager) |
| `commit_answer(...)` | Hunter commit (delegates to SubmissionContract) |
| `reveal_answer(...)` | Hunter reveal → triggers consensus → on-chain settlement |
| `verify_chain()` | Verify blockchain integrity |
| `get_leaderboard(top_n)` | Query reputation rankings |

---

## Testing

The test suite contains **62 test cases** across 8 test classes:

| Test Class | Tests | Coverage |
|-----------|-------|----------|
| `TestTransaction` | 4 | Transaction init, type validation, JSON encoding |
| `TestBlock` | 7 | Hash determinism, mining, type validation |
| `TestBlockChain` | 9 | Genesis, add/mine, balance, chain integrity, tamper detection |
| `TestDHToken` | 12 | Transfer, stake/unstake, slash, mint, edge cases |
| `TestTaskManager` | 8 | Create, cancel, permissions, parameter validation |
| `TestReputationContract` | 8 | Register, scoring, accuracy, badges, leaderboard |
| `TestSubmissionContract` | 10 | Full consensus, majority, dispute, honeypot, rewards, slashing |
| `TestDataHunterDAO` | 5 | End-to-end integration, blockchain integrity, reputation |

```bash
# Run with verbose output
python -m pytest tests/ -v

# Expected output:
# 62 passed in ~0.2s
```

---

---

<a id="中文文档"></a>

<div align="center">

# DataHunter DAO

**去中心化 AI 数据标注平台**

</div>

> [English](#table-of-contents) | **中文**

## 目录

- [设计初衷](#设计初衷)
- [架构总览](#架构总览)
- [核心机制](#核心机制)
- [技术栈](#技术栈)
- [项目结构](#项目结构-1)
- [快速开始](#快速开始-1)
- [Python Demo 使用指南](#python-demo-使用指南)
- [前端 Demo 使用指南](#前端-demo-使用指南)
- [合约模块参考](#合约模块参考)
- [测试](#测试)

---

## 设计初衷

大模型的迅猛发展，催生了对高质量标注数据的巨大需求。然而，传统中心化标注平台面临三大核心问题：

| 痛点 | 描述 |
|------|------|
| **信任缺失** | 中心化平台可以篡改结果、拖欠报酬、错误归因标注成果 |
| **质量黑箱** | 没有透明机制验证标注精度或标注者能力 |
| **激励错位** | 按件计费缺乏质量反馈闭环，标注者缺乏追求精准的动力 |

**DataHunter DAO** 通过将数据标注转化为链上共识驱动的流程来解决这些问题：

- **"数据标注"变为"链上任务"** — 任务需求、质押金额、截止时间不可篡改地记录在链上
- **"人工审核"变为"共识验证"** — 多个独立标注者通过加权投票达成一致，消除单点审核故障
- **"固定报酬"变为"质押加权奖励"** — 标注者需要质押保证金（Skin in the Game），答对获奖，答错罚没

系统无需任何中心化权威机构，即可实现**去中心化信任**。

---

## 架构总览

DataHunter DAO 采用**双层架构**：

```
┌──────────────────────────────────────────────────────────────────┐
│                       应用层 (contracts/)                        │
│                                                                  │
│   DHToken           TaskManager       Submission     Reputation  │
│   (ERC-20 代币)      (任务管理)        (提交与共识)    (信誉系统)   │
│   铸造/转账          创建/取消          承诺/揭示      评分/等级     │
│   质押/罚没          生命周期管理       共识投票        SBT 徽章    │
│                                                                  │
│                   DataHunterDAO (统一平台入口)                    │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │  结算交易写入链上
┌────────────────────────────▼─────────────────────────────────────┐
│                       区块链层 (blockchain/)                      │
│                                                                  │
│   Transaction ──→ Block (SHA-256 + PoW) ──→ BlockChain           │
│                                              (不可篡改账本)       │
└──────────────────────────────────────────────────────────────────┘
```

**关键设计决策**：只有最终结算结果（奖励发放）写入区块链。高频的 Commit/Reveal/投票操作保留在应用层——这类似于 Layer 2 扩容方案的设计思路。

---

## 核心机制

### 1. 哈希承诺机制 (Commit-Reveal)

防止"抄答案"攻击——后提交的节点无法窥探先提交节点的答案。

```
阶段一 — 承诺 (Commit):  猎手提交 hash = sha256("答案:密钥")
阶段二 — 揭示 (Reveal):  猎手揭示明文 "答案" + "密钥"
                          系统验证 sha256("答案:密钥") == 已承诺的 hash
```

承诺阶段，所有答案都隐藏在密码学哈希之后，任何节点都无法看到其他人的答案。揭示阶段，系统验证完整性——哈希不匹配立即拒绝。

### 2. 加权多数共识

并非所有投票权重相等。信誉加权投票让经验丰富、准确率高的标注者拥有更大影响力：

| 等级 | 最低分数 | 最低任务数 | 最低准确率 | 投票权重 |
|------|---------|-----------|-----------|---------|
| MASTER (大师) | 800 | 100 | 90% | **3.0x** |
| EXPERT (专家) | 600 | 50 | 80% | **2.0x** |
| SKILLED (熟练) | 300 | 20 | 70% | **1.5x** |
| NOVICE (新手) | 0 | 0 | — | **1.0x** |

共识算法流程：
1. 过滤蜜罐作弊者
2. 按答案统计加权投票
3. 若最高票答案超过阈值（默认 50%），达成共识
4. 否则标记为**争议 (DISPUTED)**

### 3. 质押与罚没经济模型

```
任务创建:   需求方质押 (每节点奖励 × 所需节点数) DHT 到金库
答案提交:   每位猎手质押 每节点奖励的 20% 作为反垃圾保证金

共识达成时:
  ✅ 正确猎手:  退还保证金 + 获得全额奖励 + 信誉 +5
  ❌ 错误猎手:  保证金罚没(销毁) + 信誉 -10

争议时:
  所有诚实猎手: 保证金退还
  蜜罐作弊者:   仍被罚没
```

### 4. 蜜罐检测

已知答案的题目（蜜罐）混入任务池。答错蜜罐的节点将被：
- 排除出共识投票（防止投票污染）
- 无论最终共识结果如何都被罚没
- 信誉分扣减

### 5. 灵魂绑定代币 (SBT) 信誉

每位猎手拥有不可转让的链上档案（类似灵魂绑定代币概念）：
- **信誉分** (0–1000)：答对增加，答错减少
- **等级**：根据分数 + 任务数 + 准确率自动计算
- **徽章**：在里程碑处铸造的 NFT 式成就（10/50/100/500 次正确标注）

---

## 技术栈

| 组件 | 技术 | 用途 |
|------|-----|------|
| 区块链层 | Python (hashlib, SHA-256) | 区块哈希、工作量证明挖矿、链验证 |
| 智能合约 | Python (纯标准库) | 代币、任务管理、共识、信誉 |
| 测试 | Python unittest (62 个用例) | 全面覆盖所有合约逻辑 |
| 前端展示 | React 18 + TypeScript + Vite | 路演级视觉仪表盘 |
| 样式 | Tailwind CSS + shadcn/ui | 深色主题设计系统 (cyan/purple) |

**Python 后端零第三方依赖** — 完全使用 Python 标准库实现。

---

## 项目结构

```
project_demo/
├── datahunter/                           # Python 核心包
│   ├── __init__.py                       # 包入口，导出所有公共 API
│   ├── blockchain/                       # 区块链层
│   │   ├── block.py                      # Block: SHA-256 哈希, PoW 挖矿
│   │   ├── chain.py                      # BlockChain: 链完整性验证, 余额查询
│   │   └── transaction.py                # Transaction: 数据模型, JSON 编码
│   └── contracts/                        # 智能合约层
│       ├── token.py                      # DHToken: ERC-20 模拟 (铸造/转账/质押/罚没)
│       ├── task_manager.py               # TaskManager: 任务生命周期, 需求方质押
│       ├── submission.py                 # SubmissionContract: 承诺-揭示 + 共识引擎
│       ├── reputation.py                 # ReputationContract: 评分, 等级, SBT 徽章
│       └── platform.py                   # DataHunterDAO: 统一集成 + 链上日志
│
├── tests/
│   └── test_datahunter.py                # 62 个单元测试，覆盖 8 个测试类
│
├── demo.py                               # 命令行演示：4 个端到端场景
│
├── frontend/                             # React 展示 Demo
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Overview.tsx              # 仪表盘: 指标卡片, 流程图, 活动流
│   │   │   ├── LiveDemo.tsx              # 交互式 5 步任务生命周期演示
│   │   │   ├── BlockExplorer.tsx         # 可视化区块链 + 区块/交易详情
│   │   │   └── Leaderboard.tsx           # 信誉排行榜 + 等级系统
│   │   ├── components/                   # 侧边栏, 统计卡片, shadcn 组件
│   │   ├── lib/mock-data.ts              # 模拟平台数据
│   │   └── index.css                     # 设计系统令牌
│   ├── package.json
│   └── tailwind.config.ts
│
├── requirements.txt
└── README.md                             # 本文件
```

---

## 快速开始

### Python 后端

```bash
# 无需安装依赖 — 仅使用 Python 标准库
# 要求 Python >= 3.8

# 运行完整演示（4 个场景）
python demo.py

# 运行所有单元测试
python -m pytest tests/ -v
# 或者
python -m unittest discover -s tests -v
```

### 前端 Demo

```bash
cd frontend

# 安装依赖（需要 Node.js >= 18）
npm install

# 启动开发服务器
npm run dev
# 打开 http://localhost:5173

# 生产构建
npm run build
```

---

## Python Demo 使用指南

`demo.py` 执行 4 个端到端场景，展示完整的任务生命周期：

### 场景 1：全票共识 (100%)

```
任务:   "这张图片是猫还是狗？" (分类)
猎手:   3 位猎手全部回答 "猫"
结果:   100% 共识 → 每人获得 20 DHT 奖励
```

- 展示基本的 Happy Path 流程：创建 → 承诺 → 揭示 → 共识 → 结算
- 3 位猎手取回质押保证金 + 获得全额奖励
- 信誉分各增加 +5

### 场景 2：多数决共识 (60%)

```
任务:   "地球上最大的哺乳动物是什么？" (问答)
猎手:   3/5 回答 "蓝鲸"，2/5 回答 "大象"
结果:   60% > 50% 阈值 → 共识答案为 "蓝鲸"
```

- 展示存在分歧时的加权多数投票
- 3 位正确猎手获得奖励
- 2 位错误猎手保证金被罚没，信誉扣减

### 场景 3：蜜罐检测

```
任务:   "这个交通灯是什么颜色？" (蜜罐，已知答案: "红色")
猎手:   2 位回答 "红色"(正确)，1 位回答 "绿色"(恶意)
结果:   蜜罐机制捕获恶意节点
```

- 恶意节点被排除出投票，防止投票污染
- 恶意节点保证金被罚没
- 诚实节点正常达成共识并获得奖励

### 场景 4：争议处理

```
任务:   "这段文本的情感倾向是？" (问答)
猎手:   3 位猎手给出 3 个不同答案（"正面"、"负面"、"中性"）
结果:   没有答案超过 50% 阈值 → 争议
```

- 展示无法达成共识时的争议处理路径
- 所有诚实猎手的保证金退还（争议时不罚没）
- 任务标记为 DISPUTED，等待人工复审或重新分配

### 示例输出

```
============================================================
  场景1: 猫狗分类 - 全票共识
============================================================
[DataHunter] 任务 #1 创建: '请判断这张图片中的动物是猫还是狗？' | 类型=classification | ...
[DataHunter] 猎手 hunter_1 对任务 #1 提交了承诺
[DataHunter] 猎手 hunter_2 对任务 #1 提交了承诺
[DataHunter] 猎手 hunter_3 对任务 #1 提交了承诺
[DataHunter] 猎手 hunter_1 对任务 #1 揭示了答案
[DataHunter] 猎手 hunter_2 对任务 #1 揭示了答案
[DataHunter] 猎手 hunter_3 对任务 #1 揭示了答案
[DataHunter] === 任务 #1 共识达成 ===
  最终答案: 猫
  共识比率: 100.0%
  正确节点: ['hunter_1', 'hunter_2', 'hunter_3']
```

---

## 前端 Demo 使用指南

前端是一个**路演级 React 仪表盘**，专为路演和项目融资展示设计。使用模拟数据可视化平台能力。

### 页面总览

| 页面 | 描述 | 核心功能 |
|------|------|---------|
| **Overview** | 平台仪表盘 | 6 个 KPI 指标卡片、5 步架构流程图、近期任务列表、实时活动流 |
| **Live Demo** | 交互式演示 | 逐步可视化: 创建 → 承诺 → 揭示 → 共识 → 结算，带动画过渡效果 |
| **Blockchain** | 区块浏览器 | 可点击的链式区块、区块元数据面板、每区块交易列表 |
| **Rankings** | 信誉排行榜 | 4 级等级系统图例、8 位猎手信誉进度条、准确率统计、SBT 徽章 |

### Live Demo 演示步骤

**Live Demo** 页面是路演展示的核心。点击 "Next Step" 逐步演示：

| 步骤 | 阶段 | 展示内容 |
|------|------|---------|
| 1 | **创建任务** | 任务卡片出现；代币从需求方流向金库 (质押 60 DHT) |
| 2 | **承诺阶段** | 3 位猎手提交 `sha256(answer:secret)` 哈希；各质押 4 DHT |
| 3 | **揭示阶段** | 哈希转化为明文 "Cat"；绿色对勾确认哈希验证通过 |
| 4 | **加权共识** | 柱状图填充至 100%；MASTER(3x) + EXPERT(2x) + SKILLED(1.5x) 投票统计 |
| 5 | **结算** | 正确猎手获得 +4 DHT (解质押) + 20 DHT (奖励) + 信誉 +30 |

### 设计系统

前端采用自定义深色主题设计系统，为大屏投影优化：

- **配色方案**: 深蓝背景 (`hsl(225, 50%, 4%)`)、青色主色 (`hsl(192, 91%, 50%)`)、紫色辅色 (`hsl(268, 60%, 58%)`)
- **设计令牌**: 定义在 `src/index.css` (CSS 变量) 和 `tailwind.config.ts` (Tailwind 扩展)
- **视觉效果**: 玻璃拟态卡片、发光边框、渐入动画、网格背景

### 关于前后端集成

Python 后端和 React 前端**各自独立运行**，这是有意为之的设计：

- **Python** (`demo.py` + `tests/`)：以真实计算证明算法正确性
- **React** (`frontend/`)：以模拟数据创造路演所需的视觉冲击力

双模式设计服务于项目定位：后端证明共识算法确实可运行，前端创造融资展示所需的视觉叙事。

---

## 合约模块参考

### DHToken (`token.py`)

ERC-20 风格代币模拟，支持质押功能。

| 方法 | 描述 |
|------|------|
| `transfer(from, to, amount)` | 地址间转账 DHT |
| `mint(address, amount)` | 向地址铸造新代币 |
| `stake(address, amount)` | 锁定代币作为质押保证金 |
| `unstake(address, amount)` | 释放质押代币回可用余额 |
| `slash(address, amount)` | 销毁质押代币（惩罚） |
| `balance_of(address)` | 查询可用余额 |
| `staked_of(address)` | 查询质押金额 |

### TaskManager (`task_manager.py`)

任务生命周期管理，自动处理需求方质押。

| 方法 | 描述 |
|------|------|
| `create_task(requester, type, desc, ...)` | 创建任务 + 自动质押 `奖励 × 节点数` DHT |
| `cancel_task(task_id, caller)` | 取消 OPEN 任务 + 退还质押（仅所有者可操作） |
| `get_task(task_id)` | 按 ID 查询任务 |
| `get_open_tasks()` | 列出所有 OPEN 状态任务 |

任务类型: `CLASSIFICATION`(分类), `QA`(问答), `OCR`(文字识别), `LABELING`(标注)

### SubmissionContract (`submission.py`)

哈希承诺机制 + 加权多数共识引擎。

| 方法 | 描述 |
|------|------|
| `commit_answer(task_id, node, hash)` | 提交答案哈希 + 自动质押奖励的 20% |
| `reveal_answer(task_id, node, answer, secret)` | 揭示明文 + 验证哈希匹配 |
| `compute_commit_hash(answer, secret)` | 工具方法: 计算 `sha256("answer:secret")` |
| `get_result(task_id)` | 查询共识结果 |

### ReputationContract (`reputation.py`)

链上信誉系统，支持灵魂绑定代币 (SBT) 徽章。

| 方法 | 描述 |
|------|------|
| `register(address)` | 注册新节点，初始分数 100 |
| `record_correct(address)` | 信誉 +5，正确计数 +1，检查徽章 |
| `record_incorrect(address)` | 信誉 -10，错误计数 +1 |
| `get_weight(address)` | 获取基于当前等级的投票权重 |
| `get_profile(address)` | 获取完整节点档案 |
| `get_leaderboard(top_n)` | 按信誉 + 准确率排序的前 N 节点 |

徽章里程碑: 10 / 50 / 100 / 500 次正确标注。

### DataHunterDAO (`platform.py`)

统一平台入口，集成所有合约与区块链层。

| 方法 | 描述 |
|------|------|
| `register_requester(addr, balance)` | 注册需求方 + 分配初始 DHT |
| `register_hunter(addr, balance)` | 注册猎手 + 分配 DHT + 初始化信誉 |
| `create_task(...)` | 发布任务（委托给 TaskManager） |
| `commit_answer(...)` | 猎手承诺（委托给 SubmissionContract） |
| `reveal_answer(...)` | 猎手揭示 → 触发共识 → 链上结算 |
| `verify_chain()` | 验证区块链完整性 |
| `get_leaderboard(top_n)` | 查询信誉排行榜 |

---

## 测试

测试套件包含 **62 个测试用例**，覆盖 8 个测试类：

| 测试类 | 用例数 | 覆盖范围 |
|--------|-------|---------|
| `TestTransaction` | 4 | 交易初始化、类型校验、JSON 编码 |
| `TestBlock` | 7 | 哈希确定性、挖矿、类型校验 |
| `TestBlockChain` | 9 | 创世块、增/挖、余额、链完整性、篡改检测 |
| `TestDHToken` | 12 | 转账、质押/解押、罚没、铸造、边界用例 |
| `TestTaskManager` | 8 | 创建、取消、权限、参数校验 |
| `TestReputationContract` | 8 | 注册、评分、准确率、徽章、排行榜 |
| `TestSubmissionContract` | 10 | 完全共识、多数决、争议、蜜罐、奖励、罚没 |
| `TestDataHunterDAO` | 5 | 端到端集成、区块链完整性、信誉 |

```bash
# 运行详细输出
python -m pytest tests/ -v

# 预期输出:
# 62 passed in ~0.2s
```

---

<div align="center">

**Built with blockchain fundamentals. Designed for decentralized trust.**

</div>
