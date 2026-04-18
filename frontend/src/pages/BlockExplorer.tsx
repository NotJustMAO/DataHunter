import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BLOCKS } from '@/lib/mock-data'
import { cn } from '@/lib/utils'
import {
  Boxes,
  CheckCircle2,
  ArrowRight,
  Hash,
  Clock,
  FileText,
  Link2,
} from 'lucide-react'

export default function BlockExplorer() {
  const [selectedIndex, setSelectedIndex] = useState<number>(BLOCKS.length - 1)
  const selected = BLOCKS[selectedIndex]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-foreground">Blockchain Explorer</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Immutable ledger recording all consensus settlements
          </p>
        </div>
        <div className="flex items-center gap-2 rounded-lg border border-success/30 bg-success/10 px-3 py-1.5">
          <CheckCircle2 className="h-4 w-4 text-success" />
          <span className="text-sm font-medium text-success">Chain Valid</span>
        </div>
      </div>

      {/* Chain visualization */}
      <Card className="border-border bg-card">
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-semibold text-foreground">Block Chain</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2 overflow-x-auto pb-2">
            {BLOCKS.map((block, i) => (
              <div key={block.index} className="flex items-center shrink-0">
                <button
                  onClick={() => setSelectedIndex(i)}
                  className={cn(
                    'flex flex-col items-center gap-1.5 rounded-xl border p-4 transition-all duration-200 min-w-[120px]',
                    selectedIndex === i
                      ? 'border-primary/50 bg-primary/10 glow-primary'
                      : 'border-border bg-muted/20 hover:border-border hover:bg-muted/40'
                  )}
                >
                  <Boxes className={cn('h-5 w-5', selectedIndex === i ? 'text-primary' : 'text-muted-foreground')} />
                  <span className={cn('text-sm font-bold', selectedIndex === i ? 'text-primary' : 'text-foreground')}>
                    {block.index === 0 ? 'Genesis' : `Block #${block.index}`}
                  </span>
                  <span className="text-xs text-muted-foreground">
                    {block.transactions.length} txn{block.transactions.length !== 1 ? 's' : ''}
                  </span>
                  <code className="text-[10px] text-muted-foreground font-mono">
                    {block.hash.slice(0, 10)}...
                  </code>
                </button>
                {i < BLOCKS.length - 1 && (
                  <div className="flex items-center px-1">
                    <div className="h-px w-4 bg-border" />
                    <ArrowRight className="h-3 w-3 text-muted-foreground/50" />
                    <div className="h-px w-4 bg-border" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Block detail */}
      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="text-base font-semibold text-foreground">Block Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <DetailRow icon={Boxes} label="Block" value={selected.index === 0 ? 'Genesis Block' : `#${selected.index}`} />
            <DetailRow icon={Hash} label="Hash" value={selected.hash} mono />
            <DetailRow icon={Link2} label="Previous Hash" value={selected.previousHash || '(none)'} mono />
            <DetailRow icon={Clock} label="Timestamp" value={selected.timestamp} />
            <DetailRow icon={FileText} label="Transactions" value={`${selected.transactions.length} transaction${selected.transactions.length !== 1 ? 's' : ''}`} />
            <DetailRow icon={Hash} label="Nonce (PoW)" value={selected.nonce.toLocaleString()} />
          </CardContent>
        </Card>

        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle className="text-base font-semibold text-foreground">Transactions</CardTitle>
          </CardHeader>
          <CardContent>
            {selected.transactions.length === 0 ? (
              <p className="text-sm text-muted-foreground py-4 text-center">No transactions (Genesis block)</p>
            ) : (
              <div className="space-y-2">
                {selected.transactions.map((tx, i) => (
                  <div key={i} className="flex items-center gap-3 rounded-lg border border-border/50 bg-muted/20 px-4 py-3">
                    <div className="min-w-0 flex-1 flex items-center gap-2 text-sm">
                      <span className="truncate text-muted-foreground font-mono text-xs">{tx.from}</span>
                      <ArrowRight className="h-3 w-3 text-primary shrink-0" />
                      <span className="truncate text-foreground font-medium text-xs">{tx.to}</span>
                    </div>
                    <span className="shrink-0 text-sm font-bold text-primary">{tx.amount} DHT</span>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function DetailRow({ icon: Icon, label, value, mono }: { icon: typeof Hash; label: string; value: string; mono?: boolean }) {
  return (
    <div className="flex items-start gap-3">
      <Icon className="mt-0.5 h-4 w-4 shrink-0 text-muted-foreground" />
      <div className="min-w-0 flex-1">
        <p className="text-xs text-muted-foreground uppercase tracking-wider">{label}</p>
        <p className={cn('mt-0.5 text-sm text-foreground break-all', mono && 'font-mono text-xs')}>
          {value}
        </p>
      </div>
    </div>
  )
}
