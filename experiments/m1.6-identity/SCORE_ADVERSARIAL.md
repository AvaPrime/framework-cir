# M1.6-B adversarial score (binder frozen)

Original nine-case 9/9 is not revised.

| Case | Theory | Binder | |
|---|---|---|---|
| reordered-persist-restore | bound | bound | pass |
| renamed-owner | bound | bound | pass |
| nested-module-path | bound | bound | pass |
| write-read-unlisted-verbs | bound | bound | pass |
| extra-same-verb-other-owner | unbound | unbound | pass |
| partial-owner | insufficient_evidence | insufficient_evidence | pass |
| unlisted-verbs-only (`snapshot`/`hydrate`) | bound | insufficient_evidence | **false insufficient** |
| pair-plus-noise (3 observations) | bound | insufficient_evidence | **false insufficient** |

6/8 pass. False-bound: **0**. Failures are abstentions.

## Reading

The 9/9 result survives reorder, owner rename, nested paths, and new nouns *when write/read is still labeled*. It does not survive:

- complementary lifecycle with verbs outside `_COMPLEMENTS` and without write/read tags;
- a same-owner pair buried in a larger observation bag (`bind` scores pairs only).

Those are the fixture-cleanliness limits. They are not a reason to reopen smolagents or to wire `bind` into `reconstruct()`.
