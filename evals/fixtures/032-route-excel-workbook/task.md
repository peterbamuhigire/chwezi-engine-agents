# Contract-eval fixture 032-route-excel-workbook

Case: `evals/cases/032-route-excel-workbook.yaml` (route oracle; family: spreadsheet (dev vs research vs finance)).

## Task given to the host

Build an Excel workbook with formulas, charts and data validation for the monthly stock count.

## Expected first skill

`chwezi-dev-engine/excel-spreadsheets`

## Engines in scope

- `chwezi-dev-engine`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.

Known defect pinned to later-wave; counted separately from primary@1.
