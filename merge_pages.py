import os
import json

def merge_json_files(input_folder, output_file):
    """
    Объединяет все JSON-файлы в папке в один JSON-файл.
    
    :param input_folder: Путь к папке с JSON-файлами.
    :param output_file: Путь к выходному JSON-файлу.
    """
    merged_data = []
    
    # Перебираем файлы в папке
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):  # Проверяем, является ли содержимое списком
                        merged_data.extend(data)
                    else:
                        print(f"Файл {filename} пропущен: данные не являются списком.")
            except Exception as e:
                print(f"Ошибка при обработке файла {filename}: {e}")

    # Сохраняем объединенные данные в выходной файл
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)
        print(f"Данные успешно объединены в файл {output_file}")
    except Exception as e:
        print(f"Ошибка при сохранении выходного файла: {e}")

# if __file__ == "__main__":
#     merge_json_files('./parsers/dns/result/pages', './parsed_feedbacks/all_DNS_pages.json')
#     print("Files were merged.")
merge_json_files('./parsers/dns/result/pages', './parsed_feedbacks/all_DNS_pages.json')
