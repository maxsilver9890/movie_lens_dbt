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

## 📁 Project Structure
<pre> 📦 <b>movie_lens_dbt</b> ├── <b>netflix/</b> # Main project folder │ ├── <b>models/</b> # dbt models (SQL transformations) │ │ ├── <b>staging/</b> # Staging models │ │ ├── <b>marts/</b> # Business logic (facts, dims) │ │ └── <b>example/</b> # Example dbt models │ ├── <b>analyses/</b> # dbt analyses (optional) │ ├── <b>tests/</b> # dbt tests (custom or generic) │ ├── <b>snapshots/</b> # Snapshot models (if used) │ ├── <b>seeds/</b> # Raw CSV seed files │ ├── <b>macros/</b> # Reusable dbt macros │ ├── <b>app.py</b> # Streamlit dashboard │ ├── <b>queries.py</b> # SQL query strings for app │ └── <b>.env</b> (🔒 ignored) # Environment variables (credentials, etc.) │ ├── <b>dbt_packages/</b> # Auto-managed dbt dependencies ├── <b>target/</b> # dbt build artifacts (ignored) ├── <b>logs/</b> # Logs (ignored) ├── <b>.gitignore</b> ├── <b>README.md</b> └── <b>requirements.txt</b> # Python packages for Streamlit app </pre>




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
