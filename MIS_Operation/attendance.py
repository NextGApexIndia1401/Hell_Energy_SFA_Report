import pandas as pd

def sum_p_values_by_employee(df):
    """
    Calculates the sum of 'P' values in the DataFrame for each employee.

    This function takes a DataFrame as input and calculates an 'Attendance' column that sums the occurrences of 'P' values
    (excluding 'PL') across specified columns for each row. Then, it groups the DataFrame by 'EMP CODE' and 'EMP NAME' and 
    aggregates the sum of 'Attendance' values for each group.

    Parameters:
        df (pandas.DataFrame): The input DataFrame containing employee data.

    Returns:
        pandas.DataFrame: A DataFrame with columns 'EMPLOYEE CODE', 'EMPLOYEE NAME', and 'Attendance', 
        containing the sum of 'P' values for each employee.
    """
    # Filter columns to exclude the ones to ignore
    columns_to_check = df.columns.difference([
    'Client Name',
    'USERNAME',
    'EMP CODE',
    'EMP NAME',
    'CITY',
    'STATE',
    'REGION',
    'POSITION',
    'LEVEL 2 EMP NAME',
    'LEVEL 3 EMP NAME',
    'LEVEL 4 EMP NAME',
    'LEVEL 5 EMP NAME',
    'LEVEL 6 EMP NAME',
    'EMP STATUS'
])

    # Convert all values in the columns of interest to string
    df[columns_to_check] = df[columns_to_check].astype(str)

    # Calculate 'Attendance' by summing up occurrences of 'P' in the columns of interest
    df['Attendance'] = df[columns_to_check].apply(lambda row: sum(1 for x in row if 'P' in x and 'PL' not in x), axis=1)

    # Group by employee code and aggregate the sum of 'P' values
    result_df = df.groupby(['EMP CODE', 'EMP NAME'])['Attendance'].sum().reset_index()

    # Rename columns for clarity
    result_df.rename(columns={'EMP CODE':'EMPLOYEE CODE','EMP NAME':'EMPLOYEE NAME'},inplace = True)

    return result_df