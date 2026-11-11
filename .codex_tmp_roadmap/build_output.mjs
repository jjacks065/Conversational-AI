import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workspace = "/Users/jjacks20/jjacks/Conversational-AI";
const inputPath = path.join(workspace, "Product Roadmap Use Cases-JJ.xlsx");
const outputDir = path.join(workspace, "outputs", "01a04934-48bd-7c61-98ba-e47d56141ffe");
const outputPath = path.join(outputDir, "Product Roadmap Use Cases-JJ-with-data-elements.xlsx");
const previewDir = path.join(workspace, ".codex_tmp_roadmap", "previews_after_data_elements");

const content = {
  COVERED_SERVICE: {
    scope: "service classification, benefit inclusion and exclusion rules, and any member eligibility conditions under the active plan",
    items: [
      ["Determine whether a rehabilitative therapy service is covered and identify applicable plan conditions or exclusions", "confirm the member’s active plan, locate the physical-therapy benefit, review coverage conditions and exclusions, and translate the result into a clear response", "the member understands whether therapy is covered and what requirements apply before scheduling care"],
      ["Retrieve the member’s diagnostic procedure benefits and clarify how coverage varies by service classification or place of service", "identify the MRI context, find the matching benefit, review diagnostic and site-of-care conditions, and summarize the plan-specific coverage", "the member receives the correct MRI benefit information for the anticipated setting"],
      ["Confirm coverage for a plan-provided medical device and surface any eligibility, timing, supplier, or frequency conditions", "verify the member’s plan and eligibility context, locate the breast-pump benefit, and explain coverage conditions and fulfillment requirements", "the member knows whether a breast pump is covered and how to obtain it"],
      ["Identify the benefit that applies to an outpatient procedural service and explain its coverage conditions", "capture the planned procedure and site of care, map it to the outpatient-surgery benefit, and review the applicable coverage language", "the member receives an accurate explanation of the benefit before the procedure"],
      ["Determine whether a supplemental support benefit is available and identify the circumstances in which it applies", "confirm the member and plan, locate caregiver-support benefits, review eligibility criteria and exclusions, and communicate available options", "the member understands whether caregiver support is available and any next steps to access it"],
    ],
  },
  MEMBER_COST_SHARE: {
    scope: "copay, coinsurance, deductible, network tier, place-of-service, and benefit-sequencing rules",
    items: [
      ["Determine the copay for a diagnostic procedure using the applicable network and site-of-care benefit", "identify the MRI setting and provider network status, retrieve the copay and deductible rules, and explain when each amount applies", "the member has a plan-specific view of the expected MRI copay"],
      ["Estimate the member’s financial responsibility for a same-day ambulatory care visit", "confirm the urgent-care facility’s network tier, review copay, coinsurance, and deductible rules, and present the expected responsibility", "the member can compare options and anticipate the cost of urgent care"],
      ["Determine the member cost for a preventive or diagnostic screening procedure, accounting for service classification and place of service", "clarify the colonoscopy’s clinical classification and setting, retrieve the corresponding cost-share rules, and explain the member responsibility", "the member understands why the expected cost may differ by circumstance"],
      ["Determine whether a service is subject to coinsurance and identify the applicable rate and sequencing", "identify the service and benefit, verify network and deductible status, and explain the coinsurance rate and when it begins", "the member receives a clear explanation of how coinsurance will be applied"],
      ["Estimate the member cost for an outpatient procedural service across facility and professional components", "capture the procedure, facility, clinicians, and network status, retrieve each applicable cost-share rule, and summarize the combined responsibility", "the member can anticipate the main cost components before outpatient surgery"],
    ],
  },
  PROVIDER_NETWORK: {
    scope: "provider-directory participation, network tier, effective dates, provider type, location, and network-specific benefit rules",
    items: [
      ["Verify whether a specialist participates in the member’s network and identify the applicable tier", "identify the specialist and location, validate participation for the member’s product and date of service, and explain the resulting network status", "the member can choose a participating specialist with confidence"],
      ["Explain benefits when an in-network facility uses an out-of-network professional provider", "validate the hospital and anesthesiologist separately, apply the network rules to each component, and explain the benefit and cost implications", "the member understands the mixed-network scenario and potential financial exposure"],
      ["Determine whether the member may use an out-of-network provider and explain restrictions or reduced benefits", "review the plan’s out-of-network access rules, confirm any exceptions or authorization requirements, and summarize the applicable benefits", "the member can make an informed choice about receiving non-network care"],
      ["Locate in-network rehabilitative therapy providers that meet the member’s geographic and plan requirements", "confirm the member’s product and preferred location, search current network participation, and present suitable physical-therapy options", "the member can contact an eligible in-network therapist"],
      ["Retrieve the benefit for a specialty office visit using the provider’s network tier and place of service", "confirm the specialist’s participation, map the office visit to the correct benefit, and explain the coverage and cost-share details", "the member understands the benefit before attending the specialist visit"],
    ],
  },
  PHARMACY_BENEFIT: {
    scope: "drug formulary status, tier, pharmacy channel, days supply, cost share, utilization-management rules, and pharmacy network",
    items: [
      ["Determine the member’s prescription-drug copay for the applicable tier and pharmacy channel", "identify the medication, supply, and dispensing channel, retrieve the tier-specific copay and deductible rules, and explain the expected cost", "the member knows the likely prescription cost before filling it"],
      ["Explain the benefit for a non-preferred formulary-tier medication, including cost share and dispensing options", "confirm the drug’s Tier 3 placement, review retail, mail, and specialty benefit rules, and summarize the applicable copay or coinsurance", "the member can select an appropriate fulfillment option and anticipate the cost"],
      ["Determine whether a named medication is covered and identify formulary or utilization-management conditions", "locate Zepbound on the member’s formulary, review its tier, prior authorization, step-therapy, and quantity-limit requirements, and communicate the result", "the member understands both coverage status and prerequisites for access"],
      ["Identify the participating specialty pharmacy the member should use for a specialty medication", "confirm the medication and plan, check mandated or participating specialty-pharmacy options, and provide the appropriate fulfillment route", "the member can send the prescription to an eligible specialty pharmacy"],
      ["Verify whether a medication is on the member’s formulary and identify its tier and restrictions", "identify the medication precisely, check current formulary placement, and explain tier, cost share, and any utilization-management conditions", "the member knows whether the drug is covered and what is required to obtain it"],
    ],
  },
  CODE_BENEFIT_MAPPING: {
    scope: "code-set definitions, code-to-service and benefit mappings, place-of-service compatibility, and plan benefit configuration",
    items: [
      ["Map a submitted diagnostic procedure code to the appropriate service and benefit category", "validate CPT 78013, review its description and service hierarchy, map it to the plan benefit, and explain the applicable benefit context", "the member inquiry is routed to the correct benefit rather than answered from the code alone"],
      ["Map an evaluation-and-management code to the applicable benefit and present its coverage and cost-share rules", "validate CPT 99214 and the visit context, map it to the correct office-visit benefit, and retrieve the relevant coverage details", "the member receives an accurate benefit explanation for the billed service"],
      ["Determine whether a preventive screening procedure code is covered after mapping it to the correct benefit", "validate CPT 77067, confirm the service context, map it to the appropriate benefit category, and review coverage conditions", "the member receives the correct coverage answer for the mammography service"],
      ["Identify the benefit category associated with a supplied procedure code", "capture and validate the procedure code, resolve its description and hierarchy, and map it to the member’s plan benefit", "the CSR can continue the inquiry using the correct service category and benefit rules"],
      ["Determine the member cost for a submitted diagnostic procedure code after mapping it to the appropriate benefit", "validate CPT 45378 and the procedure context, map it to the colonoscopy benefit, and apply network, setting, and cost-share rules", "the member receives a context-appropriate estimate for the coded procedure"],
    ],
  },
  OUT_OF_AREA_COVERAGE: {
    scope: "plan service area, destination geography, network reciprocity, travel rules, emergency-versus-routine care, and out-of-area cost share",
    items: [
      ["Determine what coverage applies while the member is traveling outside the plan’s home service area", "confirm the destination and type of care, apply out-of-area and reciprocity rules, and explain network access, coverage, and cost share", "the member knows how to obtain covered care while away from California"],
      ["Explain the member’s benefits for care received outside the plan’s home state", "identify the destination, service, and provider context, retrieve out-of-state benefit and network rules, and summarize the applicable coverage", "the member can plan out-of-state care with a clear understanding of benefits"],
      ["Determine whether the member may use a reciprocal network provider outside the plan’s service area", "confirm BlueCard eligibility for the member’s product, validate the provider and location, and explain how claims and cost sharing will be handled", "the member can select an appropriate participating provider while traveling"],
      ["Confirm coverage for emergency services received while traveling", "identify the emergency setting and location, apply emergency and out-of-area rules, and explain coverage, notification needs, and cost share", "the member can seek urgent help without uncertainty about the applicable benefit"],
      ["Determine whether international travel coverage is included and identify its limitations", "confirm the destination and care type, review international and emergency coverage provisions, and explain exclusions, payment, or reimbursement steps", "the member understands how the plan responds to care received outside the country"],
    ],
  },
  AUTHORIZATION_REFERRAL: {
    scope: "service-level authorization, referral, medical-necessity, vendor-process, effective-date, and exception rules",
    items: [
      ["Determine whether a diagnostic imaging service requires prior authorization and identify the required process", "identify the MRI and service setting, check the current authorization rule, and explain who must submit the request and when", "the member and provider can complete authorization before the MRI"],
      ["Determine whether the member needs a referral before receiving specialty care", "confirm the plan product and specialist type, review referral and network rules, and explain the required sequence of care", "the member avoids an unnecessary delay or noncovered specialist visit"],
      ["Determine whether an advanced diagnostic imaging service requires preauthorization and surface relevant exceptions", "identify the CT service and setting, check the applicable utilization-management rule, and explain submission requirements and exceptions", "the member understands what must occur before the scan is scheduled"],
      ["Determine whether the member may self-refer for behavioral-health services", "review the plan’s behavioral-health referral rules, network requirements, and access pathways, and explain how the member can initiate care", "the member can reach appropriate mental-health services without avoidable barriers"],
      ["Identify the authorization required for a specified medication or procedure", "capture the drug or procedure precisely, check prior authorization and related clinical-management rules, and communicate the required documents and steps", "the member and provider know how to proceed toward an authorization decision"],
    ],
  },
  ACCUMULATORS: {
    scope: "deductible and out-of-pocket configuration, individual and family tiers, current accumulated amounts, network separation, and benefit-year rules",
    items: [
      ["Explain the deductible amount and structure that apply to the member", "confirm the active plan, coverage tier, benefit year, and network, then retrieve and explain the applicable deductible limits", "the member understands the deductible that governs upcoming services"],
      ["Report how much of the deductible the member has met and how much remains", "verify the member, plan year, and network accumulator, retrieve current posted amounts, and explain met and remaining balances", "the member receives an up-to-date view of deductible progress"],
      ["Explain the member’s out-of-pocket maximum and its applicable tier and network", "confirm the benefit year and coverage tier, retrieve the out-of-pocket limits and current status, and distinguish in-network from out-of-network amounts", "the member understands the maximum financial exposure defined by the plan"],
      ["Determine whether spending for a covered service applies toward the deductible", "map emergency care to its benefit and accumulator rules, verify network and plan-year treatment, and explain how eligible amounts accumulate", "the member understands whether emergency-care costs advance the deductible"],
      ["Explain how individual and family deductibles interact under the member’s plan", "retrieve the plan’s embedded or aggregate deductible structure, compare individual and family progress, and explain which threshold triggers benefits", "the member understands how household spending affects coverage for each family member"],
    ],
  },
  BENEFIT_LIMITS: {
    scope: "visit, unit, day, dollar, age, frequency, replacement-interval, benefit-period, utilization, and exception rules",
    items: [
      ["Determine the number of covered rehabilitative therapy visits and any remaining allowance", "locate the physical-therapy limit, confirm the benefit period and member utilization, and explain covered, used, and remaining visits", "the member can plan therapy within the available visit allowance"],
      ["Determine whether a complementary care benefit has an annual visit limit", "retrieve the chiropractic limit and benefit-year definition, review current utilization and exceptions, and explain the remaining allowance", "the member understands the annual restriction before scheduling additional visits"],
      ["Explain how often the member may receive a specified preventive service", "identify the preventive service, apply its frequency and age rules, check prior utilization where available, and explain the next eligible date", "the member can schedule the service at an eligible interval"],
      ["Determine whether an age restriction applies to a benefit", "identify the benefit and member age, review age-based eligibility and exception rules, and explain whether the member qualifies", "the member receives a clear eligibility answer based on the plan’s age criteria"],
      ["Determine the covered quantity and replacement interval for an orthotic or medical-supply benefit", "retrieve the orthotics quantity and frequency limits, review the member’s utilization history, and explain the current remaining benefit", "the member knows whether another pair is available and when replacement is allowed"],
    ],
  },
  CLAIMS_MEMBER_ADMIN: {
    scope: "member eligibility, claim and EOB line detail, adjudication and denial codes, financial responsibility, reimbursement, and appeal rules",
    items: [
      ["Explain why an EOB displays a copay but no patient responsibility", "verify the member and claim, review the EOB line, adjustments, payments, and responsibility fields, and explain the apparent discrepancy", "the member understands the EOB and whether any payment is actually due"],
      ["Determine whether an out-of-network superbill may be submitted for reimbursement and explain the process", "confirm out-of-network benefits, review submission deadlines and required documentation, and provide the reimbursement steps", "the member can submit a complete claim for eligible reimbursement"],
      ["Verify whether a dependent is currently covered under the plan", "identify the dependent and subscriber relationship, review eligibility and effective dates, and explain the current coverage status", "the caller receives an accurate eligibility answer before care is obtained"],
      ["Identify the effective date of the member’s coverage", "verify the member and product, retrieve enrollment and coverage dates, and explain any relevant waiting period or termination context", "the member knows when plan benefits became available"],
      ["Explain why a claim was denied and identify available next steps", "locate the claim and affected lines, interpret denial and remark codes, review benefit and eligibility context, and explain correction or appeal options", "the member understands the denial and can pursue the appropriate resolution path"],
    ],
  },
};

