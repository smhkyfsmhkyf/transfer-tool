import pandas as pd

#Get connection label from component.
#If we use a one-step process:
def find_cnxlabel(df, component, cnx_no):
    #Filter the DataFrame using the composite keys (Component and cnx_key)
    filtered_df2 = df[(df['Component'] == component) & (df['CnxNo'] == cnx_no)]
    cnxlabel = filtered_df2['Cnx Label'].tolist()
    return cnxlabel



# Example usage
# connect_components(components, dfNewTRC1)

##~~~~~Same goal different way. But the one step process seems simpler. Not sure yet.~~~~~
##If we use a two-step process this is Step 1:
# def find_cnxindex(df, component, cnx_no):
#     #Filter the DataFrame using the composite keys (Component and cnx_key)
#     filtered_df = df[(df['Component'] == component) & (df['CnxNo'] == cnx_no)]
#     cnx_index = filtered_df.index.tolist()
#     #label = filtered_df['Cnx Label'].tolist()
#     return cnx_index
# #And Step 2:
# def find_cnxlabelfromindex(df, cnx_index):
#     #Filter the DataFrame using the composite keys (Component and cnx_key)
#     filtered_df1 = df[(df['cnx_index'] == cnx_index)]
#     label = filtered_df1['Cnx Label'].tolist()
#     return label


###notes to self 8/25:
#components are not distinguished from the connections throughout the program. 

#Can't use index in existing neighbors loop because interestingly, order is not exactly the same. For example in pandas  AY02A-WT-WTL-SN-633/635 is before AZ01, but not the same in the existing neighbors loop. 
#So try to use dataframe for components and pits instead of dictionaries. Can we do this? I don't know yet. So I'm leaving the existing components and pits dictionaries in tact until I know it works. 
#If it doesn't work I can probably convert the dataframe to a dictionary and it should work the same.  





