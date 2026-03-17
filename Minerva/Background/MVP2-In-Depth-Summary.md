# 1) MVP2 / Phase 2 — What it is (definition in contract language)

The Benefit Quoting Assistant MVP 2 - Draft SOW.docx defines “ **Member Benefit Quoting Assistant MVP 2** ” as a **phase 2 implementation** plus **Run Services** of the GenAI-assisted agent solution developed under MVP1 (Work Order 65) to support agents answering member questions about  **plan details, coverage, and cost sharing** , with explicit expansion to:

* **Large Group (LG)** and  **Custom plans** ,
* **pharmacy benefits** , and
* integration to **Nexus** and **Facets/Experience Cube** for “seamless workflows and data access.” 

The Accenture Work Order XX - Member Benefit Quoting MVP2_Draft.docx similarly frames MVP2 as continuing the PoC + MVP1 solution and “enhancing” it to expand to additional plan populations and benefit domains. 

---

# 2) MVP2 scope — Explicit inclusions and exclusions (with the exact wording)

## 2.1 Scope inclusions (what MVP2 adds)

The Draft SOW includes a bulleted scope list (this is the most “plain English” articulation in a single place):

* “ **Enable quoting capability for all Large Group and Custom plans including Pharmacy benefits** ”
* “ **Integrate the quoting workflow with Nexus for streamlined operations** ”
* “ **Integrate the quoting workflow with Facets/Experience Cube for quoting allowed amount based on provider network and contracted rate data** ”
* “ **Provide updated scripting compliant with internal guidelines** ”
* “ **Provide Databricks report on agent usage of AI-generated chats to quote benefits** ”

The IT Risk Assurance intake spreadsheet GAI-053 - Benefits Quoting MVP2.xlsx adds more business framing on “what this will accomplish,” describing MVP2 as scaling the Q4’25 release (IFP/SG) to:

* LG, Custom plans,  **pharmacy (based on Nexus data)** , and
* quoting on provider contract data “specifically for allowed amounts,”
* producing “real-time templatized response” with outcomes like “ **2-minute reduction in average handle time** ” and “**achieve 98% or high[t] benefit quote accuracy** … starting Q2 2026.” 

## 2.2 Exclusions (explicit)

The Draft SOW explicitly states: “ **Medicare and Medi-Cal and Federal Employee Program (FEP) data will not be utilized for the MVP** .”

The Accenture work order similarly excludes “ **Medicare Advantage, Medi-Cal, and FEP** ” from scope. 

---

# 3) MVP2 deliverables — “What must be produced” (enumerated in the SOW)

The Draft SOW contains a structured deliverables list that’s particularly useful because it describes what “done” means beyond “the model answers questions.” It enumerates:

### 3.1 Product / platform deliverables

* “ **An updated data layer consisting of vector DB that has additional Nexus and Facets/Experience Cube information loaded, and Q&A chain served as Mosaic AI Model Serving endpoint** .” 
* “ **Enhanced web page to access the model endpoint providing the chatbot functionality** .”
* “ **API integration with Facets/Experience Cube platform for provider network and contracted rate access** .”

### 3.2 Documentation deliverables

The Draft SOW lists required documentation artifacts, including:

* “ **Detailed requirements document and enhanced UI wireframe** ” 
* “ **Updated high-level architecture diagram with Nexus and Facets/Experience Cube integration** ”
* “ **Updated UAT plan with defined test cases and measurable performance metrics** ”
* “ **Updated simple user guide and FAQ** ”
* “ **Roadmap and a high-level plan for subsequent phases** ”

### 3.3 “Operationalization” deliverables (quality + telemetry)

The Draft SOW explicitly lists feature enhancements that are fundamentally “productization” controls:

* **LLM as judge** (automate response evaluation) 
* **Log processing** (capture/structure/analyze interaction logs)
* **Feedback collection** (store user/evaluator feedback for continuous improvement)
* **Session memory (STM) + persistent memory (LTM)**
* **CI/CD for model deployments via Databricks + Git**
* **Enhanced UI** (feedback capture, session management, context display)
* **Databricks report on usage of AI-generated chats**

---

# 4) Data sources & integration surface (what systems are in play, explicitly)

## 4.1 Named platforms and what each is “for”

Both the Draft SOW and the work order define terms directly:

* **“Nexus”** is the platform managing plan products, benefits, coverage, and cost sharing structures. 
* **“Facets/Experience Cube”** is defined as containing provider network contracts, fee schedules, and allowed amounts.
* **Databricks “Mosaic AI Vector Search”** is described as automatically indexing data in a vector database to improve search + LLM predictions.
* **Databricks “Mosaic AI Model Serving”** is the model deployment/querying/monitoring endpoint service.

## 4.2 Required dependencies (what Blue Shield must provide)

The Draft SOW’s “Dependencies” section is explicit that Blue Shield must provide:

* “ **PDFs, JSONs and tabular data which include Nexus product information and expected responses compliant with Compliance Script** ” for expanded plans + pharmacy. 
* “ **PDFs and tabular data** ” for provider network and contracted rate information (for allowed amount quoting).
* Environments (Azure dev/test/prod) and continued API access for Nexus and Experience Cube integrations.
* Access to SMEs and agreement on MVP2 functional requirements.

## 4.3 Reality check from discovery: Pharmacy is multi-system

The formulary discovery transcript and notes make it very clear that pharmacy inquiries are not “just a formulary PDF”:

* Agents must manually determine the correct formulary; there’s “ **no automatic identification** ,” increasing risk of wrong answers. 
* Claim troubleshooting (“why did it reject / why did it price differently”) involves a separate system,  **Darwin** , which is **not integrated** today; agents must log in and manually search (though APIs could exist).

This is echoed in the latest program email: governance guidance recommends keeping MVPs  **product-specific not member-specific** , meaning MVP2 should retrieve the **correct formulary document/data** but **not** do real-time claim/auth/cost—because those are dynamic/member-specific. 

---

# 5) Quality & acceptance — Exactly how MVP2 will be tested and “passed”

## 5.1 UAT criteria (consistent across documents)

Both the Draft SOW and Accenture work order specify UAT evaluation dimensions:

* **Accuracy:** response must be based on the correct plan selected and benefit details must align with source data (Nexus; SOW also explicitly includes allowed amounts as an example).
* **Compliance:** response must follow “Compliance Script” guidelines so no material disclosure is omitted.

## 5.2 Target thresholds — “100%” vs negotiated band

The Draft SOW includes a strong statement: “**target UAT score is 100% against 50 sample questions** to be provided by Blue Shield.” 

The Accenture work order shows an explicit negotiation in comments, culminating in:

* **95–98% accuracy** and **90–95% compliance/completeness** as the agreed targets. 

> **Interpretation:** your artifact set contains both (a) a “draft aspiration” (100% / 50 questions) and (b) an “agreed banded target” negotiated in the work order comments. 

## 5.3 Independent evaluation signal: Minerva vs BennyAI accuracy

The evaluation report main (4).pdf documents a statistical comparison between **BennyAI** and  **Minerva** :

* BennyAI accuracy: **89/121 = 73.55%** (95% CI [65.70%, 81.41%])
* Minerva accuracy: **222/225 = 98.67%** (95% CI [97.17%, 100.17%])
* Observed difference:  **25.11 percentage points** , with **Z = 7.388, p < 0.0001** (two-proportion z-test) 

The report also notes a methodological caveat that the two systems were evaluated on  **different question sets** , which “limits strict interpretability” as a head-to-head on identical items. 

---

# 6) Governance boundaries — What MVP2 is allowed to do (and why)

The most explicit “governance boundary statement” is in MVP2/Phase 2 Topics for Core Team:

* To pass AI Governance, MVP2 must be clear “what is in or out.”
* “ **Initial recommendation was to keep the information product-specific and not member-specific through the MVPs** .”
* “This means we are retrieving the correct formulary document and data and **NOT** looking at a real-time cost / claim / auth.”
* It acknowledges this “doesn’t solve the full problem statement” but reduces friction in part of the process.
* It also states that while there is governance approval for  **IFP & SG** , the team will need to go back through governance to scale to **Core/Premier** and formulary. 

The formulary discovery notes reinforce why this matters: the “full” pharmacy problem includes real-time adjudication and auth status, which are dynamic/member-specific and span other systems. 

---

# 7) Timeline & milestones — What the documents say (and what “in flight” says)

## 7.1 Contracted Accenture timeline

The Accenture work order states:

* **Work Order Effective Date:** January 5, 2026
* **Work Order End Date:** May 17, 2026 

Milestones include:

1. Technical & functional design and requirements: **01/05/2026 → 1/23/2026** (sign-off on requirements, mappings, architecture, scope coverage).
2. Initial iteration on prompt engineering: **1/23/2026 → 2/13/2026** (confirm model supports Nexus plans in scope).
3. Fine-tuning & optimization: **2/13/2026 → 3/27/2026** (achieve baseline target quality score).
4. UAT: **3/27/2026 → 4/10/2026**
5. Documentation: **4/10/2026 → 4/17/2026**
6. Run Services: **4/17/2026 → 5/17/2026**

## 7.2 Program email timeline deltas (“Now 5/31”)

The latest email provides a program-level table that also reflects evolving dates:

* Phase2 (MVP2/Phase 2) initially “April 2026,” now “ **5/31** ” (date presented in the table) with scope “+ Large Group & Premier + formulary information.” 
* Phase 3 described with dynamic member-personalized information (accums, allowed amounts for specific providers, etc.), and “October 2026 for benefits in 2027.”

## 7.3 IT Risk Assurance “target go-live”

The intake file GAI-053 - Benefits Quoting MVP2.xlsx shows:

* Request date **09/30/2025**
* Committee review date **10/06/2025**
* Target go-live date **04/15/2026** 

---

# 8) Commercials & funding — What it costs (and how it’s paid)

## 8.1 Accenture fixed-bid contract value and payment schedule

The Accenture work order includes a fixed-bid total:

* **TOTAL FIXED BID PERMITTED CHARGES: $300,000.00** 

It also lists milestone payment amounts:

* Milestone 1 (design/requirements): **$70,000** 
* Milestone 2 (initial model iteration): **$70,000**
* Milestone 3 (fine-tuning/optimization): **$77,000**
* Milestone 4 (UAT): **$45,000**
* Milestone 5 (documentation): **$23,000**
* Milestone 6 (Run Services 4/17/2026–5/17/2026): **$15,000**

## 8.2 Internal build estimate (alternative path)

The message Benefit Quoting MVP2 Funding - Nexus Team Estimates.msg provides an internal staffing-based estimate totaling **$264,000** over  **3 months** , with role rates:

* UI Dev ($140/hr) → $73,920
* Full Stack Dev ($140/hr) → $73,920
* QE ($90/hr) → $47,520
* BA ($130/hr) → $68,640

## 8.3 Decision to proceed with Accenture (and why)

The decision thread explicitly states:

* “best course… proceed with Accenture” to ensure funding in place and avoid delays, with intent to possibly revisit in-house build for MVP3 later.

---

# 9) Financial value model — What the program says it returns (and assumptions)

You have *two* detailed models surfaced as attachments and snippets in MVP2/Phase 2 Topics for Core Team.

## 9.1 High-level phase cost model (email table)

The email summarizes cost assumptions by phase:

