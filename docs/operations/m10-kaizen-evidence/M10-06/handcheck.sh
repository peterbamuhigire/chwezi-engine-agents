#!/usr/bin/env bash
# Independent hand check: print every definition site of a procedure and the raw
# table-bearing lines of its body (up to the next DELIMITER / CREATE), for a human to read.
cd /c/wamp64/www/Garage || exit 1
for p in "$@"; do
  echo "######## $p"
  grep -rlis --include=*.sql -E "create +(definer=[^ ]+ +)?procedure +(if not exists +)?\`?$p\`? *\(" database | sort | while read -r f; do
    echo "--- defined in $f"
    awk -v P="$p" 'BEGIN{IGNORECASE=1; on=0}
      on==1 && (/^[[:space:]]*DELIMITER/ || /create +(definer=[^ ]+ +)?procedure/) {on=0}
      tolower($0) ~ ("procedure +`?" tolower(P) "`? *\\(") {on=1}
      on==1 && /(from|join|into|update|call) +`?[a-z_]/ {print "    " NR ": " $0}' "$f" | cut -c1-160
  done
done
