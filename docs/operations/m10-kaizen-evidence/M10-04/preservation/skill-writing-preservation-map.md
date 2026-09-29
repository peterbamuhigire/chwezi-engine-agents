# M10-04-T01 preservation map (pre-change)

SHA-256 of raw bytes; `same-as-dev` compares CRLF-normalised hashes against the dev canonical file of the same relative path. HEAD is the engine commit at capture; restore any file with `git -C <engine> show <HEAD>:<path>`.

## chwezi-dev-engine `skills/sdlc-meta/skill-writing` (HEAD 33574d94a5)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | canonical |
| `references/completion-criteria-and-handoff.md` | 1219 | 26 | `2bb95de06524c8bce123a1c20b4d72dd88b362021aab0ea8d39891b83ced156a` | canonical |
| `references/context-pointer-quality.md` | 1363 | 29 | `3f3a1961594c788e4130020bac442a9638c898b4a286641c537fe8c5e2c93ceb` | canonical |
| `references/generation-template.md` | 5207 | 160 | `2ff48ad2621cce053cc6d2518338bdfae7032201b4d9fd4c2680fba4283fa803` | canonical |
| `references/invocation-ownership.md` | 1355 | 23 | `5e38160c0c98b6c961a403da6b3c35dbb700fd2a312557b5e76710865664f737` | canonical |
| `references/leading-words-and-trigger-design.md` | 1143 | 27 | `8d332aa77a9b386f4a69d8a2e4d11998b06aa13497ea15b3259a99f1ba4dc704` | canonical |
| `references/output-patterns.md` | 1895 | 82 | `099a049fc70b4f3c5103efc2efa171758d7952db54e3fbc74fb3a1aeabe770e4` | canonical |
| `references/prompting-patterns-for-skills.md` | 12020 | 482 | `d9e50689ef32eb17570b928b88560c84e365cd0f425a2f5e1d1c40f6d9b25c31` | canonical |
| `references/skill-authoring-best-practices.md` | 24343 | 933 | `a3f94bb70e2a0aef8883a04cb2d15fe9dbf0f09f6275ca1220825b30f618fecf` | canonical |
| `references/source-distillation-and-copyright.md` | 3551 | 77 | `ece91e92f4b607962f2fccc40b08ea72d8a4839d77cfc43c5c290e1197874bfc` | canonical |
| `references/two-loads-and-context-budget.md` | 1251 | 25 | `62dcc6310b8d0bb438a422c1da4609495fe5d7206e309f88a23a6c29dfba91fe` | canonical |
| `references/universal-agent-skill-architecture.md` | 6048 | 118 | `0c0fd99a302e67b68f9c2f61cf0b8e25fb53c7e61472fcabff9e365d7f71cc8a` | canonical |
| `references/workflows.md` | 845 | 27 | `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09` | canonical |
| `scripts/contract_gate.py` | 13456 | 414 | `662a048124f73705197ac37dcf261370bc3c523ad3fc92e1f28776d59e865b92` | canonical |
| `scripts/fix_mojibake.py` | 3490 | 99 | `771c07894772c05def4f6a8911add071b6eb4a86132a619e58f67b79a4819f0a` | canonical |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | canonical |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | canonical |
| `scripts/quick_validate.py` | 9806 | 270 | `673057d63aad23db16fbe7fab6f24225e7c5db25a68a2d2b55bc488fad3be058` | canonical |
| `scripts/split_oversized_skills.py` | 2893 | 89 | `86d9f2885fff9021d142a0d9b277b4eee1c55c3beb45673e0d95397110f56cdd` | canonical |
| `scripts/upgrade_dual_compat.py` | 7996 | 204 | `fc22edc04cf0c72a9233cbe6859fa4e983d3aa6d6cd5a6a0324ba962150a7981` | canonical |
| `SKILL.md` | 17556 | 353 | `a08948a75e0ab67e93c01c7804d1921ad1d8a90455360ce5e5c1ea85efc5913b` | canonical |

