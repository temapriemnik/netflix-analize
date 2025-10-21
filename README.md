# Netflix Movies and TV Shows — Exploratory Data Analysis

This project performs a comprehensive exploratory data analysis (EDA) of the Netflix content catalog using Python, Pandas, and Seaborn. The analysis includes data cleaning, statistical summaries, 10+ analytical queries, and multiple visualizations (histograms, box plots, scatter plots, correlation matrices, and more).

The solution is containerized with Docker to ensure reproducibility and ease of execution.

## 📁 Dataset

- **Source**: [Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) by Shivam Bansal (Kaggle)
- **Format**: CSV
- **Size**: ~8,800 entries, 12 columns
- **Content**: Metadata for Netflix titles, including type, country, release year, duration, rating, and more.

> ⚠️ **Note**: The dataset file (`netflix_titles.csv`) is **not included** in this repository due to Kaggle's licensing terms. You must download it manually and place it in the `data/` directory.

## 🛠️ Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/) (v2+)

## 🚀 Quick Start

1. **Download the dataset**  
   Go to [Kaggle: Netflix Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows), accept the terms, and download `netflix_titles.csv`.

2. **Place the file in the correct directory**  
   ```bash
   docker compose build
   docker compose up
   ```
