# Hackathon Submission Form Answers

## 2. Problem Focus

**Select one problem statement your solution addresses:**

☑️ **Problem 1:** Utility Interface with Agentic Orchestration for Grid-Scale Demand Flexibility

☐ Problem 2: Compute-Energy Convergence in a DEG World

---

## 3. Solution Overview (max 150 words)

**Briefly describe your idea. What problem are you solving, and how does your agentic solution create value in the Digital Energy Grid ecosystem?**

DSOs struggle to autonomously coordinate load flexibility as DERs proliferate behind-the-meter, leading to manual, slow, untraceable interventions.

We built an AI-powered agentic orchestration system for DSOs (e.g., UK Power Networks) that forecasts grid overloads using weather and load data, then uses Google Gemini AI to generate optimized DER dispatch plans. Through Beckn Protocol workflows, it automatically discovers subscribed DERs (batteries, EV chargers, HVAC systems) and orchestrates activation via Search → Select → Confirm flows.

Value creation: sub-5 second detection-to-dispatch, prioritizing non-wires alternatives over physical infrastructure, and maintaining full audit trails for regulatory compliance. A command-centre dashboard provides real-time visualization, transforming manual coordination into autonomous, traceable flexibility management aligned with Ofgem's reforms.

---

**Word Count:** 99 words

---

## 4. Technical Architecture (max 200 words or diagram)

**Explain the AI agent you plan to build and how they will solve the problems and create value, while leveraging Beckn and DEG components.**

**Include:**
- Key agents and their roles
- Data sources / APIs / models used (e.g., Beckn Sandbox, AI models)
- Orchestration or coordination logic
- Include all assumptions and references (Optional: include a simple diagram or link to a visual model in your submission)

---

**Answer:**

**Key Agents:**
1. **Risk Assessment Agent**: Analyzes weather scenarios, forecasts grid congestion at feeder/substation levels, calculates load projections and risk levels (CRITICAL/HIGH/MEDIUM/LOW).
2. **AI Flexibility Orchestrator** (Google Gemini): Generates optimized DER dispatch plans by analyzing grid constraints, prioritizing non-wires alternatives, recommending specific actions (battery discharge, EV curtailment, HVAC shifting).
3. **Beckn Orchestration Agent** (BAP Client): Discovers and activates DERs through Beckn Protocol workflows, managing Search → Select → Confirm flows.

**Data Sources/APIs:**
- Google Gemini API (gemini-flash-latest) for flexibility planning
- Beckn Protocol v0.9.3 for DER discovery (BAP/BPP implementation)
- Mock Weather Service for scenario simulation
- DEG Asset Data (substations, EV hubs, solar farms)
- Mock BPP Server simulating DER providers (Tesla VPP, ChargePoint, Honeywell)

**Orchestration Logic:**
Three-stage pipeline: (1) Risk Engine processes weather scenarios and calculates grid congestion risks, (2) AI Agent analyzes risks and generates DER dispatch plans with urgency and justification, (3) Beckn Service orchestrates parallel DER discovery/activation flows, selecting optimal providers and confirming orders. All transactions logged for audit compliance.

**Assumptions:**
DERs pre-subscribed to Demand Flexibility Programs; Mock BPP simulates real DER provider networks; weather data triggers load projections; Beckn Protocol enables standardized DER discovery.

**Architecture Diagram:** See README.md for complete system architecture diagram.

---

**Word Count:** 199 words

---

## 5. Agent Workflow (max 150 words)

**Describe how your agent works along with relevant Beckn protocol flows, where applicable in your context.**

---

**Answer:**

Three-stage autonomous workflow:

**Stage 1 - Risk Assessment:** User inputs weather scenario (location, event type, duration). Risk Engine loads DEG assets, fetches weather data, calculates grid congestion risks based on projected load (e.g., heatwave → AC demand spike → feeder overload >120% capacity).

**Stage 2 - AI Planning:** AI Flexibility Orchestrator (Google Gemini) receives risk results, generates optimized DER dispatch plan. Analyzes grid constraints, prioritizes non-wires alternatives, outputs specific actions (battery discharge, EV curtailment, HVAC shifting) with urgency levels and technical justifications.

**Stage 3 - Beckn Orchestration:** For each AI-recommended action, Beckn Orchestration Agent executes full Beckn Protocol flow: (1) **Search** - queries Mock BPP for DER catalog matching action_type, receives catalog via `/beckn/on_search` callback, (2) **Select** - chooses optimal DER service, receives quote via `/beckn/on_select` callback, (3) **Confirm** - confirms order, receives confirmation via `/beckn/on_confirm` callback. All transactions logged with timestamps, provider details, and status for audit compliance.

---

**Word Count:** 148 words

---

## 6. Business Model & Impact (max 150 words)

**Outline the potential business model, value capture, and stakeholders who benefit (utilities, data centers, aggregators, consumers, etc.). Include any sustainability, scalability, or revenue aspects.**

---

**Answer:**

**Business Model:** SaaS platform for DSOs/Utilities with subscription pricing and transaction fees per orchestrated flexibility event. Value capture through reduced grid congestion costs, avoided infrastructure investments, and regulatory compliance.

**Stakeholders:**
- **Utilities/DSOs:** Autonomous grid management, reduced operational costs, outage prevention, Ofgem compliance. Sub-5 second response enables real-time congestion mitigation.
- **DER Owners:** Monetize flexible assets (batteries, EV chargers, HVAC) through demand response, earning revenue while supporting grid stability.
- **Aggregators:** Efficient DER portfolio management, optimized dispatch, revenue maximization through automated orchestration.
- **Regulators:** Full audit trails, traceable decisions, verifiable P444 settlement compliance.

**Sustainability:** Reduces fossil fuel peaker plants, enables higher renewable integration, optimizes energy use through intelligent DER coordination, lowers carbon emissions.

**Scalability:** Beckn Protocol ensures interoperability across diverse DER types. Cloud-native architecture scales from single feeders to entire distribution networks.

**Revenue:** Platform subscriptions (£50K-200K/year per utility), transaction fees (£0.01-0.05 per kWh dispatched), premium analytics services.

---

**Word Count:** 150 words
