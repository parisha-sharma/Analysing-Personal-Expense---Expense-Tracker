# 💰 Personal Finance Analytics Dashboard

<div align="center">

![Finance Analytics](https://img.shields.io/badge/Finance-Analytics-8b5cf6?style=for-the-badge&logo=python&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-a855f7?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Data%20Analysis-c084fc?style=for-the-badge&logo=mysql&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-f472b6?style=for-the-badge&logo=streamlit&logoColor=white)

### *Interactive expense analytics dashboard powered by SQL and Python*

[Overview](#-overview) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Dashboard](#-dashboard-sections) • [Contributing](#-contributing)

</div>

---

## 📊 Overview

This project builds a **Personal Finance Analytics Dashboard** that transforms raw transaction data into meaningful insights using SQL analysis and interactive visualizations. The system stores expense records in a **MySQL database**, processes analytical queries using **Python and SQL**, and presents results through a **Streamlit-based dashboard** with multiple interactive charts.

The dataset contains **300+ transactions across 12 months** with details including category, payment method, cashback, and transaction value.

### 🎯 Project Goals

- Store and manage expense records using a structured MySQL database
- Perform exploratory data analysis on transaction data using Python
- Write 30 analytical SQL queries to extract meaningful financial patterns
- Visualize spending trends, cashback performance, and payment behavior
- Build an interactive BI-style dashboard using Streamlit and Plotly
- Understand how data analytics can improve personal financial awareness

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 Data Analytics
- MySQL database with 300+ expense transaction records
- 30 analytical SQL queries for financial insights
- Exploratory data analysis with statistical summaries
- Category-wise and monthly spending analysis
- Cashback tracking and efficiency metrics
- High-value transaction detection

</td>
<td width="50%">

### 📈 Interactive Dashboard
- Streamlit-based financial analytics dashboard
- Executive summary with key financial metrics
- Core analytics and advanced insight sections
- Interactive charts using Plotly
- BI-style layout with filters
- Weekday vs weekend spending breakdown

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

<div align="center">

| Library | Purpose | Version |
|---------|---------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Data processing and backend logic | 3.8+ |
| ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) | Expense data storage and SQL analytics | Latest |
| ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Data manipulation and transformation | Latest |
| ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=flat&logo=python&logoColor=white) | Data visualization | Latest |
| ![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat&logo=python&logoColor=white) | Statistical visualizations | Latest |
| ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Interactive web dashboard | Latest |
| ![Plotly](https://img.shields.io/badge/Plotly-3f4f75?style=flat&logo=plotly&logoColor=white) | Interactive charts and visualizations | Latest |

</div>

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- pip package manager

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/parisha-sharma/expense-finance-dashboard.git

# Navigate to project directory
cd expense-finance-dashboard

# Install required dependencies
pip install -r requirements.txt
```

### Requirements File
```txt
streamlit
pandas
numpy
matplotlib
seaborn
plotly
mysql-connector-python
jupyter
```

---

## 🚀 Usage

### 1. Create the MySQL Database

```sql
CREATE DATABASE expense_tracker;
```

### 2. Generate and Insert Expense Data

```bash
python data_generator.py
```

This script creates the `expenses` table, generates 300 realistic transactions, and distributes records across 12 months.

### 3. Run Exploratory Data Analysis

```bash
jupyter notebook

# Open expenses_data_analysis.ipynb
```

This notebook loads data directly from MySQL and covers:
- Dataset overview and statistical summary
- Missing value check
- Date feature engineering (month, year, day of week)
- Category and monthly spending analysis
- Payment method and cashback analysis
- High-value transaction detection
- Correlation matrix and spending distribution

### 4. Launch the Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser.

---

## 📈 Dashboard Sections

<div align="center">

| Section | Description |
|---------|-------------|
| **Executive Summary** | Total spending, total cashback, average transaction value, monthly overview |
| **Core Analytics** | Category-wise spending, monthly trends, payment method distribution, cashback by category |
| **Advanced Insights** | High-value transaction ratio, payment mode efficiency, spending ranges, monthly cashback trends |

</div>

### Key Insights

- **Spending Patterns**: Certain categories consistently dominate overall spending across all months
- **Monthly Variance**: Spending fluctuates significantly month-to-month, revealing seasonal habits
- **Payment Efficiency**: Different payment methods vary meaningfully in cashback returns
- **Transaction Distribution**: A small percentage of transactions account for a disproportionately high share of total spend
- **Cashback Impact**: Cashback rewards can measurably influence optimal payment method choice

---

## 📁 Project Structure

```
expense-finance-dashboard/
│
├── db_config.py                    # Database connection configuration
├── data_generator.py               # Generates and inserts synthetic expense data
├── expenses_data_analysis.ipynb    # EDA notebook with visualizations
├── sql_queries.py                  # 30 SQL analytics queries
├── app.py                          # Streamlit dashboard application
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── LICENSE
```

---

## 🎨 Visualizations

The project includes visualizations across both the EDA notebook and the dashboard:

- 📊 **Bar Charts** - Category-wise spending and transaction count comparison
- 📅 **Line Charts** - Monthly spending trends over the 12-month period
- 🍩 **Pie Charts** - Payment method distribution across transactions
- 💰 **Cashback Analysis** - Cashback earned by category and payment method
- 📈 **Histograms** - Spending distribution across transaction value ranges (with KDE)
- 🔥 **Correlation Heatmap** - Feature relationships across numeric columns
- 📦 **Box Plots** - Outlier detection across spending categories
- 🧾 **Data Tables** - Detailed transaction-level breakdown and summaries

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🔨 Create a new branch (`git checkout -b feature/improvement`)
3. 💾 Commit your changes (`git commit -am 'Add new feature'`)
4. 📤 Push to the branch (`git push origin feature/improvement`)
5. 🔃 Create a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Parisha Sharma**

- GitHub: [@parisha-sharma](https://github.com/parisha-sharma)
- LinkedIn: [parishasharma15](https://www.linkedin.com/in/parishasharma15)

---

## 🌟 Acknowledgments

- Inspired by business intelligence dashboards
- Built as part of learning journey in Data Science
- Demonstrates how SQL and Python can power real financial analytics

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

![Made with Love](https://img.shields.io/badge/Made%20with-❤️-8b5cf6?style=for-the-badge)
![Data Science](https://img.shields.io/badge/Data%20Science-Learning-a855f7?style=for-the-badge)

**Happy Learning! 🚀**

</div>
