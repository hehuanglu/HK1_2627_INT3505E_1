# ARCHITECTURE.md: SOA Course Material & Agent Pipeline Architecture

This document formalizes the system design, knowledge-caching architecture, and interactive execution pipeline powering the **Service-Oriented Architecture (SOA)** coursework learning and asset generation system.

---

## 1. System Architecture Overview

The system is designed around a **Human-in-the-Loop, Evidence-Driven Pedagogical Architecture**.
It places the **student's deep thinking and hands-on implementation** at the center, guided by the professor's lectures and authoritative textbooks, while leveraging LLMs for critical debate, boilerplate scaffolding, code auditing, automated verification snapshotting, and evidence-based slide synthesis.

```mermaid
flowchart TD
    subgraph KNOWLEDGE["Tier 1 & Tier 2: Static & Cached Knowledge Base"]
        AGENTS["AGENTS.md\n(Always-Active Orchestrator)"]
        SYLLABUS[".agents/context/syllabus.md\n(13-Week Curriculum Schedule)"]
        PATTERNS[".agents/context/api-design-patterns-notes.md\n(JJ Geewax)"]
        PRODUCT[".agents/context/building-api-product-notes.md\n(Bruno Pedro)"]
        GLOSSARY[".agents/context/glossary-soa.md\n(Bilingual Lexicon)"]
        TOOLING[".agents/context/tooling-notes.md\n(Stack Conventions)"]
        TEMPLATE["slides-template/base-marp.md\n(Marp Styling Engine)"]
    end

    subgraph PIPELINE["Tier 3: Master Skill & Interactive 5-Stage Pipeline"]
        MASTER["soa-study-pipeline\n(Master Orchestrator with Logic Gates)"]
        
        SK1["Chặng 1: course-digest\n(Knowledge Filtering & Scenario Alignment)"]
        GATE1{{"Gate 1: SV Duyệt Tri Thức Gốc"}}
        
        SK2["Chặng 2: api-code-scaffold\n(Architecture Debate & Scaffold + TODOs)"]
        GATE2{{"Gate 2: SV Implement Code Hạt Nhân"}}
        
        SK3["Chặng 3: Code Audit\n(Architectural Review & Refinement)"]
        GATE3{{"Gate 3: SV Đồng Thuận Mã Nguồn"}}
        
        SK4["Chặng 4: openapi-writer & postman-collection\n(Verification & Live Snapshots via Newman)"]
        GATE4{{"Gate 4: SV Nghiệm Thu Bằng Chứng"}}
        
        SK5["Chặng 5: weekly-slide-outline\n(Evidence-Based Slide Synthesis -> PDF)"]
        GATE5{{"Gate 5: SV Duyệt Kết Luận -> Xuất PDF"}}
    end

    subgraph OUTPUT["Weekly Deliverables: weeks/week-XX/"]
        subgraph OUT_CODE["code/ (Hands-on Implementation)"]
            OUT_SRV["server.js, models/ & controllers/\n(Express.js + Mongoose + Core Pattern)"]
            OUT_OAS["openapi.yaml\n(Audited OpenAPI 3.0.3 Contract)"]
            OUT_PST["postman_collection.json\n(Test Suite with Assertions)"]
            OUT_SNAP["Live Snapshots\n(Logs, HTTP Payloads, Newman PASS)"]
        end
        OUT_SLIDE["slide.md\n(Marp Deck: Problem -> Core Code -> Snapshots -> Conclusions)"]
        OUT_PDF["slide.pdf\n(Official Classroom Presentation PDF)"]
    end

    KNOWLEDGE --> MASTER
    MASTER --> SK1 --> GATE1
    GATE1 --> SK2 --> GATE2
    GATE2 --> SK3 --> GATE3
    GATE3 --> SK4 --> GATE4
    GATE4 --> SK5 --> GATE5
    
    GATE3 --> OUT_SRV
    SK4 --> OUT_OAS
    SK4 --> OUT_PST
    SK4 --> OUT_SNAP
    OUT_SNAP --> SK5
    OUT_SRV --> SK5
    GATE5 --> OUT_SLIDE
    OUT_SLIDE --> OUT_PDF
```

---

## 2. Gemini Context Caching & Progressive Disclosure Model

To maximize reasoning precision while eliminating token bloat and context dilution, the system organizes information into three distinct tiers:

| Tier | Category | Files | Loading Strategy | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Root Directives** | `AGENTS.md`, `ARCHITECTURE.md` | Auto-loaded at session root | Serves as the static system prompt prefix. Automatically cached by Gemini's prefix caching engine. |
| **Tier 2** | **Cached Knowledge Base** | `.agents/context/*.md`, `slides-template/*.md` | On-demand retrieval via `view_file` | Domain knowledge from JJ Geewax, Bruno Pedro, UET curriculum standards, and tooling guides. |
| **Tier 3** | **Active Production Runbooks** | `.agents/skills/*/SKILL.md` | Progressive disclosure | Loaded selectively when executing the corresponding pipeline step or master orchestrator. |

---

## 3. Weekly Deliverable Specification (`weeks/week-XX/`)

Each generated week is self-contained, reproducible, and strictly follows this directory structure:

```
weeks/week-XX/
├── slide.md                     # Marp presentation (Problem -> Architecture -> Core Code -> Snapshots -> Conclusions)
├── slide.pdf                    # Official presentation PDF generated via Marp CLI
└── code/                        # Self-contained Node.js microservice demo
    ├── package.json             # Minimal dependencies (express, mongoose, dotenv)
    ├── server.js                # Main HTTP server entrypoint & router
    ├── models/                  # Mongoose domain entity schemas
    ├── controllers/             # Business logic & student-implemented core pattern
    ├── openapi.yaml             # Single Source of Truth API Contract (OAS 3.0.3)
    ├── postman_collection.json  # Postman v2.1.0 collection with test assertions
    └── README.md                # Quickstart instructions for running service and tests
```

---

## 4. Technology Stack & Standard Conventions

- **Orchestration**: Custom Agent Skill Architecture with 5-stage human-in-the-loop checkpoints.
- **Service Layer**: Node.js (>= 18.x LTS), Express.js (v4.x).
- **Persistence Layer**: MongoDB with Mongoose ODM (v8.x). In-memory mock or local instance supported.
- **Contract Specification**: OpenAPI Specification v3.0.3 (YAML format).
- **Verification & Automation**: Postman Collection Schema v2.1.0 executed via Newman CLI.
- **Presentation Engine**: [Marp](https://marp.app/) Markdown format with responsive UET styling, exported via Marp CLI.
