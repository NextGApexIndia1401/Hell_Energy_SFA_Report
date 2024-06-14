import pandas as pd
def calculate_visit_planned(row):
    if row['DESIGNATION'] == 'SALES REPRESENTATIVE':
        return row['Plan Mandays'] * 50
    elif row['DESIGNATION'] == 'SALES EXECUTIVE':
        return row['Plan Mandays'] * 50
    elif row['DESIGNATION'] == 'RURAL SALES OFFICER':
        return row['Plan Mandays'] * 30
    elif row['DESIGNATION'] == 'SALES OFFICER':
        return row['Plan Mandays'] * 30
    elif row['DESIGNATION'] == 'TERRITORY SALES IN-CHARGE':
        return row['Plan Mandays'] * 30
    else:
        return 0

def filter_by_employee_code(df, search_term):
    if search_term == '':
        return pd.DataFrame(columns=df.columns)
    return df[df['EMPLOYEE CODE'].str.contains(search_term, case=False)]

def filter_by_asm(df, selected_asms):
    if not selected_asms:
        return pd.DataFrame(columns=df.columns)  # Return an empty DataFrame if no ASM is selected
    return df[df['ASM'].isin(selected_asms)]


def calculate_plan_productivity(row):
    if row['DESIGNATION'] == 'SALES REPRESENTATIVE':
        return row['Plan Mandays'] * 30
    elif row['DESIGNATION'] == 'SALES EXECUTIVE':
        return row['Plan Mandays'] * 30
    elif row['DESIGNATION'] == 'RURAL SALES OFFICER':
        return row['Plan Mandays'] * 18
    elif row['DESIGNATION'] == 'SALES OFFICER':
        return row['Plan Mandays'] * 18
    elif row['DESIGNATION'] == 'TERRITORY SALES IN-CHARGE':
        return row['Plan Mandays'] * 30
    else:
        return 0

def calculate_plan_unique_store_visited(row):
    if row['DESIGNATION'] in ['SALES REPRESENTATIVE', 'SALES EXECUTIVE']:
        return 600
    elif row['DESIGNATION'] in ['RURAL SALES OFFICER', 'SALES OFFICER', 'TERRITORY SALES IN-CHARGE']:
        return 360
    else:
        return 0  # or any default value you prefer if the designation doesn't match any of the above
