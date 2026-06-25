from identity_models.claw import ClawAgent


def test_email_claw_identity_unchanged_by_sender() -> None:
    agent = ClawAgent("email-agent", "you@company.com")
    first = agent.run("Can we meet?", sender="stranger@competitor.com")
    second = agent.run("VP role?", sender="recruiter@agency.io")

    assert first.audit_event is not None
    assert second.audit_event is not None
    assert first.audit_event.principal == second.audit_event.principal == "svc_email_agent"
    assert first.audit_event.triggered_by != second.audit_event.triggered_by
    assert "You (Email Agent)" in first.actor_label