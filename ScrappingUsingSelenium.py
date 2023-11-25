#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import openpyxl
from selenium.webdriver.common.by import By
import time
import csv

import os
import pandas as pd
import numpy as np


import sqlite3
from sqlite3 import Error



# In[2]:


# !pip install selenium
# !pip install webdriver-manager
# !pip install openpyxl


# In[2]:


# path = r'C:\Users\Hamza\Desktop\Jupyter Notebook\Selenium\company_symbol.xlsx'
# wb = openpyxl.load_workbook(path)
# sh1 = wb.active

url = 'https://www.nasdaq.com/market-activity/stocks/screener'
chrome_options = Options()

# chrome brower will not exit automatically
chrome_options.add_experimental_option('detach', True)
chrome_options.binary_location = './/chrome-win64/chrome.exe'

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

driver.get(url)
# driver.maximize_window()


# In[3]:


total_rows_in_single_page = driver.find_element(By.XPATH, "//span[@class='nsrCount']")
last_result_num = list((total_rows_in_single_page.text).split('-'))
rows_in_single_page = int(last_result_num[-1])
print(rows_in_single_page)


# In[4]:


total_rows_count = driver.find_element(By.XPATH, "//span[@class='nsrTotal'] ").text
total_rows_count = int(total_rows_count)
print(int(total_rows_count))
print(type(total_rows_count))


# In[5]:


table_headers_title = driver.find_elements(By.CLASS_NAME, "nasdaq-screener__table-container thead th")
titles = []
for i in table_headers_title:
    titles.append(i.text)
print(titles)   


# In[6]:


total_pages = driver.find_element(By.XPATH, "//div[@class='pagination__pages']")
last_page = total_pages.text.split()[-1]
print(f'last page number: {int(last_page)}')


# In[ ]:





# In[ ]:





# In[97]:


home_table_body = driver.find_element(By.XPATH,"//table[@class='nasdaq-screener__table']")
table_rows = home_table_body.find_elements(By.TAG_NAME, 'tr')

each_symbol = driver.find_elements(By.CSS_SELECTOR, "tr th[class='nasdaq-screener__cell']")
for i in each_symbol:
    print(i.text)


# balance_sheet_table_of_company = driver.find_element(By.XPATH, "//div[@class='financials__panel financials__panel--active']//table[@role='table']")
# print(balance_sheet_table_of_company.text)

# print(home_table_body.text)
# for i in table_rows:
#     print(i.text)


# In[98]:


each_symbol = driver.find_elements(By.CSS_SELECTOR, "tr th[class='nasdaq-screener__cell']")
for i in each_symbol:
    print(i.text)


# In[ ]:





# In[183]:


# home_table_body = driver.find_element(By.XPATH,"//table[@class='nasdaq-screener__table']/tbody")
# table_rows = home_table_body.find_elements(By.TAG_NAME, 'tr')
# # for i in table_rows:
# #     print(i.text)


# with open('stock_finance.csv', 'w', newline="") as file:
#     dw = csv.DictWriter(file, delimiter=',',  fieldnames=titles) 
#     dw.writeheader() 

#     writer= csv.writer(file)
#     for row in table_rows:
    
#         table_data = row.find_elements(By.CSS_SELECTOR, "td ,th")

#         row_data = [data.text for data in table_data]
#         print(row_data)
    
#         writer.writerow(row_data)
        
        
# # driver.quit()
# print('Exited')


# In[ ]:





# In[23]:


# pages = []
# page_no = driver.find_element(By.XPATH, "//button[normalize-space()='297']")
# print(type(page_no.text))


# In[28]:


# cookie_consent_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-pc-btn-handler")))



# accept_all = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-pc-sdk"]/div/div[3]/div[1]/button')))
# accept_all.click()


# In[ ]:





# In[ ]:





# In[ ]:





# In[7]:


total_pages = total_rows_count // rows_in_single_page + 1


income_statement_headers = []
total_data_scrapped = []
# Iterate through each page
current_page = 1


# Create a new folder called 'financials_for_each_company'
if not os.path.exists('financials_for_each_company'):
    os.makedirs('financials_for_each_company')

# Function to handle cookie consent dynamically
def handle_cookie_consent():
    try:
        cookie_consent_button = driver.find_element(By.ID, "onetrust-pc-btn-handler")
        cookie_consent_button.click()
        
        accept_all = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-pc-sdk"]/div/div[3]/div[1]/button')))
        accept_all.click()

    except Exception as e:
        pass

