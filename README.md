# 💰 Expense Tracker Web App

A simple and intuitive expense tracking web application built with Streamlit. Track your expenses, view transaction history, and analyze spending patterns with interactive charts.

## Features

### 🆕 Add Transactions
- Easy-to-use form for adding new expenses
- Input validation (non-empty names, positive amounts)
- Date picker with default to today
- Category selection (Food, Transport, Other)
- Automatic unique ID generation for each transaction

### 📊 View Transactions
- Complete transaction history in a sortable table
- Quick metrics: total transactions, total spent, average transaction
- Data automatically loads from persistent CSV storage

### 📈 Statistics & Analytics
- Total spending overview
- Interactive bar chart showing spending by category
- Category breakdown with percentages
- Recent transactions summary

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start

1. **Clone or download the project files:**
   ```bash
   # You should have these files:
   # - app.py (main application)
   # - requirements.txt (dependencies)
   # - README.md (this file)
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:**
   - The app will automatically open in your default browser
   - If not, navigate to: `http://localhost:8501`

## Usage Guide

### Adding Your First Transaction
1. Select **"Add Transaction"** from the sidebar
2. Fill in the expense details:
   - **Expense Name**: Description of the expense (e.g., "Coffee at Starbucks")
   - **Amount**: Cost in dollars (must be > 0)
   - **Date**: When the expense occurred (defaults to today)
   - **Category**: Choose from Food, Transport, or Other
3. Click **"Add Transaction"**
4. See confirmation and celebration balloons! 🎉

### Viewing Your Expenses
1. Select **"View Transactions"** from the sidebar
2. See your complete expense history
3. Review summary metrics at the top
4. Transactions are sorted by date (newest first)

### Analyzing Spending Patterns
1. Select **"Statistics"** from the sidebar
2. View your total spending amount
3. Analyze spending by category with the interactive bar chart
4. Check the category breakdown table for detailed percentages
5. Review recent transaction activity

## Data Storage

- All data is automatically saved to `expenses.csv`
- The CSV file is created automatically when you first run the app
- Data persists between app sessions
- You can manually edit the CSV file if needed (be careful with the format!)

## File Structure

```
expense-tracker/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
└── expenses.csv       # Auto-generated data file (created when you add first transaction)
```

## Technical Details

### Dependencies
- **Streamlit**: Web app framework
- **Pandas**: Data manipulation and CSV handling
- **Plotly**: Interactive charts and visualizations
- **UUID**: Unique transaction ID generation

### Data Format
The CSV file contains the following columns:
- `ID`: Unique identifier for each transaction
- `Name`: Description of the expense
- `Amount`: Cost in dollars (float)
- `Date`: Transaction date (YYYY-MM-DD format)
- `Category`: Expense category (Food/Transport/Other)

## Troubleshooting

### App won't start?
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)
- Try: `python -m streamlit run app.py`

### Data not saving?
- Check file permissions in the current directory
- Ensure `expenses.csv` is not open in another program
- Look for error messages in the terminal

### Charts not displaying?
- Ensure Plotly is installed: `pip install plotly`
- Clear browser cache and refresh the page

## Customization

### Adding New Categories
Edit the `CATEGORIES` list in `app.py`:
```python
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Other"]
```

### Changing CSV File Location
Modify the `CSV_FILE` variable in `app.py`:
```python
CSV_FILE = "path/to/your/expenses.csv"
```

## Contributing

Feel free to enhance this app by:
- Adding new expense categories
- Implementing data export features
- Adding more chart types
- Improving the UI/UX
- Adding data filtering and search

## License

This project is open source and available under the MIT License.

---

**Happy expense tracking! 💰📊**
