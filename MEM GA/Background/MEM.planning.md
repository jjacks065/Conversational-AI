These are the meeting notes from 3 planning sessions from March 9-12, 2026. 

**3/9/26**

Decisions

* Reach
  out to missing stakeholders for comprehensive representation.
* Use
  Nexus as primary data source and centralize for scalability.
* Prioritize
  Core and Premier lines for chatbot rollout.
* Limit
  personalization to name and plan info, avoid demographics.
* Set
  up distinct environments for development, QA, testing, and production.
* Store
  full transcripts for at least seven years for compliance.

Open questions

* Finalizing
  required participants remains open due to identified gaps.
* Sourcing
  customizations and specialty benefits outside Nexus remains unresolved.
* Training
  generative agents across lines of business needs clarification.
* Prioritizing
  claims and billing earlier remains under consideration.
* Aligning
  with voice agent team may affect rollout sequence.
* Ensuring
  bias avoidance with user-provided demographics needs further safeguards.
* Error
  handling and escalation approach for integration failures needs
  finalization.

Agenda

Goal:
Review and align on high level requirements, solution design, engagement model,
and plans for the Sierra project

Meeting notes

Meeting logistics

* SriLakshmi
  confirmed that all meetings will be recorded and the meeting notes will be
  posted via email and SharePoint.
* Julie
  suggested starting the meeting and proposed quick introductions for new
  participants, including Chance, Jay, and Brenna.

Attendance and scheduling

* Dineshwar
  informed the group about their scheduling conflict and that Chendra is on
  PTO today.

Project team introductions

* SriLakshmi
  confirmed that they will manage the AI chatbot implementation project for
  Blue Shield and introduced the project team members and their roles.
* Simi
  joined the meeting and shared their experience managing eligibility and
  benefits on the portal and app for Blue Shield.

Meeting attendance and support

* Brenna
  stated that they will be available for the first half of the meeting to
  support specific questions related to Sierra.

Stakeholder engagement

* Julie
  discussed the importance of including customer experience and Nexus team
  members in requirements review sessions to ensure all perspectives are
  covered.
* Kathleen
  stated that Blue Shield is working to align with partners on the voice
  agent strategy and is engaging with their leadership team to synchronize
  efforts.

Chatbot architecture

* Julie
  raised the need to clarify whether the chatbot will use a single engine
  for all benefits use cases or separate solutions for different scenarios.
* Rajat
  presented a high-level architecture slide to the product team, inspired by
  previous technical discussions, to socialize the chatbot's design.
* Rajat
  presented a high-level architecture slide to the product team to socialize
  the chatbot's design, confirming the architecture aligns with previous
  technical discussions.

Team participation

* SriLakshmi
  confirmed that Bradley and Chelsea from the UX team are invited to the
  meetings to support product design discussions.

Data management

* Richie
  and Dineshwar discussed the importance of building a centralized
  repository for benefits data to support chatbot scalability and coverage.
* Dineshwar
  recommended involving the enterprise architecture team to review all data
  sources and develop a comprehensive data strategy for the chatbot project.

Chatbot roadmap

* Rajat
  outlined the phased approach for the chatbot, starting with foundational
  benefits and eligibility questions in 2026, then expanding to additional
  skills and actions in later years.

Chatbot scalability

* Richie
  and Rajat discussed that expanding the chatbot across different lines of
  business requires more effort than adding new skills within a single line
  of business, due to unique training needs.

Feature integration

* Rajat
  stated that the symptom checker feature will be provided by Ada Health and
  will be part of a separate guided navigation experience, not included in
  the chatbot this year.

Chatbot rollout strategy

* Rajat
  explained that claims, billing, and payments questions require extremely
  high accuracy due to their financial impact, so the team plans to first
  launch basic chatbot skills before expanding to these complex areas.
* Rajat
  explained that the initial chatbot rollout will focus on Blue Shield
  employees, with Core and Premier lines of business prioritized due to
  their importance for company growth and sales cycles.

