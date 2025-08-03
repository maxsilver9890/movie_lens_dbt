# 🎬 MovieLens Analytics Dashboard

A data visualization dashboard powered by **[Snowflake SQL](https://docs.snowflake.com/)**, **[dbt](https://docs.getdbt.com/)**, and **[Streamlit](https://streamlit.io/)** to analyze MovieLens dataset trends including user behavior, ratings, tags, and top movies.

---

## 🚀 Features

- 📊 **Top Rated Movies** — See the highest-rated movies based on average ratings.
- 👤 **User Engagement** — Track user activity by the number of ratings given.
- 📅 **Ratings Over the Years** — Visualize how rating trends changed over time.
- 🏷️ **Tag Relevance Analysis** — Understand popular tags and their relevance scores.

Each section is interactive and includes:
- Clean charts (bar/line)
- Data tables with filtering
- Stylish UI with icons and layout

---

## 🧱 Tech Stack

|                      Tool                              | Purpose                                 |
|--------------------------------------------------------|-----------------------------------------|
| ❄️ [Snowflake SQL](https://docs.snowflake.com/)       |  Data warehousing and querying          |
| 📦 [dbt (Data Build Tool)](https://docs.getdbt.com/)  | Data transformation and modeling        |
| 🧠 [Streamlit](https://docs.streamlit.io/)            | Frontend dashboard framework            |
| 🐍 Python + pandas                                    | Query handling and plotting             |

---
```
## 📁 Project Structure
📦 movie_lens_dbt
├── netflix/                  # Main project folder
│   ├── models/               # dbt models (SQL transformations)
│   │   ├── staging/          # Staging models
│   │   ├── marts/            # Business logic 
│   │   └── dim/              # Dimension dbt models
│   │   └── fct/              # Fact dbt models
│   ├── analyses/             # dbt analyses 
│   ├── tests/                # dbt tests (custom or generic)
│   ├── snapshots/            # Snapshot models 
│   ├── seeds/                # Raw CSV seed files
│   ├── macros/               # Reusable dbt macros
│   ├── app1.py               # Streamlit dashboard
│   ├── queries1.py           # SQL query strings for app
│   └── .env                  # Environment variables (credentials, etc.)
│
├── dbt_packages/             # Auto-managed dbt dependencies
├── target/                   # dbt build artifacts (ignored)
├── logs/                     # Logs (ignored)
├── .gitignore
├── README.md
└── requirements.txt          # Python packages for Streamlit app
```


## ⚙️ How to Run Locally

1. **Clone the repo**
   git clone https://github.com/maxsilver9890/movie_lens_dbt.git
   cd movie_lens_dbt/netflix

2. Create and activate virtual environment
    python -m venv venv
    venv\Scripts\activate   # On Windows

3. Install dependencies
    pip install -r requirements.txt
    Set up Snowflake credentials
    (Already managed inside app.py or use .env file)

4. Set up Snowflake credentials
    (Already managed inside app.py or use .env file)

5. Launch Streamlit app
    streamlit run app.py


# 🚀 Project Summary: MovieLens Analytics with Snowflake, dbt & Streamlit

This project showcases a full-stack modern data workflow using **Snowflake**, **dbt**, and **Streamlit**, applied to the [MovieLens dataset](https://grouplens.org/datasets/movielens/). It covers everything from data modeling and testing to documentation and dashboarding.
---
### 🛠️ Workflow Overview
```
flowchart TD
  A[📦 Raw Data in Snowflake] --> B[🔧 dbt Models & Transformations]
  B --> C[📄 dbt Docs & Testing]
  C --> D[📊 Streamlit Dashboard]
```

Useful Resources
📘 MovieLens Dataset : https://grouplens.org/datasets/movielens/
🧊 Snowflake Docs : https://docs.snowflake.com/
🧮 dbt Docs : https://docs.getdbt.com/
💡 Streamlit Docs : https://docs.streamlit.io/



👨‍💻 Author
Prateek Saxena
🎓 B.Tech ECE Student
💼 Passionate about data storytelling & full-stack analytics
🔗 GitHub Profile : https://github.com/maxsilver9890

📝 License
This project is licensed under the MIT License.
