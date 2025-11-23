NOTE: Solutions must be implemented using Beckn Protocol workflows.

# Problem Statement 1: Utility Interface with Agentic Orchestration

# for Grid-Scale Demand Flexibility

**Context:** Utilities are increasingly unable to autonomously monitor and mitigate
feeder-level spikes in real-time as distributed energy resources (DERs) proliferate
behind-the-meter. Manual coordination is slow, expensive, and lacks visibility and
traceability.
**Challenge:** Build an agent that acts as a reliable co-pilot with a
Command-Centre Dashboard interface for the DSOs (e.g. UK Power Networks) —
forecast and manage local load flexibility at feeder/substation levels, aligned with
Ofgem’s flexibility reforms.
**Minimum Expected Capabilities:**
● The agent must achieve a sub–5 second detection-to-dispatch SLA at
feeder level, integrated with P415 VLP activation and traceable through OBP
IDs for verifiable P444 settlement.
● Agents must implement Beckn Protocol workflows for the utility to discover
available catalogues of subscribed DERs, optimise and activate the DERs to
address the spike in demand
● Forecast localized grid overloads (e.g., at feeders or substations) using
historical and real-time data.
● Coordinate with DERs to shift or shed load constrained by defined rules
(e.g., home batteries discharge, EV charging deferment, heating load
shifting).
● Maintain full audit logs: timestamped decisions, data sources, operator rule
invoked, DER response, available for regulator review.
Note: Assume that the utility has published Demand Flexibility Programs, which
have been subscribed by individuals & businesses, which forms the catalogue of
DERs for this challenge.


**Good-to-Have Capabilities:**
● Agent self-analyses exceptional scenarios and offers alternative pathways
(e.g., multi-feeder failure).
● Differentiation between incentive-based vs emergency interventions (e.g.,
voluntary demand response escalation to forced curtailment).
**Why this matters:** Because the grid of the future cannot depend on human
reflexes, it needs autonomous agents that sense, predict, and balance demand in
real time to prevent blackouts and make flexibility a first-class operational asset.

# Problem Statement 2: Compute–Energy Convergence in a DEG

# World

**Context:** As digital infrastructure and AI compute demands surge, energy grids
and data centres are becoming tightly coupled. In a DEG world, compute loads
act as dynamic nodes in the energy ecosystem—needing coordination,
optimisation, and flexibility.
**Challenge:** Design an agentic orchestration system that co-optimises compute
demand (data-centre/AI-workloads) and energy distribution/storage/flexibility
using DEG infrastructure.
**Minimum Expected Capabilities:**
● Optimisation targets should minimise £ per inference under a defined
carbon intensity cap, using workload deferral windows to monetise
flexibility participation under P415.
● Model compute assets (e.g., AI training cluster, server farm) as
energy-demanding entities with flexible scheduling windows.
● Forecast compute workload spikes and align with grid signals for energy
availability, cost, carbon intensity.


● Initiate orchestration commands: defer workloads, shift compute region,
schedule storage discharge, or enable renewable-only compute windows.
● Log decisions, data sources, compute/energy trade-offs, and system
outcomes for audit.
● Compute agents publish job slots as Beckn catalog items; grid agents
confirm via order lifecycle.
**Good-to-Have Capabilities:**
● Multi-agent negotiation: compute operator agent interacts with grid
operator agent and storage/battery agents to dynamically allocate
resources.
● Carbon-aware scheduling: workloads prioritised during
low-carbon-intensity periods and rewarded via flexibility markets.
● Dashboard simulation showing compute-energy flows, cost savings,
carbon reductions, and flexibility contributions.
**Why this matters:** Because AI and compute are now major energy loads —
integrating them intelligently with energy networks is the only way to ensure our
digital future doesn’t destabilize the physical grid that powers it.