Data integration and training

* Richie
  clarified that connecting to Nexus provides access to plan documents, but
  the chatbot must be individually trained for each line of business, as
  Nexus is only a repository and does not offer conversational relevance.

Data management and sources

* Rajat
  confirmed that desktop procedures are sourced from SharePoint and the
  portal, but there is no official repository, and updates may not always be
  synchronized with Nexus; the team will connect directly to Nexus for
  benefits and eligibility data.
* Kathleen
  clarified that Core and Premier lines require special attention because
  many customizations and buy-ups are stored in Facets, not Nexus, creating
  an additional requirement for chatbot integration.

Chatbot training strategy

* Chance
  explained that training a generative agent for a new line of business may
  require significant effort depending on data structure and overlap, and
  that training on the most complex line does not always cover simpler ones.
* Richie
  and Rajat discussed that live agents use desktop procedures and Facets to
  access customizations, and the chatbot will need to replicate this process
  to retrieve both procedural guidance and fixed data.

Chatbot maintenance

* Chance
  clarified that the generative agent requires ongoing tuning after initial
  training to prevent model drift, and cannot be set and forgotten.

Data sources for chatbot

* Rajat
  confirmed that about 80% of benefits and eligibility data is available in
  Nexus as structured JSON, while the remaining data may require working
  with PDFs.

AI architecture overview

* Chance
  described the differences between deterministic bots, generative agents,
  and fully agentic AI, and clarified that the current project uses a
  generative agent for multi-channel interactions.
* Chance
  explained that the generative agent used for Sierra with FEP is not
  deterministic except for specific transfer flows, and it autonomously
  creates responses within defined guardrails.
* Chance
  clarified that the generative agent can vary its wording for responses,
  but always aims to provide factual and contextually relevant information,
  especially for benefits and eligibility scenarios.
* Chance
  described that guardrails can be set to ensure required components, such
  as co-pay, co-insurance, and restrictions, are always quoted together in
  responses for benefits questions.

Chatbot rollout and skills

* Rajat
  confirmed the plan to cover all lines of business for benefits and
  eligibility queries by Q1 next year, with the possibility of adding more
  skills before Q1 2027 if feasible.
* Richie
  explained that once a solution is built for one channel, adapting it to
  other channels requires only about a 20% additional effort, supporting a
  cross-channel approach.

Agentic ecosystem strategy

* Chance
  explained that the agentic ecosystem aims to integrate data, knowledge,
  and interaction layers, enabling seamless omnichannel experiences and
  continuity between chatbot and human agent interactions.

Platform environments

* SriLakshmi
  asked if the platform will have separate environments for development, QA,
  performance testing, and production, and Julie confirmed that these
  environments will be established.

Data sources and coverage

* Rajat
  confirmed that 80% of plan data is available in Nexus, but network-wise
  plan data and Medicare Advantage are still sourced from WPR.

Chatbot functionality

* Rajat
  explained that the chatbot will initially provide authenticated
  experiences for members, answering coverage and visibility queries and
  educational questions about plan terminology.

Chatbot personalization

* Rajat
  and Chance discussed that the chatbot will provide authenticated
  experiences, allowing personalized responses using member name and basic
  plan information, but recommended limiting demographic personalization to
  avoid bias.
* Chance
  explained that large language models currently lack robust guardrails for
  bias, so the team should avoid including sensitive demographic data in
  chatbot responses until market solutions improve.
* Chance
  explained that the chatbot will provide minimal personalization at launch,
  using only member name and journey data, and will avoid demographic-based
  personalization to reduce bias.
* Simi
  clarified that the chatbot can tailor responses based on whether a member
  is new or historical, adjusting the level of detail accordingly.
* Chance
  confirmed that for age-related benefits, the chatbot will reference
  general guidelines and not make assumptions about the member's age,
  ensuring unbiased responses.

