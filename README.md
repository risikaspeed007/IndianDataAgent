# 🇮🇳 India Data Agent

An AI-powered data agent that answers questions about gross enrolment
data using a verified dataset and Google Gemini.

## Features

- Query gross enrolment data
- Compare countries and Indian states
- Calculate improvement between years
- Find the highest improvement
- Find the highest 2009–10 value
- View rankings
- Query year-specific values
- Ask questions using natural language
- Gemini-powered natural-language explanations

## Dataset

The project uses:

`Countries_Gross_Enrollment_Data (1).xls`

The source workbook is preserved as an input file and is not modified.

A processed CSV version is stored in:

`data/processed/gross_enrollment_data.csv`

## Technology

- Python
- Pandas
- xlrd
- Google Gemini API
- Google GenAI Python SDK

## Project Structure

```text
IndiaDataAgent/
├── data/
│   └── processed/
├── outputs/
├── scripts/
├── src/
│   └── india_data_agent/
│       ├── agent.py
│       ├── analyzer.py
│       ├── data_service.py
│       ├── gemini_service.py
│       ├── intent.py
│       └── query_engine.py
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md