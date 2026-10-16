# Fees are rounded to whole cents

## Decision

Every fee is rounded to whole cents when it is calculated, never later. Rounding
in two places once produced fees one cent apart on the receipt and the statement.