# Handle cookie consent before proceeding
handle_cookie_consent()
# Open the main CSV file for the main table data
with open('stock_finance.csv', 'w', newline="") as stock_finance_file:
    stock_finance_writer = csv.DictWriter(stock_finance_file, fieldnames=titles)
    
    # Write the header for the main table
    stock_finance_writer.writeheader()

    # Iterate through each page
    for current_page in range(1, total_pages + 1):
        print(f"Scraping data from page {current_page}...")
        
        # Handle cookie consent before scraping the main table
        handle_cookie_consent()
        
        # Get the main table data for the current page
        home_table_body = driver.find_element(By.XPATH, "//table[@class='nasdaq-screener__table']/tbody")
        table_rows = home_table_body.find_elements(By.TAG_NAME, 'tr')

        for row in table_rows:
            table_data = row.find_elements(By.CSS_SELECTOR, "td,th")
            row_data = {title: data.text for title, data in zip(titles, table_data)}
            stock_finance_writer.writerow(row_data)

        # Extract symbols from each row
        symbols = [row.find_element(By.TAG_NAME, 'th').find_element(By.TAG_NAME, 'a').text for row in table_rows]

        # Iterate through each symbol on the current page
        for symbol in symbols:
            if not symbol:
                print("Empty symbol found. Skipping...")
                continue

            print(f"Scraping data for symbol: {symbol}")

            try:
                # Open the company's page
                company_url = f"https://www.nasdaq.com/market-activity/stocks/{symbol}/financials"
                driver.get(company_url)
                print(f"\nCompany URL: {company_url}")

                # Create a new CSV file for the company's financial data
                with open(f"financials_for_each_company/{symbol}_financial_data.csv", 'w', newline="") as csvfile:
                    company_writer = csv.writer(csvfile)

                    # Iterate through tabs (Income Statement and Balance Sheet)
                    for tab_name in ['Income Statement', 'Balance Sheet']:
                        # Click on the tab
                        tab_button_xpath = f"//button[normalize-space()='{tab_name}']"
                        tab_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, tab_button_xpath)))
                        tab_button.click()

                        # Explicitly wait for the tab content to be present and visible
                        wait = WebDriverWait(driver, 10)
                        tab_content = wait.until(
                            EC.presence_of_element_located((By.XPATH, "//div[@class='financials__panel financials__panel--active']//table[@role='table']/tbody"))
                        )

                        # Extract the tab data
                        headers = tab_content.find_element(By.XPATH, "//thead[@class='financials__table-headings']")

                        # Include the symbol in the header
                        tab_headers = [header.text for header in headers.find_elements(By.TAG_NAME, 'th')] + ['symbol']

                        # Write the table header only if it's the first tab (Income Statement)
                        if tab_name == 'Income Statement':
                            company_writer.writerow(tab_headers)

                        # Extract data from each row
                        rows = tab_content.find_elements(By.TAG_NAME, 'tr')
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, 'td')
                            header_text = cells[0].find_element(By.XPATH, 'preceding-sibling::th').text if cells else None
                            row_data = [header_text] + [cell.text for cell in cells] + [symbol]
                            company_writer.writerow(row_data)

                # Navigate back to the home page
                driver.get(url)

                print(f"\nHome URL: {url}\n")

            except Exception as e:
                print(f"Error occurred while scraping {symbol}, skipping... {str(e)}")
                continue

        
            
        # If the current page is not the last page, navigate to the next page
        if current_page < total_pages:
            # Handle cookie consent before clicking the next page button
            handle_cookie_consent()

            # Find the next page button and click it
            next_page_number = current_page + 1
            next_page_button_xpath = f"//div[@class='pagination__pages']//button[@data-page='{next_page_number}']"
            next_page_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, next_page_button_xpath)))
            next_page_button.click()
            time.sleep(10)


# # DATA CLEANING
# 

# In[80]:


## DATA CLEANING

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv('C:/Users/Hamza/Desktop/Jupyter Notebook/Book1.csv')
print(df.isna().sum())


# In[81]:


# df = df.dropna()


# In[82]:


df = df.fillna(0)


# In[83]:


print(df.isna().sum())


# In[84]:


df.info()


# In[ ]:





# In[85]:


df['Column1']


# In[86]:


df['Column6']


# In[87]:


##Converting str to date object.


# In[88]:


period_ending_rows = df[df['Column1'].str.contains('Period Ending:')]

# Columns with dates to convert
date_columns = df.columns[df.columns.str.startswith('Column')]