Chatbot access controls

* Simi
  and Chance discussed that the chatbot will enforce access controls for
  dependent-related questions, only providing information if the member has
  the appropriate profile delegation.
* Chance
  clarified that multi-subscriber access and provider authentication require
  further tuning to ensure proper access controls in the chatbot.

Chatbot response design

* Rajat
  confirmed that linking to relevant documents in chatbot responses is
  beneficial, allowing members to access detailed information directly.
* Chance
  described that empathy in chatbot responses can be configured through
  instructions, allowing the agent to acknowledge sensitive topics like
  diagnoses without retaining personal details.

Chatbot training and requirements

* Chance
  explained that broad exception questions are difficult for the chatbot to
  answer and require human intervention or specific guidelines.
* Rajat
  and Chance discussed that eligibility inquiries should include coverage
  explanations, start and end dates, and ID-related information.

Chatbot maintenance and tuning

* Chance
  explained that tuning the generative agent is an ongoing process, where
  outlier scenarios are addressed as they arise during real conversations,
  and the agent is adjusted to prevent drift and ensure accurate responses.

Chatbot training and project methodology

* Chance
  described the FEP project approach, outlining three main stages: initial
  training using brochure content, establishing guardrails and rules, and
  ongoing tuning based on real conversation recordings to capture nuances
  and improve agent responses.

Chatbot management and testing

* Chance
  clarified that managing a generative agent does not involve prompt
  engineering, but instead relies on policies, rules, and base content, with
  testing and user acceptance processes differing significantly from
  traditional software releases.

Testing and monitoring

* Chance
  explained that the testing process for the generative agent includes
  simulation, regression simulation, and a unique UAT approach, followed by
  ongoing business monitoring and feedback similar to live agent audits.

Training data and requirements

* Chance
  clarified that providing a limited number of real transcripts or
  role-played conversations can help model complex or ambiguous requirements
  for the chatbot, but thousands are not needed.
* Simi
  confirmed that generic plan exclusions are already configured and asked
  for clarification on what exceptions or ambiguous cases need to be modeled
  in JIRA stories.
* Chance
  stated that the team will identify which requirements need additional
  modeling or clarification during release planning, and may request more
  information or modeled examples for ambiguous stories.

Chatbot data privacy and bias

* Chance
  explained that the generative agent does not store or reuse demographic or
  personal information provided by members during conversations, ensuring
  responses are not biased by user-supplied data.

Chatbot monitoring and QA

* Chance
  and Simi discussed that there is currently no formal QA process for
  chatbot transcripts, but monitoring and tuning are performed in other
  environments to detect and address potential bias or drift.

AI architecture and model management

* Chance
  explained that the generative agent uses a constellation of 10-12 large
  language models, including a critic agent for fact-checking and contextual
  relevance, and that hallucination mitigation techniques are applied during
  training and tuning.

Client requirements and customization

* Rajat
  raised a new requirement that some clients may want to influence which
  large language model is used for their members, and the team discussed the
  need to address this customization in future releases.
* Gaurav
  suggested taking the discussion about client-specific model selection
  offline, as it is not part of the day one release but will be considered
  for later customization.

Client-specific model customization

* The
  team discussed a new requirement from certain clients to influence which
  large language model is used for their members, but decided to address
  this customization in future releases after further discussions with the
  market team and clients.

Safety and escalation protocols

* Chance
  explained that safety instructions, such as advising users to call 911
  during medical emergencies, are enforced as hard guardrails in the
  chatbot, and escalation to a human is required for high-risk intents like
  self-harm.
* Tarun
  confirmed that safety, advice, and escalation protocols will be managed
  through rules and policies, with some controls inherent in the AI models
  and others set as explicit rules for specific clients like healthcare.

Chatbot voice and presentation options

* Chance
  clarified that the Sierra chatbot supports both text and verbal
  interactions, and the presentation layer for voice features depends on how
  the team integrates it into the web portal or other platforms.

