from meeting_miner.engine import extract_actions, extract_decisions, parse_transcript, demo, inspect, run


def test_parse_and_extract():
    lines = parse_transcript("Ada: TODO: write tests\nBen: We decided to launch.\n")
    assert lines[0]["speaker"] == "Ada"
    actions = extract_actions(lines)
    decisions = extract_decisions(lines)
    assert any("write tests" in a["text"] for a in actions)
    assert decisions


def test_run_demo():
    r = run({})
    assert "zAx4hub" in r["author"]
    assert r["metrics"]["actions"] >= 3
    assert r["metrics"]["decisions"] >= 1
    assert demo()["summary"]
    assert inspect()["name"] == "meeting-miner"
