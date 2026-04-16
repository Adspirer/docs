# Enterprise Pricing Model — Iterations & Thinking

> **Status:** Work in progress. We are still iterating on this model.
> **Last updated:** 2026-04-15

---

## Context

Our consumer plans (Free/Plus/Pro/Max) have a clean pricing framework anchored on **cost per tool call**:

| Tier | Price | Tool Calls | $/Call |
|------|-------|-----------|--------|
| Free | $0 | 15 | — |
| Plus | $49/mo | 150 | $0.33 |
| Pro | $99/mo | 600 | $0.165 |
| Max | $199/mo | Unlimited | ~$0.04 (implicit, bounded by 5 accounts) |

This works because:
- The unit is clear (tool calls)
- Every tier has a calculable $/call
- Customers understand what they're buying
- Upgrades have obvious math ("4x the calls for 2x the price")

Max gives "unlimited" tool calls, but this is bounded by the 5-account-per-platform cap. A single user with 5 accounts has a practical ceiling of ~5,000 calls/month. "Unlimited" is a marketing label — accounts are the real gate.

**The challenge:** We need the same clarity for Enterprise, where the dimensions are seats AND accounts AND both scale independently.

---

## Iteration 1: Flat Tiers with Tool Call Caps

### The idea

Mirror the consumer model — give Enterprise tiers fixed tool call allocations with cost-per-call as the anchor:

| Tier | Price | Tool Calls | $/Call | Seats | Accounts |
|------|-------|-----------|--------|-------|----------|
| Pro | $99/mo | 600 | $0.165 | 1 | 1 |
| Max | $199/mo | 3,000 | $0.066 | 1 | 2 |
| Enterprise | $999/mo | 15,000 | $0.067 | 5 | 50 |
| Enterprise Plus | $2,999/mo | 60,000 | $0.050 | Unlimited | 200 |

Plus overage rates: $0.05/call (Enterprise), $0.04/call (Enterprise Plus).

### Why we moved away from this

1. **Cost-per-call paradox.** Enterprise ($0.067/call) was marginally MORE expensive per call than Max ($0.066/call). Higher volume should mean lower unit cost, not higher.

2. **Tool call caps don't match the "unlimited" promise.** We made Max unlimited. Putting a 15,000 cap on Enterprise (which costs 5x more) feels regressive. Customers would ask: "Why am I paying more and getting less?"

3. **Overage billing not implemented.** The enterprise page promised overage rates ($0.05/call, $0.04/call), but the codebase hard-blocks users at their limit. Selling a feature we can't deliver.

4. **"Why not just buy 7 Max plans?"** At $199/mo × 7 = $1,393/mo, a team gets unlimited calls per person. Enterprise at $999/mo with 15,000 shared calls looked like a worse deal.

5. **Tool calls cost us almost nothing.** The cost to Adspirer per tool call is negligible. Capping them creates friction without reflecting real costs.

---

## Iteration 2: Unlimited Tool Calls + Account-Based Differentiation

### The idea

Remove tool call caps entirely. Make all tiers unlimited. Differentiate on accounts, seats, and features:

| | Max | Enterprise | Enterprise Plus |
|---|---|---|---|
| Tool Calls | Unlimited | Unlimited | Unlimited |
| Seats | 1 | 5 | 10 |
| Accounts/platform | 5 | 50 | 200 |
| Sequential subagents | 5 accounts | 50 accounts | 200 accounts |
| Data retention | 90 days | 12 months | 12 months |
| Support | Standard | Slack (24hr SLA) | CSM (4hr SLA) |

Pricing: Enterprise ~$12,000/yr, Enterprise Plus ~$24,000/yr (annual only).

### What improved

- Eliminated the "why not buy 7 Max plans" problem — account limits (5 per platform on Max) create a hard gate.
- Tool calls no longer a source of friction.
- Sequential subagents became the enterprise differentiator — running operations across 50 or 200 accounts is qualitatively different from 5.

### Problems that remained

1. **No clear pricing unit.** Consumer plans have $/call. Enterprise had... nothing. Just tiers with different feature bundles. How do you negotiate? How do you price a custom deal for someone with 80 accounts?

2. **The 2-3x gap between tiers.** Enterprise at $12K, Enterprise Plus at $24K-$36K. Customers in between (e.g., 100 accounts, 7 seats) had no good option.

