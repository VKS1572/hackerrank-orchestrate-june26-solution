# HackerRank Orchestrate

🧠 Multi-Modal Evidence Review System
📌 Overview

This project solves the HackerRank Orchestrate – Multi-Modal Evidence Review challenge.

The system evaluates insurance-style claims using:

🖼️ Image evidence (primary source of truth)
💬 Claim conversation (user intent)
👤 User history (risk context)
📋 Evidence requirements (validation rules)

For each claim, the system determines:

claim_status → supported / contradicted / not_enough_information
evidence validity and sufficiency
issue type & object part
risk signals and severity
supporting images for decision
🎯 Problem Objective

Given a claim involving one of:

🚗 Car
💻 Laptop
📦 Package

The system must:

Extract the actual claim from conversation
Analyze all submitted images
Validate whether evidence is sufficient
Identify visible issue type and object part
Decide claim outcome:
supported
contradicted
not_enough_information
Provide structured justification and risk flags
🧠 System Architecture

The solution follows a Hybrid Vision + Reasoning Pipeline:

1. Image Understanding (Gemini 2.5 Flash Vision)

Each image is analyzed to extract:

object type detection
visible damage or condition
object part identification
image quality assessment
validity check
2. Claim Parsing (Text Understanding)

Extracts structured intent from conversation:

claimed issue
object type
affected part
3. Evidence Validation Layer

Checks:

image clarity
required evidence completeness
mismatch detection
missing views or insufficient data
4. Decision Engine (Deterministic Logic)

Combines:

vision outputs
claim intent
evidence rules
user history risk signals

Final classification:

supported
contradicted
not_enough_information
⚙️ Model Used
Gemini 2.5 Flash (Vision API)
Used for image understanding
Structured JSON output enforced
NOT used for final decision making
🔥 Key Design Principles
Images are treated as primary truth
LLM outputs are always structured JSON (no free text decisions)
Final decision is rule-based for consistency
System avoids hallucination by separating:
perception (vision model)
reasoning (code layer)
🧪 Evaluation Strategy

Three approaches were evaluated:

1. Rule-Based Baseline
keyword + heuristic logic
fast but low accuracy
2. Vision-Only Approach
direct LLM classification
high variance, inconsistent reasoning
3. Hybrid System (Final) ⭐
Gemini extracts structured features
deterministic reasoning engine makes final decision
best balance of accuracy + reliability
📊 Output Schema

The system generates output.csv with:

evidence_standard_met
evidence_standard_met_reason
risk_flags
issue_type
object_part
claim_status
claim_status_justification
supporting_image_ids
valid_image
severity
⚠️ Risk Flags Used

The system detects and flags:

blurry_image
low_quality_image
object_mismatch
insufficient_evidence
suspicious_claim_pattern
missing_required_views
🧩 Project Flow
claims.csv
   ↓
Data Loader
   ↓
Image Processing (Gemini 2.5 Flash)
   ↓
Claim Parsing Module
   ↓
Evidence Validation Layer
   ↓
Decision Engine
   ↓
output.csv
🚀 How to Run
pip install -r requirements.txt
python code/main.py
📁 Project Structure
code/
 ├── main.py
 ├── vision.py
 ├── reasoning.py
 ├── schema.py
 ├── utils.py
 ├── evaluation/
 │    └── evaluate.py
dataset/
 ├── claims.csv
 ├── user_history.csv
 ├── evidence_requirements.csv
 ├── images/
output.csv
🧠 Key Insights
Separating vision and reasoning significantly improves reliability
Structured JSON outputs reduce hallucination from LLM
Deterministic final logic ensures consistent grading
Multi-image aggregation improves evidence accuracy
📈 Limitations
Performance depends on image quality
Edge cases with ambiguous claims may fall into not_enough_information
API latency depends on Gemini response time
🔮 Future Improvements
Confidence scoring per decision
Fine-tuned damage detection model
Multi-image attention fusion model
Cost optimization via batching + caching
👨‍💻 Author

Vikas Pradhan
HackerRank Orchestrate Submission – Multi-Modal Evidence Review System
