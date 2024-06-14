def uppercrust(df, selected_states):
    # Step 1: Filter rows based on state
    filtered_df = df[df['STATE'].isin(selected_states)]

    # Step 2: Further filter rows based on designation
    filtered_df = filtered_df[filtered_df['DESIGNATION'].isin(['SALES REPRESENTATIVE', 'SALES EXECUTIVE','RURAL SALES OFFICER','SALES OFFICER','TERRITORY SALES IN-CHARGE'])]

    # Step 3: Rename EMPLOYEE NAME column to SALES EXECUTIVE
    filtered_df.rename(columns={'EMPLOYEE NAME': 'SALES EXECUTIVE'}, inplace=True)

    # Step 4: Compute the new column 'Order Fullfilment %'
    filtered_df['Order Fullfilment %'] = (filtered_df['Order Supplied in_ CASE'] / filtered_df['Sales (Qtyin Case)'] * 100).round(2).astype(str) + '%'
      
    # Step 5: Set default values for new columns
    filtered_df['Schedule Visit'] = df['Plan Mandays']*50
    

    # Step 6: Select desired columns
    selected_columns = [
        'Sales Officer', 'STATE','SALES EXECUTIVE', 'AON','Plan Mandays', 'ACTUAL MANDAYS TILL DATE', 
        'Schedule Visit', 'ACTUAL VISITED (TOTAL CALL)', 'PLAN PRODUCTIVITY ON TOTAL CALL',
        'Productivity on Total Call', 'Unique Store Mapped', 'PLAN UNIQUE STORE VISITED','Unique Store VISITED',
        'PLAN UNIQUE STORE PRODUCTIVE CALL', 'Unique Store Productive Call', 
        'LINE SOLD', 'Target', 'Sales (Qtyin Case)', '% Ach ( CLASSIC+COFFEE)', 
        'Order Supplied in_ CASE', 'Order Fullfilment %', 
        'HELL ENERGY CLASSIC', 'HELL ENERGY WATERMELON', 'HELL ENERGY COFFEE', 'HELL ENERGY APPLE'
    ]
    selected_df = filtered_df[selected_columns]
    total_row = {
        'Sales Officer': 'Grand Total',
        'STATE': '',
        'SALES EXECUTIVE': '',
	    'AON':'',
        'Plan Mandays': '',
        'ACTUAL MANDAYS TILL DATE': round(selected_df['ACTUAL MANDAYS TILL DATE'].mean(), 2),
        'Schedule Visit': round(selected_df['Schedule Visit'].sum(), 2),
        'ACTUAL VISITED (TOTAL CALL)': round(selected_df['ACTUAL VISITED (TOTAL CALL)'].sum(), 2),
        'PLAN PRODUCTIVITY ON TOTAL CALL':round(selected_df['PLAN PRODUCTIVITY ON TOTAL CALL'].sum(),2),
        'Productivity on Total Call': round(selected_df['Productivity on Total Call'].sum(), 2),
        'Unique Store Mapped': round(selected_df['Unique Store Mapped'].sum(), 2),
        'PLAN UNIQUE STORE VISITED': round(selected_df['PLAN UNIQUE STORE VISITED'].sum(),2),
        'Unique Store VISITED': round(selected_df['Unique Store VISITED'].sum(), 2),
        'PLAN UNIQUE STORE PRODUCTIVE CALL':round(selected_df['PLAN UNIQUE STORE PRODUCTIVE CALL'].sum(),2),
        'Unique Store Productive Call': round(selected_df['Unique Store Productive Call'].sum(), 2),
	    'LINE SOLD': round(selected_df['LINE SOLD'].sum(), 2),
        'Target': '',
        'Sales (Qtyin Case)': round(selected_df['Sales (Qtyin Case)'].sum(), 2),
        '% Ach ( CLASSIC+COFFEE)': '',
        'Order Supplied in_ CASE': round(selected_df['Order Supplied in_ CASE'].sum(), 2),
        'Order Fullfilment %': round((selected_df['Order Supplied in_ CASE'].sum() / selected_df['Sales (Qtyin Case)'].sum()) * 100, 2),
        'HELL ENERGY CLASSIC': round(selected_df['HELL ENERGY CLASSIC'].sum(), 2),
        'HELL ENERGY WATERMELON': round(selected_df['HELL ENERGY WATERMELON'].sum(), 2),
        'HELL ENERGY COFFEE': round(selected_df['HELL ENERGY COFFEE'].sum(), 2),
        'HELL ENERGY APPLE': round(selected_df['HELL ENERGY APPLE'].sum(), 2),
                }
    
    selected_df = selected_df.append(total_row, ignore_index=True)
    return selected_df

