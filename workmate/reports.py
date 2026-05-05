from tabulate import tabulate


class ReportProcessor:
    def __init__(self, elements_list: list[list[str]]) -> None:
        self.elements_list = elements_list
        self.reports = {
            "clickbait": self.clickbait,
            # Сюда можно будет добавлять новые отчёты
        }

    def clickbait(self) -> None:
        result_list: list[list[str]] = []
        for row in self.elements_list:
            ctr = float(row[1])
            retention_rate = float(row[2])
            if ctr > 15 and retention_rate < 40:
                row_formatted = [row[0], row[1], row[2]]
                result_list.append(row_formatted)

        result_list = sorted(result_list, key=lambda x: float(x[1]), reverse=True)

        print(
            tabulate(
                result_list,
                headers=["title", "ctr", "retention_rate"],
                tablefmt="grid",
            )
        )

    def run_report(self, report_name: str) -> None:
        if report_name in self.reports:
            self.reports[report_name]()
        else:
            print("Неизвестный отчёт")
