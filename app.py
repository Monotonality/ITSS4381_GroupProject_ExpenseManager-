import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# Constants
CSV_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Shopping", "Grocery", "Other"]

def initialize_csv():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["ID", "Name", "Amount", "Date", "Category"])
        df.to_csv(CSV_FILE, index=False)
        st.success(f"Created new expense file: {CSV_FILE}")

def load_data():
    """Load expense data from CSV file"""
    try:
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            # Ensure Date column is datetime
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        else:
            # Return empty DataFrame with proper columns
            return pd.DataFrame(columns=["ID", "Name", "Amount", "Date", "Category"])
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame(columns=["ID", "Name", "Amount", "Date", "Category"])

def save_transaction(name, amount, date, category):
    """Save a new transaction to CSV file"""
    try:
        # Load existing data
        df = load_data()
        
        # Generate new ID
        if df.empty:
            new_id = 1
        else:
            new_id = df['ID'].max() + 1
        
        # Create new transaction
        new_transaction = {
            "ID": new_id,
            "Name": name,
            "Amount": amount,
            "Date": date,
            "Category": category
        }
        
        # Add to DataFrame
        new_row = pd.DataFrame([new_transaction])
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Save to CSV
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving transaction: {str(e)}")
        return False

def add_transaction_page():
    """Display the Add Transaction page"""
    st.header("💰 Add New Transaction")
    
    # Create form
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Expense Name*", placeholder="e.g., Lunch at restaurant")
            amount = st.number_input("Amount*", min_value=0.01, step=0.01, format="%.2f")
        
        with col2:
            date = st.date_input("Date", value=datetime.now().date())
            category = st.selectbox("Category", CATEGORIES)
        
        submitted = st.form_submit_button("Add Transaction", type="primary")
        
        if submitted:
            # Validation
            if not name.strip():
                st.error("❌ Expense name cannot be empty!")
            elif amount <= 0:
                st.error("❌ Amount must be greater than 0!")
            else:
                # Save transaction
                if save_transaction(name.strip(), amount, date, category):
                    st.success(f"✅ Transaction added successfully!")
                    st.balloons()
                    # Clear form by rerunning
                    st.rerun()

def view_transactions_page():
    """Display the View Transactions page"""
    st.header("📋 View Transactions")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.info("No transactions found. Add your first transaction!")
        return
    
    # Display summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Transactions", len(df))
    with col2:
        st.metric("Total Amount", f"${df['Amount'].sum():.2f}")
    with col3:
        latest_date = df['Date'].max() if not df.empty else "N/A"
        st.metric("Latest Transaction", latest_date)
    
    st.divider()
    
    # Display transactions table
    st.subheader("All Transactions")
    
    # Sort by ID descending (newest first)
    df_display = df.sort_values('ID', ascending=False)
    
    # Format amount column for better display
    df_display['Amount'] = df_display['Amount'].apply(lambda x: f"${x:.2f}")
    
    # Display table
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Name": st.column_config.TextColumn("Expense Name", width="large"),
            "Amount": st.column_config.TextColumn("Amount", width="small"),
            "Date": st.column_config.DateColumn("Date", width="medium"),
            "Category": st.column_config.TextColumn("Category", width="medium")
        }
    )