Language support

* Chance
  explained that English and Spanish are available for chatbot deployment,
  with additional languages like Russian and Mandarin in development and
  prioritization based on business needs.

Chatbot configuration

* Chance
  clarified that chatbot tone, voice, and response timing are configurable
  and can be adjusted through regular tuning or immediate configuration
  changes if needed.

Human escalation and integration

* Chance
  stated that warm transfer with context is supported across channels via
  Genesis, and the Genesis team will determine what information is
  transferred during handoff.

Data retention and compliance

* Julie
  stated that HIPAA regulations likely require storing chat transcripts for
  seven years, but will confirm the exact retention period.

Reporting and analytics

* Chance
  explained that Sierra provides built-in reporting and analytics, including
  intent topics and outcome conversions, and offered to walk the team
  through available reporting features.

**3/11/26**

Decisions

* Use Nexus JSON as primary data source; fallback to PDFs/web pages as needed.
* Stage integration of accumulators/claims as future enhancements, not in initial launch.
* Share sample benefit stories with Stellaris for review and refine based on feedback.
* Create a centralized reference epic to organize and link all project documents.
* Have UX team present requirements to Stellaris, following product requirements model.
* Rely on product team to bring in marketing/brand stakeholders for tone configuration.

# Open questions

* Determine data refresh frequency for chatbot; real-time vs cached not finalized.
* Choose GA structure (by LOB, skill, or master); decision pending.
* Balance explicit documentation and reliance on source data; validation scenarios are needed.
* Determine when to write LOB-specific stories based on structural differences; no final conclusion.
* Define scalable validation methods for chatbot accuracy; automation options to be finalized.
* Decide how to involve subject matter experts in requirements and validation; process undecided.
* Define coordination process for UX requirements and validation between teams.

# Agenda

Goal: Achieve alignment on high level requirements, solution design, plan, and engagement model for the Sierra project

# Meeting notes

### Team locations and visits

* Chance mentioned plans to visit Southern California and possibly meet with Julie and a conversational designer who works on Sierra.
* Debbie and Julie discussed meeting up if anyone visits the EDH office in the Sacramento area.

### Benefit stories

* Simi presented benefit stories and requested feedback from the team, emphasizing the need to avoid unnecessary detail since the bot will use plan documents as the main reference.
* Chance highlighted the importance of identifying multiple plans within documents and handling footnotes accurately during planning sessions.

### Requirements and roles

* Julie explained that business requirements will be provided by Simi, and Julie will write the engineering stories, including both business needs and technical implementation details.
* Julie stated that engineering stories will be managed in Linear, and Stellaris will have access, but others may need to review them via meetings or screen sharing.
* Julie asked whether the initial launch for Blue Shield employees should include vision and dental benefits or only medical, and the team agreed to confirm the scope internally.

### Data sources and formats

* Rajat shared that most benefit data is stored in Nexus as JSON files, with some exceptions requiring PDFs or alternative sources.
* Rajat demonstrated the structure and scope of benefit data in Nexus, including lines of business and product types, and explained that JSON files are always up to date as the system of record.
* The team discussed the scope of vendor-managed dental and vision products, clarifying that these are not stored as JSON files in the backend and are displayed on the portal.

### Requirements gathering

* Chance discussed the need to test sample JSON files in their environment to identify any issues and ensure requirements are complete.
* The team discussed that most plans are updated annually, but some products and customizations may change throughout the year, affecting the JSON files representing products.
* Simi described creating sample benefit stories using real member questions and plan documents, and invited feedback from Chance and Julie on the approach and story structure
* Simi described structuring benefit stories using real member scenarios and responses based on EOC content, with data stored in Nexus for specific products.
* Julie suggested including the data source in benefit stories to enhance clarity.

### Testing and validation