# Iterate over 'Period Ending:' rows and convert date columns to datetime
for index in period_ending_rows.index:
    for column in date_columns:
        if column != 'Column1' and column != 'Column6':
            try:
                df.at[index, column] = pd.to_datetime(df.at[index, column], errors='coerce').date()
            except:
                pass

# Print the updated DataFrame
print(df)


# In[89]:


df.head(10)


# In[96]:


df.replace('--', 0, inplace=True)
# Remove leading dollar signs
df = df.replace(r'^\$', '', regex=True)


# In[97]:


df.tail(50)


# In[92]:


print(df.dtypes)


# In[ ]:





# In[ ]:





# In[119]:


# pivoted_data = df.pivot_table(values='Value', index='Period', columns='Metric')
# print(pivoted_data)
# # 


# In[93]:


numeric_columns = df.select_dtypes(include='number').columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())


# In[98]:


df.head(10)


# In[100]:


output_file = 'cleaned_financial_data_IS_BS.csv'

# Save the DataFrame to a new CSV file
df.to_csv(output_file, index=False)

print(f"DataFrame has been saved to {output_file}.")


# In[101]:


df.head(20)


# In[24]:


# # Filter rows that have 'Period Ending:' in 'Column1'
# period_rows = df[df['Column1'] == 'Period Ending:']

# # Extract the relevant subset of the DataFrame
# subset_df = df.loc[df['Column1'] != 'Period Ending:']

# # Pivot the DataFrame to reshape it
# reshaped_df = subset_df.pivot(index='Column1', columns='Column6', values=['Column2', 'Column3', 'Column4', 'Column5'])

# # Reset the index to make 'Column1' a regular column
# reshaped_df = reshaped_df.reset_index()

# # Print the reshaped DataFrame
# print(reshaped_df)


# # cleaning main table
# 

# In[177]:


#cleaning main table

df_main_table = pd.read_csv("C:/Users/Hamza/Desktop/Jupyter Notebook/stock_finance.csv")
df_main_table.head()


# In[178]:


df_main_table.replace('--', 0, inplace=True)
# Remove leading dollar signs
df_main_table = df_main_table.replace(r'^\$', '', regex=True)


# In[179]:


# df_main_table.tail(3) # Prints last n rows of the DataFrame

# df_main_table.describe() # Summary statistics for numerical columns
# df_main_table.value_counts(dropna=False) # Views unique values and counts
# df_main_table.apply(pd.Series.value_counts) # Unique values and counts for every columns
# df_main_table.describe() # brief statistics for numerical columns
# df_main_table.mean() # Returns the mean of every columns
df_main_table.count() # Returns the number of non-null values in each DataFrame column
# df_main_table.max() # Returns the biggest value in every column
# df_main_table.min() # Returns the lowest value in every column
# df_main_table.median() 


# In[ ]:





# In[180]:


print(df_main_table.isna().sum())


# In[181]:


df_main_table = df_main_table.dropna()
print(df_main_table.isna().sum())


# In[182]:


df_main_table.info()


# In[183]:


df_main_table['Last Sale']


# In[184]:


df_main_table['Symbol']


# In[185]:


df_main_table['% Change']


# In[194]:


df_main_table['Last Sale'].tail(30)


# In[187]:


df_main_table = df_main_table.replace(',','', regex=True)


# In[188]:


df_main_table.tail(30)


# In[195]:


df_main_table['% Change'] = pd.to_numeric(df_main_table['% Change'].replace('UNCH', '0').str.replace('%', ''), errors='coerce')


# In[196]:


df_main_table.head(40)


# In[197]:


df_main_table.info()


# In[198]:


## market cap showing numbers in exponential form ... 
## use this option to show in float data type.
pd.options.display.float_format = '{:,.2f}'.format


# In[199]:


df_main_table.head()


# In[201]:


output_file = 'cleaned_stock_finance_output_file.csv'

# Save the DataFrame to a new CSV file
df_main_table.to_csv(output_file, index=False, float_format='%.2f')

print(f"DataFrame has been saved to {output_file}.")


# In[ ]:





# # Database 

# In[202]:


# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

# Function to insert DataFrame into SQLite database
def insert_dataframe(conn, table_name, df):
    try:
        # Use pandas to_sql function to insert DataFrame into SQLite
        df.to_sql(name=table_name, con=conn, index=False, if_exists='replace')
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print(e)

csv_file = "cleaned_stock_finance_output_file.csv"

database_file = "test1.db"

table_name = "stock_main_table"

