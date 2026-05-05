import builtins

from workmate import FileProcessor


def test_read_csv_skips_header_and_returns_rows(make_csv_file):
    path = make_csv_file(
        "one.csv",
        "A,10,50\nB,20,30\n",
    )
    fp = FileProcessor([])
    rows = fp.read_csv(str(path))
    assert rows == [["A", "10", "50"], ["B", "20", "30"]]


def test_read_csv_file_not_found_returns_empty_and_message(capsys):
    fp = FileProcessor([])
    rows = fp.read_csv("/nonexistent/path/___missing___.csv")
    assert rows == []
    captured = capsys.readouterr()
    assert "не найден" in captured.out


def test_read_csv_generic_error_returns_empty(monkeypatch, capsys):
    def bad_open(*_a, **_kw):
        raise OSError("simulated read failure")

    monkeypatch.setattr(builtins, "open", bad_open)
    fp = FileProcessor([])
    rows = fp.read_csv("any.csv")
    assert rows == []
    assert "Ошибка при чтении" in capsys.readouterr().out


def test_read_files_list_merges_multiple_files(make_csv_file):
    p1 = make_csv_file("a.csv", "x,1,1\n")
    p2 = make_csv_file("b.csv", "y,2,2\n")
    fp = FileProcessor([str(p1), str(p2)])
    assert fp.read_files_list() == [["x", "1", "1"], ["y", "2", "2"]]
