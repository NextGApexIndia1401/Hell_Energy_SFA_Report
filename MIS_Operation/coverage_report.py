import pandas as pd

def process_store_codes(df):
    """
    Processes store codes data to generate a summary DataFrame.

    This function filters the input DataFrame for rows where 'STORE CHANNEL TYPE' is 'GT' and 'DESIGNATION'
    is one of the specified values. It then groups the data by 'EMPLOYEE CODE' and 'EMPLOYEE NAME' and calculates
    the distinct count of 'STORE CODE' for blank and 1 values in the 'BILLED' column. The function returns a
    summary DataFrame with columns '(blank)', '1', 'Total' for each 'EMPLOYEE CODE' and 'EMPLOYEE NAME',
    and an additional 'Grand Total' row at the end of the DataFrame.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing store codes data.

    Returns:
        pandas.DataFrame: A summary DataFrame containing columns '(blank)', '1', 'Total' for each 'EMPLOYEE CODE'
        and 'EMPLOYEE NAME', and an additional 'Grand Total' row at the end of the DataFrame.
    """

    # Filter rows where STORE CHANNEL TYPE is 'GT' and DESIGNATION is one of the specified values
    print(df.columns)
    designations = ['RURAL SALES OFFICER', 'SALES EXECUTIVE', 'SALES OFFICER', 'SALES REPRESENTATIVE', 'TERRITORY SALES IN-CHARGE']
    df = df[df['DESIGNATION'].isin(designations)]
    
    # Selecting relevant columns
    relevant_columns = ['EMPLOYEE CODE', 'EMPLOYEE NAME', 'STORE CODE', 'BILLED', 'VISITED']
    df = df[relevant_columns]

    # Convert 'BILLED' column to numeric (replace 'nan' with np.nan)
    df['BILLED'] = pd.to_numeric(df['BILLED'], errors='coerce')
    df['VISITED'] = pd.to_numeric(df['VISITED'], errors='coerce')

    # Grouping by Employee Code and Employee Name
    grouped_df = df.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME'])

    # Calculating distinct count of store code for blank, 1, and visited
    store_count_blank = grouped_df.apply(lambda x: x[x['BILLED'].isna()]['STORE CODE'].nunique()).reset_index(name='(blank)')
    store_count_1 = grouped_df.apply(lambda x: x[x['BILLED'] == 1]['STORE CODE'].nunique()).reset_index(name='1')
    store_count_visited = grouped_df.apply(lambda x: x[x['VISITED'] == 1]['STORE CODE'].nunique()).reset_index(name='Total')

    # Merging the counts
    summary_df = pd.merge(store_count_blank, store_count_1, on=['EMPLOYEE CODE', 'EMPLOYEE NAME'], how='outer')
    summary_df = pd.merge(summary_df, store_count_visited, on=['EMPLOYEE CODE', 'EMPLOYEE NAME'], how='outer')

    # Filling NaN values with 0 and calculating total
    summary_df.fillna(0, inplace=True)

    # Calculate total row
    total_row = {
        'EMPLOYEE CODE': 'Grand Total',
        'EMPLOYEE NAME': '',
        '(blank)': summary_df['(blank)'].sum(),
        '1': summary_df['1'].sum(),
        'Total': summary_df['Total'].sum()
    }

    # Append the total row to the DataFrame
    summary_df = summary_df.append(total_row, ignore_index=True)

    return summary_df


def process_employee_data(df):
    """
    Processes employee data to calculate the sum of 'VISITED' and 'BILLED' columns for each employee.

    This function filters the input DataFrame for rows where 'STORE CHANNEL TYPE' is 'GT' and 'DESIGNATION'
    is one of the specified values. It then groups the data by 'EMPLOYEE CODE' and 'EMPLOYEE NAME' and calculates
    the sum of 'VISITED' and 'BILLED' columns for each employee. The function returns a DataFrame with columns
    'VISITED' and 'BILLED' for each 'EMPLOYEE CODE' and 'EMPLOYEE NAME', as well as a 'Grand Total' row.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing employee data.

    Returns:
        pandas.DataFrame: A summary DataFrame with columns 'EMPLOYEE CODE', 'EMPLOYEE NAME', 'VISITED', and 'BILLED'
        for each employee, and an additional 'Grand Total' row at the end of the DataFrame.
    """
    # Filter rows based on conditions
    designations = ['RURAL SALES OFFICER', 'SALES EXECUTIVE', 'SALES OFFICER', 'SALES REPRESENTATIVE', 'TERRITORY SALES IN-CHARGE']

    df_filtered = df[df['DESIGNATION'].isin(designations)]

    # Convert 'VISITED' and 'BILLED' columns to numeric
    df_filtered['VISITED'] = pd.to_numeric(df_filtered['VISITED'], errors='coerce')
    df_filtered['BILLED'] = pd.to_numeric(df_filtered['BILLED'], errors='coerce')

    # Group by Employee Code and Employee Name, then sum VISITED and BILLED
    grouped_df = df_filtered.groupby(['EMPLOYEE CODE', 'EMPLOYEE NAME']).agg({'VISITED': 'sum', 'BILLED': 'sum'}).reset_index()
    grand_total_row = {
        'EMPLOYEE CODE': 'Grand Total',
        'EMPLOYEE NAME': '',
        'VISITED': grouped_df['VISITED'].sum(),
        'BILLED': grouped_df['BILLED'].sum()
    }

    # Append grand total row to the DataFrame
    grouped_df = grouped_df.append(grand_total_row, ignore_index=True)

    return grouped_df