const dataElements = {
  COVERED_SERVICE: [
    "Member/plan: active plan, benefit package, effective dates",
    "Benefit configuration: covered service/category, benefit definition, inclusion/exclusion rules",
    "Service classification: service type, place of service, preventive vs. diagnostic, inpatient/outpatient",
    "Conditions: age/gender/diagnosis requirements where applicable",
  ],
  MEMBER_COST_SHARE: [
    "Benefit cost share: copay, coinsurance %, deductible applicability",
    "Network tier: in-network/out-of-network cost share",
    "Place of service: office, hospital, ambulatory center, ER, etc.",
    "Benefit sequencing: before/after deductible rules",
    "Member plan configuration: individual/family tier and applicable benefit",
  ],
  PROVIDER_NETWORK: [
    "Provider directory: NPI/provider ID, specialty, facility, location",
    "Network participation: network/product, effective/termination dates",
    "Provider hierarchy: professional vs. facility provider",
    "Place of service",
    "Network-specific benefits: INN/OON cost sharing, non-network restrictions, network exceptions",
  ],
  PHARMACY_BENEFIT: [
    "Formulary: drug/NDC/RxNorm identifier, formulary status",
    "Drug tier: Tier 1–n / preferred/non-preferred/specialty",
    "Pharmacy benefit: retail, mail order, specialty; days supply",
    "Cost share: copay/coinsurance, Rx deductible",
    "Utilization management: PA, step therapy, quantity limits",
    "Pharmacy network: participating/specialty pharmacy",
  ],
  CODE_BENEFIT_MAPPING: [
    "Code sets: CPT, HCPCS, ICD-10, revenue codes",
    "Code descriptions and hierarchies",
    "Code-to-benefit mapping",
    "Code-to-service category mapping",
    "Place-of-service compatibility",
    "Plan benefit configuration",
    "Potentially diagnosis/procedure pairing when coverage is conditional",
  ],
  OUT_OF_AREA_COVERAGE: [
    "Plan service area / geography",
    "Member home region",
    "National/network reciprocity: e.g., BlueCard/network partner rules",
    "Travel benefit rules",
    "Emergency vs. routine care distinctions",
    "International coverage rules",
    "Out-of-area network status and cost share",
  ],
  AUTHORIZATION_REFERRAL: [
    "Utilization-management rules",
    "Service/CPT authorization requirements",
    "Referral requirements by plan/product",
    "Provider/specialty rules",
    "Medical policy / clinical criteria references",
    "Prior-auth vendor/process information",
    "Effective dates and exceptions",
  ],
  ACCUMULATORS: [
    "Plan accumulator configuration: deductible/OOP limits",
    "Individual vs. family accumulators",
    "Current accumulated amounts",
    "Remaining balances",
    "INN/OON accumulator separation",
    "Benefit-to-accumulator rules",
    "Benefit/calendar year dates",
  ],
  BENEFIT_LIMITS: [
    "Benefit limits: visits, units, days, dollar maximums",
    "Frequency rules: per year, rolling period, lifetime, replacement interval",
    "Age/gender restrictions",
    "Benefit-period definition",
    "Accumulated utilization, if determining remaining benefit",
    "Exception/medical-necessity rules",
  ],
  CLAIMS_MEMBER_ADMIN: [
    "Member eligibility: coverage dates, subscriber/dependent relationships, product",
    "Claim header/lines: service date, provider, codes, billed/allowed amounts",
    "Adjudication: status, denial/remark codes, adjustments",
    "EOB/member responsibility",
    "Payment/reimbursement data",
    "Appeal/reimbursement rules",
  ],
};

