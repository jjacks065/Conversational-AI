# **Conversational AI for CSR Benefits Quoting**

###### UX Evaluation

User Experience Research & Design – April 2026

## Executive Summary

### Background

The Stellarus UX team was engaged to conduct a comprehensive UI/UX evaluation of Mira, a conversational AI benefits‑quoting tool embedded within the Nexus platform. The objective of this work was to identify usability friction, workflow gaps, and design opportunities that impact clarity, efficiency, and trust during live agent interactions.

To inform rollout readiness and scaling decisions, the evaluation combined in‑product UI review with moderated feedback sessions and a focus group of early‑access agents. This report synthesizes those findings to highlight where Mira is delivering clear value today and where UX execution currently limits its ability to be used reliably and confidently at scale.

### Key Insights

* Mira’s core value is recognized. Agents report improved efficiency, clearer explanations, better documentation, and increased confidence compared to legacy workflows.
* UX execution limits effectiveness in live use. Agents must interpret dense responses, manage system uncertainty, and work around UI limitations during calls.
* Adoption risk is driven by UX, not AI capability. Issues related to control, context, system feedback, and recovery reduce trust and increase reliance on legacy tools under pressure.

### Recommendations and Next Steps

* Address P0 UX risks before scaling Mira more broadly—particularly issues tied to agent control, context preservation, and system feedback during live calls.
* Reduce cognitive and compliance burden through clear response hierarchy and scoping required vs contextual information.
* Sequence P1 and P2 improvements intentionally once core risks are mitigated.

## Context

###### Problem, Value, and Adoption Constraints

Today’s benefits lookup workflow is fragmented, manual, and cognitively demanding. Mira’s value lies in its ability to collapse a complex, multi‑step workflow into a simple ask‑and‑answer experience that agents can confidently use during live calls.

##### Today’s Experience

1. Interpret what the member is asking
2. Translate into system categories
3. Navigate through click‑downs
4. Locate information across sections
5. Synthesize fragmented details
6. Translate into member‑friendly language
7. Share with member

##### Future Experience with Mira

1. Query Mira in natural language
2. Receive synthesized response
3. Share with member

##### **Early feedback shows**

**Mira delivers tangible value for agents, improving speed, clarity, and agent confidence.**

###### Ease of Use and Efficiency Gains

“It’s faster instead of having to scroll down all the different topics… you ask it and it just populates.”

“Having that tool to search makes our calls a lot easier.”

“It’s accessible… easy to access when opening the benefit lookup guide.”

“It’s easier and faster compared to the traditional way.”

###### Documentation and Audit Support

“We can copy it and paste it into our notes… so we’re not missing anything when we’re documenting our calls.”

“That’s a good benefit of Mira for our notes… to cover ourselves if we get audited.”

“They always want to know, if we get audited, where did we get that information from.”

###### Agent Confidence and Member Clarity

“By utilizing this tool, I feel like I’ve also as an agent felt more confident.”

“The way Mira has explained it, they’re [the member] able to be like, ‘oh, aha, I get it.’”

“It honestly kind of educates us a little bit more too on the benefits.”

##### Core UX Challenges

1. Output Not Optimized for Live Delivery
2. Dense responses are difficult to parse in real time
3. Increased risk of mis‑quoting in‑network vs out‑of‑network benefits

##### Workflow Integration Gaps

1. Mira obscures underlying Nexus content
2. Agents frequently switch back and forth for verification
3. Latency and Unclear System Feedback
4. Response delays create awkward silence on calls
5. No indication of progress, duration, or system state

### Full‑Screen UI Evaluation

##### High‑Level Interface Risks

Current UI design patterns increase cognitive load and reduce agent control during live calls:

1. Low‑contrast text reduces scannability and introduces accessibility risk
2. Unclear whether suggested prompts are editable before submission
3. “Brief Answer” lacks trust or compliance signaling
4. Documentation‑style layouts in a conversational context
5. Degraded readability across window states
6. Inconsistent timestamp behavior
7. Low discoverability of audit‑critical citations
8. Disruptive auto‑scroll behavior during response growth
9. Silent loading states
10. No way to stop or cancel an in‑progress response

##### Detailed UX Findings – Screen‑by‑Screen

**Full‑Screen Launch Obscures Context (High Severity)**
Why this matters: Agents operate under time pressure and rely on speed, familiarity, and parallel workflows. A full‑screen takeover assumes immediate trust and disrupts spatial continuity.

**User Feedback:**

> “I’d prefer to go back to how you had it a moment ago, so I could be looking [in Nexus] while I’m waiting.”

