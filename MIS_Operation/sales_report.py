import pandas as pd
from datetime import datetime, timedelta
def calculate_aggregates(df):
    # Filter the DataFrame for 'EMPLOYEE CHANNEL TYPE' == 'GT'
    filtered_df = df[df['EMPLOYEE CHANNEL TYPE'] == 'GT']

    # Aggregate the filtered data by 'Employee Code' and 'Employee Name'
    agg_df = filtered_df.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME']).agg({
        'STORE CODE': lambda x: len(set(x)),  # Counts unique store codes
        'TICKET NO': lambda x: len(set(x)),  # Counts unique ticket numbers
        'PRODUCT NAME': 'count'  # Counts the number of product occurrences for each group
    }).reset_index()

    # Rename columns to better reflect the content
    agg_df.columns = ['Employee Code', 'Employee Name', 'Distinct Store Count', 'Distinct Ticket Count', 'Product Count']

    # Calculate 'Avg Bill' and 'Avg Lines'
    agg_df['Avg Bill'] = (agg_df['Distinct Ticket Count'] / agg_df['Distinct Store Count']).fillna(0).astype(int)
    agg_df['Avg Lines'] = (agg_df['Product Count'] / agg_df['Distinct Ticket Count']).fillna(0).apply(lambda x: round(x, 2))
    # total_row = {
    #     'Employee Code': 'Total',
    #     'Employee Name': '',
    #     'Distinct Store Count': agg_df['Distinct Store Count'].sum(),
    #     'Distinct Ticket Count': agg_df['Distinct Ticket Count'].sum(),
    #     'Product Count': agg_df['Product Count'].sum(),
    #     'Avg Bill': '', 
    #     'Avg Lines': ''  
    # }

    # # Append the total row to the DataFrame
    # total_df = pd.DataFrame([total_row], columns=agg_df.columns)
    # agg_df = pd.concat([agg_df, total_df], ignore_index=True)
    agg_df.rename(columns={'Employee Code':'EMPLOYEE CODE','Employee Name':'EMPLOYEE NAME'},inplace=True)
    return agg_df
    


def calculate_avg_lines(df):
    # Define yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
    # Define today's date
    today_str = datetime.now().strftime('%Y-%m-%d')

    # Define the subcategories
    subcategories = ['CLASSIC', 'WATERMELON', 'COFFEE', 'APPLE']
    
    # Convert 'RESPONSE DATE' to datetime format
    df['RESPONSE DATE'] = pd.to_datetime(df['RESPONSE DATE'])
    
    # Filter rows where 'EMPLOYEE CHANNEL TYPE' is 'GT' and 'RESPONSE DATE' is up to yesterday
    df_filtered = df[(df['EMPLOYEE CHANNEL TYPE'] == 'GT') & (df['RESPONSE DATE'] < today_str)]
    
    # Convert 'QTY IN CASE' to numeric format
    df_filtered['QTY IN CASE'] = pd.to_numeric(df_filtered['QTY IN CASE'], errors='coerce')
    
    # Group by 'EMPLOYEE CODE' and 'EMPLOYEE NAME', summing 'QTY IN CASE' for each subcategory
    grouped_df = df_filtered.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME', 'SUB CATEGORY'])['QTY IN CASE'].sum().reset_index()
    
    # Pivot the table to make subcategory values as columns
    pivot_df = grouped_df.pivot_table(index=['EMPLOYEE CODE', 'EMPLOYEE NAME'],
                                      columns='SUB CATEGORY',
                                      values='QTY IN CASE',
                                      aggfunc='sum').reset_index()
    
    # Ensure all subcategories are included in the pivot table
    for subcat in subcategories:
        if subcat not in pivot_df.columns:
            pivot_df[subcat] = 0
    
    # Fill NaN values with 0
    pivot_df.fillna(0, inplace=True)
    
    # Add a "Grand Total" column
    pivot_df['Grand Total'] = pivot_df[subcategories].sum(axis=1)
    
    # Reorder columns as per the specified order
    pivot_df = pivot_df[['EMPLOYEE CODE', 'EMPLOYEE NAME'] + subcategories + ['Grand Total']]
    
    return pivot_df

def calculate_avg_lines_today(df):
    # Define yesterday's date

    
    # Define today's date


    # Define the subcategories
    subcategories = ['CLASSIC', 'WATERMELON', 'COFFEE', 'APPLE']
    
    # Convert 'RESPONSE DATE' to datetime format
    df['RESPONSE DATE'] = pd.to_datetime(df['RESPONSE DATE'])
    
    # Filter rows where 'EMPLOYEE CHANNEL TYPE' is 'GT' and 'RESPONSE DATE' is up to yesterday
    df_filtered = df[df['EMPLOYEE CHANNEL TYPE'] == 'GT']
    
    # Convert 'QTY IN CASE' to numeric format
    df_filtered['QTY IN CASE'] = pd.to_numeric(df_filtered['QTY IN CASE'], errors='coerce')
    
    # Group by 'EMPLOYEE CODE' and 'EMPLOYEE NAME', summing 'QTY IN CASE' for each subcategory
    grouped_df = df_filtered.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME', 'SUB CATEGORY'])['QTY IN CASE'].sum().reset_index()
    
    # Pivot the table to make subcategory values as columns
    pivot_df = grouped_df.pivot_table(index=['EMPLOYEE CODE', 'EMPLOYEE NAME'],
                                      columns='SUB CATEGORY',
                                      values='QTY IN CASE',
                                      aggfunc='sum').reset_index()
    
    # Ensure all subcategories are included in the pivot table
    for subcat in subcategories:
        if subcat not in pivot_df.columns:
            pivot_df[subcat] = 0
    
    # Fill NaN values with 0
    pivot_df.fillna(0, inplace=True)
    
    # Add a "Grand Total" column
    pivot_df['Grand Total'] = pivot_df[subcategories].sum(axis=1)
    
    # Reorder columns as per the specified order
    pivot_df = pivot_df[['EMPLOYEE CODE', 'EMPLOYEE NAME'] + subcategories + ['Grand Total']]
    
    return pivot_df