3. **Seat vs. account tension.** Some customers need many accounts but few seats (solo agency owner with 50 clients). Others need many seats but few accounts (in-house brand with 10 marketers on 5 accounts). A fixed bundle doesn't fit either well.

---

## Iteration 3: Per-Account Pricing (Cost per Account per Month)

### The idea

Use accounts as the primary pricing unit, like consumer plans use tool calls:

| Tier | Accounts | Annual | $/Account/Mo |
|------|----------|--------|-------------|
| Max | 5 | $2,000/yr | $33 |
| Enterprise | 50 | $12,000/yr | $20 |
| Enterprise Plus | 200 | $24,000/yr | $10 |

Custom deals calculated by: `accounts × $/account/mo × 12`.

### What improved

- Clear unit economics, mirroring $/call for consumer plans.
- Custom deals calculable with simple math.
- Volume discount story is clean: more accounts = cheaper per account.

### Why it wasn't enough

1. **Doesn't account for seats.** An in-house brand with 10 people and 5 accounts generates massive compute — 10 people hammering 5 accounts all day. Per-account pricing would put them on Max ($33/account × 5 = $165/mo), which dramatically underprices the actual system load.

2. **Ignores the interaction effect.** 10 seats × 200 accounts is not 10 + 200 — it's a multiplicative load. More users on more accounts means cross-account queries, concurrent sequential subagent runs, and exponentially more agent work.

3. **No framework for handling seat-heavy customers.** "We have 3 people but 200 accounts" prices correctly. "We have 20 people but 5 accounts" doesn't.

---

## Iteration 4: Seats + Accounts (Additive Model)

### The idea

Price as the SUM of seat costs and account costs:

```
price = (seats × per_seat_rate) + (accounts × per_account_rate)
```

With volume discounts on both:
- Per seat: $120/mo (Max) → $100/mo (Enterprise) → $80/mo (Enterprise Plus)
- Per account: $16/mo (Max) → $12/mo (Enterprise) → $8/mo (Enterprise Plus)

### Test scenarios

| Customer | Seats | Accounts | Calculation | Monthly |
|----------|-------|----------|-------------|---------|
| Max | 1 | 5 | (1×$120) + (5×$16) | $200 |
| Enterprise | 5 | 50 | (5×$100) + (50×$12) | $1,100 |
| E. Plus | 10 | 200 | (10×$80) + (200×$8) | $2,400 |
| Katie | 9 | 200 | (9×$80) + (200×$8) | $2,320 |
| In-house | 10 | 5 | (10×$100) + (5×$12) | $1,060 |
| Solo buyer | 1 | 50 | (1×$100) + (50×$12) | $700 |

### Why it wasn't enough

Still treats seats and accounts as independent dimensions. The reality: **10 users on 200 accounts produce exponentially more compute than 10 users on 5 accounts or 1 user on 200 accounts.** The additive model misses the interaction entirely.

---

## Iteration 5: Compute Units = Seats × Accounts (Multiplicative Model)

### The core insight

The agent's workload scales with the **cross-product** of seats and accounts, not the sum. Why:

- **Cross-account operations**: A user says "pull performance across all 200 accounts." The agent fans out across all 200 — fetching data, loading context, aggregating results. That's O(accounts) per request.
- **User amplification**: 10 users triggering cross-account operations concurrently = 10 × O(accounts) concurrent load.
- **Sequential subagents**: Running campaigns across 50 accounts means 50 account traversals with context switching. With 5 users doing this simultaneously, that's 250 concurrent account contexts.
- **Read-only users (analysts)**: Even read-only users generate heavy compute — "compare CTR across all 200 accounts" requires the agent to fetch and reason over 200 datasets.

**Parallel: Datadog / Snowflake.** Datadog charges per host per month — each host generates monitoring data and query compute. More hosts = more data = more queries = superlinear cost. Our "host" is an ad account. Snowflake separates compute (how hard the system works) from storage (how much data you hold). Both scale independently but interact.

### The formula

```
CU = seats × accounts
```

One Compute Unit (CU) = one seat with access to one account for one month.

| Configuration | Seats | Accounts | CU |
|---------------|-------|----------|-----|
| Max | 1 | 5 | 5 |
| Enterprise | 5 | 50 | 250 |
| Enterprise Plus | 10 | 200 | 2,000 |
| Katie (agency) | 9 | 200 | 1,800 |
| In-house brand | 10 | 5 | 50 |
| Solo buyer | 1 | 50 | 50 |
| Mega agency | 30 | 500 | 15,000 |

The CU range spans 5 to 15,000 — a 3,000× difference. This is why Enterprise can't be "Max + a little more."

### Effective $/CU at published prices

| Tier | CU | Annual | $/CU/mo |
|------|-----|--------|---------|
| Max | 5 | $2,000/yr | $33.33 |
| Enterprise | 250 | $12,000/yr | $4.00 |
| Enterprise Plus | 2,000 | $30,000/yr | $1.25 |

### Why does $/CU drop with volume? (Important caveat)

It **shouldn't** from a pure cost perspective. Compute INCREASES with more seats × accounts — the agent works harder, not less hard. There are no real economies of scale: 2,000 CU doesn't cost less per unit to serve than 5 CU.

The volume discount is a **sales/business decision**, not a cost reality:
- Larger annual deals = lower customer acquisition cost per dollar of revenue
- Annual lock-in = lower churn
- First enterprise logos = marketing/social proof value
- Competitive pressure = enterprise buyers expect volume discounts

The honest framing: there's a base cost per CU, and any discount from that is a conscious concession to win the deal. This means our "floor" in negotiations should be tied to actual costs, not to the discounted published price.

---

## Current Thinking: Base + Add-On Model (Built on CU Framework)

### Published tiers (on the docs page — current)

| | Max | Enterprise | Enterprise Plus |
|---|---|---|---|
| **Annual** | $2,000/yr | $12,000/yr | $30,000/yr |
| **Billing** | Monthly or annual | Annual only | Annual only |
| **Tool calls** | Unlimited | Unlimited | Unlimited |
| **Seats** | 1 | 5 (minimum) | 10 |
| **Ad Accounts per Platform** | 5 | Up to 50 | 200+ |
| **Sequential subagents** | Across 5 accounts | Across 50 accounts | Across 200+ accounts |
| **Tool call pooling** | — | Shared across all seats | Shared across all seats |
| **Data retention** | 90 days | 12 months | 12 months |
| **Support** | Standard | Slack (24hr SLA) | CSM (4hr SLA) |
| **Onboarding** | Self-serve | Guided | White-glove |
| **Custom integrations** | — | — | 2 included |

Enterprise and Enterprise Plus are annual-only. Max is available monthly or annual.

### Add-on rates (for custom configurations)

| Add-on | Rate | Notes |
|--------|------|-------|
| Additional accounts (Max tier) | $8/account/mo | For Max users who need >5 accounts |
| Additional accounts (Enterprise tier) | $5/account/mo | For Enterprise users who need >50 accounts |
| Additional accounts (E. Plus tier) | $3/account/mo | For E. Plus users who need >200 accounts |
| Additional seats (Enterprise tier) | $100/seat/mo | For Enterprise users who need >5 seats |
| Additional seats (E. Plus tier) | $80/seat/mo | For E. Plus users who need >10 seats |

### Natural upgrade breakpoints

**Max → Enterprise:**
At $8/additional account on Max:
```
$199 + (X × $8) = $1,000 → X = 100 accounts
```
At ~100 accounts, Enterprise ($1,000/mo for 50 accounts + 5 seats) becomes the better deal vs. Max + add-ons. But most users hit this threshold much earlier because they also need seats.

**Enterprise → Enterprise Plus:**
At $5/additional account + $100/additional seat on Enterprise:
```
Enterprise with 10 seats + 200 accounts:
$1,000 + (5 × $100) + (150 × $5) = $1,000 + $500 + $750 = $2,250/mo
Enterprise Plus: $2,000/mo ← cheaper
```
Enterprise Plus becomes the better deal when you need both more seats AND more accounts.

### Custom deal scenarios

**Katie (agency): 9 seats, 200 accounts**
```
Enterprise Plus published: $30,000/yr
CU model: 9 × 200 = 1,800 CU
Katie negotiates 15% off: $25,500/yr
Katie negotiates 20% off: $24,000/yr
```

**In-house brand: 10 seats, 5 accounts, $2M/mo ad spend**
```
Enterprise at $12,000/yr (covers 5 seats + 50 accounts)
They need 10 seats → add 5 seats at add-on rate
Custom price: ~$18,000/yr
```

**Solo media buyer: 1 seat, 50 accounts**
```
Max ($199/mo) + additional accounts at add-on rate
Custom price: $500-$600/mo = ~$6,000-$7,200/yr
```

**Mega agency: 30 seats, 500 accounts**
```
CU: 30 × 500 = 15,000 — well beyond Enterprise Plus
Custom deal territory — contact sales
```

