import requests
import re
import multiprocessing
import matplotlib.pyplot as plt
from collections import Counter

# URL для аналізу (можна змінити)
URL = "https://www.gutenberg.org/files/1342/1342-0.txt"  # Приклад: "Гордість і упередження" Джейн Остін

# Функція для завантаження тексту з URL
def fetch_text(url):
    response = requests.get(url)
    response.raise_for_status()  # Перевіряємо, чи запит успішний
    return response.text

# Функція Map: розбиває текст на слова та створює пари (слово, 1)
def map_function(text):
    words = re.findall(r'\b\w+\b', text.lower())  # Виділяємо слова, ігноруємо регістр
    return [(word, 1) for word in words]

# Функція Reduce: підсумовує кількість входжень кожного слова
def reduce_function(word_counts):
    counter = Counter()
    for word, count in word_counts:
        counter[word] += count
    return counter

# Функція для візуалізації результатів
def visualize_top_words(word_counts, top_n=10):
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel("Слова")
    plt.ylabel("Частота використання")
    plt.title(f"Топ-{top_n} найчастіше вживаних слів")
    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    # Завантажуємо текст
    text = fetch_text(URL)

    # Виконуємо MapReduce у багатопоточному режимі
    with multiprocessing.Pool() as pool:
        mapped_data = pool.map(map_function, [text])  # Запускаємо Map у потоках
        flattened_data = [pair for sublist in mapped_data for pair in sublist]  # Розгортаємо список списків
        word_counts = reduce_function(flattened_data)  # Reduce: підрахунок частоти

    # Візуалізуємо результат
    visualize_top_words(word_counts, top_n=10)
