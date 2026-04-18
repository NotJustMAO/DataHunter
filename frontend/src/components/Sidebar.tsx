import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  PlayCircle,
  Boxes,
  Trophy,
  Hexagon,
} from 'lucide-react'

const NAV_ITEMS = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'demo', label: 'Live Demo', icon: PlayCircle },
  { id: 'explorer', label: 'Blockchain', icon: Boxes },
  { id: 'leaderboard', label: 'Rankings', icon: Trophy },
] as const

export type PageId = (typeof NAV_ITEMS)[number]['id']

interface SidebarProps {
  activePage: PageId
  onNavigate: (page: PageId) => void
}

export default function Sidebar({ activePage, onNavigate }: SidebarProps) {
  return (
    <aside className="fixed left-0 top-0 z-40 flex h-screen w-64 flex-col border-r border-border bg-card">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 glow-primary">
          <Hexagon className="h-6 w-6 text-primary" />
        </div>
        <div>
          <h1 className="text-lg font-bold tracking-tight text-foreground">
            DataHunter
          </h1>
          <p className="text-xs text-muted-foreground">DAO Platform</p>
        </div>
      </div>

      {/* Divider */}
      <div className="mx-4 border-t border-border" />

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon
          const isActive = activePage === item.id
          return (
            <button
              key={item.id}
              onClick={() => onNavigate(item.id)}
              className={cn(
                'flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-primary/10 text-primary border-glow'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground'
              )}
            >
              <Icon className="h-5 w-5 shrink-0" />
              <span>{item.label}</span>
              {isActive && (
                <div className="ml-auto h-1.5 w-1.5 rounded-full bg-primary animate-pulse-glow" />
              )}
            </button>
          )
        })}
      </nav>

      {/* Bottom status */}
      <div className="border-t border-border px-4 py-4">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <div className="h-2 w-2 rounded-full bg-success animate-pulse" />
          <span>Chain Synced</span>
          <span className="ml-auto font-mono">v1.0.0</span>
        </div>
      </div>
    </aside>
  )
}
