# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 17:33:42 2022

@author: Etienne.CLAUSS
"""
import numpy as np, pandas as pd, os
from ToolKit import TraceManager, PlotFactory


folder_exp = r"C:\Etienne.CLAUSS\Lab\Exp\Imagerie\GrabOTR\Stim\ILC"
 
#Define parameters of the analysis
cut_time, Paired = 60, False
stim_time = 480

#Combine the root and the file to obtain the file location
folder_exp_list = [x for x in os.listdir(folder_exp)]

conditions = (folder_exp_list[i] for i,_ in enumerate(folder_exp_list))

TC_comb = []
delta_AUC = []
delta_max_df = []


for condition in folder_exp_list:  
    if '.' in condition: continue
    TMF = TraceManager.FileManager()
    #Create folder to stock analysis and create Output data frame
    file_glob, Analysis, Parameters, Plot_param = TMF.FileMaker(folder_exp, condition)    
    Output = pd.DataFrame(columns = Parameters)    
          
    for file in file_glob:
        #Extract file name and data from excel sheet
        file_name, data_raw = TMF.DataExtractor(file)
        
        TMD = TraceManager.DataManager(stim_time, Analysis, file_name, data_raw) 

        #Find the parameter to fit an inverse exponential and plot the raw data + fit
        data, xdata = TMD.FitFinder(data_raw)

        import copy
        data_cop = copy.copy(data)

        #Quantify the AUC and max df/F0 in baseline and after light-stimulation
        auc, max_df, data = TMD.TheMeasurer(data_cop)

        #General Stock
        Out = (file_name, data, auc, max_df, data_raw)  
        Output = Output.append({x:y for x, y in zip(Parameters, Out)}, 
                            ignore_index = True)
            
        #Plot Section

        PF = PlotFactory.PlotFactory(data, xdata, stim_time, Analysis, 
                                     file_name, Paired)
        
        #Plot individual traces after substracting the fit     
        PF.TracePloter()
    
    #Create an array with all the data for the HeatMap and TimeCourse
    data_tot = np.zeros((len(Output['Data']), 1302))
    for i,x in enumerate(Output['Data']):
        data_tot[i] = x

    #Plot histo for AUC   
    PF.Histo(Output, 'AUC')
    
    # Plot max df/F0  
    PF.Histo(Output, 'Max df')
    
    #Plot Heat Map
    PF.HeatMap(data_tot)
    
    #Plot Time course
    PF.TimeCourse(data_tot)
    
    TC_comb.append(Output['Data'])
    delta_AUC.append(Output['AUC'])
    delta_max_df.append(Output['Max df'])
    
    #Detailled Output to excel
    writer_exp = pd.ExcelWriter(f'{Analysis}/{condition}.xlsx')
    Output.to_excel(writer_exp, sheet_name = 'All data')
    writer_exp.save()

#Plot Time Course with the 3 conditions
PF.TimeCourseCombined(TC_comb, folder_exp)

#Plot histo of the delta AUC in the 3 conditions
val_stat_AUC = PF.HistoDelta(delta_AUC, folder_exp, 'AUC')

#Plot histo of the delta max fluo in the 3 conditions
val_stat_df = PF.HistoDelta(delta_max_df, folder_exp, 'Max df')



# Output for stat to excel

df_AUC = pd.DataFrame(val_stat_AUC)
writer_exp = pd.ExcelWriter(f'{folder_exp}/AUC.xlsx')
df_AUC.to_excel(writer_exp)
writer_exp.save()

df_max_df = pd.DataFrame(val_stat_df)
writer_exp = pd.ExcelWriter(f'{folder_exp}/Max df.xlsx')
df_max_df.to_excel(writer_exp)
writer_exp.save()