# Project Name: Golden Dataset Quality Validation MVP

**PDLC Phase:** Definition
**Primary Delivery Partners:** Data Science, Product, Engineering
**Reference Experience:** Compass CSR Chat

## Problem Statement

Stellarus Compass Products need a repeatable way to establish customer-specific ground truth, evaluate conversational-agent responses, and communicate quality confidence before a pilot or full-product launch. Today, platform taxonomies, illustrative questions, canonical answers, agent outputs, human review, and quality evidence can be distributed across spreadsheets, testing tools, and implementation knowledge. This makes customer onboarding slow, obscures which questions are applicable, and makes quality decisions difficult to reproduce.

The workflow must initially support CSR Chat while establishing a portable information model for Member Chat, Member Inbound Voice, Outbound Voice, and future experiences. It must also distinguish reusable platform assets from customer-owned data and support both rapid pilots and paying-customer onboarding without requiring customers to use the internal tool.

## Proposed Solution

Create a Golden Dataset Quality Workspace for Data Science and Product. The MVP will use CSR Chat as the reference experience and support the complete single-turn workflow:

`Customer onboarding → taxonomy review → base-question selection → customer augmentation → canonical-answer approval → agent-response collection → LLM critique → human adjudication → quality scoring → Product approval → customer-facing exports`

The interface should support each stage, but manual workflows, structured imports, and exports are acceptable where they allow the process to operate. Data Science and Engineering will determine how responses are executed against or collected from the agent; the product contract requires traceable responses and run metadata, not a prescribed integration method.

The canonical answer is the primary accuracy reference. Supporting evidence, required facts, expected behaviors, and prohibited claims provide additional context for LLM critique and human review but do not replace the approved canonical answer.

## Target Users

**Primary Users:**

* **Data Science:** Curates taxonomy and question coverage, drafts and reviews canonical answers, evaluates LLM critiques, adjudicates case results, and monitors judge usefulness.
* **Product:** Defines experience and customer scope, approves datasets and exceptions, owns the quality decision, and produces customer-facing confidence evidence.

**Secondary Users:**

* **Engineering:** Provide agent-response execution or ingestion, environment/build metadata, and technical support for repeatable runs.
* **Customer implementation and benefits stakeholders:** Supply customer-specific questions, source material, and feedback through the implementation process without directly using the MVP interface.
* **Customers:** Consume the executive confidence report and detailed evidence export as indirect users.

## Success Metrics

| Metric                                      | Baseline                                                                           | MVP target                                                                                                                                                                                                                     | Measurement                                                                                |
| ------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **Review-ready onboarding time**      | Current workflow is fragmented and has no measured end-to-end baseline.            | By the third CSR Chat onboarding, move a complete customer intake from workspace creation to`In Review` within **2 business days**.                                                                                    | Workspace and lifecycle timestamps, excluding time waiting for incomplete customer inputs. |
| **Dataset and evidence completeness** | Existing artifacts do not provide one enforced lifecycle or traceability contract. | 100% of platform base questions are classified for the customer; 100% of`Applicable` approved cases have a canonical answer, ownership, version, and response result; every approved dataset produces both required exports. | Completeness validation at approval and export generation.                                 |
| **LLM-judge usefulness**              | No production baseline supplied.                                                   | Achieve at least**85% agreement** between the judge recommendation and final human case decision across the first three approved datasets; retain critique and resolution for 100% of disagreements.                     | Judge recommendation compared with final Data Science decision by dataset and taxonomy.    |

The first three onboardings establish the operating baselines for total setup effort, review effort, questions per dataset, rerun effort, and customer-requested augmentations.

## Scope

### 1. Customer and Experience Onboarding

* Create an internal customer workspace with customer identifier, deployment type (`Rapid pilot` or `Paying customer`), selected experience, owners, source/data versions, and intended review date.
* Enable CSR Chat as the only operational MVP experience.
* Include an experience identifier and configurable taxonomy/question metadata so the same model can later support Member Chat, Member Inbound Voice, Outbound Voice, bundled experiences, and future channels without redefining lifecycle, ownership, scoring, or export concepts.

### 2. Platform Taxonomy and Base-Question Library