* Chance explained the simulation and QA process used for validating agent responses, including role-playing and automated answer checking
* Chance described the simulation and QA process for validating agent responses, including role-playing, multiple simulation runs, and grading by a separate LLM before advancing to the next development stage.
* Chance explained that a manual simulation tool is available to test scenarios in the current production environment without impacting it, allowing the team to validate how questions are handled.

### Benefit calculation logic

* Chance and Simi discussed the risks and considerations of using user-provided input to calculate remaining benefit limits, emphasizing the need for clear disclosure if this approach is used.

### Model tuning and adaptation

* Chance explained the ongoing need to tune and adapt the model to prevent drift, especially as conversation patterns change, and highlighted the importance of designing specific instructions for Medicare and Medicaid interactions.

### Benefit data sources

* Simi explained that benefit data for specific products is stored in Nexus, and some language or copy may be sourced from EOC PDFs if not available in Nexus.
* David suggested including the data source (such as Nexus, DLPs, or PDFs) in benefit stories, and Simi agreed to double check and map where each piece of information is written from.
* Chendra clarified that benefit limits are defined in Nexus as part of product configuration, while member utilization (accumulators) is stored separately in Facets and displayed on the portal.
* Chendra clarified that accumulators, such as real-time utilization, are not included in plan documents and require separate consideration from benefit limits.
* Simi confirmed that Med Supp benefit information and related visuals will be sourced from Nexus and plan documents, and offered to include screenshots or product IDs for clarity.

### Feature release planning

* Chance explained that accumulations and billing complexities will be staged as feature releases after initial plan launch to avoid a "Big Bang" rollout.

### Benefit story scenarios

* Simi presented three sample stories focused on cost shares, highlighting their importance and the need to cover various scenarios such as medical encounters and bundled services.
* Simi presented a new benefit story structure focused on grouping common member questions by category, such as deductibles, providers, and wellness benefits, and requested feedback from the team.
* Simi decided to use a hybrid approach for benefit stories, combining service-specific and frequently asked member questions to address areas of confusion like annual health exams.

### Requirements and use case detail

* Chendra discussed the necessity of detailing use cases for procedures like knee replacement, emphasizing the involvement of multiple services and backend tools like treatment cost estimators.

### Backend data sources and rollout

* The team discussed that backend data sources for the initial phase have not been finalized, and the first group to be supported will be employees, with expansion to other lines of business planned later.
* Julie clarified that claims and transaction-level data will not be included in the initial launch, and Rajat confirmed that claims integration is planned for a future phase after facets system updates.

### Requirements and benefit story detail

* Simi and the team discussed the need to determine the appropriate level of detail to include in benefit stories, especially for complex scenarios like hospitalizations, and agreed to refine this as requirements are developed.
* Rajat raised the question of how much product and cost nuance needs to be explicitly documented in stories, given that plan documents serve as the ground truth across different lines of business.

### Benefit story structure

* David explained that benefit stories should focus on structural differences between plan types, such as HMO, PPO, or tiered benefits, rather than minor details like copay amounts.
* Simi and the team discussed that line-of-business-specific scenarios should be written only when the benefit structure is fundamentally different and may impact tool logic or inference.
* Simi described the structural differences in Med Supp benefit stories, emphasizing the need to check multiple deductibles and highlight unique perks such as hearing aid discounts and wellness programs.

### Backend data integration

* Rajat discussed the availability of an API from Nexus to return Med Supp JSON files and raised the question of whether these should be pulled in real time or cached for use.

### Benefit data integration

* Chance explained that the GA can be structured to control how benefit data is loaded and updated, including options for real-time or cached data from Nexus, and the ability to set update frequencies such as hourly, monthly, or annually.

### System versioning and rollback

* Chance confirmed that Sierra supports versioning for knowledge, conversational changes, and configuration, allowing the team to revert to previous versions if needed.
* Chance explained that Sierra supports versioning for knowledge, conversational changes, and configuration, allowing the team to revert to previous versions if needed.