def uppercrust_city(df, city):
    # Step 1: Filter rows based on state
    filtered_df = df[df['CITY'].isin(city)]

    # Step 2: Further filter rows based on designation
    filtered_df = filtered_df[filtered_df['DESIGNATION'].isin(['SALES REPRESENTATIVE', 'SALES EXECUTIVE','RURAL SALES OFFICER','SALES OFFICER','TERRITORY SALES IN-CHARGE'])]

    # Step 3: Rename EMPLOYEE NAME column to SALES EXECUTIVE
    filtered_df.rename(columns={'EMPLOYEE NAME': 'SALES EXECUTIVE'}, inplace=True)

    # Step 4: Compute the new column 'Order Fullfilment %'
    filtered_df['Order Fullfilment %'] = (filtered_df['Order Supplied in_ CASE'] / filtered_df['Sales (Qtyin Case)'] * 100).round(2).astype(str) + '%'
      
    # Step 5: Set default values for new columns
    filtered_df['Schedule Visit'] = df['Plan Mandays']*50

    # Step 6: Sort the DataFrame by 'ASM'
    filtered_df.sort_values(by='ASM', inplace=True)

    # Step 7: Select desired columns
    selected_columns = [
        'Sales Officer', 'STATE','SALES EXECUTIVE', 'AON','Plan Mandays', 'ACTUAL MANDAYS TILL DATE', 
        'Schedule Visit', 'ACTUAL VISITED (TOTAL CALL)', 'PLAN PRODUCTIVITY ON TOTAL CALL',
        'Productivity on Total Call', 'Unique Store Mapped', 'PLAN UNIQUE STORE VISITED','Unique Store VISITED',
        'PLAN UNIQUE STORE PRODUCTIVE CALL', 'Unique Store Productive Call', 
        'LINE SOLD', 'Target', 'Sales (Qtyin Case)', '% Ach ( CLASSIC+COFFEE)', 
        'Order Supplied in_ CASE', 'Order Fullfilment %', 
        'HELL ENERGY CLASSIC', 'HELL ENERGY WATERMELON', 'HELL ENERGY COFFEE', 'HELL ENERGY APPLE'
    ]
    selected_df = filtered_df[selected_columns]
    total_row = {
        'Sales Officer': 'Grand Total',
        'STATE': '',
        'SALES EXECUTIVE': '',
	    'AON':'',
        'Plan Mandays': '',
        'ACTUAL MANDAYS TILL DATE': round(selected_df['ACTUAL MANDAYS TILL DATE'].mean(), 2),
        'Schedule Visit': round(selected_df['Schedule Visit'].sum(), 2),
        'ACTUAL VISITED (TOTAL CALL)': round(selected_df['ACTUAL VISITED (TOTAL CALL)'].sum(), 2),
        'PLAN PRODUCTIVITY ON TOTAL CALL':round(selected_df['PLAN PRODUCTIVITY ON TOTAL CALL'].sum(),2),
        'Productivity on Total Call': round(selected_df['Productivity on Total Call'].sum(), 2),
        'Unique Store Mapped': round(selected_df['Unique Store Mapped'].sum(), 2),
        'PLAN UNIQUE STORE VISITED': round(selected_df['PLAN UNIQUE STORE VISITED'].sum(),2),
        'Unique Store VISITED': round(selected_df['Unique Store VISITED'].sum(), 2),
        'PLAN UNIQUE STORE PRODUCTIVE CALL':round(selected_df['PLAN UNIQUE STORE PRODUCTIVE CALL'].sum(),2),
        'Unique Store Productive Call': round(selected_df['Unique Store Productive Call'].sum(), 2),
	    'LINE SOLD': round(selected_df['LINE SOLD'].sum(), 2),
        'Target': '',
        'Sales (Qtyin Case)': round(selected_df['Sales (Qtyin Case)'].sum(), 2),
        '% Ach ( CLASSIC+COFFEE)': '',
        'Order Supplied in_ CASE': round(selected_df['Order Supplied in_ CASE'].sum(), 2),
        'Order Fullfilment %': round((selected_df['Order Supplied in_ CASE'].sum() / selected_df['Sales (Qtyin Case)'].sum()) * 100, 2),
        'HELL ENERGY CLASSIC': round(selected_df['HELL ENERGY CLASSIC'].sum(), 2),
        'HELL ENERGY WATERMELON': round(selected_df['HELL ENERGY WATERMELON'].sum(), 2),
        'HELL ENERGY COFFEE': round(selected_df['HELL ENERGY COFFEE'].sum(), 2),
        'HELL ENERGY APPLE': round(selected_df['HELL ENERGY APPLE'].sum(), 2),
                }
    
    selected_df = selected_df.append(total_row, ignore_index=True)
    return selected_df

