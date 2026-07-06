# Full-suite paired re-scoring (airline)

- 50 tasks run; **27 tau3 PASS / 23 FAIL**
- **50** tasks lifted; **12** carry a grounded constraint and were paired re-scored
- **1 flips** (tau3 PASS -> preflight FAIL): a stated requirement the DB grade missed

| task | tau3 | preflight | | violated action(s) |
|---|:--:|:--:|---|---|
| 2 | FAIL | PASS |  | — |
| 5 | PASS | PASS | agree | — |
| 6 | PASS | FAIL | **FLIP** | transfer_to_human_agents |
| 13 | PASS | PASS | agree | — |
| 27 | PASS | PASS | agree | — |
| 31 | FAIL | PASS |  | — |
| 35 | FAIL | PASS |  | — |
| 36 | PASS | PASS | agree | — |
| 42 | FAIL | PASS |  | — |
| 43 | PASS | PASS | agree | — |
| 45 | FAIL | PASS |  | — |
| 47 | PASS | PASS | agree | — |

## Flips (the revealed-but-missed set)

### task 6
- `transfer_to_human_agents` fired at turn 7; authorization DENIED — source: *"Under no circumstances do you want to be transferred to another agent."*
