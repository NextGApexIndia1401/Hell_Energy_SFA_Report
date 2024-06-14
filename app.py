import streamlit as st
import pandas as pd
import numpy as np
from MIS_Operation import SFA as sf
from MIS_Operation import sales_report as sr
from MIS_Operation import coverage_report as cr
from MIS_Operation import excel_download as eo
from MIS_Operation import attendance as att
from MIS_Operation import call_cycle_report as cc
from MIS_Operation import utils
import pyodbc
import json
import datetime
import plotly.express as px
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pyautogui


# Database connection details
server = '103.7.181.119'
database = 'NEXTG_DWH_HELLENERGY'
database_1 = 'SimplyAmplify'
username = 'Yashs'
password = 'yashshinde$0310$'

stored_procedures = {
    "usp_web_master_callcycle": "Web Master Call Cycle",
    "usp_web_report_mtdattendance": "Web Report MTD Attendance",
    "usp_web_report_coverage_daily": "Web Report Coverage Daily",
    "usp_web_report_customersales": "Web Report Customer Sales",
    "usp_web_report_order_fullfillment": "Web Report Order Fullfillment"
}

@st.cache(allow_output_mutation=True)
def execute_stored_procedure(sp_name, from_date, to_date):
    """
    Execute a stored procedure with a JSON payload and return the results as a pandas DataFrame.

    This function connects to a SQL Server database using the provided connection details and executes a stored procedure
    with a JSON payload. The payload contains information about the report type and date filters. The function fetches
    the results of the stored procedure, converts them to a pandas DataFrame, and returns the DataFrame.

    Parameters:
        sp_name (str): The name of the stored procedure to execute.
        from_date (datetime.date): The starting date for the date filter.
        to_date (datetime.date): The ending date for the date filter.
        server (str): The server name for the database connection.
        database (str): The database name for the connection.
        username (str): The username for the database connection.
        password (str): The password for the database connection.

    Returns:
        pandas.DataFrame: A DataFrame containing the results of the stored procedure.
    """
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()

    # Prepare the payload
    payload = {
        "Data": {
            "report": "customer-sales",
            "filters": {
                "from": from_date.strftime("%Y-%m-%d"),
                "to": to_date.strftime("%Y-%m-%d")
            }
        },
        "requesttype": "web"
    }

    # Convert payload dictionary to JSON string
    payload_json = json.dumps(payload)

    # Execute the stored procedure with the payload
    cursor.execute(f"EXEC [dbo].[{sp_name}] ?", payload_json)

    # Fetch all results
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    # Extract data from tuples and create DataFrame
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in results]

    # Create DataFrame
    df = pd.DataFrame(data)

    return df

@st.cache(allow_output_mutation=True)
def extract_table_data(server, database_1, username, password):
    # Establish connection to the database
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database_1+';UID='+username+';PWD='+password)
    cursor = conn.cursor()
    current_month = datetime.datetime.now().month
    # Execute SQL query to fetch data from the table
    cursor.execute(f"SELECT userID,target FROM MobiTarget where year = 2024 and month = 4")

    # Fetch all results
    results = cursor.fetchall()

    # Close the connection
    conn.close()

    # Extract data from tuples and create DataFrame
    columns = [desc[0] for desc in cursor.description]
    data = [dict(zip(columns, row)) for row in results]

    # Create DataFrame
    df = pd.DataFrame(data)

    return df

# def login(username, password):
#     correct_username = 'hell'
#     correct_password = '1234'
#     return username == correct_username and password == correct_password
def login(username, password):
    credentials = {
        'admin@hellenergy': 'nextg@2024',
        'mis@hellenergy': 'nextg@1234',  # Add as many users as needed
    }
    return credentials.get(username) == password

