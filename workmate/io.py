import csv


class FileProcessor:
    def __init__(self, files_list: list[str]) -> None:
        self.files_list = files_list

    def read_files_list(self) -> list[list[str]]:
        full_list: list[list[str]] = []
        for file_path in self.files_list:
            full_list += self.read_csv(file_path)
        return full_list

    def read_csv(self, file_path: str) -> list[list[str]]:
        try:
            with open(file_path, "r", newline="") as file:
                res = csv.reader(file, delimiter=",")
                next(res)  # пропускаем заголовок
                return list(res)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден")
            return []
        except Exception as error:
            print(f"Ошибка при чтении файла {file_path}: {error}")
            return []
