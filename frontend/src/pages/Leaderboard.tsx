import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { HUNTERS, TIER_CONFIG } from '@/lib/mock-data'
import { cn } from '@/lib/utils'
import {
  Trophy,
  Award,
  Shield,
  TrendingUp,
  Star,
} from 'lucide-react'

const TIER_STYLES: Record<string, string> = {
  MASTER: 'bg-primary/15 text-primary border-primary/30',
  EXPERT: 'bg-secondary/15 text-secondary border-secondary/30',
  SKILLED: 'bg-accent/15 text-accent border-accent/30',
  NOVICE: 'bg-muted text-muted-foreground border-border',
}

export default function Leaderboard() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">Reputation Rankings</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Hunter leaderboard powered by Soulbound Token reputation system
        </p>
      </div>

      {/* Tier legend */}
      <Card className="border-border bg-card">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-base font-semibold text-foreground">
            <Shield className="h-5 w-5 text-primary" />
            Reputation Tiers
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-4 gap-3">
            {(Object.entries(TIER_CONFIG) as [string, typeof TIER_CONFIG.MASTER][]).map(([key, tier]) => (
              <div
                key={key}
                className={cn(
                  'flex flex-col items-center gap-1.5 rounded-lg border p-3',
                  TIER_STYLES[key]
                )}
              >
                <span className="text-sm font-bold">{tier.label}</span>
                <span className="text-xs opacity-80">Voting Weight: {tier.weight}</span>
                <span className="text-xs opacity-60">Score &ge; {tier.minScore}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Leaderboard table */}
      <Card className="border-border bg-card">
        <CardHeader className="pb-3">
          <CardTitle className="flex items-center gap-2 text-base font-semibold text-foreground">
            <Trophy className="h-5 w-5 text-warning" />
            Top Hunters
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {/* Header */}
            <div className="grid grid-cols-12 gap-4 px-4 py-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">
              <span className="col-span-1">Rank</span>
              <span className="col-span-3">Hunter</span>
              <span className="col-span-2">Reputation</span>
              <span className="col-span-1">Tier</span>
              <span className="col-span-2">Accuracy</span>
              <span className="col-span-1">Tasks</span>
              <span className="col-span-2">Badges</span>
            </div>

            {/* Rows */}
            {HUNTERS.map((hunter, i) => {
              const repPercent = Math.min(100, (hunter.reputation / 1000) * 100)
              return (
                <div
                  key={hunter.address}
                  className={cn(
                    'grid grid-cols-12 gap-4 items-center rounded-lg border border-border/50 bg-muted/20 px-4 py-3 transition-all hover:border-border animate-fade-in opacity-0',
                    `stagger-${i + 1}`
                  )}
                >
                  {/* Rank */}
                  <div className="col-span-1">
                    {hunter.rank <= 3 ? (
                      <div className={cn(
                        'flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold',
                        hunter.rank === 1 && 'bg-warning/20 text-warning',
                        hunter.rank === 2 && 'bg-muted-foreground/20 text-muted-foreground',
                        hunter.rank === 3 && 'bg-warning/10 text-warning/70',
                      )}>
                        {hunter.rank === 1 ? <Trophy className="h-4 w-4" /> : `#${hunter.rank}`}
                      </div>
                    ) : (
                      <span className="text-sm text-muted-foreground pl-1.5">#{hunter.rank}</span>
                    )}
                  </div>

                  {/* Hunter */}
                  <div className="col-span-3 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">{hunter.displayName}</p>
                    <p className="text-xs text-muted-foreground font-mono">{hunter.address}</p>
                  </div>

                  {/* Reputation bar */}
                  <div className="col-span-2">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
                        <div
                          className="h-full rounded-full bg-primary transition-all duration-700"
                          style={{ width: `${repPercent}%` }}
                        />
                      </div>
                      <span className="text-xs font-mono font-bold text-foreground w-8 text-right">{hunter.reputation}</span>
                    </div>
                  </div>

                  {/* Tier badge */}
                  <div className="col-span-1">
                    <span className={cn('inline-flex rounded-full px-2 py-0.5 text-xs font-medium border', TIER_STYLES[hunter.tier])}>
                      {hunter.tier}
                    </span>
                  </div>

                  {/* Accuracy */}
                  <div className="col-span-2">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-3.5 w-3.5 text-success" />
                      <span className="text-sm font-medium text-foreground">{(hunter.accuracy * 100).toFixed(1)}%</span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {hunter.correctTasks}W / {hunter.incorrectTasks}L
                    </p>
                  </div>

                  {/* Tasks */}
                  <div className="col-span-1">
                    <span className="text-sm text-foreground">{hunter.correctTasks + hunter.incorrectTasks}</span>
                  </div>

                  {/* Badges */}
                  <div className="col-span-2 flex flex-wrap gap-1">
                    {hunter.badges.length > 0 ? hunter.badges.slice(0, 2).map((badge) => (
                      <span key={badge} className="inline-flex items-center gap-0.5 rounded-md bg-muted px-1.5 py-0.5 text-[10px] text-muted-foreground">
                        {badge === 'Founding Member' ? <Star className="h-2.5 w-2.5" /> :
                         badge === 'Centennial' ? <Award className="h-2.5 w-2.5" /> :
                         badge === 'Precision Star' ? <TrendingUp className="h-2.5 w-2.5" /> :
                         null}
                        {badge}
                      </span>
                    )) : (
                      <span className="text-[10px] text-muted-foreground">--</span>
                    )}
                    {hunter.badges.length > 2 && (
                      <span className="text-[10px] text-muted-foreground">+{hunter.badges.length - 2}</span>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
