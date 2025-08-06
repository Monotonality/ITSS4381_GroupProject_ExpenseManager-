import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
import plotly.express as px
import uuid

# Configuration
CSV_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Other"]

def initialize_csv():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["ID", "Name", "Amount", "Date", "Category"])
        df.to_csv(CSV_FILE, index=False)

def load_data():
    """Load data from CSV file"""
    try:
        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            # Convert Date column to datetime for proper sorting
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        else:
            return pd.DataFrame(columns=["ID", "Name", "Amount", "Date", "Category"])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["ID", "Name", "Amount", "Date", "Category"])

def save_transaction(name, amount, date, category):
    """Save a new transaction to CSV file"""
    try:
        # Generate unique ID
        transaction_id = str(uuid.uuid4())[:8]
        
        # Create new transaction
        new_transaction = {
            "ID": transaction_id,
            "Name": name,
            "Amount": amount,
            "Date": date,
            "Category": category
        }
        
        # Load existing data
        df = load_data()
        
        # Add new transaction
        new_df = pd.DataFrame([new_transaction])
        df = pd.concat([df, new_df], ignore_index=True)
        
        # Save to CSV
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Error saving transaction: {e}")
        return False

def add_transaction_page():
    """Add Transaction page"""
    st.header("💰 Add New Transaction")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Expense Name*", placeholder="e.g., Lunch at restaurant")
            amount = st.number_input("Amount*", min_value=0.01, step=0.01, format="%.2f")
        
        with col2:
            transaction_date = st.date_input("Date", value=date.today())
            category = st.selectbox("Category", CATEGORIES)
        
        submitted = st.form_submit_button("Add Transaction", type="primary")
        
        if submitted:
            # Validation
            if not name.strip():
                st.error("Please enter an expense name.")
            elif amount <= 0:
                st.error("Amount must be greater than 0.")
            else:
                # Save transaction
                if save_transaction(name.strip(), amount, transaction_date, category):
                    st.success(f"Transaction '{name}' added successfully!")
                    st.balloons()
                else:
                    st.error("Failed to save transaction. Please try again.")

def view_transactions_page():
    """View Transactions page"""
    st.header("📊 View Transactions")
    
    df = load_data()
    
    if df.empty:
        st.info("No transactions found. Add your first transaction using the sidebar!")
    else:
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Transactions", len(df))
        with col2:
            st.metric("Total Spent", f"${df['Amount'].sum():.2f}")
        with col3:
            st.metric("Average Transaction", f"${df['Amount'].mean():.2f}")
        
        st.subheader("All Transactions")
        
        # Sort by date (newest first)
        df_display = df.copy()
        df_display = df_display.sort_values('Date', ascending=False)
        
        # Format amount for display
        df_display['Amount'] = df_display['Amount'].apply(lambda x: f"${x:.2f}")
        
        # Display table
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small"),
                "Name": st.column_config.TextColumn("Expense Name"),
                "Amount": st.column_config.TextColumn("Amount", width="small"),
                "Date": st.column_config.DateColumn("Date", width="medium"),
                "Category": st.column_config.TextColumn("Category", width="medium")
            }
        )

def statistics_page():
    """Statistics page"""
    st.header("📈 Spending Statistics")
    
    df = load_data()
    
    if df.empty:
        st.info("No data available for statistics. Add some transactions first!")
        return
    
    # Total spent metric
    total_spent = df['Amount'].sum()
    st.metric("💸 Total Amount Spent", f"${total_spent:.2f}")
    
    # Spending by category
    st.subheader("Spending by Category")
    category_totals = df.groupby('Category')['Amount'].sum().reset_index()
    category_totals = category_totals.sort_values('Amount', ascending=False)
    
    if not category_totals.empty:
        # Create bar chart
        fig = px.bar(
            category_totals,
            x='Category',
            y='Amount',
            title='Total Spending by Category',
            color='Category',
            text='Amount'
        )
        
        # Format text on bars
        fig.update_traces(texttemplate='$%{text:.2f}', textposition='outside')
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Amount ($)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show category breakdown table
        st.subheader("Category Breakdown")
        category_display = category_totals.copy()
        category_display['Amount'] = category_display['Amount'].apply(lambda x: f"${x:.2f}")
        category_display['Percentage'] = (category_totals['Amount'] / total_spent * 100).apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(
            category_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Category": st.column_config.TextColumn("Category"),
                "Amount": st.column_config.TextColumn("Total Spent"),
                "Percentage": st.column_config.TextColumn("% of Total")
            }
        )
    
    # Recent transactions summary
    st.subheader("Recent Activity")
    if len(df) > 0:
        recent_df = df.nlargest(5, 'Date')
        recent_display = recent_df[['Name', 'Amount', 'Date', 'Category']].copy()
        recent_display['Amount'] = recent_display['Amount'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(
            recent_display,
            use_container_width=True,
            hide_index=True
        )

def main():
    """Main application"""
    st.set_page_config(
        page_title="Expense Tracker",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize CSV file
    initialize_csv()
    
    # Sidebar navigation
    st.sidebar.title("💰 Expense Tracker")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["Add Transaction", "View Transactions", "Statistics"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This app helps you track your expenses. "
        "Add transactions, view your spending history, "
        "and analyze your spending patterns."
    )
    
    # Main content
    if page == "Add Transaction":
        add_transaction_page()
    elif page == "View Transactions":
        view_transactions_page()
    elif page == "Statistics":
        statistics_page()

if __name__ == "__main__":
    main()