## digital-research-engine `skills/skill-writing` (HEAD 2aa54bcdfd)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | yes |
| `references/generation-template.md` | 5207 | 160 | `2ff48ad2621cce053cc6d2518338bdfae7032201b4d9fd4c2680fba4283fa803` | yes |
| `references/output-patterns.md` | 1895 | 82 | `099a049fc70b4f3c5103efc2efa171758d7952db54e3fbc74fb3a1aeabe770e4` | yes |
| `references/prompting-patterns-for-skills.md` | 12020 | 482 | `d9e50689ef32eb17570b928b88560c84e365cd0f425a2f5e1d1c40f6d9b25c31` | yes |
| `references/skill-authoring-best-practices.md` | 24343 | 933 | `a3f94bb70e2a0aef8883a04cb2d15fe9dbf0f09f6275ca1220825b30f618fecf` | yes |
| `references/workflows.md` | 845 | 27 | `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09` | yes |
| `scripts/contract_gate.py` | 13044 | 412 | `b61d6c7c8ff7067b9790ece6ed31eca4106fb91553164d063ebdd6e69624ce8e` | no |
| `scripts/fix_mojibake.py` | 1960 | 68 | `c81cae9ce30addd82987e363f3eb9780c7ee63c18cff1420a1ec18dea682fed8` | no |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | yes |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | yes |
| `scripts/quick_validate.py` | 7996 | 241 | `e7648b406093b1bd0b30d99f49a4f13b940cb44bbbc7abfc157976effb050345` | no |
| `scripts/split_oversized_skills.py` | 2893 | 89 | `86d9f2885fff9021d142a0d9b277b4eee1c55c3beb45673e0d95397110f56cdd` | yes |
| `scripts/upgrade_dual_compat.py` | 9169 | 219 | `3a7de23a851c52e0b0f5fb6a60d7d0dae2f0232c0707e9e889545c611bc1e3bb` | no |
| `SKILL.md` | 9838 | 247 | `a651be42eb2461f98e0c69b851e20b3074d15bf107a5e657508f6f957d467576` | no |

## social-media-skills `skills/meta-utility/skill-writing` (HEAD 52399fc556)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | yes |
| `references/output-patterns.md` | 1895 | 82 | `099a049fc70b4f3c5103efc2efa171758d7952db54e3fbc74fb3a1aeabe770e4` | yes |
| `references/prompting-patterns-for-skills.md` | 12020 | 482 | `d9e50689ef32eb17570b928b88560c84e365cd0f425a2f5e1d1c40f6d9b25c31` | yes |
| `references/skill-authoring-best-practices.md` | 24483 | 933 | `524616f9915568a6763594905d5e88ff910564958817226094088909d026c1ec` | no |
| `references/workflows.md` | 845 | 27 | `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09` | yes |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | yes |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | yes |
| `scripts/quick_validate.py` | 3617 | 94 | `b4f8d934d887a98418e24f86da22f20fbc9dda4e664b7ad7101cd85e0fddabf8` | no |
| `SKILL.md` | 10580 | 193 | `11ceaee95214c912d20b25b827f4db902238267305fe681a60d50f1493d2abab` | no |

## website-skills `skills/meta/skill-writing` (HEAD 26677c5f2d)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | yes |
| `references/generation-template.md` | 5264 | 160 | `51c96916015e05595dfdb296520ffa976d07e54b4b8d655b8e2db3e65d7e1a38` | no |
| `references/legacy-guidance.md` | 24040 | 514 | `555707cca3e662d048b50616e48adb8a95fba22b626c5b777fdabbb962a3e881` | absent-in-dev |
| `references/output-patterns.md` | 1895 | 82 | `099a049fc70b4f3c5103efc2efa171758d7952db54e3fbc74fb3a1aeabe770e4` | yes |
| `references/prompting-patterns-for-skills.md` | 12020 | 482 | `d9e50689ef32eb17570b928b88560c84e365cd0f425a2f5e1d1c40f6d9b25c31` | yes |
| `references/skill-authoring-best-practices.md` | 24797 | 933 | `003711b99b8d0409f510c149593adb79209c25c93a22c170726d6cbb6ffc9422` | no |
| `references/workflows.md` | 845 | 27 | `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09` | yes |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | yes |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | yes |
| `scripts/quick_validate.py` | 3617 | 94 | `b4f8d934d887a98418e24f86da22f20fbc9dda4e664b7ad7101cd85e0fddabf8` | no |
| `SKILL.md` | 5734 | 121 | `161707adf6738ea280d69a9f32b9ecff2cb95fff716a4b6766d4b630e6ac7147` | no |