* Maintain platform-owned CSR Chat taxonomies and reusable base questions.
* Load the platform base questions into every customer CSR Chat workspace.
* Allow Data Science and Product to review taxonomy descriptions, question wording, intended coverage, and portability metadata.
* Preserve platform ownership and lineage when a base question is reused across customers.

### 3. Customer Applicability and Augmentation

* Classify every platform base question as `Applicable`, `Not applicable`, or `Deferred` for the customer.
* Allow customer-specific questions to be added through the Data Science/Product workflow.
* Mark customer-added questions and all customer-specific canonical answers, evidence, facts, behaviors, prohibitions, and review data as customer-owned.
* Report all three applicability states so exclusions and deferrals remain visible and cannot silently inflate confidence.

### 4. Golden Case Authoring

Each single-turn golden case must support:

* Experience, taxonomy, platform/customer ownership, and question origin.
* Question text and optional structured context supplied with the single turn.
* Required customer/product/plan and effective-version context.
* One approved canonical answer as the primary accuracy reference.
* Optional source evidence, required facts, expected behaviors, prohibited claims, notes, and risk/severity classification.
* Applicability, lifecycle status, version, authorship, review history, and approval metadata.

An item cannot become `Approved/Active` without a canonical answer and named Data Science/Product approval.

### 5. Simple Dataset Lifecycle and Versioning

* Support `Draft → In Review → Approved/Active → Retired`.
* Treat an approved dataset version as immutable for evaluation and export purposes.
* Changes to approved question text, canonical answers, applicability, or other decision-relevant content create a new draft version while preserving prior run and approval history.
* Permit only one current `Approved/Active` version for the same customer and experience dataset.

### 6. Agent Response Collection and Run Management

* Allow an authorized user to manually initiate a run against an approved dataset.
* Associate each run with customer, experience, dataset version, date/time, agent/application version when available, environment/configuration metadata when available, and initiator.
* Capture or ingest one agent response for each applicable case through an Engineering-selected execution path.
* Permit manual import or entry as an MVP fallback.
* Preserve each rerun as a distinct run. Do not automatically initiate a run when an agent or configuration changes.
* Provide run history without requiring automated regression orchestration.

### 7. LLM-as-Judge Critique

* Compare each agent response primarily with the approved canonical answer.
* Use supplementary evidence, facts, behaviors, and prohibitions when present.
* Produce a concise critique, recommended `Pass` or `Fail`, rationale, and confidence or uncertainty indicator.
* Identify missing, incorrect, contradictory, unsupported, or prohibited content when detected.
* Never make the final case, dataset, exception, or launch decision.

### 8. Human-in-the-Loop Review

* Present the question, canonical answer, agent response, supplementary guidance, and judge critique in one review context.
* Allow Data Science to record the final case result, rationale, notes, and disagreement with the judge.
* Allow Product to approve the dataset and accept a failed case as a documented exception based on customer input.
* Preserve the underlying failed result when an exception is accepted; an exception does not convert the case to `Pass`.
* Record approver, customer basis, mitigation or limitation, and revisit/expiry condition for each exception.

### 9. Scoring and Quality Bands

* The pass-rate denominator contains all `Applicable` cases in the approved dataset.
* Dataset approval requires a recorded result for every applicable case. Missing results cannot be omitted from the denominator.
* `Not applicable` and `Deferred` cases are excluded from the pass-rate denominator but remain visible in coverage reporting.
* Calculate quality status as:
  * **Pass:** at least 90% and no more than 100% of applicable cases pass.
  * **Warn:** at least 80% and less than 90% pass.
  * **Fail:** less than 80% pass.
* A critical accuracy, safety, grounding, or customer-data defect fails the individual case but does not automatically override the aggregate quality band.
* Product-approved exceptions remain failed cases in the score and appear separately in the confidence report.
* Show overall score, quality band, taxonomy-level results, applicability coverage, unresolved review count, and accepted exceptions.

### 10. Customer Confidence Outputs

Generate two versioned outputs for every Product-approved run:

1. **Executive confidence report:** Customer, experience, dataset/run versions, overall quality band, pass rate, taxonomy coverage, applicable/not-applicable/deferred counts, accepted exceptions, limitations, and approval evidence.
2. **Detailed evidence export:** Taxonomies, questions, ownership, canonical answers, agent responses, judge critiques, final human results, reviewer rationale, exceptions, source/version metadata, and lifecycle history needed to interpret the approved run.

