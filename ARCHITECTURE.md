# ARCHITECTURE.md: SOA Course Material & Agent Pipeline Architecture

This document formalizes the system design, knowledge-caching architecture, and automated execution pipeline powering the **Service-Oriented Architecture (SOA)** coursework generation system.

---

## 1. System Architecture Overview

The system is designed around a **Spec-First, Pipeline-Driven Generation Architecture**.
It decouples static pedagogical knowledge from operational execution agents, ensuring deterministic, reproducible, and verifiable weekly curriculum deliverables.

```mermaid
flowchart TD
    subgraph KNOWLEDGE["Tier 1 & Tier 2: Static & Cached Knowledge Base"]
        AGENTS["AGENTS.md\n(Always-Active Orchestration)"]
        SYLLABUS[".agents/context/syllabus.md\n(15-Week Curriculum)"]
        PATTERNS[".agents/context/api-design-patterns-notes.md\n(JJ Geewax)"]
        PRODUCT[".agents/context/building-api-product-notes.md\n(Bruno Pedro)"]
        GLOSSARY[".agents/context/glossary-soa.md\n(Lexicon)"]
        TOOLING[".agents/context/tooling-notes.md\n(Stack Conventions)"]
        TEMPLATE["slides-template/base-marp.md\n(Marp Styling Engine)"]
    end

    subgraph PIPELINE["Tier 3: Sequential Agent Generation Pipeline"]
        SK1["1. course-digest\n(Knowledge Extraction)"]
        SK2["2. weekly-slide-outline\n(Pedagogical Structuring)"]
        SK3["3. api-code-scaffold\n(Service Implementation)"]
        SK4["4. openapi-writer\n(Contract Formulation)"]
        SK5["5. postman-collection\n(Test & Verification)"]
    end

    subgraph OUTPUT["Weekly Deliverables: weeks/week-XX/"]
        OUT_SLIDE["slide.md\n(Marp Presentation Deck)"]
        subgraph OUT_CODE["code/"]
            OUT_SRV["server.js & models/\n(Express.js + Mongoose)"]
            OUT_OAS["openapi.yaml\n(OpenAPI 3.0.3 Contract)"]
            OUT_PST["postman_collection.json\n(Postman v2.1.0 Test Suite)"]
        end
    end

    KNOWLEDGE --> SK1
    SK1 --> SK2
    TEMPLATE --> SK2
    SK2 --> OUT_SLIDE
    SK2 --> SK3
    TOOLING --> SK3
    SK3 --> OUT_SRV
    OUT_SRV --> SK4
    SK4 --> OUT_OAS
    OUT_OAS --> SK5
    SK5 --> OUT_PST
```

---

## 2. Gemini Context Caching & Progressive Disclosure Model

To maximize Gemini's reasoning precision while avoiding token bloat and context dilution, the system organizes information into three distinct tiers:

| Tier | Category | Files | Loading Strategy | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Root Directives** | `AGENTS.md`, `ARCHITECTURE.md` | Auto-loaded at session root | Serves as the static system prompt prefix. Automatically cached by Gemini's prefix caching engine. |
| **Tier 2** | **Cached Knowledge Base** | `.agents/context/*.md`, `slides-template/*.md` | On-demand retrieval via `view_file` | Domain knowledge from JJ Geewax, Bruno Pedro, and UET curriculum standards. |
| **Tier 3** | **Active Production Runbooks** | `.agents/skills/*/SKILL.md` | Progressive disclosure | Loaded selectively when executing the corresponding pipeline step. |

---

## 3. Weekly Deliverable Specification (`weeks/week-XX/`)

Each generated week must be self-contained, reproducible, and strictly follow this directory structure:

```
weeks/week-XX/
├── slide.md                     # 14-slide Marp presentation (Concept -> Problem -> Example -> Comparison)
└── code/                        # Self-contained Node.js microservice demo
    ├── package.json             # Minimal dependencies (express, mongoose, etc.)
    ├── server.js                # Main HTTP server entrypoint
    ├── models/                  # Mongoose domain entity schemas
    │   └── Resource.js
    ├── openapi.yaml             # Single Source of Truth API Contract (OAS 3.0.3)
    ├── postman_collection.json  # Postman v2.1.0 collection with test assertions
    └── README.md                # Quickstart instructions for running service and tests
```

---

## 4. Technology Stack & Standard Conventions

- **Presentation Engine**: [Marp](https://marp.app/) Markdown format with custom responsive themes.
- **Service Layer**: Node.js (>= 18.x LTS), Express.js (v4.x).
- **Persistence Layer**: MongoDB with Mongoose ODM (v8.x). In-memory mock or local instance supported.
- **Contract Specification**: OpenAPI Specification v3.0.3 (YAML format).
- **Verification & Automation**: Postman Collection Schema v2.1.0 executed via Newman CLI.
