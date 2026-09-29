# Implementation Timeline (synthetic sample)

Fictional sample built for M10-13-T06 evidence. Dates and lead times are illustrative assumptions of this sample, not PPDA statutory periods; verify every lead time against the current PPDA instrument before use.

```mermaid
%% alt: Implementation Gantt for a fictional water-kiosk expansion: procurement evaluation, then the Contracts Committee award as a blocking milestone, then the standstill period and contract signature, after which kiosk construction, staff training and commissioning follow; critical-path tasks are highlighted.
%% caption: Implementation timeline with the PPDA Contracts Committee award as a blocking gate
gantt
  title Kiosk expansion, fictional sample
  dateFormat YYYY-MM-DD
  axisFormat %b %Y
  tickInterval 1month
  section Procurement
  Bid evaluation                      :crit, eval, 2027-01-11, 30d
  Contracts Committee award (gate)    :milestone, crit, award, after eval, 0d
  Standstill and contract signature   :crit, sign, after award, 21d
  section Delivery
  Kiosk construction                  :crit, build, after sign, 60d
  Staff recruitment and training      :train, after sign, 45d
  Commissioning and handover          :milestone, crit, done, after build, 0d
```
