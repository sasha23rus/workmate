import pytest


@pytest.fixture
def csv_header_line() -> str:
    return "title,ctr,retention_rate\n"


@pytest.fixture
def make_csv_file(csv_header_line, tmp_path):
    def _write(name: str, body: str):
        path = tmp_path / name
        path.write_text(csv_header_line + body, encoding="utf-8")
        return path

    return _write
