# AI Tooling

## Overview

ChatGPT was the only AI tool used during development of the QuantNova HR
Assistant project. It was used to accelerate requirements analysis,
implementation support, documentation, testing strategy, evaluation
design, and presentation preparation.

AI-generated suggestions were treated as development assistance rather
than authoritative output. The team reviewed, tested, and revised
generated code and documentation before using it in the project.

## Tool Used

### ChatGPT

ChatGPT was used to:

-   Translate the project requirements into implementation and
    submission checklists.
-   Help design the agentic HR architecture, including RAG, MCP tools,
    structured HR data access, and agent orchestration.
-   Assist with implementation ideas for FastAPI, LangChain, MCP,
    PostgreSQL/pgvector, testing, CI/CD, and deployment.
-   Review the implementation against the grading rubric and identify
    missing requirements.
-   Design synthetic HR evaluation scenarios covering policy questions,
    PTO calculations, benefits eligibility, ambiguity, safety, and
    failure handling.
-   Help draft and refine repository documentation.
-   Prepare and refine the live demonstration and presentation script.

## What Worked Well

ChatGPT was especially useful for requirements analysis, architecture
review, documentation, and evaluation design. It helped the team break a
large project specification into concrete engineering tasks and identify
important distinctions, such as the difference between direct function
calls and actual MCP-exposed tool invocation.

It was also useful for reviewing workflows end-to-end, including policy
retrieval, structured employee data, tool traces, citations,
calculations, safety behavior, and deployment requirements.

## What Did Not Work Well

ChatGPT-generated suggestions still required manual verification.
Generated code or recommendations could make assumptions about package
versions, deployment environments, MCP APIs, configuration, or runtime
behavior that did not necessarily match the actual application.

For this reason, the team did not treat AI-generated explanations as
evidence that a feature worked. Important behavior was verified using
the actual application, automated tests, CI results, deployed-system
behavior, and visible tool traces.

## Human Review and Verification

The team retained responsibility for the final implementation. Important
behavior was verified through the application and test suite, including:

-   MCP-exposed tool usage and visible tool traces.
-   Employee, PTO, benefits, and policy retrieval.
-   Traceable policy citations.
-   PTO calculations that distinguish retrieved balances from calculated
    estimates.
-   Safety and confirmation behavior for potentially state-changing
    actions.
-   Evaluation cases and automated tests.

## Responsible Use

The project uses fictional QuantNova AI policies and synthetic employee
data. No real employee HR records are required for the demonstration.
Secrets and API credentials are kept outside the repository through
environment variables and deployment configuration.

ChatGPT assisted the development process, but final system behavior,
evaluation results, deployment status, and documentation are based on
the implemented and observed project outputs.
