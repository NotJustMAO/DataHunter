import StatCard from '@/components/StatCard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { PLATFORM_STATS, RECENT_TASKS, ACTIVITY_FEED } from '@/lib/mock-data'
import {
  ListChecks,
  Users,
  Coins,
  Boxes,
  TrendingUp,
  CircleDollarSign,
  Activity,
  CheckCircle2,
  Clock,
  AlertTriangle,
  ArrowRight,
  Lock,
  Unlock,
  Scale,
  BadgeDollarSign,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const STATUS_CONFIG: Record<string, { label: string; className: string }> = {
  completed: { label: 'Completed', className: 'bg-success/15 text-success' },
  in_progress: { label: 'In Progress', className: 'bg-primary/15 text-primary' },
  disputed: { label: 'Disputed', className: 'bg-destructive/15 text-destructive' },
  open: { label: 'Open', className: 'bg-warning/15 text-warning' },
  consensus: { label: 'Consensus', className: 'bg-accent/15 text-accent' },
}

const FEED_ICONS: Record<string, { icon: typeof Activity; color: string }> = {
  consensus: { icon: CheckCircle2, color: 'text-success' },
  reward: { icon: Coins, color: 'text-primary' },
  block: { icon: Boxes, color: 'text-secondary' },
  reveal: { icon: Unlock, color: 'text-info' },
  commit: { icon: Lock, color: 'text-muted-foreground' },
  slash: { icon: AlertTriangle, color: 'text-destructive' },
  dispute: { icon: AlertTriangle, color: 'text-warning' },
}

const FLOW_STEPS = [
  { icon: ListChecks, title: 'Publish', desc: 'Stake tokens' },
  { icon: Lock, title: 'Commit', desc: 'Hash answers' },
  { icon: Unlock, title: 'Reveal', desc: 'Verify hashes' },
  { icon: Scale, title: 'Consensus', desc: 'Weighted vote' },
  { icon: BadgeDollarSign, title: 'Settle', desc: 'Reward / Slash' },
]

export default function Overview() {
  return (
    <div className="space-y-8">
      {/* Hero header */}
      <div className="relative overflow-hidden rounded-xl border border-border bg-card p-8">
        <img src="/images/hero-bg.png" alt="" className="absolute inset-0 h-full w-full object-cover opacity-20" loading="lazy" />
        <div className="absolute inset-0 bg-grid opacity-20" />
        <div className="absolute inset-0" style={{ background: 'var(--gradient-glow)' }} />
        <div className="relative z-10">
          <h1 className="text-4xl font-bold tracking-tight text-foreground">
            DataHunter <span className="text-gradient-primary">DAO</span>
          </h1>
          <p className="mt-2 max-w-2xl text-base text-muted-foreground leading-relaxed">
            Decentralized AI Data Labeling Platform powered by Weighted Majority Consensus,
            Commit-Reveal mechanism, and on-chain reputation staking.
          </p>
        </div>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-3 xl:grid-cols-6">
        <StatCard icon={ListChecks} label="Total Tasks" value={PLATFORM_STATS.totalTasks.toLocaleString()} accentColor="primary" delay={0} />
        <StatCard icon={Users} label="Active Hunters" value={PLATFORM_STATS.activeHunters.toLocaleString()} accentColor="secondary" delay={80} />
        <StatCard icon={Coins} label="DHT Staked" value={`${(PLATFORM_STATS.tokensStaked / 1000).toFixed(1)}K`} accentColor="accent" delay={160} />
        <StatCard icon={Boxes} label="Chain Blocks" value={PLATFORM_STATS.chainBlocks.toString()} accentColor="primary" delay={240} />
        <StatCard icon={TrendingUp} label="Consensus Rate" value={`${PLATFORM_STATS.consensusRate}%`} accentColor="accent" delay={320} />
        <StatCard icon={CircleDollarSign} label="Total Volume" value={`${(PLATFORM_STATS.totalVolume / 1_000_000).toFixed(1)}M`} sub="DHT" accentColor="warning" delay={400} />
      </div>

      {/* How It Works */}
      <Card className="border-border bg-card">
        <CardHeader>
          <CardTitle className="text-lg font-semibold text-foreground">How It Works</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between gap-2">
            {FLOW_STEPS.map((step, i) => {
              const Icon = step.icon
              return (
                <div key={step.title} className="flex items-center gap-2 flex-1">
                  <div className="flex flex-col items-center gap-2 flex-1">
                    <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 border border-primary/20">
                      <Icon className="h-6 w-6 text-primary" />
                    </div>
                    <p className="text-sm font-medium text-foreground">{step.title}</p>
                    <p className="text-xs text-muted-foreground">{step.desc}</p>
                  </div>
                  {i < FLOW_STEPS.length - 1 && (
                    <ArrowRight className="h-4 w-4 shrink-0 text-muted-foreground/40 -mt-6" />
                  )}
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-5">
        {/* Recent Tasks */}
        <Card className="border-border bg-card lg:col-span-3">
          <CardHeader>
            <CardTitle className="text-lg font-semibold text-foreground">Recent Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {RECENT_TASKS.map((task) => {
                const statusCfg = STATUS_CONFIG[task.status]
                return (
                  <div
                    key={task.id}
                    className="flex items-center gap-4 rounded-lg border border-border/50 bg-muted/20 px-4 py-3 transition-colors hover:border-border"
                  >
                    <span className="shrink-0 font-mono text-xs text-muted-foreground">
                      #{task.id}
                    </span>
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-foreground">
                        {task.description}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {task.requester} &middot; {task.rewardPerNode} DHT/node &middot; {task.requiredNodes} nodes
                      </p>
                    </div>
                    <span className={cn('shrink-0 rounded-full px-2.5 py-0.5 text-xs font-medium', statusCfg.className)}>
                      {statusCfg.label}
                    </span>
                    {task.consensusRatio !== undefined && (
                      <span className="shrink-0 font-mono text-xs text-muted-foreground">
                        {(task.consensusRatio * 100).toFixed(0)}%
                      </span>
                    )}
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>

        {/* Activity Feed */}
        <Card className="border-border bg-card lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg font-semibold text-foreground">
              <Activity className="h-5 w-5 text-primary" />
              Live Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {ACTIVITY_FEED.map((item, i) => {
                const cfg = FEED_ICONS[item.type] ?? FEED_ICONS.commit
                const Icon = cfg.icon
                return (
                  <div key={i} className="flex items-start gap-3">
                    <Icon className={cn('mt-0.5 h-4 w-4 shrink-0', cfg.color)} />
                    <div className="min-w-0 flex-1">
                      <p className="text-sm text-foreground leading-snug">{item.message}</p>
                      <p className="text-xs text-muted-foreground">{item.time}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
