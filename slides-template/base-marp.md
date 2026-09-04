---
marp: true
theme: default
paginate: true
header: "VNU-UET | Service-Oriented Architecture (SOA)"
footer: "Department of Software Engineering"
style: |
  section {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    padding: 40px;
    font-size: 24px;
  }
  h1 {
    color: #003366;
  }
  h2 {
    color: #006699;
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 8px;
  }
  footer {
    font-size: 14px;
    color: #888888;
  }
  header {
    font-size: 14px;
    color: #003366;
    font-weight: bold;
  }
  table {
    font-size: 20px;
  }
  th {
    background-color: #003366;
    color: white;
  }
  .highlight {
    background-color: #fff3cd;
    padding: 2px 6px;
    border-radius: 4px;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->
<!-- _header: "" -->
<!-- _footer: "" -->

# [Topic Title: E.g., Cursor-Based Pagination]
### Service-Oriented Architecture (SOA) - Week XX
**Lecturer / Presenter:** [Presenter Name]  
**Faculty of Information Technology - VNU-UET**

<!-- Note: Welcome everyone to this week's seminar. Today we will explore the design pattern, why it matters in distributed systems, and practical implementation details. -->

---

## Agenda & Learning Objectives

1. **The Core Concept**: Architectural definition and industry background.
2. **The Problem**: Failure modes and bottlenecks of naive approaches.
3. **Pattern Design**: Concrete specifications, URI structure, and schemas.
4. **Implementation & Demo**: Express.js + Mongoose walkthrough.
5. **Trade-offs & Comparison**: Alternatives and decision criteria.
6. **API-as-a-Product Lens**: Developer Experience (DX) and reliability.

<!-- Note: Outline the presentation flow. Emphasize that we start with the fundamental problem before looking at the code. -->

---

## 1. The Core Concept

- **Pattern Name**: `[Pattern Name]` (*API Design Patterns*, JJ Geewax).
- **Core Definition**:
  > *"[Insert formal definition highlighting loose coupling and resource orientation]"*
- **Primary Goal**: Ensure high predictability, backward compatibility, and optimal performance across distributed service boundaries.

<!-- Note: Clarify the terminology in both English and Vietnamese so the audience has a clear baseline. -->

---

## 2. The Problem: Naive Approach Pitfalls

### What goes wrong without this pattern?
- **Symptom 1**: [E.g., High database latency on deep offsets: `OFFSET 1000000`].
- **Symptom 2**: [E.g., Inconsistent record reads during concurrent inserts].
- **System Impact**:
  - Cascading failures under high load.
  - Degraded Developer Experience (DX) and unpredictable latency spikes.

<!-- Note: Walk through the real-world consequence. Make the pain point vivid for the class. -->

---

## 3. The Solution: Architectural Pattern

### Resource & Interaction Model
- **Endpoint**: `GET /api/v1/resources?pageSize=20&pageToken=eyJpZCI6MTAwfQ==`
- **HTTP Method & Status**: Standard HTTP verbs with semantic status codes.
- **Key Headers**: Relevant custom headers (e.g., `Idempotency-Key`).

```json
{
  "resources": [
    { "id": "res_101", "name": "Example Item" }
  ],
  "nextPageToken": "eyJpZCI6MTAxfQ=="
}
```

<!-- Note: Explain how this contract decouples client complexity from backend database state. -->

---

## 4. Concrete Implementation (Express + Mongoose)

```javascript
// Express controller implementing the pattern
router.get('/resources', async (req, res) => {
  const pageSize = parseInt(req.query.pageSize) || 10;
  const cursor = req.query.pageToken ? decodeCursor(req.query.pageToken) : null;

  const query = cursor ? { _id: { $gt: cursor } } : {};
  const items = await Resource.find(query).limit(pageSize + 1);

  // Compute nextPageToken and return response
  const hasMore = items.length > pageSize;
  res.status(200).json({
    items: items.slice(0, pageSize),
    nextPageToken: hasMore ? encodeCursor(items[pageSize - 1]._id) : null
  });
});
```

<!-- Note: Highlight the key lines on the screen where the pattern logic resides. -->

---

## 5. Trade-offs & Alternatives

| Evaluation Criteria | Naive Approach | Proposed Pattern |
| :--- | :--- | :--- |
| **Read Latency ($O(1)$ vs $O(N)$)** | Degrades with scale ($O(N)$) | Consistent index seek ($O(1)$) |
| **Resilience to Mutations** | Page drift & duplicate items | Stable snapshot consistency |
| **Client Implementation Complexity** | Trivial (`page=1,2,3`) | Requires opaque token tracking |
| **Best Used When** | Static datasets, admin panels | Feeds, large datasets, public APIs |

<!-- Note: Discuss the trade-offs honestly. No pattern is a silver bullet for every use case. -->

---

## 6. The API-as-a-Product Lens (Bruno Pedro)

- **Developer Experience (DX)**:
  - Transparent error payloads (`400 Bad Request` with structured error codes).
  - Predictable Time To First Hello World (TTFHW).
- **Service Level Objectives (SLO)**:
  - Sub-50ms p99 latency by leveraging database indexes directly.
- **Contract Stability**:
  - Encapsulated cursor token allows changing storage backend without breaking client contracts.

<!-- Note: Connect back to the business and product dimension of building APIs. -->

---

<!-- _class: lead -->

## Summary & Discussion (Q&A)

### Key Takeaways:
1. Always align API design with underlying distributed system constraints.
2. Contracts are commitments: avoid leaking internal database details.
3. Choose patterns based on explicit operational trade-offs.

**Questions & Discussion?**
