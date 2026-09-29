# Technical Approach and Methodology (synthetic sample)

This is a fictional sample built for M10-13-T02 evidence. It is not a client deliverable.

## Solution context

The proposed system sits inside the client organisation and exchanges data with three external services.

<!-- diagram-ir: FIG-001 -->

## Delivery workflow

Delivery follows the ERP sequence in the methodology skill: each phase closes with a finance-owner approval gate before the next begins.

```mermaid
%% alt: Delivery workflow: discovery, posting-rule design, configured prototype, migrated-data rehearsal, user acceptance testing, cutover and first close, each separated by a finance-owner approval gate.
%% caption: Delivery workflow and approval gates
flowchart LR
  d[Discovery] --> g1{Finance-owner approval}
  g1 --> p[Posting-rule design] --> g2{Finance-owner approval}
  g2 --> c[Configured prototype] --> m[Migrated-data rehearsal]
  m --> u[User acceptance testing] --> g3{Go-live approval}
  g3 --> k[Cutover] --> f[First close]
```

Figure numbering, captions and alt text are applied at build time.
