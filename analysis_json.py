import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

np.random.seed(10)

with open("characters.json", "r", encoding="utf-8") as f:
    json_data = json.load(f) 

df = pd.DataFrame(json_data["female_anime_characters"])

print("Статиcтика количества персонажей по цвету волос:")

hair_color_count = df["hair_color"].value_counts()

i = 1
for color, count in hair_color_count.items():
    percent = (count / len(df)) * 100
    print(f"{i}) {color} волосы - {count} персонажей ({int(percent)}%)")
    i += 1
    
plt.figure(figsize=(16, 8))
hair_colors = ["Чёрные",
    "Фиолетовые",
    "Каштановые",
    "Розовые",
    "Голубые",
    "Серебряные",
    "Рыжие",
    "Зелёные",
    "Блонд",
    "Разноцветные",
    "Бирюзовые",
    "Синие",
    ]

diagram2 = plt.bar(hair_colors, hair_color_count, color="pink", alpha= 0.8)
plt.xlabel("Цвет волос персонажа")
plt.ylabel("Количество персонажей")
plt.title("Статистика количества персонажей по цвету их волос", fontweight = 14)

plt.tight_layout()
plt.show()

print(" "  * 20)
print("Статистика персонажей по возрасту:")

age_group_count = df["age_group"].value_counts()

i = 1
for i,  (age_group, count) in enumerate(age_group_count.items(), 1):
    print(f"{i}) {age_group} - {count} персонажей")
    
plt.figure(figsize=(10, 8))
age_groups = ["16-18",
    "18-20",
    "20-25",
    "25-35",
    "40-60",
    "100+",
    ]

diagram = plt.bar(age_groups, age_group_count, color="black", alpha= 0.8)
plt.xlabel("Возраст персонажа")
plt.ylabel("Количество персонажей")
plt.title("Статистика количества персонажей по их возрасту", fontweight = 14)

plt.tight_layout()
plt.show()

print(" " * 20)

print("Рейтинг популярности жанров(своя рандомная генерация данных):")
list_genres = []
for genres in df["genres"]:
    for genre in genres:
        list_genres.append(genre)
different_genres = list(set(list_genres))

genre_popularity = {}
for genre in different_genres:
    popularity = np.random.uniform(30, 95)
    genre_popularity[genre] = popularity
    
sorted_popularity_genres = sorted(genre_popularity.items(), key=lambda x: x[1], reverse=True)

for i,  (genre, popularity) in enumerate(sorted_popularity_genres, 1):
    print(f"{i}) {genre} - {popularity:.1f}%")
    
plt.figure(figsize=(10, 8))
genres_list = [item[0] for item in sorted_popularity_genres]
popularity_list = [item[1] for item in sorted_popularity_genres]

diagram3 = plt.bar(genres_list, popularity_list, color="blue", alpha= 0.8)
plt.xlabel("Жанры")
plt.ylabel("Популярность (%)")
plt.title("Статистика популярности жанров аниме-персонажей", fontweight = 14)
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()