## business-plan-skills `skills/meta-utility/skill-writing` (HEAD 7b21210b22)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | yes |
| `references/dual-compatible-skill-template.md` | 3836 | 108 | `8bf28d58c62fd04d8346171132865a4daecae4aa77fed523f89f76623599fd6e` | absent-in-dev |
| `references/dual-surface-migration-rules.md` | 2334 | 36 | `ee313c68824492f2058d53d79e11e1220b1e82313fa95f2d5959551fc02d0792` | absent-in-dev |
| `references/output-patterns.md` | 1895 | 82 | `099a049fc70b4f3c5103efc2efa171758d7952db54e3fbc74fb3a1aeabe770e4` | yes |
| `references/prompting-patterns-for-skills.md` | 12020 | 482 | `d9e50689ef32eb17570b928b88560c84e365cd0f425a2f5e1d1c40f6d9b25c31` | yes |
| `references/skill-authoring-best-practices.md` | 24343 | 933 | `a3f94bb70e2a0aef8883a04cb2d15fe9dbf0f09f6275ca1220825b30f618fecf` | yes |
| `references/workflows.md` | 845 | 27 | `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09` | yes |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | yes |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | yes |
| `scripts/quick_validate.py` | 3793 | 86 | `95fc20e708e03fc80f9bfff36742c5899f9904ca6b290733d522f5547e53487c` | no |
| `SKILL.md` | 9108 | 118 | `2c2e98dc40e3aea9894d940ed3ee3b4c5f16c2f4edc059fe4bd8ef4fdaf1fc90` | no |

## linux-skills `meta/skill-writing` (HEAD 42b3c1b7e7)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | yes |
| `references/generation-template.md` | 5207 | 160 | `2ff48ad2621cce053cc6d2518338bdfae7032201b4d9fd4c2680fba4283fa803` | yes |
| `references/output-patterns.md` | 1895 | 82 | `099a049fc70b4f3c5103efc2efa171758d7952db54e3fbc74fb3a1aeabe770e4` | yes |
| `references/prompting-patterns-for-skills.md` | 12020 | 482 | `d9e50689ef32eb17570b928b88560c84e365cd0f425a2f5e1d1c40f6d9b25c31` | yes |
| `references/skill-authoring-best-practices.md` | 24343 | 933 | `a3f94bb70e2a0aef8883a04cb2d15fe9dbf0f09f6275ca1220825b30f618fecf` | yes |
| `references/workflows.md` | 845 | 27 | `82c591fb4d7fe184954c52db7697719c044755cd704fe49904a0350cfa748d09` | yes |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | yes |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | yes |
| `scripts/quick_validate.py` | 3617 | 94 | `b4f8d934d887a98418e24f86da22f20fbc9dda4e664b7ad7101cd85e0fddabf8` | no |
| `SKILL.md` | 6565 | 110 | `d6909793929cd0063cb5d9f953e8b380d2a834f256038a729a33fa1b9da816ca` | no |

## proposal-skills `skills/meta/skill-writing` (HEAD ead7a38ae2)

| File | Bytes | Lines | SHA-256 | same-as-dev |
|---|---:|---:|---|---|
| `LICENSE.txt` | 11558 | 201 | `49bbe9114e49214df2ccc324cb3ac8d1d1aa1c3a0947f94c286765e86647b32e` | yes |
| `references/output-patterns.md` | 1942 | 84 | `da9dcb436e055755a950fe6e1e4752ffc45f17eaa00723543d1df0ab3d25e673` | no |
| `references/prompting-patterns-for-skills.md` | 12067 | 484 | `8cd8d3004647b36cb7f7909aa8458806509394cf6f49e8e9e98933a0ddcce67a` | no |
| `references/skill-authoring-best-practices.md` | 24471 | 935 | `b4e75f44bfa03e7f4564dde862c7ae712f7cba3295d4c175f93525bbbc59eac1` | no |
| `references/source-distillation-and-copyright.md` | 4001 | 86 | `5ea55e67662025ce3430a82e574f8b242b9ff74256400798955549b2162423ba` | no |
| `references/workflows.md` | 894 | 30 | `ad85f86d6a7a902db77fa44e6840c16d99374ee532843d7ebc5dc7af9a73983c` | no |
| `scripts/init_skill.py` | 11166 | 303 | `caa5b25a47228d65aec335414cdce1d1e0e4f5a42b34dd1ee327c84719e55074` | yes |
| `scripts/package_skill.py` | 3398 | 110 | `afc74988da979933ab76966a5539d78acc95b734f7201171c97c9edce3cc8966` | yes |
| `scripts/quick_validate.py` | 3617 | 94 | `b4f8d934d887a98418e24f86da22f20fbc9dda4e664b7ad7101cd85e0fddabf8` | no |
| `SKILL.md` | 6775 | 106 | `592d2843bdb3ec97e2d95be7d8384b3f9d4c0b397e8aa4601353790601a095b1` | no |