* **MVP1** : build $325K, ongoing $36K/year (also notes $25K Nexus UI build internally and scrum master cost). 
* **Phase2 (MVP2)** : “+ Large Group & Premier + formulary information,” build $300K, ops resource $25K, ongoing $60K/year (and “expect ongoing costs to be lower, but build cost approximately flat”).
* **Phase 3** : dynamic member-personalized info (accums, allowed amounts for specific providers, etc.), build $1M, ops $100K, plus “$35K of portion of an FTE in Ops + compute/consumption,” and notes this was increased from an earlier Accenture ballpark due to integration and operational support.

## 9.2 Investment summary (ROI/NPV/DPP and totals)

The attachment Benefits Quoting Investment Summary - MVP1 &amp; MVP2 - 2026 Version.xlsx includes (in the “Input for Investment Summary” sheet) computed totals:

* **Total Benefits (5 Year): 3,965,830**
* **Total Ongoing Cost (5 Year): 300,000**
* **Total Cost of Ownership (All Years): 1,190,002**
* **Total OpEx Project Investment (All Years): 200,000**
* **Total CapEx Project Investment (All Years): 690,002**
* **Discounted Payback Period:** 2.7023…
* **Return on Investment (5 Year):** 2.3326… 

The same workbook’s “Benefits” sheet frames the KPI driver as:

* “Average **2 minute reduction in average call handle time** for member benefits quoting inquiry response,” baseline 15 minutes, projected to 13 minutes. 

The “On-Going Costs” sheet shows an annual cost line of **60,000** repeated across 2026–2030 (totaling 300,000) under Customer Experience in the snippet. 

## 9.3 Financial savings model (phase-by-phase savings, with explicit assumptions)

The attachment Benefit Quoting_Financial Savings Model.xlsx is more granular and includes:

* A “Total Benefit Summary” describing 2026 savings based on phased rollout and two data sources:
  * Scenario 1 = CSR-reported call purpose
  * Scenario 2 = AI-assigned call intent from transcripts
* It explicitly states: “Actual savings are likely to fall in a range somewhere between the two data sets.”
* For MVP2 (June 2026), scope is “Portfolio Fully Insured Groups (Core and Premier)… Formulary,” with example subtotals in the model table.
* It includes an assumption: “Per Greg R, cost per Minerva transaction is  **$0.03** .”

---

# 10) MVP2 product expansion discovery — what changes when moving from IFP/SG to Core/Premier/LG

The meeting transcript for Initial Discussion on Benefit Differences is highly relevant to MVP2 planning because it details the **differences between IFP/SG products and Core/Premier portfolio products** and what new requirements emerge.

## 10.1 What’s happening and why (from transcript)

Deborah states MVP1 is for IFP and small group, and now the team needs requirements for feeding “Core and Premiere data” and understanding “nuance” between Core/Premier portfolio products and IFP/SG. 

## 10.2 Plan type “tier” complexity and Virtual Blue

Key points captured in transcript:

* Discussion that “Virtual Blue” was previously out of scope but is now important; suggests adding it back into MVP2 and notes it’s critical because PPO/EPO savings plans are moving to Virtual Blue, including Core changes for 2027.
* Clarification that Virtual Blue $0 tier is only for Teladoc/Virtual Blue providers, and other virtual visits may be standard office visit cost share.
* Need for scalable “plan indicator” logic to avoid per-plan maintenance (“we need some sort of indicator that identifies the plan and what we can expect from it”).

## 10.3 Scope decisions: grandfathered

The transcript includes an explicit decision to keep “grandfathered” out of scope, citing plans being withdrawn “as of 1/1/27,” making it not worth effort now.

## 10.4 Portfolio product nuances that impact ground truths / testing

The transcript captures specific “watch outs” for large group portfolio products:

* Groups with non-1/1 effective dates and “plan year deductibles.”
* Riders: PPO side hearing aids ($2,000 allowance every 24 months) and HMO hearing aids + acupuncture + chiropractic.
* Fully insured large group includes infertility benefits (new benefit set, actively evolving with DMHC guidance).
* Out-of-state coverage nuances: Blue Card vs Blue HPN; and mention that for 2027 EOCs will be tagged with out-of-state coverage data in Nexus.