### Platform flexibility and language support

* Chance described that Sierra's platform allows flexible configuration of tone, language, and conversational identity, with options for multiple languages and customizable AI personas.
* David mentioned that priority languages for Medicare and medical can be provided to guide future language support planning.

### Platform roadmap and updates

* Chance explained that Sierra currently supports multiple languages, including English and Spanish, and has a roadmap for expanding to additional languages and dialects
* Chance described that Sierra's language auto-detection feature is not yet available but is planned for a future release

### System demonstration

* Chance agreed to provide a tutorial session next week to demonstrate the FEB system in action, including a walkthrough in chat and visuals of its setup, followed by Q&A.
* Julie sent out a meeting invite for a high-level Sierra demo for the BSC leadership team and mentioned a separate, more detailed session will be scheduled for the team to review technical setup.

### Brand identity and configuration

* Chance explained that the conversational agent's brand identity, tone, and language style are configured separately for chat and voice, and input from the team will be used to shape these aspects with support from Martha.

### Brand identity and stakeholder coordination

* Julie explained that the team will rely on Debbie's group to bring in the appropriate marketing contacts for brand and tone discussions, and suggested listing these people on the RACI to ensure no one is missed.

### Project documentation and playbook

* Julie stated that a playbook is being developed, using previous FEP work as a reference, to guide this team and others in future projects.

### Project documentation

* Simi agreed to create a reference documentation epic to organize shared documents and resources for the team.

### Benefit story sharing

* Rajat confirmed that all sample benefit stories will be shared with Chance and the larger team by the end of the day.

### Work organization

* Debbie raised concerns about the limitations of using BPRs for organizing work at Blue Shield and suggested revisiting the possibility of having a dedicated BPR for the benefits chatbot.
* Julie acknowledged the need to learn and adapt to the new process for managing epics and work tracking at Blue Shield.

### Work tracking and tools

* Julie agreed to share resources explaining Linear terminology and methods to help the team align on work tracking language

### Project planning

* Julie planned to review current requirements and objectives, clarify success metrics, and prepare discussion points for the next session

### Technical integration

* Julie stated that technical integration and architecture discussions for Sierra will be handled in a separate Stellaris engineering kickoff, with possible updates to the broader team

### Knowledge sharing

* Chance offered to share their published articles and an upcoming GOAT CX series to help the team understand AI concepts, use cases, and testing approaches.
* Chance offered to send their published magazine article on the importance of the voice channel to the team.

### Project priorities

* Debbie explained the urgency for their team to deliver an accurate and live member benefits experience, highlighting different pressures and goals compared to Rajat's team.

### Requirements handoff

* Julie confirmed that the engineering team will write UX requirements but will collaborate with the UX team for input and validation.
* Debbie suggested inviting Rand and Kamal as guest participants during story writing to help identify benefit nuances and potential issues.




**3/12/26**

Open questions

* Review
  timing for BSC and UX requirements is pending internal meetings.
* EA
  blueprint and solution design timeline is pending technical kickoff.
* Environment
  setup timelines are not planned; roadmaps are pending.
* Next
  steps after handoff to Stellaris are unclear; engagement model needs
  clarification.

Agenda

Meeting notes

Project documentation

* Julie
  stated they may not be able to review Rajat's email today due to a busy
  schedule.

Requirements review

* SriLakshmi
  explained that BSC and UX teams need to meet internally to review
  requirements before providing feedback.

Engagement process

* Julie
  and SriLakshmi discussed the need for clarity on the engagement model and
  next steps after handing off epics and requirements to Stellaris.

Architecture and solution design

* Julie
  stated that timelines for the EA blueprint and solution design are not yet
  available and will be determined after a technical kickoff with the team.

Project environment setup

* Julie
  explained that environment setup timelines for development, QA,
  performance testing, and production are pending coordination with the
  engineering team and will be shared once planned.

