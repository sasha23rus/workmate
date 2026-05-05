import argparse

from .io import FileProcessor
from .reports import ReportProcessor


def main() -> None:
    arguments = argparse.ArgumentParser(
        description="Программа формирования отчётов метрики видео на YouTube"
    )
    # required=True убран для отображения ошибки в случае отсутствия аргумента
    arguments.add_argument("--files", nargs="+", help="Список путей к файлам")
    arguments.add_argument("--report", help="Название отчёта")

    args = arguments.parse_args()

    if not args.files:
        print("Ошибка: аргумент --files не может быть пустым")
        return
    if not args.report:
        print("Ошибка: аргумент --report не может быть пустым")
        return

    full_list = FileProcessor(args.files).read_files_list()

    if not full_list:
        print("Ошибка: не удалось прочитать файлы")
        return

    report_processor = ReportProcessor(full_list)
    report_processor.run_report(args.report)