---

# 11) Pharmacy/formulary discovery — what MVP2 must decide (interim vs full solve)

## 11.1 The core problem statement from discovery

The transcript and notes show common pharmacy inquiry triggers:

* Tier and cost questions after a prescription is rejected or costs differ from expectation.
* Questions requiring formulary: coverage, tier, quantity limits, step therapy, limitations, non-formulary/OTC flags, alternative Rx (generic) options.

## 11.2 Current workflow described

Agents are directed via KBs to:

* Navigate Blue Shield website and locate the correct formulary; this is described as tedious and error-prone—especially because the agent must choose the correct formulary manually.

## 11.3 System fragmentation & “full solve” complexity

Discovery explicitly distinguishes:

* Formulary lookup (web) vs claim adjudication details (Darwin), and notes there is no integration today, though APIs might exist.
* Suggests “interim” could be retrieving the right formulary + finding the medication, while Phase 3 would be the “full solve” with member-specific data (claim/auth/real-time).

---

# 12) Implementation workstreams in flight (so you can see “what’s being done right now”)

The transcript snippet captures concrete integration work items:

* “what it takes to get the Nexus APIs connected to the Stellaris network” and the need for “QA to QA on both sides.”
* Mentions APIM/API connectivity needs (“APIM to API / API to API”).

The cost model meeting transcript captures details on how call volumes were used in cost modeling (example: IFP calls “46,000 in December,” taking “one in three” applicable, etc.) and explicitly notes that estimates are conservative and expected to be revised.

---

# 13) “One-page” MVP2 summary (consolidated, complete)

Here’s a consolidated “all details in one place” view that you can copy/paste as a self-contained MVP2 brief:

**MVP2 / Phase 2 objective:** Expand the GenAI agent-assist benefit quoting capability delivered in MVP1 to  **Large Group + Core/Premier portfolio products + custom plans** , add  **pharmacy benefits** , and enable **allowed amount quoting** by integrating provider contract/rate data via  **Facets/Experience Cube** , while maintaining compliant, templatized responses for agents. 

**Out of scope:** Medicare / Medi-Cal / FEP (explicit). 

**Key deliverables:** updated vector DB with Nexus + Experience Cube data; Mosaic Model Serving endpoint; enhanced UI; Experience Cube API integration; updated architecture and requirements; UAT plan; user guide/FAQ; usage reporting via Databricks; plus productization controls (LLM-as-judge, logging, feedback capture, CI/CD). 

**Governance boundary (critical):** MVP2 should remain **product-specific** and avoid **member-specific real-time** (claim/auth/cost) data; pharmacy is therefore expected to focus on retrieving the correct formulary and drug information rather than real-time claim adjudication (Darwin) in the MVPs. 

**Acceptance criteria:** responses must pass **accuracy** and **compliance** checks; Draft SOW calls for 100% on 50 questions, while the Accenture work order records agreed targets of **95–98% accuracy** and  **90–95% compliance/completeness** . 

**Contract & schedule (Accenture option):** fixed-bid  **$300K** , running  **Jan 5, 2026 → May 17, 2026** , with milestone payments and Run Services in the final month. 

**Program plan updates:** email describes Phase2 scope as “Large Group & Premier + formulary,” build cost  **$300K** , ops resource  **$25K** , ongoing  **$60K/year** , with target shifting to “Now 5/31.” 

**Financial model signals:** investment summary shows  **5‑year benefits 3,965,830** ,  **5‑year ongoing costs 300,000** ,  **TCO 1,190,002** ,  **DPP ~2.70** ,  **ROI ~2.33** ; savings model uses two scenarios (CSR vs AI call intent) and assumes **$0.03 per Minerva transaction** in one sheet.
