from identity_models.comparison import run_comparison


def test_comparison_snapshot() -> None:
    results = run_comparison()
    assert len(results) == 5

    salary_alice = results[0]
    assert salary_alice["query"] == "salary"
    assert salary_alice["user_id"] == "alice@co"
    assert salary_alice["assistant"]["pages"] == ["Alice Chen — Compensation"]
    assert salary_alice["claw"]["pages"] == []

    salary_bob = results[1]
    assert salary_bob["assistant"]["pages"] == ["Bob Martinez — Compensation"]

    roadmap_alice = results[2]
    assert "Q3 Roadmap (Team)" in roadmap_alice["assistant"]["pages"]
    assert "Exec Only" not in " ".join(roadmap_alice["assistant"]["pages"])
    assert any("Exec Only" in page for page in roadmap_alice["claw"]["pages"])

    memory = results[4]["memory"]
    assert memory["assistant_alice"] == ["salary", "Q3 roadmap"]
    assert memory["assistant_bob"] == ["salary", "Q3 roadmap"]
    assert len(memory["claw"]) == 4