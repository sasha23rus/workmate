import sys

from main import main


def test_main_requires_files(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["prog"])
    main()
    assert "аргумент --files" in capsys.readouterr().out


def test_main_requires_report(monkeypatch, capsys, tmp_path):
    csv_path = tmp_path / "empty_args.csv"
    csv_path.write_text("title,ctr,retention_rate\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--files", str(csv_path)],
    )
    main()
    assert "аргумент --report" in capsys.readouterr().out


def test_main_no_data_after_read(monkeypatch, capsys, tmp_path):
    """Только заголовок — данных нет, full_list пуст после read."""
    csv_path = tmp_path / "only_header.csv"
    csv_path.write_text("title,ctr,retention_rate\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--files", str(csv_path), "--report", "clickbait"],
    )
    main()
    assert "не удалось прочитать файлы" in capsys.readouterr().out


def test_main_success_clickbait(monkeypatch, capsys, tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "title,ctr,retention_rate\n"
        "skip,10,50\n"
        "cb,22,35\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "--files", str(csv_path), "--report", "clickbait"],
    )
    main()
    out = capsys.readouterr().out
    assert "cb" in out and "skip" not in out