# Read CSV file into a DataFrame
data_frame = pd.read_csv(csv_file)

# Create a database connection
connection = create_connection(database_file)

if connection:
    # Call the insert_dataframe function
    insert_dataframe(connection, table_name, data_frame)

    # Close the database connection
    connection.close()


# In[ ]:





# In[203]:


# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to insert DataFrame into SQLite database with custom data types
def insert_dataframe(conn, table_name, df, dtype_dict):
    try:
        # Use pandas to_sql function to insert DataFrame into SQLite
        df.to_sql(name=table_name, con=conn, index=False, if_exists='replace', dtype=dtype_dict)
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print(e)
        
# Function to drop a table from SQLite database
def drop_table(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        print(f"Table '{table_name}' dropped successfully.")
    except sqlite3.Error as e:
        print(e)
        
def fetch_all(conn, query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)
        return None
    
def execute_select_query(conn, query):
    try:
        # Use pandas to read the result of the query into a DataFrame
        result_df = pd.read_sql_query(query, conn)
        return result_df
    except sqlite3.Error as e:
        print(e)
        return None
        
        

# Specify the data types for each column
dtype_mapping = {
    'Symbol': 'TEXT',
    'Name': 'TEXT',
    'Last Sale': 'REAL',  
    'Net Change': 'REAL',
    '% Change': 'REAL',
    'Market Cap': 'INT', 
}

csv_file = "cleaned_stock_finance_output_file.csv"
database_file = "test1.db"
table_name = "stock_main_table"

# Read CSV file into a DataFrame
data_frame = pd.read_csv(csv_file)

# Create a database connection
connection = create_connection(database_file)

if connection:
    
    drop_table(connection, table_name)

    # Call the insert_dataframe function with the custom data types
    insert_dataframe(connection, table_name, data_frame, dtype_mapping)
    
    
    
    select_query = "SELECT * FROM stock_main_table;"

    

    # Execute the SELECT query and fetch data
    result = fetch_all(connection, select_query)

    if result:
        # Print the retrieved data
        for row in result:
            print(row)

    # Close the database connection
#     connection.close()


# In[204]:


if connection:
    
    # Example 1: Group by Symbol and Calculate Average Net Change

    query1 = """
    SELECT Symbol, AVG(`Net Change`) AS AvgNetChange
    FROM stock_main_table
    GROUP BY Symbol;
    """
    result1 = execute_select_query(connection, query1)
    print("Example 1:  Group by Symbol and Calculate Average Net Change")
    print(result1)
    
    # Example 2: Group by Symbol and Calculate Total Market Cap
    query2 = """
    SELECT Symbol, SUM(CAST(REPLACE(`Market Cap`, ',', '') AS INTEGER)) AS TotalMarketCap
    FROM stock_main_table
    GROUP BY Symbol;
    """
    result2 = execute_select_query(connection, query2)
    print("\nExample 2: Group by Symbol and Calculate Total Market Cap")
    print(result2)

    # Example 3: Filter Groups with HAVING Clause
    query3 = """
    SELECT Symbol, AVG(`% Change`) AS AvgPercentChange
    FROM stock_main_table
    GROUP BY Symbol
    HAVING AVG(`% Change`) > 0.5;
    """
    result3 = execute_select_query(connection, query3)
    print("\nExample 3: Filter Groups with HAVING Clause")
    print(result3)
    
    
    
    # Example 4: Retrieve top N rows
    top_n = 5
    query4 = f"""
    SELECT *
    FROM stock_main_table
    LIMIT {top_n};
    """
    result4 = execute_select_query(connection, query4)
    print("\nExample 4: Retrieve top N rows")
    print(result4)
    
    # Example 5: Retrieve specific columns and filter based on conditions
    query5 = """
    SELECT Symbol, Name, `Last Sale`, `% Change`
    FROM stock_main_table
    WHERE `% Change` > 1
    ORDER BY `% Change` DESC;
    """
    result5 = execute_select_query(connection, query5)
    print("\nExample 5: Retrieve specific columns and filter based on conditions")
    print(result5)
    
     # Example 6: Retrieve all columns for a specific Symbol
    symbol_to_select = 'NVDA'
    query6 = f"""
    SELECT *
    FROM stock_main_table
    WHERE Symbol = '{symbol_to_select}';
    """
    result6 = execute_select_query(connection, query6)
    print("Example 6: Retrieve all columns for a specific Symbol")
    print(result6)

    # Close the database connection
    connection.close()


# In[ ]:




