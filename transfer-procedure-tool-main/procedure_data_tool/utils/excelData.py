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

###

###file for regular use: '//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/1 Transfers/1C - Procedure Review Tools/MasterProcedureData.xlsx'
### TEST FILE !!!change back file to regular use file when complete !!!
def importComponents(filepath='//hanford/data/sitedata/WasteTransferEng/Waste Transfer Engineering/1 Transfers/1C - Procedure Review Tools/MasterProcedureData.xlsx'):
    try:
        wb = load_workbook(filename=filepath, data_only=True)
    except FileNotFoundError as e:
        raise e

    pits_sheet = wb["Pit Components"]
    pits = {}

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

    connections_sheet = wb['Transfer Route Components']
    conections_matrix = connections_sheet["F2:H400"]

    #Initialize component objects into "components" dictionary. Key = Name, value = Component object
    for row in connections_sheet.iter_rows(min_row=2, values_only= True, max_row=350, max_col=15):
        component_name = row[0]
        component_type = row[1]
        components[component_name] = types[component_type](component_name, pit = row[2], jumper = row[3], dvi = row[4], field_label = row[12])

    #For all component object in "components". Call their .conect() method to its neighbors
    for component, neighbors in zip(components.values(), conections_matrix):
        for neighbor in neighbors:
            #if the neighbor listed in excel exists as an initialized object in the "components" dictionary
            if neighbor.value in components:
                #if neighbor object != None (might be a reduntant check)
                if neighbor.value:
                    component.connect(components[neighbor.value])

    return components, pits

importComponents()