# Main function
def main():
    st.sidebar.title("MIS Automation Software")
    st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ4vvJv6peKLV5eBhXKD_S2_HPh9OFGXl6UzAzMmJNJMA&s")
    
    st.sidebar.info("Streamlining operations and boosting productivity through advanced MIS automation.")
    choice = st.sidebar.selectbox("Navigation", ["Login", "Hell Energy MIS", "Visualisation"])

    if choice == "Login":
        st.title("Login")
        userss = st.text_input("Username")
        passs = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(userss, passs):
                st.session_state.logged_in = True
                st.success("Login successful!")
            
            else:
              st.error("Invalid username or password. Please try again.")
    
    elif st.session_state.get("logged_in", False):

        if choice == "Hell Energy MIS":
            st.header('MIS Automation Software', divider='rainbow')
            st.write("MIS Automation Software is a cutting-edge solution designed to automate mundane tasks, streamline data management, and enhance decision-making processes within organizations, ultimately boosting efficiency and productivity.")
        
            # Date input for "from" and "to" filters
            from_date = st.date_input('From Date')
            to_date = st.date_input('To Date')

            # Execute each stored procedure and store results in separate DataFrames
            sp_names = ['usp_web_master_callcycle', 'usp_web_report_mtdattendance',
                        'usp_web_report_coverage_daily', 'usp_web_report_customersales',
                        'usp_web_report_order_fullfillment','usp_web_master_user']

            sp_dfs = {}  # Dictionary to store DataFrames for each stored procedure

            for sp_name in sp_names:
                sp_dfs[sp_name] = execute_stored_procedure(sp_name, from_date, to_date)
                
            
            df_1 = extract_table_data(server, database_1, username, password)
            
            # aa = sp_dfs["usp_web_report_customersales"]
            # excel_data, excel_filename = eo.download_excel(aa, "Summary Report")
            # st.download_button(label=excel_filename, data=excel_data, file_name=excel_filename, mime="application/vnd.ms-excel")

            # User Master
            active_master_df = sp_dfs['usp_web_master_user']
            
            # Filter rows where STATUS is ACTIVE
            master_df = active_master_df[active_master_df['STATUS'] == 'ACTIVE']
            master_df['DATE OF JOINING'] = pd.to_datetime(master_df['DATE OF JOINING'])
            master_df['DATE OF JOINING'] = master_df['DATE OF JOINING'].dt.strftime('%Y-%m-%d')
            # master_df.drop('EMPLOYEE CODE.1', axis=1, inplace=True)
            master_df.loc[master_df['Client Name'] == 'HellEnergy', 'PAYROLL'] = 'NextG'

            # Replace 'Upper Crust' with 'Upper Crust' in the 'PAYROLL' column
            master_df.loc[master_df['Client Name'] == 'Upper Crust', 'PAYROLL'] = 'Upper Crust'
            master_df['Sales Officer'] = master_df['LEVEL2 EMPLOYEE NAME']
            master_df['ASM'] = master_df['LEVEL3 EMPLOYEE NAME']
            master_df = pd.merge(master_df, df_1[['userID', 'target']], left_on='USERID', right_on='userID', how='left')
            master_df.rename(columns={'target': 'Target'}, inplace=True)
            master_df['Target'].fillna(0, inplace=True)
            st.write("## User Master Data")
            st.write(master_df)
                    

            st.header(':rainbow[View and Download Pivot Data]',divider='rainbow')      
            # Average Lines
            avg_lines_df = sr.calculate_aggregates(sp_dfs['usp_web_report_customersales'])
            
            brand_df_1 = sr.calculate_avg_lines_today(sp_dfs['usp_web_report_customersales'])
            # Brand Wise Sales    
            brand_df = sr.calculate_avg_lines(sp_dfs['usp_web_report_customersales'])
            # Order Book & Fullfillment
            order_dump_summary = sr.process_order_dump(sp_dfs['usp_web_report_order_fullfillment'])
            # Order Off Bill
            order_drop_summary_2 = sr.process_order_dump_total_tickets_with_filter(sp_dfs['usp_web_report_order_fullfillment'])
            # Unique Coverage
            uts = cr.process_store_codes(sp_dfs['usp_web_report_coverage_daily'])
            # TCPC
            tcpc = cr.process_employee_data(sp_dfs['usp_web_report_coverage_daily'])
            # Attendance MTD
            attc = att.sum_p_values_by_employee(sp_dfs['usp_web_report_mtdattendance'])
            # Callcycle         
            callc = cc.process_employee_data(sp_dfs['usp_web_master_callcycle'])

            def concatenate_filtered_dataframes(selected_dfs):
                filtered_dfs = []
                for df in selected_dfs:
                    # Filter DataFrame based on the condition
                    filtered_df = df[df['EMPLOYEE CODE'].str.match(r'TEMP\d{4,5}$')]
                    filtered_dfs.append(filtered_df)
                
                # Merge filtered DataFrames on the 'EMPLOYEE CODE' column
                concatenated_df = filtered_dfs[0]
                for i, df in enumerate(filtered_dfs[1:], start=2):
                    # Rename 'EMPLOYEE NAME' column to avoid duplication
                    df = df.rename(columns={"EMPLOYEE NAME": f"EMPLOYEE NAME_{i}"})
                    concatenated_df = pd.merge(concatenated_df, df, on='EMPLOYEE CODE', how='outer')
                
                # Choose one 'EMPLOYEE NAME' column to retain and drop the rest
                employee_name_columns = [col for col in concatenated_df.columns if 'EMPLOYEE NAME' in col]
                if len(employee_name_columns) > 1:
                    concatenated_df = concatenated_df.drop(columns=employee_name_columns[1:])
                
                # Drop duplicate 'EMPLOYEE NAME' columns
                concatenated_df = concatenated_df.rename(columns={employee_name_columns[0]: 'EMPLOYEE NAME'})
                concatenated_df = concatenated_df.dropna(thresh=len(concatenated_df.columns) - 2)
                return concatenated_df

        # Your list of DataFrames
            dataframes = [
                ("Attendance", attc),
                ("Total TC PC", tcpc),
                ("Unique Coverage", uts),
                ("Order Off Bill", order_drop_summary_2),
                ("Ord Book & FF", order_dump_summary),
                ("Brand Wise Sales", brand_df_1),
                ("Avg Lines", avg_lines_df),
                ("Call Cycle", callc)
            ]

            # Create a multiselect option to allow the user to choose multiple DataFrames
            selected_names = st.multiselect("Select Pivot data to display and download:", [name for name, df in dataframes])

            # Find the selected DataFrames based on the selected names
            selected_dfs = []
            for name, df in dataframes:
                if name in selected_names:
                    selected_dfs.append(df)

            # Display the selected DataFrames as a single DataFrame and provide a download button
            if selected_dfs:
                # Concatenate selected DataFrames into a single DataFrame
                concatenated_df = concatenate_filtered_dataframes(selected_dfs)
                
                # Display the concatenated DataFrame
                st.dataframe(concatenated_df)
                
                # Create a download button for the concatenated DataFrame
                excel_data, excel_filename = eo.download_excel(concatenated_df, "selected_data.xlsx")
                st.download_button(
                    label=f"Download {excel_filename}",
                    data=excel_data,
                    file_name=excel_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # Select the required columns from the filtered master_df
            result_df = master_df[['EMPLOYEE CODE', 'EMPLOYEE NAME', 'DATE OF JOINING', 'Sales Officer', 'ASM','DESIGNATION' ,'AON','Target']]
            # result_df = result_df.rename(columns={'LEVEL2 EMPLOYEE NAME': 'Sales Officer', 'LEVEL3 EMPLOYEE NAME': 'ASM'})

            st.header(':blue[Enter the Plan Mandays] :1234:',divider='blue')        
            


            selected_states_rajasthan = ['RAJASTHAN']
            selected_states_other = ['CHANDIGARH', 'PUNJAB', 'HARYANA', 'JAMMU & KASHMIR', 'HIMACHAL PRADESH', 'JAMMU']
            selected_states_UP = ['UTTAR PRADESH','UTTAR PRADESH EAST','UTTARAKHAND']
            selected_states_delhi = ['DELHI']
            selected_states_karnataka  = ['KARNATAKA']
            selected_states_tamil = ['TAMIL NADU']
            selected_states_ap_tel = ['ANDHRA PRADESH','TELANGANA']
            selected_states_guj = ['GUJARAT','CHHATTISGARH','MADHYA PRADESH']
            selected_states_assam = ['ASSAM']
            selected_states_mum = ['MUMBAI']

            # Remove duplicate rows for 'TEMP804'
            result_df =  result_df.drop_duplicates(subset=['EMPLOYEE CODE'])

            # Add a new column with a default value of 15
            def get_distinct_states(df):
                return df['STATE'].unique()
            # current_month = datetime.datetime.now().month
            # current_year = datetime.datetime.now().year
            # days_in_current_month = (datetime.datetime.now() - datetime.datetime(current_year, current_month, 1)).days + 1
            distinct_states = get_distinct_states(master_df)
        
            selected_states = st.multiselect("Select State(s)", distinct_states)

            # Default Plan Mandays value for states not selected
            default_plan_mandays = st.number_input("Enter Default Plan Mandays", min_value=0)
            
        
            # Input fields for each selected state
            for state in selected_states:
                plan_mandays = st.number_input(f'Enter Plan Mandays for {state}', min_value=0)
                

                # Update Plan Mandays for selected states
                result_df.loc[master_df['STATE'] == state, 'Plan Mandays'] = plan_mandays
                # employees_in_current_month = master_df[(master_df['STATE'] == state) & (master_df['DATE OF JOINING'].dt.month == current_month)]
                # for index, row in employees_in_current_month.iterrows():
                #     result_df.loc[index, 'Plan Mandays'] -= days_in_current_month
            # Set default Plan Mandays for states not selected
            not_selected_states = set(distinct_states) - set(selected_states)
            for state in not_selected_states:
                result_df.loc[master_df['STATE'] == state, 'Plan Mandays'] = default_plan_mandays
            
                    
            # Drop duplicate attendance records and select only the 'Employee Code' and 'Attendance Name' columns
            unique_attendance = attc.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Attendance']]
                    
            # Merge with Employee Code
            merged_df = pd.merge(result_df, unique_attendance, on='EMPLOYEE CODE', how='left')
            merged_df.rename(columns={'Attendance': 'ACTUAL MANDAYS TILL DATE'}, inplace=True)
            merged_df['Mandays'] = ( merged_df['ACTUAL MANDAYS TILL DATE'] /merged_df['Plan Mandays']) * 100
            merged_df['Mandays'] = merged_df['Mandays'].map(lambda x: '{:.0f}%'.format(x))
            merged_df['VISIT PLANNED'] = merged_df.apply(utils.calculate_visit_planned, axis=1)
                            
            unique_visit = tcpc.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'VISITED']]
            merged_df_2 = pd.merge(merged_df, unique_visit, on='EMPLOYEE CODE', how='left')
            merged_df_2.rename(columns={'VISITED': 'ACTUAL VISITED (TOTAL CALL)'}, inplace=True)
            merged_df_2['COVERAGE % (TOTAL CALL ON PLANNED)'] = ( merged_df_2['ACTUAL VISITED (TOTAL CALL)'] /merged_df_2['VISIT PLANNED']) * 100
            merged_df_2['COVERAGE % (TOTAL CALL ON PLANNED)'] = merged_df_2['COVERAGE % (TOTAL CALL ON PLANNED)'].map(lambda x: '{:.0f}%'.format(x))
                
            unique_visit_1 = tcpc.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'BILLED']]
            merged_df_3 = pd.merge(merged_df_2, unique_visit_1, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'BILLED': 'Productivity on Total Call'}, inplace=True)
            merged_df_3['% Productivity (on Total Visit)'] = ( merged_df_3['Productivity on Total Call'] /merged_df_3['ACTUAL VISITED (TOTAL CALL)']) * 100
            merged_df_3['% Productivity (on Total Visit)'] = merged_df_3['% Productivity (on Total Visit)'].map(lambda x: '{:.0f}%'.format(x))
        
            unique_visit_2 = callc.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Distinct Store Count']]
            unique_visit_3 = uts.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Total']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_2, on='EMPLOYEE CODE', how='left')
            merged_df_3 = pd.merge(merged_df_3, unique_visit_3, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Distinct Store Count': 'Unique Store Mapped','Total':'Unique Store VISITED'}, inplace=True)
            merged_df_3['Coverage_% (on Unique Store Mapped)'] = ( merged_df_3['Unique Store VISITED'] /merged_df_3['Unique Store Mapped']) * 100
            merged_df_3['Coverage_% (on Unique Store Mapped)'] = merged_df_3['Coverage_% (on Unique Store Mapped)'].map(lambda x: '{:.0f}%'.format(x))
            
            unique_visit_4 = uts.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', '1']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_4, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'1': 'Unique Store Productive Call'}, inplace=True)
            merged_df_3['% Productivity on Unique Store Visit'] = ( merged_df_3['Unique Store Productive Call'] /merged_df_3['Unique Store VISITED']) * 100
            merged_df_3['% Productivity on Unique Store Visit'] = merged_df_3['% Productivity on Unique Store Visit'].map(lambda x: '{:.0f}%'.format(x))
            merged_df_3['PLAN PRODUCTIVITY ON TOTAL CALL'] = merged_df_3.apply(utils.calculate_plan_productivity, axis=1)
            merged_df_3['PLAN UNIQUE STORE VISITED'] = merged_df_3.apply(utils.calculate_plan_unique_store_visited, axis=1)
            merged_df_3['PLAN UNIQUE STORE PRODUCTIVE CALL'] = merged_df_3.apply(utils.calculate_plan_unique_store_visited, axis=1)
            
            column_order = ['EMPLOYEE CODE', 'EMPLOYEE NAME', 'DATE OF JOINING', 'Sales Officer', 'ASM', 'DESIGNATION','AON',
                        'Plan Mandays', 'ACTUAL MANDAYS TILL DATE', 'Mandays', 'VISIT PLANNED', 'ACTUAL VISITED (TOTAL CALL)',
                        'COVERAGE % (TOTAL CALL ON PLANNED)', 'PLAN PRODUCTIVITY ON TOTAL CALL','Productivity on Total Call', '% Productivity (on Total Visit)',
                        'Unique Store Mapped', 'PLAN UNIQUE STORE VISITED','Unique Store VISITED', 'Coverage_% (on Unique Store Mapped)','PLAN UNIQUE STORE PRODUCTIVE CALL',
                        'Unique Store Productive Call', '% Productivity on Unique Store Visit', 'Target']
            
            merged_df_3 = merged_df_3.reindex(columns=column_order)
            unique_visit_7 = brand_df.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Grand Total']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_7, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Grand Total': 'Sales (Qtyin Case)'}, inplace=True)
            merged_df_3['Sales (Qtyin Case)'] = merged_df_3['Sales (Qtyin Case)'].fillna(0)
            merged_df_3['Sales (Qtyin Case)'] = merged_df_3['Sales (Qtyin Case)'].map(lambda x: '{:.0f}'.format(round(x))).astype('float')

            merged_df_3['Target'] = pd.to_numeric(merged_df_3['Target'], errors='coerce')  # Convert to numeric, replacing errors with NaN

            merged_df_3['% Ach ( CLASSIC+COFFEE)'] = np.where(
                merged_df_3['Target'] != 0,  # Check if denominator is not zero (including NaN)
                np.divide(merged_df_3['Sales (Qtyin Case)'], merged_df_3['Target'])*100,
                0  # Replace division by zero or NaN with NaN
            )

            merged_df_3['% Ach ( CLASSIC+COFFEE)'] = merged_df_3['% Ach ( CLASSIC+COFFEE)'].map(lambda x: '{:.0f}%'.format(x))

            # merged_df_3 = pd.merge(merged_df_3, brand_df[['EMPLOYEE CODE', 'Grand Total']], on='EMPLOYEE CODE', how='left')

            # # Rename the 'Grand Total' column to 'Sales (Qtyin Case)'
            # merged_df_3.rename(columns={'Grand Total': 'Sales (Qtyin Case)'}, inplace=True)

            unique_visit_5 = brand_df.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'CLASSIC','WATERMELON','COFFEE','APPLE']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_5, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'CLASSIC': 'HELL ENERGY CLASSIC','WATERMELON':'HELL ENERGY WATERMELON','COFFEE':'HELL ENERGY COFFEE','APPLE':'HELL ENERGY APPLE'}, inplace=True)
                
            unique_visit_6 = avg_lines_df.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Avg Lines']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_6, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Avg Lines': 'LINE SOLD'}, inplace=True)
                    

            merged_df_3['PER STORE AVG CASE SOLD'] = (merged_df_3['Sales (Qtyin Case)'] /merged_df_3['Productivity on Total Call'])
            merged_df_3['PER STORE AVG CASE SOLD'] = merged_df_3['PER STORE AVG CASE SOLD'].map(lambda x: '{:.0f}'.format(x))

            merged_df_3['AVG. Per Day sales'] = np.where(
            merged_df_3['ACTUAL MANDAYS TILL DATE'] != 0,
            merged_df_3['Sales (Qtyin Case)'] / merged_df_3['ACTUAL MANDAYS TILL DATE'],
            np.nan  # Replace division by zero with NaN
            )

            # Fill NaN values with 0
            merged_df_3['AVG. Per Day sales'] = merged_df_3['AVG. Per Day sales'].fillna(0)

            # Apply formatting to 'AVG. Per Day sales' column
            merged_df_3['AVG. Per Day sales'] = merged_df_3['AVG. Per Day sales'].map(lambda x: '{:.0f}'.format(round(x))) 

            merged_df_3['AVG. Per Day Visit (on Total)'] = np.where(
            merged_df_3['ACTUAL MANDAYS TILL DATE'] != 0,
            merged_df_3['ACTUAL VISITED (TOTAL CALL)'] / merged_df_3['ACTUAL MANDAYS TILL DATE'],
            np.nan  # Replace division by zero with NaN
            )
            # Fill NaN values with 0
            merged_df_3['AVG. Per Day Visit (on Total)'] = merged_df_3['AVG. Per Day Visit (on Total)'].fillna(0)
            # Apply formatting to 'AVG. Per Day Visit (on Total)' column
            merged_df_3['AVG. Per Day Visit (on Total)'] = merged_df_3['AVG. Per Day Visit (on Total)'].map(
                lambda x: '{:.0f}'.format(round(x)) if np.isfinite(x) else ''
            )
            
            merged_df_3['AVG. Per Day Productivity (On Total)'] = np.where(
            merged_df_3['ACTUAL MANDAYS TILL DATE'] != 0,
            merged_df_3['Productivity on Total Call'] / merged_df_3['ACTUAL MANDAYS TILL DATE'],
            np.nan  # Replace division by zero with NaN
            )

            # Fill NaN values with 0
            merged_df_3['AVG. Per Day Productivity (On Total)'] = merged_df_3['AVG. Per Day Productivity (On Total)'].fillna(0)

            # Apply formatting to 'AVG. Per Day Productivity (On Total)' column
            merged_df_3['AVG. Per Day Productivity (On Total)'] = merged_df_3['AVG. Per Day Productivity (On Total)'].map(
                lambda x: '{:.0f}'.format(round(x)) if np.isfinite(x) else ''
            ).astype(float)


            merged_df_3['AVG. Per Day Visit (on Unique Call)'] = np.where(
            merged_df_3['ACTUAL MANDAYS TILL DATE'] != 0,
            merged_df_3['Unique Store VISITED'] / merged_df_3['ACTUAL MANDAYS TILL DATE'],
            np.nan  # Replace division by zero with NaN
            )

            # Fill NaN values with 0
            merged_df_3['AVG. Per Day Visit (on Unique Call)'] = merged_df_3['AVG. Per Day Visit (on Unique Call)'].fillna(0)

            # Apply formatting to 'AVG. Per Day Visit (on Unique Call)' column
            merged_df_3['AVG. Per Day Visit (on Unique Call)'] = merged_df_3['AVG. Per Day Visit (on Unique Call)'].map(
                lambda x: '{:.0f}'.format(round(x)) if np.isfinite(x) else ''
            ).astype(float)

            unique_visit_8 = order_dump_summary.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Ticket Count']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_8, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Ticket Count': 'Count of _Bills Generated'}, inplace=True)

            unique_visit_9 = order_drop_summary_2.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Total Tickets']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_9, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Total Tickets': 'Count of Bill`s Supplied'}, inplace=True)
            merged_df_3['Count of Bill`s Supplied'] = merged_df_3['Count of Bill`s Supplied'].fillna(0)
                    
            merged_df_3['Order Fullfilment ( Order Bill  Vs Supplied Bill)'] = (merged_df_3['Count of Bill`s Supplied'] /merged_df_3['Count of _Bills Generated'])*100
            merged_df_3['Order Fullfilment ( Order Bill  Vs Supplied Bill)'] = merged_df_3['Order Fullfilment ( Order Bill  Vs Supplied Bill)'].map(lambda x: '{:.0f}%'.format(x))

            unique_visit_10 = order_dump_summary.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Quantity Sum']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_10, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Quantity Sum': 'Order Generated in_ CASE'}, inplace=True)
            merged_df_3['Order Generated in_ CASE']  =  merged_df_3['Order Generated in_ CASE'].map(lambda x: '{:.0f}'.format(x))

            unique_visit_11 = order_dump_summary.drop_duplicates(subset=['EMPLOYEE CODE'])[['EMPLOYEE CODE', 'Units']]
            merged_df_3 = pd.merge(merged_df_3, unique_visit_11, on='EMPLOYEE CODE', how='left')
            merged_df_3.rename(columns={'Units': 'Order Supplied in_ CASE'}, inplace=True)
            merged_df_3['Order Supplied in_ CASE']  =  merged_df_3['Order Supplied in_ CASE'].map(lambda x: '{:.0f}'.format(x))
                    
            merged_df_3['Order Supplied in_ CASE'] = pd.to_numeric(merged_df_3['Order Supplied in_ CASE'], errors='coerce')
            merged_df_3['Order Generated in_ CASE'] = pd.to_numeric(merged_df_3['Order Generated in_ CASE'], errors='coerce')

            # Perform the division and calculate the percentage
            merged_df_3['Order Fullfilment  ( Order Vs Invoice) %'] = (merged_df_3['Order Supplied in_ CASE'] / merged_df_3['Order Generated in_ CASE']) * 100

            # Format the percentage as a string with 0 decimal places
            merged_df_3['Order Fullfilment  ( Order Vs Invoice) %'] = merged_df_3['Order Fullfilment  ( Order Vs Invoice) %'].map(lambda x: '{:.0f}%'.format(x))
                    
            final_df = pd.merge(merged_df_3, master_df[['EMPLOYEE CODE', 'STATUS', 'REGION', 'STATE', 'CITY','PAYROLL']], on='EMPLOYEE CODE', how='left')
            # Create the 'PAYROLL' column with the values from 'Client Name'

            final_df = final_df[final_df['DESIGNATION'].isin(['SALES REPRESENTATIVE', 'SALES EXECUTIVE','RURAL SALES OFFICER','SALES OFFICER','TERRITORY SALES IN-CHARGE'])]
            final_df = final_df[~((final_df['DESIGNATION'] == "SALES OFFICER") & (final_df['Sales (Qtyin Case)'].isnull() | (final_df['Sales (Qtyin Case)'] == 0)))]
            final_df = final_df[(final_df['ACTUAL MANDAYS TILL DATE'] != 0) & (~final_df['ACTUAL VISITED (TOTAL CALL)'].isnull())]

            
            ## Don't Touch
            st.session_state.df = final_df
            numeric_columns = ['ACTUAL MANDAYS TILL DATE', 'VISIT PLANNED', 'ACTUAL VISITED (TOTAL CALL)','Productivity on Total Call',
                    'Unique Store Mapped', 'Unique Store VISITED', 'Unique Store Productive Call', 'Sales (Qtyin Case)',
                    'HELL ENERGY CLASSIC', 'HELL ENERGY WATERMELON', 'HELL ENERGY COFFEE', 'HELL ENERGY APPLE',
                    'LINE SOLD', 'PER STORE AVG CASE SOLD', 'AVG. Per Day sales', 'AVG. Per Day Visit (on Total)',
                    'AVG. Per Day Productivity (On Total)', 'Count of _Bills Generated', 'Count of Bill`s Supplied',
                    'Order Generated in_ CASE', 'Order Supplied in_ CASE']
            final_df[numeric_columns] = final_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
            total_row = {
        'EMPLOYEE CODE': 'Grand Total',
        'EMPLOYEE NAME': '',
        'DATE OF JOINING': '',
        'Sales Officer': '',
        'ASM': '',
        'DESIGNATION': '',
        'Plan Mandays': '',
        'ACTUAL MANDAYS TILL DATE': round(final_df['ACTUAL MANDAYS TILL DATE'].mean(), 2),
        'VISIT PLANNED': round(final_df['VISIT PLANNED'].sum(), 2),
        'ACTUAL VISITED (TOTAL CALL)': round(final_df['ACTUAL VISITED (TOTAL CALL)'].sum(), 2),
        'COVERAGE % (TOTAL CALL ON PLANNED)': round((final_df['ACTUAL VISITED (TOTAL CALL)'].sum() / final_df['VISIT PLANNED'].sum()) * 100, 2),
        'PLAN PRODUCTIVITY ON TOTAL CALL':round(final_df['PLAN PRODUCTIVITY ON TOTAL CALL'].sum(),2),
        'Productivity on Total Call': round(final_df['Productivity on Total Call'].sum(), 2),
        '% Productivity (on Total Visit)': round((final_df['Productivity on Total Call'].sum() / final_df['ACTUAL VISITED (TOTAL CALL)'].sum()) * 100, 2),
        'Unique Store Mapped': round(final_df['Unique Store Mapped'].sum(), 2),
        'PLAN UNIQUE STORE VISITED': round(final_df['PLAN UNIQUE STORE VISITED'].sum(),2),
        'Unique Store VISITED': round(final_df['Unique Store VISITED'].sum(), 2),
        'Coverage_% (on Unique Store Mapped)': round((final_df['Unique Store VISITED'].sum() / final_df['Unique Store Mapped'].sum()) * 100, 2),
        'PLAN UNIQUE STORE PRODUCTIVE CALL':round(final_df['PLAN UNIQUE STORE PRODUCTIVE CALL'].sum(),2),
        'Unique Store Productive Call': round(final_df['Unique Store Productive Call'].sum(), 2),
        '% Productivity on Unique Store Visit': round((final_df['Unique Store Productive Call'].sum() / final_df['Unique Store VISITED'].sum()) * 100, 2),
        'Target': '',
        'Sales (Qtyin Case)': round(final_df['Sales (Qtyin Case)'].sum(), 2),
        '% Ach ( CLASSIC+COFFEE)': '',
        'HELL ENERGY CLASSIC': round(final_df['HELL ENERGY CLASSIC'].sum(), 2),
        'HELL ENERGY WATERMELON': round(final_df['HELL ENERGY WATERMELON'].sum(), 2),
        'HELL ENERGY COFFEE': round(final_df['HELL ENERGY COFFEE'].sum(), 2),
        'HELL ENERGY APPLE': round(final_df['HELL ENERGY APPLE'].sum(), 2),
        'LINE SOLD': round(final_df['LINE SOLD'].sum(), 2),
        'PER STORE AVG CASE SOLD': round(final_df['PER STORE AVG CASE SOLD'].mean(), 2),
        'AVG. Per Day sales': round(final_df['AVG. Per Day sales'].sum(), 2),
        'AVG. Per Day Visit (on Total)': round(final_df['AVG. Per Day Visit (on Total)'].sum(), 2),
        'AVG. Per Day Productivity (On Total)': round(final_df['AVG. Per Day Productivity (On Total)'].sum(), 2),
        'AVG. Per Day Visit (on Unique Call)': round(final_df['AVG. Per Day Visit (on Unique Call)'].mean(), 2),
        'Count of _Bills Generated': round(final_df['Count of _Bills Generated'].sum(), 2),
        'Count of Bill`s Supplied': round(final_df['Count of Bill`s Supplied'].sum(), 2),
        'Order Fullfilment ( Order Bill  Vs Supplied Bill)': round((final_df['Count of Bill`s Supplied'].sum() / final_df['Count of _Bills Generated'].sum()) * 100, 2),
        'Order Generated in_ CASE': round(final_df['Order Generated in_ CASE'].sum(), 2),
        'Order Supplied in_ CASE': round(final_df['Order Supplied in_ CASE'].sum(), 2),
        'Order Fullfilment  ( Order Vs Invoice) %': round((final_df['Order Supplied in_ CASE'].sum() / final_df['Order Generated in_ CASE'].sum()) * 100, 2),
        'STATUS': '',
        'REGION': '',
        'STATE': '',
        'CITY': '',
        'PAYROLL': ''
        }
            filter_df = final_df.append(total_row, ignore_index=True)

            # Streamlit app

            st.header(':green[Employee Search] :mag:',divider='green')
            # Search bar
            search_term = st.text_input('Enter Employee Code:', '')
            st.write(filter_df)
            # Filter DataFrame based on search term
            filtered_df = utils.filter_by_employee_code(final_df, search_term)
            if filtered_df.empty:
                st.write('Please Enter the Employee Code')
            else:
                st.write(filtered_df)
            
            st.header(':green[ASM Filter] :mag:',divider='green')
            selected_asms = st.multiselect('Select ASM(s):', final_df['ASM'].unique())
            filtered_df_1 = utils.filter_by_asm(final_df, selected_asms)
            if filtered_df_1.empty:
                pass
                
            else:
                st.write(filtered_df_1)
                excel_data, excel_filename = eo.download_excel(filtered_df_1, "Perfomance By ASM")
                st.download_button(label=excel_filename, data=excel_data, file_name=excel_filename, mime="application/vnd.ms-excel")
            st.header(':blue[Download Performance By SR] :arrow_down:', divider='blue')
            excel_data, excel_filename = eo.download_excel(filter_df, "Perfomance By SR")
            st.download_button(label=excel_filename, data=excel_data, file_name=excel_filename, mime="application/vnd.ms-excel")
            
            grouped_df = final_df.groupby(['PAYROLL', 'REGION', 'STATE', 'ASM']).agg({
                          # Count number of employees
                        'ACTUAL MANDAYS TILL DATE': lambda x: int(np.round(x.fillna(0).mean())),  # Calculate the average and round to the nearest integer
                        'VISIT PLANNED': 'sum',  # Sum of VISIT PLANNED
                        'ACTUAL VISITED (TOTAL CALL)': 'sum',  # Sum of ACTUAL VISITED (TOTAL CALL)
                        'PLAN PRODUCTIVITY ON TOTAL CALL':'sum',
                        'Productivity on Total Call': 'sum',
                        'Unique Store Mapped': 'sum',
                        'PLAN UNIQUE STORE VISITED':'sum',
                        'Unique Store VISITED':'sum',
                        'PLAN UNIQUE STORE PRODUCTIVE CALL':'sum',
                        'Unique Store Productive Call':'sum',
                        'HELL ENERGY CLASSIC': 'sum',
                        'HELL ENERGY WATERMELON':'sum',
                        'Count of _Bills Generated':'sum',
                        'Count of Bill`s Supplied':'sum'
                    })
            
                            # Calculate % Coverage On Visit Plan
            grouped_df['% Coverage On Visit Plan'] = (grouped_df['ACTUAL VISITED (TOTAL CALL)'] / grouped_df['VISIT PLANNED']) * 100
            grouped_df['% Coverage On Visit Plan'] = grouped_df['% Coverage On Visit Plan'].map(lambda x: '{:.0f}%'.format(x))

                    # Calculate % Productivity on TOTAL Visited Store
            grouped_df['% Productivity on TOTAL Visited Store'] = (grouped_df['Productivity on Total Call'] / grouped_df['ACTUAL VISITED (TOTAL CALL)']) * 100
            grouped_df['% Productivity on TOTAL Visited Store'] = grouped_df['% Productivity on TOTAL Visited Store'].map(lambda x: '{:.0f}%'.format(x))

                    # Calculate % Coverage (on Unique Store Mapped)
            grouped_df['% Coverage (on Unique Store Mapped)'] = (grouped_df['Unique Store VISITED'] / grouped_df['Unique Store Mapped']) * 100
            grouped_df['% Coverage (on Unique Store Mapped)'] = grouped_df['% Coverage (on Unique Store Mapped)'].map(lambda x: '{:.0f}%'.format(x))
            grouped_df['% Productivity on Unique Store Visit'] = (grouped_df['Unique Store Productive Call'] / grouped_df['Unique Store VISITED']) * 100
            grouped_df['% Productivity on Unique Store Visit'] = grouped_df['% Productivity on Unique Store Visit'].map(lambda x: '{:.0f}%'.format(x))
            grouped_df['Sum of % Order Fullfilment ( Order Vs Invoice)'] = (grouped_df['Count of Bill`s Supplied'] / grouped_df['Count of _Bills Generated']) * 100
            grouped_df['Sum of % Order Fullfilment ( Order Vs Invoice)'] = grouped_df['Sum of % Order Fullfilment ( Order Vs Invoice)'].map(lambda x: '{:.0f}%'.format(x))
            grouped_df['HELL ENERGY CLASSIC'] = grouped_df['HELL ENERGY CLASSIC'].astype(int)
            grouped_df['HELL ENERGY WATERMELON'] = grouped_df['HELL ENERGY WATERMELON'].astype(int)
            # Reset index to make the grouped columns as regular columns
            grouped_df = grouped_df.reset_index()
            st.header(':blue[Download Summary Report Region Wise] :arrow_down:',divider='blue')
            # if st.button("Summary"):
            #     st.write(grouped_df)
            excel_data, excel_filename = eo.download_excel(final_df, "Summary Report")
            st.download_button(label=excel_filename, data=excel_data, file_name=excel_filename, mime="application/vnd.ms-excel")
            # Print or return the grouped DataFrame
            
            st.header(':rainbow[View and Download the SFA Report]', divider='rainbow')
            options = [
                ("Upper Crust", sf.uppercrust, final_df, selected_states_other, "Upper Crust"),
                ("UC Rajasthan", sf.uppercrust, final_df, selected_states_rajasthan, "UC Rajasthan"),
                ("UC UP & Uttarakhand", sf.uppercrust, final_df, selected_states_UP, "UC UP & Uttarakhand"),
                ("Delhi", sf.uppercrust, final_df, selected_states_delhi, "Delhi"),
                ("Karnataka", sf.uppercrust, final_df, selected_states_karnataka, "Karnataka"),
                ("Tamil Nadu", sf.uppercrust, final_df, selected_states_tamil, "Tamil Nadu"),
                ("AP & TEL", sf.uppercrust, final_df, selected_states_ap_tel, "AP & TEL"),
                ("Assam", sf.uppercrust, final_df, selected_states_assam, "Assam"),
                ("Guj & MP", sf.uppercrust, final_df, selected_states_guj, "Guj & MP"),
                ("Mumbai", sf.uppercrust_city, final_df, selected_states_mum, "Mumbai"),
                ("ROM", sf.uppercrust_som, final_df, None, "ROM")
                ]

            # Create a select box for the user to choose an option
            selected_option = st.selectbox("Select an option:", [option[0] for option in options])

            # Execute code based on the user's selection
            for option in options:
                name, function, df, params, filename = option
                if selected_option == name:
                    # Execute the function with the provided parameters
                    if params is not None:
                        result_df = function(df, params)
                    else:
                        result_df = function(df)
                    
                    # Display the resulting DataFrame
                    st.write(result_df)
                    
                    # Create download link for the resulting DataFrame
                    excel_data, excel_filename = eo.download_excel(result_df, filename)
                    st.download_button(
                        label=excel_filename,
                        data=excel_data,
                        file_name=excel_filename,
                        mime="application/vnd.ms-excel"
                    )

            def extract_numeric_mean(column):
                # Remove unwanted characters and convert to numeric
                numeric_values = pd.to_numeric(column.str.replace(r'[^0-9.]+', '', regex=True), errors='coerce')
                # Calculate the mean, ignoring NaN values
                mean_value = np.nanmean(numeric_values)
                # Round the mean value and format it as a percentage
                rounded_mean_percentage = round(mean_value)  # Round to 2 decimal places
                return f"{rounded_mean_percentage}%"
                                
            
            

        elif choice == "Visualisation":
            st.title("Visualisation Chart")
        
            df_graph = st.session_state.df
            st.write(df_graph)
            sales_sum = df_graph['Sales (Qtyin Case)'].sum()
            order_supplied = df_graph['Order Supplied in_ CASE'].sum()

            sales_by_ASM = df_graph.groupby('ASM')['Sales (Qtyin Case)'].sum().map(lambda x: round(x, 2)).reset_index()
            sales_by_state = df_graph.groupby('STATE')['Sales (Qtyin Case)'].sum().map(lambda x: round(x, 2)).reset_index()
            col1, col2 = st.columns((2))
            with col1:
                st.subheader("Category wise Sales")
                
                fig = px.bar(sales_by_ASM, x='ASM', y='Sales (Qtyin Case)', title='Sales by ASM')
                fig.update_xaxes(tickangle=-75)
                st.plotly_chart(fig, use_container_width=True,height=200)
            
            with col2:
                
                fig = px.pie(sales_by_state, values='Sales (Qtyin Case)', names='STATE', title='State-wise Sales Quantity',labels=None)
                fig.update_traces(textposition='inside')
                fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
                
                # Display Plotly chart
                st.plotly_chart(fig, use_container_width=True, height=200)

            cl1, cl2 = st.columns((2))
            with cl1:
                st.write(sales_by_ASM.style.background_gradient(cmap="Blues"),height=200)
                csv = sales_by_ASM.to_csv(index = False).encode('utf-8')
                st.download_button("Download Data", data = csv, file_name = "ASM_Sales.csv", mime = "text/csv",
                                help = 'Click here to download the data as a CSV file')

            with cl2: 
                st.write(sales_by_state.style.background_gradient(cmap="Oranges"),height=200)
                csv = sales_by_state.to_csv(index = False).encode('utf-8')
                st.download_button("Download Data", data = csv, file_name = "State_Sales.csv", mime = "text/csv",
                                help = 'Click here to download the data as a CSV file')

            cl3, cl4, cl5 = st.columns(3)
            with cl3:
                cl3.metric(label="Total Sales 📊",
            value=sales_sum)
                
            with cl4:
                cl4.metric(label="Total Order Supplied in CASE 📊",
            value=order_supplied)
                
            with cl5:
                cl5.metric(label="Total Order Supplied in CASE 📊",
            value=order_supplied)
            

if __name__ == "__main__":
    main()
