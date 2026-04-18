/* ========== Mock Data for DataHunter DAO Demo ========== */

export const PLATFORM_STATS = {
  totalTasks: 156,
  activeHunters: 1842,
  tokensStaked: 458200,
  chainBlocks: 89,
  consensusRate: 94.2,
  totalVolume: 2_400_000,
}

export interface TaskItem {
  id: number
  description: string
  type: string
  status: 'open' | 'in_progress' | 'consensus' | 'disputed' | 'completed'
  requester: string
  rewardPerNode: number
  requiredNodes: number
  finalAnswer?: string
  consensusRatio?: number
  timestamp: string
}

export const RECENT_TASKS: TaskItem[] = [
  { id: 156, description: '电商产品图片分类', type: 'classification', status: 'completed', requester: 'ByteAI Inc.', rewardPerNode: 20, requiredNodes: 5, finalAnswer: '电子产品', consensusRatio: 1.0, timestamp: '2 min ago' },
  { id: 155, description: '医学影像病灶标注', type: 'labeling', status: 'in_progress', requester: 'MedVision', rewardPerNode: 50, requiredNodes: 7, timestamp: '8 min ago' },
  { id: 154, description: '自然语言情感分析', type: 'qa', status: 'completed', requester: 'NLPCore', rewardPerNode: 15, requiredNodes: 5, finalAnswer: '正面', consensusRatio: 0.8, timestamp: '15 min ago' },
  { id: 153, description: '交通标志识别标注', type: 'classification', status: 'disputed', requester: 'AutoDrive', rewardPerNode: 25, requiredNodes: 5, timestamp: '22 min ago' },
  { id: 152, description: '语音转写文本校对', type: 'qa', status: 'completed', requester: 'VoiceLab', rewardPerNode: 12, requiredNodes: 3, finalAnswer: '正确', consensusRatio: 0.667, timestamp: '35 min ago' },
  { id: 151, description: 'OCR 手写体数字识别', type: 'ocr', status: 'completed', requester: 'ScanTech', rewardPerNode: 10, requiredNodes: 5, finalAnswer: '7', consensusRatio: 1.0, timestamp: '48 min ago' },
]

export interface HunterProfile {
  rank: number
  address: string
  displayName: string
  reputation: number
  tier: 'NOVICE' | 'SKILLED' | 'EXPERT' | 'MASTER'
  correctTasks: number
  incorrectTasks: number
  accuracy: number
  badges: string[]
  balance: number
}

export const HUNTERS: HunterProfile[] = [
  { rank: 1, address: '0x7a3b...c2f1', displayName: 'CryptoLabeler', reputation: 850, tier: 'MASTER', correctTasks: 142, incorrectTasks: 8, accuracy: 0.947, badges: ['Founding Member', 'Centennial', 'Precision Star'], balance: 15420 },
  { rank: 2, address: '0x4e1f...8d3a', displayName: 'DataNinja', reputation: 780, tier: 'EXPERT', correctTasks: 118, incorrectTasks: 11, accuracy: 0.915, badges: ['Centennial', 'Precision Star'], balance: 11230 },
  { rank: 3, address: '0x9c2d...1e7b', displayName: 'AIAnnotator', reputation: 720, tier: 'EXPERT', correctTasks: 95, incorrectTasks: 12, accuracy: 0.888, badges: ['Precision Star'], balance: 8750 },
  { rank: 4, address: '0x3f8a...6c4d', displayName: 'BlockHunter', reputation: 580, tier: 'SKILLED', correctTasks: 73, incorrectTasks: 13, accuracy: 0.849, badges: ['First Label'], balance: 5430 },
  { rank: 5, address: '0x1d5e...9a2f', displayName: 'NeuralNode', reputation: 530, tier: 'SKILLED', correctTasks: 64, incorrectTasks: 13, accuracy: 0.831, badges: ['First Label'], balance: 4280 },
  { rank: 6, address: '0x8b7c...3e1a', displayName: 'ChainWorker', reputation: 430, tier: 'SKILLED', correctTasks: 52, incorrectTasks: 13, accuracy: 0.8, badges: ['First Label'], balance: 3100 },
  { rank: 7, address: '0x2a6f...7d4c', displayName: 'PixelMiner', reputation: 320, tier: 'SKILLED', correctTasks: 38, incorrectTasks: 11, accuracy: 0.776, badges: ['First Label'], balance: 2150 },
  { rank: 8, address: '0x5c3d...4b8e', displayName: 'TokenSeeker', reputation: 280, tier: 'NOVICE', correctTasks: 28, incorrectTasks: 9, accuracy: 0.757, badges: [], balance: 1580 },
]

export interface BlockItem {
  index: number
  hash: string
  previousHash: string
  timestamp: string
  transactions: { from: string; to: string; amount: number }[]
  nonce: number
}

