# C2 — cross-host fixture boundary

29 October 2026. Root cause: `Path.drive` follows the executing OS; POSIX interpreted `C:/Windows/win.ini` as a relative filename. `PureWindowsPath.drive` now rejects both drive-absolute and drive-relative forms before resolving the bounded target. UNC, backslash traversal and symlink containment checks remain. Existing failing Windows-path case now passes; two additional regression inputs cover drive-relative and network-share forms. No target operation or model call ran.

The full registered Python replay reports 161 passed, three skipped; snapshot, book-path integrity, three Kaizen cards, union collisions and 77 contract assertions pass. Eight existing shared-asset drift findings remain assigned to C5. MCP changes are independent and tested in C1. Revert this parser/test commit to roll back; no user content was altered.
