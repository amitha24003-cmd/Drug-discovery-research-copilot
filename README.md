
# Drug Discovery Research Copilot

## Overview

Drug Discovery Research Copilot is an AI-powered platform that assists researchers in evaluating therapeutic targets for drug discovery.

Features:
- Disease and target analysis
- Risk assessment
- PubMed literature mining
- Research gap identification
- Recommendation generation

## Workflow

Disease + Target
↓
General Analysis Agent
↓
Risk Assessment Agent
↓
PubMed Search
↓
Research Gap Analysis
↓
Final Recommendation

## Technologies Used

- Python
- Streamlit
- Groq
- PubMed API
- XML Parsing

## Installation

Install dependencies:

pip install groq

Run the application:

streamlit run app.py

## Example Inputs

Alzheimer's Disease - BACE1

Breast Cancer - HER2

Parkinson's Disease - LRRK2

## Challenges Faced

- Integrating multiple AI agents
- Parsing JSON outputs from LLMs
- Processing PubMed XML data
- Converting Colab code into Streamlit

## Key Learnings

- API integration
- PubMed literature mining
- Streamlit deployment
- Multi-agent workflow design

## Future Improvements

- Open Targets integration
- DrugBank integration
- Clinical trial analysis
- Molecular docking support

## Author

Amitha C U


