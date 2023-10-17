
import streamlit as st
import pandas as pd
import csv
from faker import Faker
import random
import base64

# Function to check authentication
def check_auth(username, password):
    return username == 'admin' and password == 'admin123'

# Function to generate customer data
def generate_customer_data(num_records):
    fake = Faker()
    data = []
    for _ in range(num_records):
        customer_id = fake.uuid4()
        visit_date = fake.date_this_decade()
        total_spend = round(random.uniform(10, 200), 2)
        product_category = fake.random_element(elements=('Electronics', 'Clothing', 'Books', 'Toys'))
        data.append([customer_id, visit_date, total_spend, product_category])
    return pd.DataFrame(data, columns=['CustomerID', 'VisitDate', 'TotalSpend', 'ProductCategory'])

# Function to download data as CSV
def download_csv(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV File</a>'
    return href

# Function to calculate KPIs
def calculate_kpis(data):
    avg_spending = data['TotalSpend'].mean()
    popular_category = data['ProductCategory'].mode().iloc[0]
    data['VisitDate'] = pd.to_datetime(data['VisitDate'])
    monthly_revenue_growth = data.groupby(data['VisitDate'].dt.to_period("M"))['TotalSpend'].sum().pct_change().fillna(0)
    return avg_spending, popular_category, monthly_revenue_growth

# Function to provide optimization suggestions
def optimization_suggestions(avg_spending, popular_category):
    suggestions = []
    if popular_category == 'Electronics':
        suggestions.append("Consider special promotions for Electronics products.")
    elif popular_category == 'Clothing':
        suggestions.append("Introduce new clothing collections to boost sales.")
    if avg_spending < 50:
        suggestions.append("Offer targeted discounts to low-spending customers.")
    return suggestions

def main_app():
    st.title("Online Store Marketing Analysis")
    # Page selection
    page = st.sidebar.selectbox("Choose a page", ["Generate Customer Data", "Data Analysis"])

    if page == "Generate Customer Data":
        st.title("Generate Customer Data")
        st.write("This page allows you to generate simulated customer data for analysis.")
        if st.button("Generate Data"):
            df = generate_customer_data(500)
            st.write(download_csv(df, 'customer_data.csv'), unsafe_allow_html=True)
            
    elif page == "Data Analysis":
        st.title("Data Analysis")
        uploaded_file = st.file_uploader("Upload Customer Data (CSV file)", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            avg_spending, popular_category, monthly_revenue_growth = calculate_kpis(df)
            suggestions = optimization_suggestions(avg_spending, popular_category)
            
            # Display KPIs
            st.header("Key Performance Indicators (KPIs)")
            st.write(f"Average Spending per Customer: ${avg_spending:.2f}")
            st.write(f"Most Popular Product Category: {popular_category}")
            st.line_chart(monthly_revenue_growth, use_container_width=True)

            # Display optimization suggestions
            st.header("Optimization Suggestions")
            st.write("The suggestions below are generated based on the calculated KPIs to help you optimize your marketing strategies.")
            for suggestion in suggestions:
                st.write(suggestion)

            # Display the data table
            st.header("Customer Data")
            st.dataframe(df)

if __name__ == "__main__":
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type='password')
    if check_auth(username, password):
        main_app()
    elif username and password:
        st.warning("Incorrect username or password.")
