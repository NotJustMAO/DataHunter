import { useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { DEMO_STEPS } from '@/lib/mock-data'
import { cn } from '@/lib/utils'
import {
  ChevronLeft,
  ChevronRight,
  ListChecks,
  Lock,
  Unlock,
  Scale,
  BadgeDollarSign,
  ArrowRight,
  Check,
  Hash,
  ShieldAlert,
  Coins,
} from 'lucide-react'

const STEP_ICONS = [ListChecks, Lock, Unlock, Scale, BadgeDollarSign]

const HUNTERS = [
  { name: 'Alice', tier: 'MASTER', weight: '3x', answer: 'Cat' },
  { name: 'Bob', tier: 'EXPERT', weight: '2x', answer: 'Cat' },
  { name: 'Charlie', tier: 'SKILLED', weight: '1.5x', answer: 'Cat' },
]

function StepScene({ stepId }: { stepId: number }) {
  if (stepId === 0) {
    return (
      <div className="flex flex-col items-center gap-6">
        <div className="w-full max-w-lg rounded-xl border border-border bg-muted/20 p-6 animate-fade-in">
          <div className="flex items-center gap-3 mb-4">
            <ListChecks className="h-5 w-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">Task #157</h3>
            <span className="ml-auto rounded-full bg-primary/15 px-2.5 py-0.5 text-xs font-medium text-primary">Classification</span>
          </div>
          <p className="text-sm text-foreground mb-3">Is this image a cat or dog?</p>
          <div className="flex gap-2 mb-4">
            <span className="rounded-md bg-muted px-3 py-1 text-xs text-foreground">Cat</span>
            <span className="rounded-md bg-muted px-3 py-1 text-xs text-foreground">Dog</span>
          </div>
          <div className="flex items-center justify-between text-xs text-muted-foreground border-t border-border pt-3">
            <span>Reward: 20 DHT/node</span>
            <span>Nodes: 3</span>
            <span>Threshold: 50%</span>
          </div>
        </div>
        <div className="flex items-center gap-3 animate-fade-in stagger-2 opacity-0">
          <div className="rounded-lg bg-secondary/10 px-4 py-2 text-sm text-secondary font-medium">ByteAI Inc.</div>
          <ArrowRight className="h-4 w-4 text-muted-foreground" />
          <div className="rounded-lg bg-warning/10 px-4 py-2 text-sm font-medium text-warning">60 DHT</div>
          <ArrowRight className="h-4 w-4 text-muted-foreground" />
          <div className="rounded-lg bg-primary/10 px-4 py-2 text-sm font-medium text-primary">Treasury</div>
        </div>
      </div>
    )
  }

  if (stepId === 1) {
    return (
      <div className="space-y-4">
        {HUNTERS.map((h, i) => (
          <div key={h.name} className={cn('flex items-center gap-4 rounded-xl border border-border bg-muted/20 p-4 animate-fade-in opacity-0', i === 0 && 'stagger-1', i === 1 && 'stagger-2', i === 2 && 'stagger-3')}>
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 text-sm font-bold text-primary">{h.name[0]}</div>
            <div className="flex-1">
              <p className="text-sm font-medium text-foreground">{h.name} <span className="text-xs text-muted-foreground">({h.tier})</span></p>
              <div className="flex items-center gap-2 mt-1">
                <Hash className="h-3 w-3 text-muted-foreground" />
                <code className="text-xs text-muted-foreground font-mono">sha256("{h.answer}:secret_{h.name.toLowerCase()}") = a3f4e2...</code>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="h-4 w-4 text-warning" />
              <span className="text-xs text-warning font-medium">Stake 4 DHT</span>
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (stepId === 2) {
    return (
      <div className="space-y-4">
        {HUNTERS.map((h, i) => (
          <div key={h.name} className={cn('flex items-center gap-4 rounded-xl border border-border bg-muted/20 p-4 animate-fade-in opacity-0', i === 0 && 'stagger-1', i === 1 && 'stagger-2', i === 2 && 'stagger-3')}>
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-accent/10 text-sm font-bold text-accent">{h.name[0]}</div>
            <div className="flex-1">
              <p className="text-sm font-medium text-foreground">{h.name}</p>
              <div className="flex items-center gap-2 mt-1">
                <code className="text-xs text-muted-foreground font-mono line-through">a3f4e2...hash</code>
                <ArrowRight className="h-3 w-3 text-primary" />
                <span className="rounded-md bg-primary/15 px-2 py-0.5 text-xs font-semibold text-primary">"{h.answer}"</span>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <Check className="h-4 w-4 text-success" />
              <span className="text-xs text-success font-medium">Verified</span>
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (stepId === 3) {
    const totalWeight = 3 + 2 + 1.5
    return (
      <div className="space-y-6">
        <div className="rounded-xl border border-border bg-muted/20 p-6 animate-fade-in">
          <h4 className="text-sm font-semibold text-foreground mb-4">Weighted Voting Tally</h4>
          <div className="space-y-3">
            <div>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-foreground font-medium">"Cat"</span>
                <span className="text-primary font-mono font-bold">{totalWeight}/{totalWeight} = 100%</span>
              </div>
              <div className="h-3 rounded-full bg-muted overflow-hidden">
                <div className="h-full rounded-full bg-primary transition-all duration-1000" style={{ width: '100%' }} />
              </div>
              <div className="flex gap-2 mt-2">
                {HUNTERS.map((h) => (
                  <span key={h.name} className="text-xs text-muted-foreground">
                    {h.name}({h.weight})
                  </span>
                ))}
              </div>
            </div>
            <div>
              <div className="flex items-center justify-between text-sm mb-1">
                <span className="text-foreground font-medium">"Dog"</span>
                <span className="text-muted-foreground font-mono">0/{totalWeight} = 0%</span>
              </div>
              <div className="h-3 rounded-full bg-muted overflow-hidden">
                <div className="h-full rounded-full bg-destructive transition-all duration-1000" style={{ width: '0%' }} />
              </div>
            </div>
          </div>
        </div>
        <div className="flex items-center justify-center gap-3 animate-fade-in stagger-2 opacity-0">
          <ShieldAlert className="h-5 w-5 text-success" />
          <span className="text-sm font-semibold text-success">Consensus Reached: 100% &ge; 50% threshold</span>
        </div>
      </div>
    )
  }

  // stepId === 4
  return (
    <div className="space-y-4">
      {HUNTERS.map((h, i) => (
        <div key={h.name} className={cn('flex items-center gap-4 rounded-xl border border-border bg-muted/20 p-4 animate-fade-in opacity-0', i === 0 && 'stagger-1', i === 1 && 'stagger-2', i === 2 && 'stagger-3')}>
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-success/10 text-sm font-bold text-success">
            <Check className="h-5 w-5" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium text-foreground">{h.name}</p>
            <p className="text-xs text-muted-foreground">Correct answer &middot; Reputation +30</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1">
              <Unlock className="h-3.5 w-3.5 text-accent" />
              <span className="text-xs text-accent font-medium">+4 DHT</span>
            </div>
            <div className="flex items-center gap-1">
              <Coins className="h-3.5 w-3.5 text-primary" />
              <span className="text-xs text-primary font-medium">+20 DHT</span>
            </div>
          </div>
        </div>
      ))}
      <div className="flex items-center justify-center gap-3 pt-2 animate-fade-in stagger-4 opacity-0">
        <span className="text-xs text-muted-foreground">Settlement transactions mined into Block #90</span>
      </div>
    </div>
  )
}

export default function LiveDemo() {
  const [currentStep, setCurrentStep] = useState(0)
  const step = DEMO_STEPS[currentStep]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">Interactive Demo</h2>
        <p className="mt-1 text-sm text-muted-foreground">Walk through a complete task lifecycle step by step</p>
      </div>

      {/* Stepper */}
      <div className="flex items-center gap-1">
        {DEMO_STEPS.map((s, i) => {
          const Icon = STEP_ICONS[i]
          const isActive = i === currentStep
          const isDone = i < currentStep
          return (
            <div key={s.id} className="flex items-center flex-1">
              <button
                onClick={() => setCurrentStep(i)}
                className={cn(
                  'flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-all duration-200 w-full',
                  isActive && 'bg-primary/10 text-primary border border-primary/30',
                  isDone && 'text-success',
                  !isActive && !isDone && 'text-muted-foreground hover:text-foreground',
                )}
              >
                {isDone ? <Check className="h-4 w-4 shrink-0" /> : <Icon className="h-4 w-4 shrink-0" />}
                <span className="font-medium truncate">{s.title}</span>
              </button>
              {i < DEMO_STEPS.length - 1 && (
                <div className={cn('h-px w-4 shrink-0', isDone ? 'bg-success' : 'bg-border')} />
              )}
            </div>
          )
        })}
      </div>

      {/* Step content */}
      <Card className="border-border bg-card overflow-hidden">
        <CardContent className="p-8">
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <span className="rounded-full bg-primary/15 px-2.5 py-0.5 text-xs font-bold text-primary">{step.phase}</span>
              <h3 className="text-xl font-bold text-foreground">{step.title}</h3>
            </div>
            <p className="text-sm text-muted-foreground">{step.subtitle}</p>
          </div>

          <div className="mb-6 rounded-xl border border-border/50 bg-background/50 p-6" key={currentStep}>
            <StepScene stepId={currentStep} />
          </div>

          <p className="text-sm text-muted-foreground leading-relaxed border-l-2 border-primary/30 pl-4">
            {step.description}
          </p>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
          disabled={currentStep === 0}
        >
          <ChevronLeft className="mr-1 h-4 w-4" />
          Previous
        </Button>
        <div className="flex gap-1.5">
          {DEMO_STEPS.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrentStep(i)}
              className={cn(
                'h-2 rounded-full transition-all duration-200',
                i === currentStep ? 'w-6 bg-primary' : 'w-2 bg-border hover:bg-muted-foreground',
              )}
            />
          ))}
        </div>
        <Button
          variant={currentStep === DEMO_STEPS.length - 1 ? 'outline' : 'glow'}
          onClick={() => setCurrentStep(Math.min(DEMO_STEPS.length - 1, currentStep + 1))}
          disabled={currentStep === DEMO_STEPS.length - 1}
        >
          Next Step
          <ChevronRight className="ml-1 h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}
