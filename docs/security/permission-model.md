# Permission model

Operations are classified before dispatch:

| Class | Examples | Permission |
| --- | --- | --- |
| read | Read routers, files, Git metadata, and catalog entries. | Default. |
| validate | Run a declared validator in its declared checkout. | Requires shell and a readable dependency; no mutation approval is implied. |
| approved_write | Install, update, uninstall, pull, edit, submit, publish. | Explicit host confirmation. |
| blocked | Reset, clean, force-push, arbitrary shell, broad deletion, unapproved external message. | Always denied by this package. |

Every approved write records `requested_by`, `approved`, `target_repo`,
`target_branch`, `operation`, `confirmation_id`, `before_head`, `after_head`,
`result`, and a rollback action. A host without an approval channel is
read-only for this package.