Service model distinctions

* Greg
  explained that Core and Premier plans require separate service models,
  including concierge and clinical elements, and must be handled by
  dedicated teams due to their complexity.
* Greg
  described that ASO Connect buyers receive a dedicated service model, and
  Blue Shield does not provide member servicing for Shared Advantage, which
  manages its own contact center.

AI automation and expertise sharing

* Greg
  described ongoing work using generative AI to automate benefit quotes for
  IFP, highlighting Heather White's involvement and the potential to
  leverage this expertise for the current project.

Readiness and support planning

* Greg
  explained that Candice Markham's team is responsible for readiness
  activities, including process adjustments, training, communication, and
  post-launch support for changes impacting CE, and confirmed these plans
  apply to the current initiative.

Privacy and security coordination

* Julie
  and Debbie discussed the importance of involving privacy and security
  teams early in the project to ensure smooth sign-off and avoid issues
  before launch.

Engagement model and meeting cadence

* Julie,
  Rajat, SriLakshmi, and the team agreed to hold more frequent meetings—at
  least twice a week—during the initial requirements gathering phase, with
  the possibility of increasing to daily check-ins if needed.

Project planning and best practices

* Debbie
  suggested reviewing previous Blue Shield projects with high data
  sensitivity to inform the current project's playbook and ensure best
  practices are followed.

Governance and compliance

* Julie
  discussed the need to initiate the Blue Shield and Stellaris governance
  processes soon, noting that Mike Beck may assist based on his recent
  experience with Minerva.

Quality assurance involvement

* Debbie
  and Simi discussed the involvement of the QA lead, Kumal, highlighting
  their strong expertise and the importance of determining the appropriate
  forum for QA participation in requirements and technical discussions.

Project planning and leadership alignment

* SriLakshmi
  explained the need to align on leadership sign-offs for requirements,
  architecture, solution design, product demos, and release planning, and
  confirmed plans to set up separate sign-off meetings for leadership from
  both Stellaris and BSC.

Project planning

* Debbie
  discussed the importance of defining clear project goals for the year and
  suggested working backwards from the desired December launch date.
* Rajat
  explained the target for this year is to deliver benefit coding for IFP,
  small business, core premier, and employee plans, with the possibility of
  including accumulator limits if technical constraints allow.
* Greg
  emphasized the importance of aligning project timelines with operations
  and support requirements to avoid launching during peak periods and ensure
  adequate subject matter expert involvement.
* Julie
  and SriLakshmi discussed the need to prepare a high-level project plan
  with tentative dates to assess the feasibility of a Q2 delivery timeline.

Project communication

* Debbie
  and Julie discussed holding a monthly open meeting to showcase project
  progress and invite company-wide participation, with the first session
  potentially in April.

Sprint planning

* SriLakshmi
  explained the proposed sprint structure for Q2, allocating four sprints
  for development and testing and two sprints for production deployment and
  testing, and highlighted the need to align sprint planning with the
  readiness of the agile team.

Team coordination

* Julie
  confirmed that the engineering team led by Richie and Dave will be closely
  involved in the project, with additional support from Mike's team as
  needed.

UX and UI design

* Rajat
  explained that the UX team, including Chelsea and Bradley, will hold
  discussions next week to rethink the chat experience for members, aiming
  to share a high-level overview soon.
* Greg
  emphasized the importance of pre-planning transitions in the chat
  experience to ensure members are smoothly transferred to agents or other
  channels without losing context.
* Chance
  described that conversational designers are actively modeling
  conversations and outcomes to optimize member experience and ensure
  effective escalation when needed.

Model tuning and maintenance

* Chance
  explained that ongoing tuning of GA models is essential to adapt to
  changing customer conversations and maintain high CX, with current efforts
  focused on FEP and plans to include this in the new project.

Team roles and responsibilities

