# M1.7 — Structural role discovery

Question:

> Can complementary semantic roles be derived from structural evidence rather than an increasingly large verb list?

Method names are noise. Observations carry AST/data-flow facts only.

Success: recall rises on useless names (`a`/`b`, `q`/`z`) with **false-bound = 0**.
Failure: false-bound > 0, or recall only when a verb from `_PUT`/`_GET` is present.

Gates: synthetic only. M1 and M1.6 frozen. No `reconstruct()`. No smolagents.
