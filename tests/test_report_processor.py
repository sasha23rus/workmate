from workmate import ReportProcessor


def test_clickbait_filters_and_sorts_by_ctr_desc(capsys):
    rows = [
        ["low_ctr", "10", "20"],
        ["hit1", "25", "30"],
        ["hit2", "30", "20"],
        ["high_retention", "20", "50"],
        ["boundary_ctr", "15", "30"],
        ["boundary_ret", "16", "40"],
    ]
    rp = ReportProcessor(rows)
    rp.clickbait()
    out = capsys.readouterr().out
    assert "hit2" in out and "hit1" in out
    assert "low_ctr" not in out
    assert "high_retention" not in out
    assert "boundary_ctr" not in out
    assert "boundary_ret" not in out
    pos_hi2 = out.index("hit2")
    pos_hi1 = out.index("hit1")
    assert pos_hi2 < pos_hi1


def test_run_report_known_invokes_clickbait(capsys):
    rows = [["t", "20", "30"]]
    rp = ReportProcessor(rows)
    rp.run_report("clickbait")
    assert capsys.readouterr().out.strip() != ""


def test_run_report_unknown_prints_message(capsys):
    rp = ReportProcessor([])
    rp.run_report("no_such_report")
    assert "Неизвестный отчёт" in capsys.readouterr().out