**Design Recommendation:**

1. Remove full‑screen launch as default
2. Use non‑modal, contextual panel

**Fixed Right‑Docked Chat Prevents Side‑by‑Side Verification (Medium Severity)**
Why this matters: Verification is required behavior in audited environments. Fixed placement blocks benefit fields and prevents trust‑building workflows.

**Design Recommendation:**

1. Enable movable panel
2. Allow flexible, resizable width

**AI Loading State Lacks Visibility, Predictability, and Control (High Severity)**
Why this matters: Silent loading shifts uncertainty onto agents, increasing call friction and reducing trust.

**Design Recommendations:**

1. Replace skeleton bars with labeled system states
2. Indicate anticipated wait or progress
3. Allow cancel, rephrase, or fallback actions during processing

**AI Responses Overload Agents with Unscoped Multi‑Path Information (High Severity)**

**Issues Identified:**

1. Required vs contextual information not distinguished
2. INN and OON paths interwoven
3. No disclosure hierarchy
4. Visual emphasis competes for attention

**Design Recommendations:**

1. Introduce explicit information hierarchy: Required disclosures (audit‑complete script)
2. Contextual explanation
3. Optional or situational details
4. Default to progressive disclosure
5. Scope responses to confirmed member intent

**Error Responses Fail to Support Recovery (High Severity)**

**Heuristic Violations:**

1. Help users recognize and recover from errors
2. Visibility of system status
3. Trust and predictability

**Design Recommendations:**

1. Replace generic errors with diagnostic states
2. Preserve prompt context
3. Offer guided recovery options

### CASTLE Assessment Framework

**Summary**

| C<br />Cognitive Load                                                                                                                                                              | A<br />Advanced Feature Usage                                                                                                                      | S<br />Satisfaction                                                                            | T<br />Task Efficiency                                                                                       |                                        L<br />Learnability                                        |                                E<br />Errors                                |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- | :-----------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------: |
| Level of mental effort<br />required to complete<br />key tasks                                                                                                                     | Adoption of advanced<br />features to ensure <br />maximum product value                                                                           | How users feel about<br />using the product                                                    | How quickly users can<br />successfully complete <br />key workflows                                         | Effort , time, and resources<br />needed for a user to effectively <br />learn to use the product | Level of successful task<br />completion, or speed of <br />error resolution |
| High                                                                                                                                                                                | Under Leveraged                                                                                                                                    | Moderate                                                                                       | Poor                                                                                                         |                                           Medium Effort                                           |                             Difficult Resolution                             |
| 3                                                                                                                                                                                   | 3                                                                                                                                                  | 2                                                                                              | 3                                                                                                            |                                                 2                                                 |                                      3                                      |
| The interface imposes<br />excessive cognitive load by <br />presenting dense, multi‑path <br />responses without no clear <br />hierarchy, scoping, or <br />disclosure priority. | Advanced system cap abilities<br />(AI context awareness, structured <br />responses) exist but are not <br />surfaced in us able ways for agents. | Agents see clear value in<br />Mira but express caution <br />and hesitation in call scenarios | Basic usage is approachable,<br />but expert‑level, audit‑safe <br />usage is not obvious through the U I. |                                                                                                  |                                                                              |
| Agents must actively decide what<br />to vs . not to say.                                                                                                                           | No system‑driven signaling for<br />required disclosures.                                                                                         | Repeated “trust but verify” behavior                                                         | Users must learn how best<br />to ask questions : “Gym vs gym <br />membership gives different results .”  |                                                                                                  |                                                                              |
|                                                                                                                                                                                     | Source metadata is displayed but not<br />deep linked for quick action.                                                                            | Frust ration appears when<br />responses are verbose, <br />ambiguous , or slow.               |                                                                                                              |                                                                                                  |                                                                              |

**1** - Good | **2** - Fair | **3** - Poor 

*Overall Score: 16 / 18*

### Design Recommendations by Priority

