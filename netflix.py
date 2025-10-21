import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Настройки
pd.set_option('display.max_columns', None)
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Путь к данным (в volume)
DATA_FILE = "data/netflix_titles.csv"

# Загрузка
df = pd.read_csv(DATA_FILE)
print(f"Downloaded: {df.shape[0]} rows, {df.shape[1]} columns")

# --- Предобработка ---
print("\n=== Предобработка ===")
print("Пропуски до:")
print(df.isnull().sum())

# Удаляем строки без даты добавления или рейтинга
df = df.dropna(subset=['date_added', 'rating'])

# Заполняем пропуски в других полях
df[['director', 'cast', 'country']] = df[['director', 'cast', 'country']].fillna("Unknown")

# Удаляем дубликаты
df = df.drop_duplicates()

# 🔧 ИСПРАВЛЕНИЕ: убираем пробелы и парсим дату
df['date_added'] = df['date_added'].astype(str).str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

# Удаляем строки, где дата не распарсилась (остались NaT)
df = df.dropna(subset=['date_added'])

print("Пропуски после:")
print(df.isnull().sum().sum(), "осталось")
print(f"Новый размер: {df.shape}")

# Извлекаем год добавления
df['year_added'] = df['date_added'].dt.year

# Обработка длительности
def parse_duration(duration):
    if pd.isna(duration):
        return np.nan
    s = str(duration).strip()
    if 'min' in s:
        return int(s.split()[0])
    elif 'Season' in s:
        return int(s.split()[0])
    return np.nan

df['duration_num'] = df['duration'].apply(parse_duration)
df['is_tv_show'] = (df['type'] == 'TV Show').astype(int)

# --- Аналитические запросы ---
print("\n=== Аналитические запросы ===")
queries = []

q1 = df['type'].value_counts(normalize=True) * 100
queries.append(("1. Доля фильмов и сериалов", q1))

q2 = df['year_added'].value_counts().idxmax()
queries.append(("2. Год с наибольшим количеством добавлений", q2))

top_country = df['country'].str.split(',').explode().value_counts().index[0]
queries.append(("3. Страна-лидер", top_country))

q4 = df['rating'].value_counts().idxmax()
queries.append(("4. Самый популярный рейтинг", q4))

avg_movie = df[df['type'] == 'Movie']['duration_num'].mean()
queries.append(("5. Средняя длительность фильмов (мин)", round(avg_movie, 1)))

avg_seasons = df[df['type'] == 'TV Show']['duration_num'].mean()
queries.append(("6. Среднее число сезонов у сериалов", round(avg_seasons, 2)))

corr_years = df[['release_year', 'year_added']].corr().iloc[0, 1]
queries.append(("7. Корреляция release_year и year_added", round(corr_years, 3)))

tv_by_year = df[(df['year_added'] >= 2015) & (df['year_added'] <= 2021)].groupby('year_added')['is_tv_show'].mean()
queries.append(("8. Доля сериалов (2015-2021)", tv_by_year.round(3)))

top_directors = df[df['director'] != 'Unknown']['director'].str.split(',').explode().value_counts().head(3)
queries.append(("9. Топ-3 режиссёра", top_directors))

dec_content = df[df['date_added'].dt.month == 12]['type'].value_counts()
queries.append(("10. Контент в декабре", dec_content))

for q, ans in queries:
    print(f"\n{q}:")
    print(ans)

# --- Визуализации ---
print("\n=== Генерация визуализаций ===")
os.makedirs("plots", exist_ok=True)

# Гистограммы
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
sns.histplot(df[df['type'] == 'Movie']['duration_num'].dropna(), bins=30, kde=True, color='skyblue')
plt.title('Длительность фильмов')
plt.xlabel('Минуты')

plt.subplot(1, 2, 2)
sns.histplot(df[df['type'] == 'TV Show']['duration_num'].dropna(), bins=10, kde=True, color='salmon')
plt.title('Сезоны у сериалов')
plt.xlabel('Количество сезонов')
plt.tight_layout()
plt.savefig("plots/histograms.png")
plt.close()

# Boxplots
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.boxplot(data=df[df['type'] == 'Movie'], y='duration_num', color='lightblue')
plt.title('Фильмы: выбросы')

plt.subplot(1, 2, 2)
sns.boxplot(data=df[df['type'] == 'TV Show'], y='duration_num', color='lightcoral')
plt.title('Сериалы: выбросы')
plt.tight_layout()
plt.savefig("plots/boxplots.png")
plt.close()

# Barplots
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
top_countries = df['country'].str.split(',').explode().value_counts().head(10)
sns.barplot(x=top_countries.values, y=top_countries.index, palette='viridis')
plt.title('Топ-10 стран')
plt.xlabel('Контент')

plt.subplot(1, 2, 2)
rating_counts = df['rating'].value_counts()
sns.barplot(x=rating_counts.values, y=rating_counts.index, palette='magma')
plt.title('Рейтинги')
plt.xlabel('Количество')
plt.tight_layout()
plt.savefig("plots/barplots.png")
plt.close()

# Корреляции
plt.figure(figsize=(8, 6))
num_cols = df[['release_year', 'year_added', 'duration_num']].dropna()
corr = num_cols.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Корреляции')
plt.savefig("plots/correlation_matrix.png")
plt.close()

# Scatter plots
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
sns.scatterplot(data=df, x='release_year', y='year_added', hue='type', alpha=0.6)
plt.title('Год выпуска vs добавления')

plt.subplot(1, 2, 2)
movie_data = df[df['type'] == 'Movie']
sns.scatterplot(data=movie_data, x='release_year', y='duration_num', alpha=0.6, color='green')
plt.title('Фильмы: год vs длительность')
plt.tight_layout()
plt.savefig("plots/scatterplots.png")
plt.close()

# Contingency heatmap
ct = pd.crosstab(df['type'], df['rating'])
plt.figure(figsize=(10, 6))
sns.heatmap(ct, annot=True, fmt='d', cmap='Blues')
plt.title('Тип vs Рейтинг')
plt.savefig("plots/contingency_heatmap.png")
plt.close()

print("✅ Все графики сохранены в папку 'plots/'")