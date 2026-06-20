# Evaluation Report

## Model
Gemini 2.5 Flash

## Sample Evaluation
Used sample_claims.csv to validate pipeline and output schema.

## Images Processed
111

## Claims Processed
44

## Approximate Model Calls
44

## Prompt Strategy
- Extract claim from conversation
- Analyze all images together
- Compare visual evidence against claim
- Generate structured JSON output

## Runtime
Approximately 3-10 minutes depending on API latency.

## Error Handling
- JSON cleanup
- Fallback values
- Manual review flag
- Retry strategy

## Cost Estimate
Used Gemini Flash free tier during development.