import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const workbookPath = process.argv[2];
if (!workbookPath) throw new Error("Usage: node validate_output.mjs <workbook.xlsx>");

const workbook = await SpreadsheetFile.importXlsx(await FileBlob.load(workbookPath));
const source = workbook.worksheets.getItem("Skills Questions v2");
const destination = workbook.worksheets.getItem("Compass CSR Chat-JJ");
const sourceRows = source.getRange("A2:E11").values;
const expected = [];

const dataElements = {
  COVERED_SERVICE: ["Member/plan: active plan, benefit package, effective dates", "Benefit configuration: covered service/category, benefit definition, inclusion/exclusion rules", "Service classification: service type, place of service, preventive vs. diagnostic, inpatient/outpatient", "Conditions: age/gender/diagnosis requirements where applicable"],
  MEMBER_COST_SHARE: ["Benefit cost share: copay, coinsurance %, deductible applicability", "Network tier: in-network/out-of-network cost share", "Place of service: office, hospital, ambulatory center, ER, etc.", "Benefit sequencing: before/after deductible rules", "Member plan configuration: individual/family tier and applicable benefit"],
  PROVIDER_NETWORK: ["Provider directory: NPI/provider ID, specialty, facility, location", "Network participation: network/product, effective/termination dates", "Provider hierarchy: professional vs. facility provider", "Place of service", "Network-specific benefits: INN/OON cost sharing, non-network restrictions, network exceptions"],
  PHARMACY_BENEFIT: ["Formulary: drug/NDC/RxNorm identifier, formulary status", "Drug tier: Tier 1–n / preferred/non-preferred/specialty", "Pharmacy benefit: retail, mail order, specialty; days supply", "Cost share: copay/coinsurance, Rx deductible", "Utilization management: PA, step therapy, quantity limits", "Pharmacy network: participating/specialty pharmacy"],
  CODE_BENEFIT_MAPPING: ["Code sets: CPT, HCPCS, ICD-10, revenue codes", "Code descriptions and hierarchies", "Code-to-benefit mapping", "Code-to-service category mapping", "Place-of-service compatibility", "Plan benefit configuration", "Potentially diagnosis/procedure pairing when coverage is conditional"],
  OUT_OF_AREA_COVERAGE: ["Plan service area / geography", "Member home region", "National/network reciprocity: e.g., BlueCard/network partner rules", "Travel benefit rules", "Emergency vs. routine care distinctions", "International coverage rules", "Out-of-area network status and cost share"],
  AUTHORIZATION_REFERRAL: ["Utilization-management rules", "Service/CPT authorization requirements", "Referral requirements by plan/product", "Provider/specialty rules", "Medical policy / clinical criteria references", "Prior-auth vendor/process information", "Effective dates and exceptions"],
  ACCUMULATORS: ["Plan accumulator configuration: deductible/OOP limits", "Individual vs. family accumulators", "Current accumulated amounts", "Remaining balances", "INN/OON accumulator separation", "Benefit-to-accumulator rules", "Benefit/calendar year dates"],
  BENEFIT_LIMITS: ["Benefit limits: visits, units, days, dollar maximums", "Frequency rules: per year, rolling period, lifetime, replacement interval", "Age/gender restrictions", "Benefit-period definition", "Accumulated utilization, if determining remaining benefit", "Exception/medical-necessity rules"],
  CLAIMS_MEMBER_ADMIN: ["Member eligibility: coverage dates, subscriber/dependent relationships, product", "Claim header/lines: service date, provider, codes, billed/allowed amounts", "Adjudication: status, denial/remark codes, adjustments", "EOB/member responsibility", "Payment/reimbursement data", "Appeal/reimbursement rules"],
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

for (const [code, taxonomy, , questionCell, coreDataElementCell] of sourceRows) {
  const questions = String(questionCell ?? "")
    .split(/\r?\n/)
    .map((line) => line.replace(/^\s*[•*-]\s*/, "").trim())
    .filter(Boolean);
  if (questions.length !== 5) {
    throw new Error(`Expected five questions for ${code}; found ${questions.length}`);
  }
  const normalizedSourceElements = normalizeForSourceCheck(coreDataElementCell);
  for (const element of dataElements[code] ?? []) {
    if (!normalizedSourceElements.includes(normalizeForSourceCheck(element))) {
      throw new Error(`${code} Data Element is not traceable to the Skills source: ${element}`);
    }
  }
  questions.forEach((question, questionIndex) => {
    const indexes = relevantElementIndexes[code]?.[questionIndex];
    const selectedElements = indexes.map((elementIndex) => dataElements[code][elementIndex]);
    expected.push({
      code,
      taxonomy,
      question,
      selectedElements,
      formattedDataElements: selectedElements.join("\n"),
    });
  });
}

const headers = destination.getRange("C1:F1").values[0];
const actualRows = destination.getRange(`A2:F${expected.length + 1}`).values;
const actualDataElements = destination.getRange(`K2:K${expected.length + 1}`).values.flat();
const issues = [];

if (headers[0] !== "Category/Taxonomy" || headers[1] !== "Use Case" || headers[2] !== "Illustrative Question?" || headers[3] !== "User Story") {
  issues.push(`Unexpected C:F headers: ${JSON.stringify(headers)}`);
}
if (actualRows.length !== expected.length) issues.push(`Expected ${expected.length} destination rows; found ${actualRows.length}`);

actualRows.forEach((row, index) => {
  const [module, persona, category, useCase, illustrativeQuestion, story] = row;
  const exp = expected[index];
  if (module !== "Compass CSR Chat") issues.push(`Row ${index + 2}: Product Module is not Compass CSR Chat`);
  if (persona !== "CSR Agent") issues.push(`Row ${index + 2}: Persona is not CSR Agent`);
  if (!useCase || String(useCase).length < 70) issues.push(`Row ${index + 2}: Use Case is missing or insufficiently specific`);
  if (category !== `${exp.taxonomy}\n${exp.code}`) issues.push(`Row ${index + 2}: taxonomy/code mismatch or missing newline separator`);
  if (illustrativeQuestion !== exp.question) issues.push(`Row ${index + 2}: Illustrative Question is not verbatim`);
  if (useCase && !String(useCase).startsWith("The CSR Agent asks to ")) issues.push(`Row ${index + 2}: Use Case is missing the persona-led prefix`);
  if (!story || !String(story).includes(exp.question)) issues.push(`Row ${index + 2}: User Story does not retain its source question`);
  if (story && !(String(story).startsWith("Given ") && String(story).includes("\nWhen ") && String(story).includes("\nThen "))) {
    issues.push(`Row ${index + 2}: User Story is not in plain-text Gherkin format`);
  }
  if (actualDataElements[index] !== exp.formattedDataElements) {
    issues.push(`Row ${index + 2}: Data Elements do not match the plain-text question-specific subset with preserved newlines`);
  }
  const crossPlatformText = `${story ?? ""}\n${actualDataElements[index] ?? ""}`;
  if (/[\u{1D400}-\u{1D7FF}]/u.test(crossPlatformText)) {
    issues.push(`Row ${index + 2}: User Story or Data Elements still contains mathematical Unicode styling characters`);
  }
});

const questionSpecificSubsetCount = expected.filter((row) => row.selectedElements.length < dataElements[row.code].length).length;
if (questionSpecificSubsetCount < 40) {
  issues.push(`Only ${questionSpecificSubsetCount} rows use a question-specific subset; expected at least 40`);
}

if (destination.getRange("K1").values[0][0] !== "Data Elements") {
  issues.push("Column K header is not Data Elements");
}

const specificTermsByRow = new Map([
  [0, "physical therapy"], [1, "mri"], [2, "breast-pump"], [3, "outpatient surgery"], [4, "caregiver"],
  [5, "mri"], [6, "urgent-care"], [7, "colonoscopy"], [9, "outpatient surgery"],
  [11, "anesthesiologist"], [13, "physical therapists"], [17, "zepbound"],
  [20, "78013"], [21, "99214"], [22, "77067"], [24, "45378"],
  [25, "california"], [27, "bluecard"], [30, "mri"], [32, "ct scan"],
  [40, "physical-therapy"], [41, "chiropractic"], [44, "orthotics"],
]);
for (const [index, term] of specificTermsByRow) {
  const useCase = String(actualRows[index]?.[3] ?? "").toLowerCase();
  if (useCase.includes(term.toLowerCase())) {
    issues.push(`Row ${index + 2}: Use Case retains question-specific term “${term}” instead of expressing the generic intent`);
  }
}

const expectedMriUseCase = "The CSR Agent asks to retrieve the member’s diagnostic procedure benefits and clarify how coverage varies by service classification or place of service. Apply service classification, benefit inclusion and exclusion rules, and any member eligibility conditions under the active plan.";
if (actualRows[1]?.[3] !== expectedMriUseCase) {
  issues.push("Row 3: diagnostic-procedure Use Case does not match the approved generic-intent example");
}

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "formula error scan",
});
if (/\"kind\":\"match\"/.test(formulaErrors.ndjson) && !/No matches/i.test(formulaErrors.ndjson)) {
  const matchLines = formulaErrors.ndjson.split("\n").filter((line) => line.includes('"kind":"match"'));
  if (matchLines.length > 0) issues.push(`Workbook contains ${matchLines.length} formula-error match(es)`);
}

for (const range of ["F2:F51", "K2:K51"]) {
  const styleCheck = await workbook.inspect({
    kind: "computedStyle",
    sheetId: "Compass CSR Chat-JJ",
    range,
    maxChars: 60000,
  });
  if (/\"bold\":true/.test(styleCheck.ndjson)) {
    issues.push(`${range}: body cells still contain bold font formatting`);
  }
}

if (issues.length) {
  console.error(`VALIDATION FAILED (${issues.length} issues)`);
  console.error(issues.slice(0, 20).join("\n"));
  process.exit(1);
}

console.log(`VALIDATION PASSED: ${expected.length} question-derived rows; plain-text User Stories and Data Elements, source-order newlines, question-specific subsets, headers, taxonomy codes, use cases, and formula errors checked.`);
