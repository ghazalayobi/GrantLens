# GrantLens: Project Brief

## 1. Project Overview

GrantLens is an independent Applied AI portfolio project
that helps nonprofit researchers explore publicly available
grant information through natural-language questions.

The application retrieves relevant grant records and
generates source-grounded answers with verifiable citations.

## 2. Problem Statement

Public grant information is often distributed across
multiple webpages, reports, and program descriptions.

Researchers may need to manually search many sources
to identify relevant grants, recipients, funding amounts,
program areas, and publicly stated purposes.

GrantLens aims to make this information easier to explore
while preserving traceability to original sources.

## 3. Intended Users

Primary users:

- Nonprofit researchers
- Foundation program staff
- Grant research professionals

## 4. Core User Questions

The initial application should support questions such as:

1. What grants related to youth engagement are in the dataset?
2. Which organizations received environment-related grants?
3. What are the publicly stated purposes of grants in Flint?
4. Which grants fall within a specified funding amount range?
5. Can you summarize the available grants related to civil society?

Answers must be limited to the available source material.

## 5. Data Scope

The initial dataset will contain approximately 50–100
publicly available grant records.

Potential sources include public grant webpages and
published reports from the Mott Foundation.

Each record should contain, where publicly available:

- Grant identifier
- Recipient
- Grant title
- Grant purpose or description
- Grant amount
- Grant period
- Program area
- Source URL
- Retrieval date

Missing information must remain explicitly identified
rather than invented.

## 6. Functional Requirements

The system should:

FR1. Collect and store public grant information.

FR2. Clean and standardize grant records.

FR3. Support keyword-based searching.

FR4. Support basic filtering by available metadata.

FR5. Retrieve relevant source passages for user questions.

FR6. Generate answers grounded in retrieved evidence.

FR7. Display source citations and clickable URLs.

FR8. Indicate when available evidence is insufficient.

## 7. Non-Functional Requirements

The system should:

NFR1. Be reproducible from documented setup instructions.

NFR2. Avoid exposing API keys or other credentials.

NFR3. Preserve source attribution.

NFR4. Handle missing or incomplete records.

NFR5. Clearly distinguish retrieved facts from generated summaries.

NFR6. Provide understandable error messages.

## 8. Definition of Success

The MVP will be considered complete when:

- A structured public dataset is available.
- Basic keyword search works.
- Users can submit natural-language questions.
- Answers contain verifiable source references.
- Unsupported questions receive an appropriate response.
- At least 20 evaluation questions have been tested.
- The application can run locally.
- The GitHub repository includes setup and evaluation documentation.

## 9. Risks and Limitations

Potential risks include:

- Outdated public information.
- Incomplete grant records.
- Changes to source webpages.
- Retrieval failures.
- Hallucinated or unsupported AI responses.
- Incorrect interpretation of grant descriptions.

GrantLens will not make funding recommendations,
predict application success, or represent an official
Mott Foundation product.

## 10. Initial Technology Stack

Language: Python

Data collection: requests, BeautifulSoup

Data processing: pandas

Storage: CSV, SQLite

Retrieval: Keyword search followed by vector search

AI: LLM API with source-grounded prompting

Interface: Streamlit

Version control: Git and GitHub

Evaluation: Manually curated question-answer test set