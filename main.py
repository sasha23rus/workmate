import argparse
import csv
from tabulate import tabulate

class FileProcessor:
    def __init__(self, files_list: list) -> None:
        self.files_list = files_list

    def read_files_list(self) -> list:
        full_list = []
        for file_path in self.files_list:
            full_list += self.read_csv(file_path)
        return full_list

    def read_csv(self, file_path: str) -> list:
        try:
            with open(file_path, 'r', newline='') as file:
                res = csv.reader(file, delimiter=',')
                next(res)  # пропускаем заголовок
                return list(res)
        except FileNotFoundError:
            print(f'Файл {file_path} не найден')
            return []
        except Exception as e:
            print(f'Ошибка при чтении файла {file_path}: {e}')
            return []


class ReportProcessor:
    def __init__(self, elements_list) -> None:
        self.elements_list = elements_list
        self.reports = {
            'clickbait': self.clickbait,
            # Сюда можно будет добавлять новые отчёты
        }

    def clickbait(self) -> None:
        result_list = []
        for row in self.elements_list:
            ctr = float(row[1])
            retention_rate = float(row[2])
            if ctr > 15 and retention_rate < 40:
                row_formatted = [row[0], row[1], row[2]]
                result_list.append(row_formatted)

        result_list = sorted(result_list, key=lambda x: float(x[1]), reverse=True)

        print(tabulate(result_list, headers=['title', 'ctr', 'retention_rate'], tablefmt="grid"))

    def run_report(self, report_name: str) -> None:
        if report_name in self.reports:
            self.reports[report_name]()
        else:
            print("Неизвестный отчёт")


def main():
    arguments = argparse.ArgumentParser(description="Программа формирования отчётов метрики видео на YouTube")
    # required=True убран для отображения ошибки в случае отсутствия аргумента
    arguments.add_argument('--files', nargs='+', help='Список путей к файлам')
    arguments.add_argument('--report', help='Название отчёта')

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


if __name__ == "__main__":
    main()
