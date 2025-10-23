from ast import If
from logging import _srcfile
from math import nan
from multiprocessing import Value
from operator import index
import string
from openpyxl import load_workbook
from utils.valve import Valve
from utils.valve2 import Valve2
from utils.nozzle import Nozzle
from utils.line import Line
from utils.valve3 import Valve3
from utils.split import Split
from utils.pump import Pump
from utils.tankreturn import TankReturn
from utils.pit import Pit
from utils.dataManipulate import find_cnxlabel
from tkinter import messagebox
import pandas as pd


###
###file for regular use: '//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/1 Transfers/1C - Procedure Review Tools/MasterProcedureData.xlsx'
### TEST FILE !!!change back file to regular use file when complete !!!

def importComponents(filepath='//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/2 Team Members/Sarah Hunter/transfer-pro - related files/DONT USE MasterProcedureData 2025-03-19.xlsx'):
    try:
        wb = load_workbook(filename=filepath, data_only=True)
    except FileNotFoundError as e:
        raise e

    pits_sheet = wb["Pit Components"]
    #dataframe of spreadsheet
    dfOriginalPits = pd.read_excel(filepath, "Pit Components",  index_col=None, na_values='')
    pits = {}
    
    
    #with dataframe might not need this. 
    for row in pits_sheet.iter_rows(min_row=3, values_only=True, max_row=150, max_col=26):
        pit_name = row[1]
        # if a pit hasn't been initialized as an object, create it
        if pit_name not in pits:
            pits[pit_name] = Pit(
                name=pit_name, leak_detector_id=row[2], leak_detector_pmid=row[3],
                leak_detector_tfsps=row[4], tfsps_transmitter=row[5],
                tfsps_pmid=row[6], drain_seal_location=row[7], drain_seal_name=[8],
                drain_seal_position=row[9], annulus_leak_detector=row[12],
                annulus_leak_detector_pmid=row[13], pit_nace=row[14],
                pit_nace_pmid=row[15], in_pit_heater=row[16],
                tfmcs=row[17], tsr_structure=row[18]
            )
        # if a pit has been initialized, add the other fields in the excel row
        else:
            pits[pit_name].add_missing_fields(
                tfsps_transmitter=row[5], tfsps_pmid=row[6], 
                annulus_leak_detector=row[12], annulus_leak_detector_pmid=row[13],
                in_pit_heater=row[16],
            )

    # "Components" dictionary to store and retrieve all objects representing waste transffer valves, pumps, lines, etc.
    components = { }
    
    # Types dictionary to initialize objects of the Class specified in the Excel sheet for each component 
    types = {
        "2-Way-Valve": Valve2,
        "3-Way-Valve": Valve3,
        "Tee Fitting": Split,
        "Split Point": Split,
        "Pump": Pump,
        "Transfer Line": Line,
        "Nozzle": Nozzle,
        "": Valve,
        "Tank Return": TankReturn,
        None: Valve
    }
    #Excel sheet
    connections_sheet = wb['Transfer Route Components']
    connections_matrix = connections_sheet["F2:H400"]
    
    #Create existing data structure and new data stucture dataframes so data manipulation is easier. 
    #Cnx is an abbreviation for connections.
    #Create existing data structure and new data stucture dataframes so data manipulation is easier. 
    #Acronyms and abbreviations: Cnx = connections; TRC = Transfer route components.

    oldfilepath = '//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/2 Team Members/Sarah Hunter/transfer-pro - related files/Copy of MasterProcedureData for testing, with column name changes'
    dfOldSheet = pd.read_excel(oldfilepath, "Transfer Route Components",  index_col=None)

    #Original spreadsheet modified to sort by component name and then ID column added. (so that consistent order without disagreement b/t excel and python.)
    dfRev0TRC = pd.read_excel(filepath, "Transfer Route Components",  index_col=None)
    dfRev1TRC = dfRev0TRC.copy()
    # dfRev1TRC = dfRev1TRC.sort_values(by = 'Component')
    dfRev1TRC['ID'] = range(1, len(dfRev1TRC) +1)
    

    #Transform the wide multi-column format into a long multi-row format. First we melt the connections then the connections labels.
    dfCnx1 = pd.melt(dfRev1TRC, id_vars = ['Component'], 
                         value_vars = ['Connection 1', 'Connection 2', 'Connection 3'], 
                         var_name = 'CnxNo', 
                         value_name = 'Cnx')
    dfCnxLabels = pd.melt(dfRev1TRC, id_vars = ['Component'], 
                         value_vars = ['Connection Label 1', 'Connection Label 2', 'Connection Label 3'], 
                         var_name = 'Label No', 
                         value_name = 'Cnx Label')
    #Get the connection number from the variable names
    dfCnx1['CnxNo'] = dfCnx1['CnxNo'].str[-1].astype(int) 
    dfCnxLabels['Label No'] = dfCnxLabels['Label No'].str[-1].astype(int)

    #Join the connections and label tables and put them in order
    dfCnx_result1 = pd.merge(dfCnx1, dfCnxLabels, left_on=['Component', 'CnxNo'], right_on=['Component', 'Label No'])
    dfCnx_result1 = dfCnx_result1.drop(columns=['Label No'])
    dfCnx_result1 = dfCnx_result1.sort_values(by=['Component', 'CnxNo']).reset_index(drop=True)
    #create numerical ID to match the Component to Connection (just in case we need it.)
    dfCnx_result1['PairID'] = range(1, len(dfCnx_result1) + 1)
    #Make one key for each connection pair so that we don't need composite keys. This is so that we can make a join with the neighbors output.
    dfCnx_result1['CompCnxID'] = dfCnx_result1['Component'] + dfCnx_result1['CnxNo'].astype(str)

    dfNewRoutComp = pd.merge(dfCnx_result1, dfRev1TRC, on='Component')
    dfNewRoutComp = dfNewRoutComp.drop(columns=['Connection 1', 'Connection 2', 'Connection 3', 'Connection Label 1', 'Connection Label 2', 'Connection Label 3'])
    #drop rows where Cnx is blank (so that we can merge with the neighbors output)
    dfNewRoutCompCnxFilter = dfNewRoutComp[dfNewRoutComp['Cnx'].notna()]
    dfNewRoutCompCnxFilter = dfNewRoutCompCnxFilter.sort_values(by=['Type', 'Component', 'CompCnxID']).reset_index(drop=True)

    ###~~~~~Can look at the dataframe in excel for reference if desired. Please keep this code.~~~~~~~~
    dfNewRoutCompCnxFilter.to_excel('dfNewRoutCompCnxFilter251015-4.xlsx', index=False)

    ###~~~~~Can look at the dataframe in excel for reference if desired. Please keep this code.~~~~~~~~
    #dfTypes.to_excel('dfTypes.xlsx', index=False)

    #Initialize component objects into "components" dictionary. Key = Name, value = Component object
    for row in connections_sheet.iter_rows(min_row=2, values_only= True, max_row=350, max_col=15):
        component_name = row[0]
        component_type = row[1]
        components[component_name] = types[component_type](component_name, pit = row[2], jumper = row[3], dvi = row[4], field_label = row[12])
 
    neighbors_data = []
    #For all component object in "components". Call their .conect() method to its neighbors
    for row_index1, (component, neighbors) in enumerate(zip(components.values(), connections_matrix)):
        for col_index1, neighbor in enumerate(neighbors):
            #if the neighbor listed in excel exists as an initialized object in the "components" dictionary
            if neighbor.value in components:
                #if neighbor object != None (might be a reduntant check)
                if neighbor.value:
                    component.connect(components[neighbor.value])
                    
                    #create unique ID for each row
                    neighbor_lp_id = f"{row_index1 + 1}{col_index1 + 1}"
                    #key to merge with other dataframes
                    comp_cnx_id = f"{component}{str(col_index1 + 1)}"
                    #Put into dictionary
                    neighbors_data.append({
                    'Component': component,
                    'Neighbor': neighbor.value,
                    #'CnxNo': col_index1+1,
                    'NeighborLpID': neighbor_lp_id,
                    'CompCnxID': comp_cnx_id
                })


    dfneighbors_data = pd.DataFrame(neighbors_data)
    #do a join with another data table to get rest of the data?
    dfConnectionsTable = pd.merge(dfNewRoutCompCnxFilter, dfneighbors_data, on=['CompCnxID'], how='outer')
    dfneighbors_data.to_excel('neighborsLoop251021-2.xlsx', index = True)
    dfConnectionsTable.to_excel('dfConnectionsTable.xlsx', index=True)
    


    return components, pits
importComponents()
