# SOA Course Syllabus & 15-Week Curriculum Registry

This registry serves as the authoritative curriculum index for the **Service-Oriented Architecture (SOA)** course at **VNU-UET**.
It establishes the cross-reference mapping between academic weeks, design patterns from *API Design Patterns* (JJ Geewax), and API product principles from *Building an API Product* (Bruno Pedro).

---

## 15-Week Curriculum Schedule

| Week | Core Topic | JJ Geewax Pattern Reference | Bruno Pedro Product Principle | Target Output Directory |
| :--- | :--- | :--- | :--- | :--- |
| **Week 01** | **Foundations of SOA & The API-as-a-Product Mindset** | Resource Naming Conventions (Ch. 2) | API-as-a-Product Mindset & DX Hierarchy of Needs | `weeks/week-01/` |
| **Week 02** | **Resource-Oriented Architecture & Standard Methods** | Standard Methods: List, Get, Create, Update, Delete (Ch. 3) | Contract-First / Spec-First Methodology & OpenAPI | `weeks/week-02/` |
| **Week 03** | **Resource Hierarchy, Scoping & Singleton Sub-resources** | Resource Hierarchy & Singleton Sub-resources (Ch. 4, 8) | API Boundary Modeling & Domain-Driven Scoping | `weeks/week-03/` |
| **Week 04** | **Partial Updates & Field Masks** | Partial Updates with FieldMasks (Ch. 5) | Minimizing Payload Overhead & Bandwidth Optimization | `weeks/week-04/` |
| **Week 05** | **Custom Methods & State Transitions** | Custom Methods & Non-CRUD RPC Actions (Ch. 6) | Modeling Workflows vs. Raw Entity Manipulation | `weeks/week-05/` |
| **Week 06** | **Long-Running Operations (LRO) & Async Workflows** | Long-Running Operations & Polling Patterns (Ch. 7) | Managing High-Latency Operations & Client Expectation | `weeks/week-06/` |
| **Week 07** | **Rerunnable Jobs & Idempotency Key Pattern** | Rerunnable Requests & Idempotency Keys (Ch. 9) | Fault-Tolerant Distributed Integration & Reliability | `weeks/week-07/` |
| **Week 08** | **Pagination: Cursor/Token-Based vs. Offset/Limit** | Token/Cursor-Based Pagination (Ch. 10) | Query Performance at Scale & SLA Guarantees | `weeks/week-08/` |
| **Week 09** | **Filtering, Searching & Structured Querying** | Filtering, Ordering & Search Syntax (Ch. 11) | Developer Experience: Ergonomic Search Interfaces | `weeks/week-09/` |
| **Week 10** | **Soft Deletion & Undelete Patterns** | Soft Deletion, Trash & Undelete (Ch. 12) | Audit Trails, Compliance & Data Governance | `weeks/week-10/` |
| **Week 11** | **Association Resources & Many-to-Many Relationships** | Association Resources & Relationship Entities (Ch. 13) | Graph vs. Relational API Representation | `weeks/week-11/` |
| **Week 12** | **Request Validation, Dry-Run & Safe Mutations** | Validation-Only & Dry-Run Operations (Ch. 14) | Preventing Mutation Errors in Complex Workflows | `weeks/week-12/` |
| **Week 13** | **API Versioning, Evolution & Deprecation** | Semantic Versioning & Non-Breaking Changes (Ch. 15) | Sunset Headers, Deprecation Schedules & Migration DX | `weeks/week-13/` |
| **Week 14** | **API Gateway, Rate Limiting & Security Governance** | Security Context & Gateway Routing Patterns | Traffic Shaping, Quota Tiers & OAuth2/JWT Access | `weeks/week-14/` |
| **Week 15** | **Distributed Observability & Course Retrospective** | System Health Check & Telemetry Patterns | Distributed Tracing, Logs, Metrics & SLO Monitoring | `weeks/week-15/` |

---

## Deliverable Quality Checklist per Week
For every entry `weeks/week-XX/`, the generation pipeline must produce:
1. `slide.md`: 14-slide Marp deck adhering to `slides-template/base-marp.md`.
2. `code/server.js`: Node.js/Express service highlighting that week's specific pattern.
3. `code/openapi.yaml`: OpenAPI 3.0.3 contract fully describing schemas and status codes.
4. `code/postman_collection.json`: Postman v2.1.0 collection with pre-written `pm.test` assertions.