def uppercrust_som(df):
    # Step 1: Filter rows based on state
    filtered_df = df[(df['STATE'] == 'GOA') | ((df['CITY'] == 'PUNE') | (df['STATE'] == 'MAHARASHTRA') & (df['CITY'] != 'MUMBAI'))]

    # Step 2: Further filter rows based on designation
    filtered_df = filtered_df[filtered_df['DESIGNATION'].isin(['SALES REPRESENTATIVE', 'SALES EXECUTIVE','RURAL SALES OFFICER','SALES OFFICER','TERRITORY SALES IN-CHARGE'])]

    # Step 3: Rename EMPLOYEE NAME column to SALES EXECUTIVE
    filtered_df.rename(columns={'EMPLOYEE NAME': 'SALES EXECUTIVE'}, inplace=True)

    # Step 4: Compute the new column 'Order Fullfilment %'
    filtered_df['Order Fullfilment %'] = (filtered_df['Order Supplied in_ CASE'] / filtered_df['Sales (Qtyin Case)'] * 100).round(2).astype(str) + '%'
      
    # Step 5: Set default values for new columns
    filtered_df['Schedule Visit'] = df['Plan Mandays']*50
    filtered_df['Schedule Prodcutive Visit'] = 600
    filtered_df['Schedule Unique Store Product Visit'] = 600

    # Step 6: Sort the DataFrame by 'ASM'
    filtered_df.sort_values(by='ASM', inplace=True)

    # Step 7: Select desired columns
    selected_columns = [
        'Sales Officer', 'STATE','SALES EXECUTIVE','AON', 'Plan Mandays', 'ACTUAL MANDAYS TILL DATE', 
        'Schedule Visit', 'ACTUAL VISITED (TOTAL CALL)', 'PLAN PRODUCTIVITY ON TOTAL CALL',
        'Productivity on Total Call', 'Unique Store Mapped', 'PLAN UNIQUE STORE VISITED','Unique Store VISITED',
        'PLAN UNIQUE STORE PRODUCTIVE CALL', 'Unique Store Productive Call', 
        'LINE SOLD', 'Target', 'Sales (Qtyin Case)', '% Ach ( CLASSIC+COFFEE)', 
        'Order Supplied in_ CASE', 'Order Fullfilment %', 
        'HELL ENERGY CLASSIC', 'HELL ENERGY WATERMELON', 'HELL ENERGY COFFEE', 'HELL ENERGY APPLE'
    ]
    selected_df = filtered_df[selected_columns]
    total_row = {
        'Sales Officer': 'Grand Total',
        'STATE': '',
        'SALES EXECUTIVE': '',
	    'AON':'',
        'Plan Mandays': '',
        'ACTUAL MANDAYS TILL DATE': round(selected_df['ACTUAL MANDAYS TILL DATE'].mean(), 2),
        'Schedule Visit': round(selected_df['Schedule Visit'].sum(), 2),
        'ACTUAL VISITED (TOTAL CALL)': round(selected_df['ACTUAL VISITED (TOTAL CALL)'].sum(), 2),
        'PLAN PRODUCTIVITY ON TOTAL CALL':round(selected_df['PLAN PRODUCTIVITY ON TOTAL CALL'].sum(),2),
        'Productivity on Total Call': round(selected_df['Productivity on Total Call'].sum(), 2),
        'Unique Store Mapped': round(selected_df['Unique Store Mapped'].sum(), 2),
        'PLAN UNIQUE STORE VISITED': round(selected_df['PLAN UNIQUE STORE VISITED'].sum(),2),
        'Unique Store VISITED': round(selected_df['Unique Store VISITED'].sum(), 2),
        'PLAN UNIQUE STORE PRODUCTIVE CALL':round(selected_df['PLAN UNIQUE STORE PRODUCTIVE CALL'].sum(),2),
        'Unique Store Productive Call': round(selected_df['Unique Store Productive Call'].sum(), 2),
	    'LINE SOLD': round(selected_df['LINE SOLD'].sum(), 2),
        'Target': '',
        'Sales (Qtyin Case)': round(selected_df['Sales (Qtyin Case)'].sum(), 2),
        '% Ach ( CLASSIC+COFFEE)': '',
        'Order Supplied in_ CASE': round(selected_df['Order Supplied in_ CASE'].sum(), 2),
        'Order Fullfilment %': round((selected_df['Order Supplied in_ CASE'].sum() / selected_df['Sales (Qtyin Case)'].sum()) * 100, 2),
        'HELL ENERGY CLASSIC': round(selected_df['HELL ENERGY CLASSIC'].sum(), 2),
        'HELL ENERGY WATERMELON': round(selected_df['HELL ENERGY WATERMELON'].sum(), 2),
        'HELL ENERGY COFFEE': round(selected_df['HELL ENERGY COFFEE'].sum(), 2),
        'HELL ENERGY APPLE': round(selected_df['HELL ENERGY APPLE'].sum(), 2),
                }
    
    selected_df = selected_df.append(total_row, ignore_index=True)
    return selected_df

