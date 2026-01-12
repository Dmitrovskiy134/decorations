import os
from datetime import datetime
from functools import wraps


def logger(path):
    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            call_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            result = old_function(*args, **kwargs)

            log_entry = (
                f"{call_time} - "
                f"Функция: {old_function.__name__} - "
                f"Аргументы: args={args}, kwargs={kwargs} - "
                f"Результат: {result}\n"
            )

            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)

            return result

        return new_function

    return __logger


class DocumentProcessor:
    @logger('document_processor.log')
    def __init__(self, file_path):
        self.file_path = file_path
        self.content = None
        # Убрали вызов load_file здесь, будем вызывать явно

    @logger('document_processor.log')
    def load_file(self):
        """Загружает содержимое файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
            return True
        except FileNotFoundError:
            self.content = ""
            return False

    @logger('document_processor.log')
    def get_word_count(self):
        """Возвращает количество слов в документе"""
        if not self.content:
            return 0
        words = self.content.split()
        return len(words)

    @logger('document_processor.log')
    def search_word(self, word):
        """Ищет слово в документе"""
        if not self.content:
            return False
        return word.lower() in self.content.lower()

    @logger('document_processor.log')
    def add_text(self, new_text):
        """Добавляет текст к документу"""
        if self.content is None:
            self.content = ""
        self.content += "\n" + new_text
        return len(self.content)


# Пример использования
@logger('app.log')
def main():
    # Сначала создаем файл
    if not os.path.exists('sample.txt'):
        with open('sample.txt', 'w', encoding='utf-8') as f:
            f.write("Это тестовый документ.\nОн содержит несколько слов.")
        print("Создан файл sample.txt")

    # Затем создаем процессор и загружаем файл
    processor = DocumentProcessor('sample.txt')
    processor.load_file()

    print(f"Количество слов: {processor.get_word_count()}")
    print(f"Содержит слово 'документ': {processor.search_word('документ')}")
    print(f"Содержит слово 'Python': {processor.search_word('Python')}")
    print(f"Содержит слово 'тестовый': {processor.search_word('тестовый')}")

    processor.add_text("Добавленный текст для примера.")
    print(f"Новое количество слов: {processor.get_word_count()}")

    return "Обработка завершена успешно"


if __name__ == "__main__":
    # Удаляем старые логи для чистоты теста
    log_files = ['app.log', 'document_processor.log']
    for log_file in log_files:
        if os.path.exists(log_file):
            os.remove(log_file)

    result = main()
    print(f"\n{result}")

    # Показываем логи
    print("\n" + "=" * 50)
    print("Содержимое лога app.log:")
    print("=" * 50)
    with open('app.log', 'r', encoding='utf-8') as log_file:
        print(log_file.read())

    print("\n" + "=" * 50)
    print("Содержимое лога document_processor.log:")
    print("=" * 50)
    with open('document_processor.log', 'r', encoding='utf-8') as log_file:
        print(log_file.read())