def process_order_dump(df):
    # Filter rows where 'EMPLOYEE CHANNEL TYPE' is 'GT'
    df_gt = df[df['EMP CHANNEL'] == 'GT']

    # Selecting relevant columns
    relevant_columns = ['EMPLOYEE CODE', 'EMPLOYEE NAME', 'TICKET NO', 'QTY IN CASE', 'SIGNOFF QTY']
    df_gt = df_gt[relevant_columns]

    # Convert 'SIGNOFF QTY' and 'QTY IN CASE' columns to numeric
    # df_gt['SIGNOFF QTY'] = pd.to_numeric(df_gt['SIGNOFF QTY'].str.replace(',', ''), errors='coerce')
    # df_gt['QTY IN CASE'] = pd.to_numeric(df_gt['QTY IN CASE'].str.replace(',', ''), errors='coerce')
    df_gt['SIGNOFF QTY'] = pd.to_numeric(df_gt['SIGNOFF QTY'].astype(str).str.replace(',', ''), errors='coerce')
    df_gt['QTY IN CASE'] = pd.to_numeric(df_gt['QTY IN CASE'], errors='coerce')


    # Grouping by Employee Code and Employee Name
    grouped_df = df_gt.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME'])

    # Calculating distinct count of ticket no for each employee
    ticket_count = grouped_df['TICKET NO'].nunique().reset_index(name='Ticket Count')

    # Calculating sum of quantity_in_case for each employee
    quantity_sum = grouped_df['QTY IN CASE'].sum().reset_index(name='Quantity Sum')
    quantity_sum['Quantity Sum'] = quantity_sum['Quantity Sum'].round(2)
    # Calculating sum of sign off qty for each employee
    signoff_sum = grouped_df['SIGNOFF QTY'].sum().reset_index(name='Signoff Sum')

    # Adding units column
    signoff_sum['Units'] = signoff_sum['Signoff Sum'] / 24
    signoff_sum['Units'] = signoff_sum['Units'].round(2)
    # Merging all summaries
    summary_df = pd.merge(ticket_count, quantity_sum, on=['EMPLOYEE CODE', 'EMPLOYEE NAME'])
    summary_df = pd.merge(summary_df, signoff_sum, on=['EMPLOYEE CODE', 'EMPLOYEE NAME'])

    # # Calculate totals
    # total_row = {
    #     'EMPLOYEE CODE': 'Total',
    #     'EMPLOYEE NAME': '',
    #     'Ticket Count': summary_df['Ticket Count'].sum(),
    #     'Quantity Sum': summary_df['Quantity Sum'].sum(),
    #     'Signoff Sum': summary_df['Signoff Sum'].sum(),
    #     'Units': summary_df['Units'].sum()
    # }

    # # Append total row to DataFrame
    # summary_df = summary_df.append(total_row, ignore_index=True)

    return summary_df

def process_order_dump_total_tickets_with_filter(df):
    # Convert 'SIGNOFF QTY' to numeric
    df['SIGNOFF QTY'] = pd.to_numeric(df['SIGNOFF QTY'], errors='coerce')

    # Filter rows where 'EMPLOYEE CHANNEL TYPE' is 'GT' and 'SIGNOFF QTY' is not blank or 0
    df_gt = df[(df['EMP CHANNEL'] == 'GT') & (df['SIGNOFF QTY'].notnull()) & (df['SIGNOFF QTY'] != 0)]

    # Selecting relevant columns
    relevant_columns = ['EMPLOYEE CODE', 'EMPLOYEE NAME', 'TICKET NO']
    df_gt = df_gt[relevant_columns]

    # Grouping by Employee Code and Employee Name
    grouped_df = df_gt.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME'])

    # Calculating distinct count of ticket no for each employee
    ticket_count = grouped_df['TICKET NO'].nunique().reset_index(name='Total Tickets')

    # total_tickets = ticket_count['Total Tickets'].sum()

    # # Append a row with total ticket count
    # total_row = {'EMPLOYEE CODE': 'Total', 'EMPLOYEE NAME': '', 'Total Tickets': total_tickets}
    # ticket_count = ticket_count.append(total_row, ignore_index=True)
    
    return ticket_count