# Data Visualization — Data Science Job Market (2025)

This project analyzes **2025 Data Science job postings** to explore **in-demand skills**, **salary distributions**, **seniority**, and **work models** (remote / hybrid / on-site), and presents the findings through clear visualizations and (optionally) an interactive app.

---

## Project Goals

The analysis aims to answer questions like:

- Which **skills** (and skill combinations) are most frequently requested in 2025?
- How do job postings distribute across **seniority levels** (Junior / Mid / Senior / Lead)?
- How do **work models** (Remote–Hybrid–On-site) vary by seniority?
- How do **salary ranges** shift across seniority levels, and where is variability highest?
- How much does **location** influence both posting volume and salary patterns?

---

## Key Takeaways (Summary)

- Demand clusters around core technical skills such as **Python**, **SQL**, and **Machine Learning**, indicating a strong “data → analysis → modeling” pipeline across roles.
- Postings tend to be more concentrated at **Senior** levels, while **Junior** opportunities appear more limited in many settings.
- Work model distribution commonly follows: **On-site** (most), **Hybrid** (second), **Remote** (least).
- Salaries generally increase with seniority, while variability grows at higher levels (often influenced by scope, company, and location).
- Location is a strong driver of compensation differences; some cities show higher medians and wider salary spreads.

---

## Repository Structure

- `app.py` — Streamlit app entry point
- `requirements.txt` — Python dependencies
- `data_science_job_posts_2025.csv` — Dataset
- `data_science_analysis_notebook.ipynb` — EDA + analysis notebook
- `poster_analysis.ipynb` — Poster charts / final visual outputs
- `Data Science Careers & Salaries 2025.pdf` — Poster / final export
- `Tuan Doğukan TEKEŞ Project.pdf` — Project report / submission document
- `README.md` — This file

---



# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
