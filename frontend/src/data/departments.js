// Single source of truth for the eight department agents. Keys match the
// backend's department slugs (see core/orchestrator.py) so this file can be
// wired directly to the real API without renaming anything.
import {
  ChartLineUp,
  Users,
  Monitor,
  Scales,
  Megaphone,
  TrendUp,
  Headset,
  ShieldWarning,
} from '@phosphor-icons/react';

export const departments = [
  {
    slug: 'risk_restructuring',
    name: 'Risk & Restructuring',
    short: 'Risk',
    icon: ShieldWarning,
    tagline: 'Risk exposure and restructuring strategy',
    description:
      'Assesses financial and operational risk, and models restructuring scenarios before they reach the board.',
    accent: 'amber',
    prompts: [
      'Summarize our current restructuring risk exposure',
      'What covenants are closest to breach this quarter?',
      'Draft a mitigation plan for supplier concentration risk',
    ],
  },
  {
    slug: 'finance',
    name: 'Finance',
    short: 'Finance',
    icon: ChartLineUp,
    tagline: 'Financial analysis, modeling, cost optimization',
    description:
      'Builds models, tracks cost drivers, and answers questions grounded in the finance knowledge base.',
    accent: 'signal',
    prompts: [
      'Where can we cut cost without touching headcount?',
      'Explain the variance in Q3 operating margin',
      'Model the cash impact of a 90-day payment term',
    ],
  },
  {
    slug: 'sales',
    name: 'Sales',
    short: 'Sales',
    icon: TrendUp,
    tagline: 'Revenue strategy, customer retention',
    description: 'Reads pipeline signal and retention data to recommend where revenue is won or at risk.',
    accent: 'current',
    prompts: [
      'Which accounts show the highest churn risk this month?',
      'Draft a retention play for our top 10 enterprise accounts',
      'What is dragging down our win rate in APAC?',
    ],
  },
  {
    slug: 'it',
    name: 'IT',
    short: 'IT',
    icon: Monitor,
    tagline: 'Technology strategy, systems integration',
    description: 'Advises on architecture, vendor tradeoffs, and integration paths across the tech stack.',
    accent: 'signal',
    prompts: [
      'What are the risks of migrating billing off the legacy system?',
      'Compare our current stack against a headless alternative',
      'Draft an integration checklist for the new CRM',
    ],
  },
  {
    slug: 'hr',
    name: 'Human Resources',
    short: 'HR',
    icon: Users,
    tagline: 'Workforce planning, change management',
    description: 'Supports org design, workforce planning, and communication through periods of change.',
    accent: 'current',
    prompts: [
      'Draft a communication plan for the upcoming reorg',
      'What does attrition look like by department this year?',
      'Outline a change-management timeline for a team merge',
    ],
  },
  {
    slug: 'marketing',
    name: 'Marketing',
    short: 'Marketing',
    icon: Megaphone,
    tagline: 'Communications, market positioning',
    description: 'Shapes messaging and positioning, and stress-tests campaigns against market signal.',
    accent: 'amber',
    prompts: [
      'Position our restructuring announcement for investors',
      'Draft talking points for the Q4 press briefing',
      'How should messaging differ across our three core segments?',
    ],
  },
  {
    slug: 'legal_compliance',
    name: 'Legal & Compliance',
    short: 'Legal',
    icon: Scales,
    tagline: 'Regulatory compliance, legal guidance',
    description: 'Surfaces regulatory obligations and compliance guidance grounded in policy documents.',
    accent: 'signal',
    prompts: [
      'What disclosure obligations apply to this restructuring?',
      'Summarize outstanding compliance gaps by region',
      'Explain the notice period required for this contract change',
    ],
  },
  {
    slug: 'customer_support',
    name: 'Customer Support',
    short: 'Support',
    icon: Headset,
    tagline: 'Customer communication, service continuity',
    description: 'Keeps support continuity and messaging consistent while the business changes underneath it.',
    accent: 'current',
    prompts: [
      'Draft a service-continuity notice for affected customers',
      'What are customers asking most about the transition?',
      'Summarize open escalations tied to the restructuring',
    ],
  },
];

export const getDepartment = (slug) => departments.find((d) => d.slug === slug);
