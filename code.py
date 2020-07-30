# -*- coding: utf-8 -*-
"""code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1A5MU41hO_qu4Y0PO9jBLl1FtraSZtFWH

# Code File
"""
"""
Dependencies: openpyxl xlsxwriter xlrd, pandas, pickle
Installing can be done by writing following commands in command prompt/terminal
        
        pip install openpyxl xlsxwriter xlrd
        pip install pandas
        pip install pickle

"""
import pandas as pd
import pickle

# Load from file
with open("pickle_event_domain_model.pkl", 'rb') as file:
    pickle_event_domain_model = pickle.load(file)

# Load from file
with open("pickle_event_type_model.pkl", 'rb') as file:
    pickle_event_type_model = pickle.load(file)

employee_df = pd.read_csv('CCMLEmployeeData.csv')   
event_df = pd.read_csv('Input.csv', names=['Event Title'], encoding= 'unicode_escape')  ##Ensure you have uploaded Input.csv in same folder; else result will be of default Input.csv provided
employee_df['Domain'] = employee_df['Domain'].apply(lambda x:x.replace(' ',''))

#Output DataFrame which will later be converted to XLS format
Output_df=pd.DataFrame(
    {
        'Event Title': [],
        'Recommended Employees': []
    }
)
Output_Intermediate_df=pd.DataFrame(
    {
        'Event Title': [],
        'Domain': [],
        'Event Type': []
    }
)

for index, row in event_df.iterrows():
    Event_Title = row['Event Title']
    predicted_domain = list(pickle_event_domain_model.predict([Event_Title])) #could be multiple too eg: MachineLearning Python
    domain_list = predicted_domain[0].split(' ') #thus splitting multi-domains & obtaining iterable list form of domains Eg:[MachineLearning,Python]
    ## Handling the case of No Domain Predicted
    if domain_list == list():
      domain_list = ['Other']
    predicted_event = list(pickle_event_type_model.predict([Event_Title]))
    event_list = predicted_event[0].split(' ')
    ## Handling the case of No Event Type Predicted
    if event_list == list():
      event_list = ['Webinars']
    Output_Intermediate_df = Output_Intermediate_df.append({'Event Title': Event_Title,'Domain': predicted_domain,'Event Type':predicted_event}, ignore_index=True)
    
    ## String Matching Algorithm to check which Employees have interests as predicted Domain & Event type
    for domain in domain_list:
      for event in event_list:
        relevant_employees = list(employee_df.loc[(employee_df['Domain'] == domain) & ( (employee_df['Event1'] == event) |(employee_df['Event2'] == event))]['Name'])
        single_event_result = ','.join(relevant_employees)
        Output_df = Output_df.append({'Event Title': Event_Title,'Recommended Employees': single_event_result}, ignore_index=True)

# Generating Output Excel file
Output_df.to_excel('./Output.xlsx', sheet_name='Output', index=False)
Output_Intermediate_df.to_excel('./OutputIntermediate.xlsx', sheet_name='OutputIntermediate', index=False)


"""
I/P: Input.csv (This is a CSV file of event titles with no header)
O/P: Auto-generated "Output.xlsx" (This is a Excel file of event titles with matched recommended employees)
Auxiliary Files Generated: Auto-generated "Output_Intermediate.xlsx"  (This is a Excel file of event titles with prdicted domains an event types)

Other files Used: 
    Trained Models in the form of Pickle i.e. ".pkl" files
    --> pickle_event_domain_model.pkl
    --> pickle_event_type_model.pkl
    Located in root folder itself

    Can be modified by feeding more data to 
    --> Event_Domain_Prediction.py
    --> Event_Type_Prediction.py
    Located in training_data folder of root folder

"""