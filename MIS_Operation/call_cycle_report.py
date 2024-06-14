import pandas as pd
import re
def process_employee_data(df):
    """
    Processes employee data to generate a summary DataFrame.

    This function filters rows from the input DataFrame where the 'Designation' is not blank or 'TEST SR'.
    It then groups the filtered data by 'EMP Code' and calculates the distinct count of 'Store Code' and 'BEAT NAME'.
    The function returns a DataFrame with columns 'EMPLOYEE CODE', 'EMPLOYEE NAME', 'Distinct Store Count',
    and 'Distinct Beat Count'.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing employee data.

    Returns:
        pandas.DataFrame: A summary DataFrame containing 'EMPLOYEE CODE', 'EMPLOYEE NAME', 'Distinct Store Count',
        and 'Distinct Beat Count' columns.
    """

    # Filter rows where Designation is not blank or 'TEST SR'
    filtered_df = df[(df['Designation'] != '') & (df['Designation'] != 'TEST SR')]
    filtered_df['BEAT NAME'] = filtered_df['BEAT NAME'].astype(str).str.strip().apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))
    # filtered_df['BEAT NAME'] = filtered_df['BEAT NAME'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    # Group by EMP Code and calculate distinct count of Store Code and Beat Name
    target_row = filtered_df[filtered_df['EMP Code'] == 'TEMP1492']
    if not target_row.empty:
        print(f"Unique Beat Names for Employee Code : {target_row['BEAT NAME'].unique().tolist()}")

    summary_df = filtered_df.groupby('EMP Code').agg({
        'Employee Name': 'first',
        'Store Code': pd.Series.nunique,
        'BEAT NAME': pd.Series.nunique
    }).reset_index()
   
    # Rename columns for clarity
    summary_df.rename(columns={'EMP Code':'EMPLOYEE CODE','Employee Name':'EMPLOYEE NAME','Store Code': 'Distinct Store Count', 'BEAT NAME': 'Distinct Beat Count'}, inplace=True)
    
    # grand_total_row = {
    #     'EMP Code': 'Grand Total',
    #     'Employee Name': '',
    #     'Distinct Store Count': summary_df['Distinct Store Count'].sum(),
    #     'Distinct Beat Count': summary_df['Distinct Beat Count'].sum()
    # }

    # # Append the Grand Total row to the DataFrame
    # summary_df = summary_df.append(grand_total_row, ignore_index=True)


    return summary_df