* Chance
  and Greg discussed the need to define roles and responsibilities for
  ongoing GA tuning, including distributing tasks among business, technical,
  QA, and audit teams.

Organizational change planning

* Chance
  described that GA implementation represents a cultural shift, and future
  organizational changes may be needed to consolidate agent review and
  tuning processes.

Testing and validation

* Rajat
  raised the topic of validation at scale, asking about automated testing
  options, and Chance outlined that Sierra has capabilities for mass
  simulation and automated pass/fail testing during sprints.
* Chance
  described the end-to-end simulation and QA process for agent output,
  including critic agent evaluation, subset review for consistency, and user
  acceptance testing before post-production monitoring.
* Chance
  explained that the QA group can provide test cases and expected responses
  in a specific format, which can be loaded for automated simulation and
  testing.
* Chance
  outlined that post-production involves 30 days of 100% review, after which
  tuning feedback is stacked for future releases and ongoing monitoring is
  handled by audit teams.
* Chance
  explained that regression testing will be required after each product
  initialization, with a focus on identifying crucial test cases to avoid
  unnecessary expansion as more products are added.
* Chance
  described that in user acceptance testing, "must" and
  "never" requirements are clearly defined during story review,
  while "should" items are treated as experience-based and
  evaluated for their impact on the member experience.
* Chance
  stated that training will be provided for the updated user acceptance
  testing approach, based on lessons learned from the FEP pilot, to ensure
  the process is easy to apply for testers.
* Chance
  explained that the "must-never-should" method for user
  acceptance testing has been successfully applied with multiple clients,
  making the process easier and more effective compared to strict pass/fail
  approaches.
* Greg
  emphasized the importance of involving team members with deep business
  expertise during testing to ensure accurate evaluation and efficient
  progress.
* Chance
  described that internal audit teams play a key role in tuning and
  monitoring GA outputs, catching subtle issues such as formatting and
  context errors in transcripts and chat environments.
* Chance
  outlined that ongoing production monitoring involves internal audit teams
  sampling GA agent outputs, sentiment and keyword analysis, and additional
  audits by associations, with the possibility of adopting an AI supervisor
  role for more comprehensive oversight.

Post-production monitoring and tuning

* Chance
  explained that post-production monitoring involves internal teams
  consolidating feedback, which is then reviewed with the conversational
  designer to prioritize fixes and tuning for the GA agent.

Error detection and escalation

* Chance
  described that monitoring systems are in place to detect technical errors
  or failures in the GA, with rules to divert members to agents and platform
  notifications for major outages.

Policy monitoring and safeguards

* Chance
  clarified that guardrails and policies can be directly monitored for
  drift, and advanced monitoring techniques are used as the GA handles more
  complex actions.

Quality assurance and monitoring

* Chance
  explained that business teams and conversation designers will conduct
  audits and review conversation quality, using sentiment analysis and tags
  to monitor and improve agent interactions.
* Rajat
  discussed the need for real-time quality alerts, such as notifications
  when a high number of negative feedback events occur, and Chance confirmed
  that tags and sentiment analysis can be used to trigger these alerts for
  immediate intervention.

Agent readiness and feedback

* Chance
  described how agents are given opportunities to test the system before
  launch, allowing them to experience the tool, provide feedback, and help
  identify potential issues prior to rollout.

Agent monitoring and alerts

* Chance
  explained that the Sierra platform can generate alerts for monitoring
  agent conversations, and additional alert delivery methods can be
  configured based on requirements.
* Rajat
  and Julie discussed the need to define clear requirements for alert
  notifications, including who should receive them and how they should be
  delivered.

Agent maintenance and quality

* Chance
  described the importance of ongoing agent maintenance and monitoring,
  noting that agent quality cannot be guaranteed if left unmonitored for
  extended periods.

Platform maintenance

* Chance
  explained that the GA platform allows for immediate fixes to conversation
  elements without taking the entire system offline, supporting ongoing
  maintenance and tuning.
