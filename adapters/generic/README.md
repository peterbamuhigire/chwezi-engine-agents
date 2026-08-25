# Generic adapter

Use the three Markdown prompts when the host has file access but no native
adapter convention. Load the prompt, inspect the current checkout, and run
the portable PowerShell, POSIX, or Python command only when the host exposes
that capability.

There is no automatic discovery or approval channel in the generic path.
Treat writes, pulls, publication, and external messages as blocked until a
human confirms them. Model/provider configuration is outside this package.