### Negotiation framework

For any deal, the sales calculator works as:

1. **Calculate CU**: seats × accounts
2. **Compare to published tier** that best fits
3. **Negotiation room**: up to 15-20% off published price
4. **For configurations between tiers**: use add-on rates from base tier
5. **For configurations beyond Enterprise Plus**: custom pricing via sales

Example — Katie negotiating:
```
Published (E. Plus): $30,000/yr
Katie asks for 15% off: $25,500/yr
Katie asks for 20% off: $24,000/yr
Floor: TBD based on final cost model
```

---

## Open Questions

1. **What are the right account limits per tier?** Currently anchored at Max=5, Enterprise=50, Enterprise Plus=200+. But if we learn from the market that a typical Max user manages 25 accounts, the entire tier structure needs recalibration. The model should be parameterized so we can adjust without redesigning.

2. **Parameterized model for recalibration.** The pricing formula should use tunable parameters:
   ```
   BASE_ACCOUNTS = { max: 5, enterprise: 50, enterprise_plus: 200 }
   BASE_SEATS    = { max: 1, enterprise: 5, enterprise_plus: 10 }
   BASE_PRICE    = { max: $199/mo, enterprise: $1,000/mo, enterprise_plus: $2,500/mo }
   ADDON_ACCOUNT = { max: $8/mo, enterprise: $5/mo, enterprise_plus: $3/mo }
   ADDON_SEAT    = { enterprise: $100/mo, enterprise_plus: $80/mo }
   ```
   If we discover Max users need 25 accounts, we have three levers:
   - **Expand base, keep price**: BASE_ACCOUNTS[max]=25, price stays $199 → more generous, competitive
   - **Expand base, raise price**: BASE_ACCOUNTS[max]=25, price goes to $299 → captures value
   - **Keep base, lower add-on rate**: ADDON_ACCOUNT[max]=$3 → gradual expansion without cliff

3. **What are the actual Stripe metadata values for `max_accounts` per tier?** The code enforces account limits via `get_max_accounts_for_tier()` in `stripe_product_service.py`, but we need to verify the current Stripe configuration matches the model.

4. **Is S × A the right formula, or should it be sublinear?** Not every seat touches every account. In practice, planners are assigned account subsets. Pure S × A may overstate compute for large agencies where each planner manages 20-30 accounts, not all 200. But read-only users (analysts, managers) querying across all accounts push it back toward multiplicative.

5. **How do we handle the in-house brand edge case?** 10 seats on 5 accounts = 50 CU, same as 1 seat on 50 accounts. Are they really equivalent in system load? The in-house team may generate more per-account compute (10 people drilling into the same 5 accounts all day).

6. **Should add-on rates be published or internal only?** Publishing makes pricing transparent but reduces negotiation flexibility. Keeping them internal means custom deals require a sales conversation. Current leaning: keep internal for sales tool.

7. **What is our actual cost floor per CU?** We know tool calls cost almost nothing, but at enterprise scale (200 accounts, 10 users), what are the real costs? Ad platform API calls, data storage for 12-month retention, LLM inference for cross-account operations, MCP server compute. Need to quantify so we have a true floor for negotiations.

8. **Enterprise Plus at $30K — is that the right anchor?** For an agency like Katie managing $7-15M/yr in ad spend, $30K is 0.2-0.4% — easy to justify. But at our current stage (pre-enterprise-logo), we may need founding partner pricing ($20-24K) to close the first few deals. The published $30K gives us room to offer that as a concession.

---

## Appendix: Consumer Plan Reference

For context, the consumer plan pricing that this enterprise model extends:

| Tier | Monthly | Annual | Tool Calls | Accounts/Platform | Seats | $/Call |
|------|---------|--------|-----------|-------------------|-------|--------|
| Free | $0 | — | 15 | 1 | 1 | — |
| Plus | $49/mo | $485/yr | 150 | 1 | 1 | $0.33 |
| Pro | $99/mo | $999/yr | 600 | 1 | 1 | $0.165 |
| Max | $199/mo | $2,000/yr | Unlimited | 5 | 1 | ~$0.04 (implicit) |

Key design principles from consumer plans:
- One clear unit (tool calls) with transparent $/unit
- Each tier step has obvious value math ("4x calls for 2x price")
- Account limits create natural upgrade triggers
- "Unlimited" is bounded by account caps (practical ceiling)