Exports must distinguish platform-owned base questions from customer-owned additions and customer-specific data. Product controls which detailed fields are shared externally.

## Out-of-Scope

* Operational enablement of Member Chat, Member Inbound Voice, Outbound Voice, bundled experiences, or other channels; the MVP only preserves portability in the information model.
* Customer login, customer self-service review, or a customer-facing portal.
* Multi-turn scripts, conversational-memory evaluation, voice transcription quality, audio quality, or channel-specific latency evaluation.
* Automatic run initiation based on agent, prompt, model, configuration, code, or data changes.
* A mandated technical mechanism for invoking the agent; Engineering selects the execution/ingestion design.
* Automatic approval by LLM-as-judge or automatic acceptance of exceptions.
* Continuous production monitoring, drift detection, automated dataset healing, model retraining, or prompt optimization.
* Cross-customer reuse of customer-owned canonical answers, evidence, or review data.
* Replacing source-data validation, tenant isolation, security review, UAT, or production launch approval processes.

## Acceptance Examples

1. **Platform question reuse**Given a new CSR Chat customer workspace, when onboarding begins, then every current platform base question is loaded with platform ownership and must receive an applicability classification.
2. **Customer augmentation**Given a customer needs a question not present in the platform library, when Data Science adds it, then the question and its canonical answer are marked customer-owned and remain isolated from other customers.
3. **Canonical answer requirement**Given an applicable case lacks an approved canonical answer, when Product attempts to activate the dataset, then approval is blocked.
4. **Judge recommendation and human authority**Given the judge recommends `Pass`, when Data Science identifies a material conflict with the canonical answer, then Data Science can record `Fail`, explain the decision, and preserve the disagreement.
5. **Accepted exception**Given a case fails and the customer accepts a documented limitation, when Product accepts the exception, then the case remains failed in the score and the exception appears in both outputs.
6. **Applicability and scoring**Given 100 platform questions include 70 applicable, 20 not applicable, and 10 deferred cases, when all 70 applicable cases are evaluated and 63 pass, then the score is 90%, the quality band is `Pass`, and coverage still shows all 100 questions.
7. **Manual rerun**Given an approved dataset already has a completed run, when an authorized user manually initiates another run, then the new responses and decisions are stored as a separate run without changing the prior evidence.
8. **Portability contract**
   Given Product later defines a Member Chat experience, when its taxonomies and questions are configured, then the customer, ownership, lifecycle, case, run, decision, scoring, and export concepts do not require semantic redefinition.

## Exit Criteria

* [ ] CSR Chat is enabled as the reference experience, and portability fields exist without enabling another experience.
* [ ] A new customer workspace can be created for a rapid pilot or paying-customer engagement.
* [ ] Every platform base question is loaded and classified as applicable, not applicable, or deferred.
* [ ] Customer-added questions and all customer-specific data are marked customer-owned and isolated.
* [ ] Applicable cases cannot become approved/active without a canonical answer and required ownership/version metadata.
* [ ] Dataset lifecycle supports `Draft`, `In Review`, `Approved/Active`, and `Retired`, with immutable approved versions and preserved history.
* [ ] LLM-as-judge produces critique, rationale, confidence/uncertainty, and a pass/fail recommendation for every completed case.
* [ ] Data Science or Product can adjudicate each case and override the judge with recorded rationale.
* [ ] Product can accept a documented exception based on customer input without converting the failed case to pass.
* [ ] The system calculates `Pass`, `Warn`, and `Fail` using the approved thresholds and reports taxonomy and applicability coverage.
* [ ] Critical defects fail their cases but do not automatically override the aggregate band.
* [ ] Manual reruns preserve separate run results and prior approval evidence.
* [ ] Every Product-approved run generates an executive confidence report and detailed evidence export.
* [ ] Two representative CSR Chat customer onboardings and runs complete using the same workflow and data contract.
* [ ] Success-metric instrumentation records lifecycle time, completeness, judge recommendations, human decisions, disagreement resolution, and export generation.
* [ ] Internal access, customer isolation, retention, and export controls pass Security review with no unresolved high-severity findings.

---

Template: `Feature-1-Pager-PRD.md` `v2.0`

Feature PRD Skill: `v1.1`