const relevantElementIndexes = {
  COVERED_SERVICE: [[0, 1, 2], [0, 1, 2], [0, 1, 3], [0, 1, 2], [0, 1, 3]],
  MEMBER_COST_SHARE: [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4]],
  PROVIDER_NETWORK: [[0, 1], [0, 1, 2, 3, 4], [1, 4], [0, 1], [0, 1, 3, 4]],
  PHARMACY_BENEFIT: [[0, 1, 2, 3, 5], [1, 2, 3], [0, 1, 4], [0, 1, 2, 5], [0, 1, 3, 4]],
  CODE_BENEFIT_MAPPING: [[0, 1, 2, 3, 5], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 5], [0, 1, 2, 3, 4, 5, 6]],
  OUT_OF_AREA_COVERAGE: [[0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 6], [0, 1, 3, 4, 6], [0, 1, 3, 4, 5, 6]],
  AUTHORIZATION_REFERRAL: [[0, 1, 4, 5, 6], [2, 3, 6], [0, 1, 4, 5, 6], [2, 3, 5, 6], [0, 1, 4, 5, 6]],
  ACCUMULATORS: [[0, 1, 4, 6], [0, 1, 2, 3, 4, 6], [0, 1, 2, 3, 4, 6], [0, 4, 5, 6], [0, 1, 2, 3, 6]],
  BENEFIT_LIMITS: [[0, 1, 3, 4, 5], [0, 1, 3, 4, 5], [1, 2, 3, 4, 5], [2, 5], [0, 1, 3, 4, 5]],
  CLAIMS_MEMBER_ADMIN: [[0, 1, 2, 3, 4], [0, 1, 4, 5], [0], [0], [0, 1, 2, 3, 5]],
};

