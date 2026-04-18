import { useState } from 'react'
import Sidebar, { type PageId } from '@/components/Sidebar'
import Overview from '@/pages/Overview'
import LiveDemo from '@/pages/LiveDemo'
import BlockExplorer from '@/pages/BlockExplorer'
import Leaderboard from '@/pages/Leaderboard'

const PAGES: Record<PageId, React.ComponentType> = {
  overview: Overview,
  demo: LiveDemo,
  explorer: BlockExplorer,
  leaderboard: Leaderboard,
}

export default function App() {
  const [activePage, setActivePage] = useState<PageId>('overview')
  const PageComponent = PAGES[activePage]

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />
      <main className="ml-64 min-h-screen p-8">
        <div className="mx-auto max-w-7xl" key={activePage}>
          <PageComponent />
        </div>
      </main>
    </div>
  )
}