export const BLOCKS: BlockItem[] = [
  { index: 0, hash: '0000000000000000...genesis', previousHash: '', timestamp: '2024-06-11 00:00:00', transactions: [], nonce: 0 },
  { index: 1, hash: '00a3f4e2b8c19d7...block01', previousHash: '0000000000000000...genesis', timestamp: '2024-06-11 00:12:34', transactions: [
    { from: 'treasury', to: 'CryptoLabeler', amount: 20 },
    { from: 'treasury', to: 'DataNinja', amount: 20 },
    { from: 'treasury', to: 'AIAnnotator', amount: 20 },
  ], nonce: 347 },
  { index: 2, hash: '007d2a1c3f1e84b...block02', previousHash: '00a3f4e2b8c19d7...block01', timestamp: '2024-06-11 00:25:18', transactions: [
    { from: 'treasury', to: 'CryptoLabeler', amount: 15 },
    { from: 'treasury', to: 'BlockHunter', amount: 15 },
    { from: 'treasury', to: 'NeuralNode', amount: 15 },
  ], nonce: 512 },
  { index: 3, hash: '00b8e7f2a1d34c9...block03', previousHash: '007d2a1c3f1e84b...block02', timestamp: '2024-06-11 00:38:45', transactions: [
    { from: 'treasury', to: 'DataNinja', amount: 50 },
    { from: 'treasury', to: 'CryptoLabeler', amount: 50 },
    { from: 'treasury', to: 'AIAnnotator', amount: 50 },
    { from: 'treasury', to: 'ChainWorker', amount: 50 },
    { from: 'treasury', to: 'PixelMiner', amount: 50 },
  ], nonce: 189 },
  { index: 4, hash: '001c5f3d8a2e76b...block04', previousHash: '00b8e7f2a1d34c9...block03', timestamp: '2024-06-11 00:51:02', transactions: [
    { from: 'treasury', to: 'NeuralNode', amount: 25 },
    { from: 'treasury', to: 'DataNinja', amount: 25 },
    { from: 'treasury', to: 'CryptoLabeler', amount: 25 },
  ], nonce: 764 },
  { index: 5, hash: '009a4b2e7f1c83d...block05', previousHash: '001c5f3d8a2e76b...block04', timestamp: '2024-06-11 01:03:29', transactions: [
    { from: 'treasury', to: 'AIAnnotator', amount: 10 },
    { from: 'treasury', to: 'BlockHunter', amount: 10 },
    { from: 'treasury', to: 'TokenSeeker', amount: 10 },
    { from: 'treasury', to: 'CryptoLabeler', amount: 10 },
    { from: 'treasury', to: 'DataNinja', amount: 10 },
  ], nonce: 421 },
]

export const ACTIVITY_FEED = [
  { type: 'consensus', message: 'Task #156 Consensus Reached (100%)', time: '2 min ago' },
  { type: 'reward', message: 'CryptoLabeler earned 20 DHT reward', time: '2 min ago' },
  { type: 'block', message: 'Block #89 mined (3 transactions)', time: '2 min ago' },
  { type: 'reveal', message: 'Task #155 entered Reveal phase', time: '8 min ago' },
  { type: 'commit', message: 'DataNinja committed answer to Task #155', time: '10 min ago' },
  { type: 'consensus', message: 'Task #154 Consensus Reached (80%)', time: '15 min ago' },
  { type: 'slash', message: 'BlockHunter slashed 3 DHT (honeypot)', time: '18 min ago' },
  { type: 'dispute', message: 'Task #153 Disputed', time: '22 min ago' },
]

export interface DemoStep {
  id: number
  phase: string
  title: string
  subtitle: string
  description: string
}

export const DEMO_STEPS: DemoStep[] = [
  { id: 0, phase: 'CREATE', title: 'Create Task', subtitle: 'Requester publishes task & stakes tokens', description: 'ByteAI Inc. publishes a classification task "Is this image a cat or dog?", staking 60 DHT (20 DHT/node x 3 nodes) into the treasury as reward pool.' },
  { id: 1, phase: 'COMMIT', title: 'Commit Phase', subtitle: 'Hunters submit hashed answers', description: 'Three hunters compute sha256(answer:secret) and submit the hash on-chain. Each hunter stakes 4 DHT (20% of reward) as anti-spam deposit. No one can see others\' answers.' },
  { id: 2, phase: 'REVEAL', title: 'Reveal Phase', subtitle: 'Hunters reveal plaintext answers', description: 'All hunters reveal their plaintext answer + secret. The system verifies sha256(answer:secret) matches the committed hash. Any mismatch is rejected.' },
  { id: 3, phase: 'CONSENSUS', title: 'Weighted Consensus', subtitle: 'Reputation-weighted majority voting', description: 'The system tallies votes weighted by reputation tier: MASTER(3x), EXPERT(2x), SKILLED(1.5x), NOVICE(1x). Answer "Cat" receives 100% weighted votes, exceeding the 50% threshold.' },
  { id: 4, phase: 'SETTLE', title: 'Settlement', subtitle: 'Rewards & slashing executed on-chain', description: 'Correct hunters: unstake 4 DHT + receive 20 DHT reward + reputation +30. Incorrect hunters: staked 4 DHT slashed + reputation -50. Settlement transactions written to blockchain.' },
]

export const TIER_CONFIG = {
  MASTER: { label: 'Master', weight: '3x', color: 'primary', minScore: 800 },
  EXPERT: { label: 'Expert', weight: '2x', color: 'secondary', minScore: 600 },
  SKILLED: { label: 'Skilled', weight: '1.5x', color: 'accent', minScore: 300 },
  NOVICE: { label: 'Novice', weight: '1x', color: 'muted-foreground', minScore: 0 },
} as const