const normalizeForSourceCheck = (text) => String(text ?? "")
  .replace(/\*\*/g, "")
  .replace(/\s+/g, "")
  .toLowerCase();

const parseQuestions = (value) => String(value ?? "")
  .split(/\r?\n/)
  .map((line) => line.replace(/^\s*[•*-]\s*/, "").trim())
  .filter(Boolean);

await fs.mkdir(outputDir, { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(inputPath));
const source = workbook.worksheets.getItem("Skills Questions v2");
const destination = workbook.worksheets.getItem("Compass CSR Chat-JJ");
const sourceRows = source.getRange("A2:E11").values;
const outputRows = [];
const outputDataElements = [];

for (const [code, taxonomy, , questionCell, coreDataElementCell] of sourceRows) {
  const definition = content[code];
  if (!definition) throw new Error(`Missing content definition for ${code}`);
  const normalizedSourceElements = normalizeForSourceCheck(coreDataElementCell);
  for (const element of dataElements[code] ?? []) {
    if (!normalizedSourceElements.includes(normalizeForSourceCheck(element))) {
      throw new Error(`${code} Data Element is not traceable to the Skills source: ${element}`);
    }
  }
  const questions = parseQuestions(questionCell);
  if (questions.length !== definition.items.length) {
    throw new Error(`${code} has ${questions.length} source questions and ${definition.items.length} content definitions`);
  }

  questions.forEach((question, index) => {
    const [intent, journey, outcome] = definition.items[index];
    const genericIntent = `${intent.charAt(0).toLowerCase()}${intent.slice(1)}`;
    const useCase = `The CSR Agent asks to ${genericIntent}. Apply ${definition.scope}.`;
    const userStory = `Given a CSR Agent is assisting a member who asks, “${question}”\nWhen the CSR Agent uses the member’s context to ${journey}\nThen ${outcome}.`;
    outputRows.push(["Compass CSR Chat", "CSR Agent", `${taxonomy}\n${code}`, useCase, question, userStory]);
    const indexes = relevantElementIndexes[code]?.[index];
    if (!indexes?.length) throw new Error(`Missing Data Element relevance selection for ${code} question ${index + 1}`);
    const selected = indexes.map((elementIndex) => dataElements[code]?.[elementIndex]);
    if (selected.some((element) => !element)) throw new Error(`Invalid Data Element selection for ${code} question ${index + 1}`);
    outputDataElements.push(selected.join("\n"));
  });
}

if (outputRows.length !== 50) throw new Error(`Expected 50 output rows; created ${outputRows.length}`);

for (let row = 3; row <= outputRows.length + 1; row += 1) {
  destination.getRange(`A${row}:N${row}`).copyFrom(destination.getRange("A2:N2"), "all");
}
destination.getRange(`A2:F${outputRows.length + 1}`).values = outputRows;
destination.getRange(`A2:F${outputRows.length + 1}`).format = {
  wrapText: true,
  verticalAlignment: "top",
  horizontalAlignment: "left",
};
destination.getRange(`F2:F${outputRows.length + 1}`).format.font = { bold: false };
destination.getRange(`A1:A${outputRows.length + 1}`).format.columnWidthPx = 155;
destination.getRange(`B1:B${outputRows.length + 1}`).format.columnWidthPx = 125;
destination.getRange(`C1:C${outputRows.length + 1}`).format.columnWidthPx = 315;
destination.getRange(`D1:D${outputRows.length + 1}`).format.columnWidthPx = 470;
destination.getRange(`E1:E${outputRows.length + 1}`).format.columnWidthPx = 330;
destination.getRange(`F1:F${outputRows.length + 1}`).format.columnWidthPx = 570;
destination.getRange(`K1:K${outputRows.length + 1}`).format.columnWidthPx = 500;
destination.getRange(`A2:N${outputRows.length + 1}`).format.rowHeightPx = 176;
destination.freezePanes.freezeRows(1);

destination.getRange(`K2:K${outputRows.length + 1}`).values = outputDataElements.map((value) => [value]);
destination.getRange(`K2:K${outputRows.length + 1}`).format = {
  wrapText: true,
  verticalAlignment: "top",
  horizontalAlignment: "left",
  font: { bold: false },
};

const keyCheck = await workbook.inspect({
  kind: "table",
  range: `Compass CSR Chat-JJ!A1:F${outputRows.length + 1}`,
  include: "values,formulas",
  tableMaxRows: 8,
  tableMaxCols: 6,
  tableMaxCellChars: 220,
  maxChars: 12000,
});
console.log(keyCheck.ndjson);

const dataElementsCheck = await workbook.inspect({
  kind: "table",
  range: "Compass CSR Chat-JJ!K1:K8",
  include: "values,formulas",
  tableMaxRows: 8,
  tableMaxCols: 1,
  tableMaxCellChars: 500,
  maxChars: 8000,
});
console.log(dataElementsCheck.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
});
console.log(errors.ndjson);

for (let i = 0; i < workbook.worksheets.items.length; i += 1) {
  const sheet = workbook.worksheets.getItemAt(i);
  const used = sheet.getUsedRange();
  const range = used?.address ?? "A1";
  const preview = await workbook.render({ sheetName: sheet.name, range, scale: 0.25, format: "png" });
  const safeName = `${String(i + 1).padStart(2, "0")}_${sheet.name.replace(/[^a-z0-9_-]+/gi, "_")}.png`;
  await fs.writeFile(path.join(previewDir, safeName), new Uint8Array(await preview.arrayBuffer()));
}

for (const [name, range] of [["destination_top", "A1:N12"], ["destination_middle", "A20:N32"], ["destination_bottom", "A40:N51"]]) {
  const preview = await workbook.render({ sheetName: "Compass CSR Chat-JJ", range, scale: 0.75, format: "png" });
  await fs.writeFile(path.join(previewDir, `${name}.png`), new Uint8Array(await preview.arrayBuffer()));
}

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`EXPORTED ${outputPath}`);
