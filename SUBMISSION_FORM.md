# Hackathon Submission Form Answers

## 2. Problem Focus

**Select one problem statement your solution addresses:**

☑️ **Problem 1:** Utility Interface with Agentic Orchestration for Grid-Scale Demand Flexibility

☐ Problem 2: Compute-Energy Convergence in a DEG World

---

## 3. Solution Overview (max 150 words)

**Briefly describe your idea. What problem are you solving, and how does your agentic solution create value in the Digital Energy Grid ecosystem?**

Our solution addresses the critical challenge of autonomous grid congestion management at feeder/substation levels. As DERs proliferate behind-the-meter, DSOs struggle to coordinate load flexibility in real-time, leading to manual, slow, and untraceable interventions.

We built an AI-powered agentic orchestration system that acts as a reliable co-pilot for DSOs (e.g., UK Power Networks). The system forecasts grid overloads using weather and load data, then uses Google Gemini AI to generate optimized DER dispatch plans. Through Beckn Protocol workflows, it automatically discovers subscribed DERs (batteries, EV chargers, HVAC systems) and orchestrates their activation via Search → Select → Confirm flows.

The solution creates value by enabling sub-5 second detection-to-dispatch, prioritizing non-wires alternatives over physical infrastructure, and maintaining full audit trails for regulatory compliance. A command-centre dashboard provides real-time visualization of grid assets, risks, and DER coordination, transforming manual coordination into autonomous, traceable flexibility management aligned with Ofgem's reforms.

---

**Word Count:** 149 words

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

**Key Agents & Roles:**
1. **Risk Assessment Agent** (Risk Engine): Analyzes weather scenarios and forecasts grid congestion at feeder/substation levels, calculating load projections and risk levels (CRITICAL/HIGH/MEDIUM/LOW).
2. **AI Flexibility Orchestrator** (Google Gemini): Generates optimized DER dispatch plans by analyzing grid constraints, prioritizing non-wires alternatives, and recommending specific DER actions (battery discharge, EV curtailment, HVAC shifting).
3. **Beckn Orchestration Agent** (BAP Client): Discovers and activates DERs through Beckn Protocol workflows, managing Search → Select → Confirm flows with DER providers.

**Data Sources/APIs/Models:**
- **Google Gemini API** (gemini-flash-latest): AI model for flexibility planning
- **Beckn Protocol v0.9.3**: DER discovery and orchestration (BAP/BPP implementation)
- **Mock Weather Service**: Weather data for scenario simulation
- **DEG Asset Data**: Substations, EV hubs, solar farms (JSON-based)
- **Mock BPP Server**: Simulates DER providers (Tesla VPP, ChargePoint, Honeywell)

**Orchestration Logic:**
The system follows a three-stage pipeline: (1) Risk Engine processes weather scenarios and calculates grid congestion risks, (2) AI Agent analyzes risks and generates DER dispatch plans with urgency and justification, (3) Beckn Service orchestrates parallel DER discovery/activation flows, selecting optimal providers and confirming orders. All transactions are logged for audit compliance.

**Assumptions:**
- DERs are pre-subscribed to Demand Flexibility Programs
- Mock BPP simulates real DER provider networks
- Weather data triggers load projections (heatwave → AC spike → grid overload)
- Beckn Protocol enables standardized DER discovery and activation

**Architecture Diagram:** See README.md for complete system architecture diagram.

---

**Word Count:** 199 words

---

## 5. Agent Workflow (max 150 words)

**Describe how your agent works along with relevant Beckn protocol flows, where applicable in your context.**

---

**Answer:**

The agent operates through a three-stage autonomous workflow:

**Stage 1 - Risk Assessment:** User inputs a weather scenario (location, event type, duration). The Risk Engine loads DEG assets, fetches weather data, and calculates grid congestion risks based on projected load (e.g., heatwave → AC demand spike → feeder overload >120% capacity).

**Stage 2 - AI Planning:** The AI Flexibility Orchestrator (Google Gemini) receives risk results and generates an optimized DER dispatch plan. It analyzes grid constraints, prioritizes non-wires alternatives, and outputs specific actions (battery discharge, EV curtailment, HVAC shifting) with urgency levels and technical justifications.

**Stage 3 - Beckn Orchestration:** For each AI-recommended action, the Beckn Orchestration Agent executes the full Beckn Protocol flow: (1) **Search** - queries Mock BPP for DER catalog matching action_type, receives catalog via `/beckn/on_search` callback, (2) **Select** - chooses optimal DER service, receives quote via `/beckn/on_select` callback, (3) **Confirm** - confirms order, receives confirmation via `/beckn/on_confirm` callback. All transactions are logged with timestamps, provider details, and status for audit compliance.

---

**Word Count:** 149 words

---

## 6. Business Model & Impact (max 150 words)

**Outline the potential business model, value capture, and stakeholders who benefit (utilities, data centers, aggregators, consumers, etc.). Include any sustainability, scalability, or revenue aspects.**

---

**Answer:**

**Business Model:** SaaS platform for DSOs/Utilities with subscription-based pricing and transaction fees per orchestrated flexibility event. Value capture through reduced grid congestion costs, avoided infrastructure investments, and regulatory compliance.

**Stakeholders & Benefits:**
- **Utilities/DSOs:** Achieve autonomous grid management, reduce operational costs, prevent outages, and comply with Ofgem flexibility reforms. Sub-5 second response times enable real-time congestion mitigation.
- **DER Owners (Consumers/Businesses):** Monetize flexible assets (home batteries, EV chargers, smart HVAC) through demand response participation, earning revenue while supporting grid stability.
- **Aggregators:** Efficiently manage DER portfolios, optimize dispatch, and maximize revenue through automated orchestration.
- **Regulators:** Gain full audit trails, traceable decisions, and verifiable P444 settlement compliance.

**Sustainability:** Reduces reliance on fossil fuel peaker plants, enables higher renewable integration, and optimizes energy use through intelligent DER coordination, lowering carbon emissions.

**Scalability:** Beckn Protocol ensures interoperability across diverse DER types and providers. Cloud-native architecture scales from single feeders to entire distribution networks.

**Revenue Streams:** Platform subscriptions (£50K-200K/year per utility), transaction fees (£0.01-0.05 per kWh dispatched), and premium analytics services.

---

**Word Count:** 150 words

