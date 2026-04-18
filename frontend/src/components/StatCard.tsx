import { cn } from '@/lib/utils'
import type { LucideIcon } from 'lucide-react'

interface StatCardProps {
  icon: LucideIcon
  label: string
  value: string
  sub?: string
  accentColor?: 'primary' | 'secondary' | 'accent' | 'warning'
  delay?: number
}

const colorMap = {
  primary: {
    iconBg: 'bg-primary/10',
    iconText: 'text-primary',
    glow: 'glow-primary',
  },
  secondary: {
    iconBg: 'bg-secondary/10',
    iconText: 'text-secondary',
    glow: 'glow-secondary',
  },
  accent: {
    iconBg: 'bg-accent/10',
    iconText: 'text-accent',
    glow: 'glow-success',
  },
  warning: {
    iconBg: 'bg-warning/10',
    iconText: 'text-warning',
    glow: '',
  },
}

export default function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  accentColor = 'primary',
  delay = 0,
}: StatCardProps) {
  const colors = colorMap[accentColor]
  return (
    <div
      className={cn(
        'rounded-lg border border-border bg-card p-5 card-hover animate-fade-in opacity-0',
      )}
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {label}
          </p>
          <p className="mt-2 text-3xl font-bold tracking-tight text-foreground">
            {value}
          </p>
          {sub && (
            <p className="mt-1 text-xs text-muted-foreground">{sub}</p>
          )}
        </div>
        <div
          className={cn(
            'flex h-10 w-10 items-center justify-center rounded-lg',
            colors.iconBg,
            colors.glow
          )}
        >
          <Icon className={cn('h-5 w-5', colors.iconText)} />
        </div>
      </div>
    </div>
  )
}