| Priority | Problem(Context)                                                                                                     | Design Recommendations                                                                     | Impact                                                                                     | Evidence                                                                                                                                               |
| -------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| P0       | Full‑screen takeover disrupts context at start of live call and slows re‑orientation.                              | Default Mira to non‑modal / non‑full‑screen launch                                      | Faster ramp into task; reduces early abandonment to legacy workflows; improves adoption.   | “I’d prefer to go back to how you had it a moment ago, so I could perhaps be looking… while I’m waiting…”                                        |
| P0       | Silent skeleton bars provide no meaningful system status.                                                            | Explicit loading state labels                                                              | Reduces member-facing dead air; improves trust & pacing.                                   | “I’ve had members like, ‘ are you still there ? ’… it does take a bit of time.”                                                                  |
| P0       | A gents can’t predict latency; compensates by switching tools.                                                      | Progress or timing hints                                                                   | Less tool switching; fewer redundant lookups and re-asks.                                  | “I’m like waiting and waiting for it to respond.”                                                                                                   |
| P0       | While loading, the only available action is sending another message; agents can’t interrupt a bad query.            | Stop / Cancel control during generation                                                    | Prevents runaway waits; reduces confusion; preserves agent control.                        | A gents describe waiting and managing silence (“are you still there ? ”) which is worsened when they can’t intervene.                               |
| P0       | A gents must decide what to say vs. skip; risk of audit failure.                                                     | tandard response hierarchy: Required / Context / Optional                                  | Reduces compliance risk; increases clarity; lowers cognitive load.                         | “In lieu of the ‘ brief answer,’ I would ideally hope that it would have the like correct scripting for how we ' resupposed to q uote the benefit” |
| P1       | Fixed placement blocks key benefit fields and prevents side-by-side verification.                                    | Enable movable panel (drag to reposition)                                                  | Supports “trust‑but‑verify” workflow; reduces misquotes; improves confidence.          | “I was… hoping… we’d be able to kind of move it around the screen… but it stays on the right side.”                                              |
| P1       | Narrow view creates long vertical blocks; wide view creates long line length; both harm scanability.                 | Enable resizable width (and remember preference)                                           | Faster scanning; lower fatigue; fewer reading errors.                                      | “If it’s taking a second to load… I’ll minimize the box…” (workflow suggests frequent resizing/space management)                                 |
| P1       | Sources hidden behind low-aff ordance “Expand T able” can be missed; agents need audit confidence without clutter. | Sources & citations : collapsible section with strong aff ordance                          | Improves trust + audit support; reduces visual noise during live calls.                    | “They always want to know… if we get audited, where did we get that information from?”                                                              |
| P1       | Mira shows agents where information comes from , but does not support real‑time verification actions.               | Make citations actionable via deep links to Nexus sections                                 | Reduces manual navigation and supports “trust but verify” behavior without slowing calls | “I still want to verify… I can’t help but to just double check.”                                                                                   |
| P1       | Mixed INN/OON details increase confusion and misquoting risk.                                                        | Separate INN vs OON into distinct visual blocks (cards/tabs/accordion)                     | Reduces compliance risk , improve scannability; fewer wrong-path readouts.                 | “Worried like, oh, did I… accidentally giving… out of network… instead of in-network.”                                                            |
| P1       | Current errors are generic and stop task completion.                                                                 | Error states become diagnostic + guided recovery ( 2 + suggested next steps)               | Lower abandonment; fewer escalations; improved trust.                                      | Focus group : agents discuss waiting and needing workflows; error recovery complements these issues.                                                   |
| P2       | “Message Mira” doesn’t guide what to ask; weak onboarding and recovery affordance.                                | Improve placeholder microcopy (task-oriented, supportive)                                  | Reduces hesitation; improves learnability and query quality.                               | “I might not necessarily know if the way I'm entering a question is a way that the system's going to Really recognize.”                              |
| P2       | Suggested prompts are prominent but may not feel adaptable; agents may avoid using them.                             | Prompt guidance + editability clarity (prompt chips editable before send)                  | Improves adoption of prompts; reduces malformed queries.                                   | “I usually will ask… including the deductibles and max out of pocket …” (agents tailor prompts)                                                    |
| P2       | Content drops agents to bo tt om during response growth; agents must manually scroll back to find start.             | Auto-scroll behavior : preserve orientation (anchor to top / “Jump to top”)              | Faster comprehension; less re-orientation; fewer missed details.                           | Agents already describe switching and waiting behaviors; orientation loss compounds this.                                                              |
| P2       | Some users don’t notice resize / collapse affordances; assume they must “exit” to see underlying system.          | Make panel expansion / collapse controls discoverable (tooltip/label/first‑run coachmark) | Reduces friction & training burden; speeds adoption.                                       | “I didn’t know that li tt le arrow feature… I thought I had to exit out of the whole thing…”                                                      |
| P2       | Low contrast and over-bolding reduce scanability; can introduce accessibility risk.                                  | Accessibility polish : contrast + semantic emphasis                                        | Faster scanning; reduced fatigue; fewer missed qualifiers.                                 | A gents cite difficulty “sifting” and confusion; improved visual semantics reduce burden.                                                            |
