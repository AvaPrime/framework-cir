from framework_cir import CIR_VERSION, LANGGRAPH_RULES, apply_rules, ScanResult


def test_cir_version() -> None:
    assert CIR_VERSION.startswith("1.")


def test_apply_rules_hits_state_graph() -> None:
    scan = ScanResult(classes={"StateGraph", "SqliteSaver"})
    anchors = apply_rules(scan, LANGGRAPH_RULES)
    claims = {a.claim for a in anchors}
    assert any("state_graph" in c for c in claims)
    assert any("sqlite_checkpoint" in c for c in claims)