def statistics_page():
    """Display the Statistics page"""
    st.header("📊 Spending Statistics")
    
    # Load data
    df = load_data()
    
    if df.empty:
        st.info("No transactions found. Add some transactions to see statistics!")
        return
    
    # Convert Date to datetime for better analysis
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Total spending metric
    total_spent = df['Amount'].sum()
    st.metric("💸 Total Amount Spent", f"${total_spent:.2f}")
    
    st.divider()
    
    # Spending by category
    st.subheader("Spending by Category")
    
    category_totals = df.groupby('Category')['Amount'].sum().reset_index()
    category_totals = category_totals.sort_values('Amount', ascending=True)
    
    if not category_totals.empty:
        # Create bar chart
        fig = px.bar(
            category_totals,
            x='Amount',
            y='Category',
            orientation='h',
            title="Total Spending by Category",
            labels={'Amount': 'Amount ($)', 'Category': 'Category'},
            color='Amount',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_tickformat='$,.2f'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Category breakdown table
        st.subheader("Category Breakdown")
        category_display = category_totals.copy()
        category_display['Amount'] = category_display['Amount'].apply(lambda x: f"${x:.2f}")
        category_display['Percentage'] = (category_totals['Amount'] / total_spent * 100).apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            category_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Category": "Category",
                "Amount": "Total Spent",
                "Percentage": "% of Total"
            }
        )
    
    st.divider()
    
    # Time-based statistics
    st.subheader("📅 Time-based Statistics")
    
    # Daily statistics
    daily_stats = df.groupby(df['Date'].dt.date).agg({
        'Amount': ['sum', 'mean', 'count', 'min', 'max']
    }).round(2)
    daily_stats.columns = ['Total', 'Average', 'Count', 'Min', 'Max']
    daily_stats = daily_stats.reset_index()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📅 Daily Average", f"${daily_stats['Total'].mean():.2f}")
        st.metric("📅 Daily Highest", f"${daily_stats['Total'].max():.2f}")
        st.metric("📅 Daily Lowest", f"${daily_stats['Total'].min():.2f}")
    
    # Weekly statistics
    df['Week'] = df['Date'].dt.isocalendar().week
    df['Year'] = df['Date'].dt.year
    weekly_stats = df.groupby(['Year', 'Week']).agg({
        'Amount': ['sum', 'mean', 'count', 'min', 'max']
    }).round(2)
    weekly_stats.columns = ['Total', 'Average', 'Count', 'Min', 'Max']
    weekly_stats = weekly_stats.reset_index()
    
    with col2:
        st.metric("📆 Weekly Average", f"${weekly_stats['Total'].mean():.2f}")
        st.metric("📆 Weekly Highest", f"${weekly_stats['Total'].max():.2f}")
        st.metric("📆 Weekly Lowest", f"${weekly_stats['Total'].min():.2f}")
    
    # Monthly statistics
    df['Month'] = df['Date'].dt.month
    monthly_stats = df.groupby(['Year', 'Month']).agg({
        'Amount': ['sum', 'mean', 'count', 'min', 'max']
    }).round(2)
    monthly_stats.columns = ['Total', 'Average', 'Count', 'Min', 'Max']
    monthly_stats = monthly_stats.reset_index()
    
    with col3:
        st.metric("📊 Monthly Average", f"${monthly_stats['Total'].mean():.2f}")
        st.metric("📊 Monthly Highest", f"${monthly_stats['Total'].max():.2f}")
        st.metric("📊 Monthly Lowest", f"${monthly_stats['Total'].min():.2f}")
    
    st.divider()
    
    # Overall transaction statistics
    st.subheader("💰 Overall Transaction Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_transaction = df['Amount'].mean()
        st.metric("📈 Average Transaction", f"${avg_transaction:.2f}")
    
    with col2:
        max_transaction = df['Amount'].max()
        st.metric("🔺 Largest Transaction", f"${max_transaction:.2f}")
    
    with col3:
        min_transaction = df['Amount'].min()
        st.metric("🔻 Smallest Transaction", f"${min_transaction:.2f}")
    
    with col4:
        transaction_count = len(df)
        st.metric("🧾 Total Transactions", transaction_count)

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="Expense Tracker",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize CSV file
    initialize_csv()
    
    # App title
    st.title("💰 Personal Expense Tracker")
    st.markdown("Track your expenses easily and view spending insights!")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["Add Transaction", "View Transactions", "Statistics"],
        index=0
    )
    
    st.sidebar.divider()
    
    # Quick stats in sidebar
    df = load_data()
    if not df.empty:
        st.sidebar.subheader("Quick Stats")
        st.sidebar.metric("Total Spent", f"${df['Amount'].sum():.2f}")
        st.sidebar.metric("Transactions", len(df))
        
        # Most expensive category
        if not df.empty:
            category_totals = df.groupby('Category')['Amount'].sum()
            top_category = category_totals.idxmax()
            st.sidebar.metric("Top Category", top_category)
    
    st.sidebar.divider()
    st.sidebar.markdown("---")
    st.sidebar.markdown("**💡 Tips:**")
    st.sidebar.markdown("• Add transactions regularly")
    st.sidebar.markdown("• Use clear expense names")
    st.sidebar.markdown("• Check statistics weekly")
    
    # Display selected page
    if page == "Add Transaction":
        add_transaction_page()
    elif page == "View Transactions":
        view_transactions_page()
    elif page == "Statistics":
        statistics_page()

if __name__ == "__main__":
    main()