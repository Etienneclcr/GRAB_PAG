# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 11:55:24 2021

@author: Angel.BAUDON
"""
import numpy as np, glob
import os, pandas as pd, matplotlib.pyplot as plt
from scipy.optimize import curve_fit


class FileManager():
    def __init__(self):
        self = self
        
    def FileMaker(self, folder_exp, condition):
        
        folder_cond = f'{folder_exp}\{condition}'
        file_glob = glob.glob(rf'{folder_cond}\*.xlsx')
        
        #Folder to stock the final analysis
        Analysis = f'{folder_cond}\Analysis'
        if not os.path.exists(Analysis): os.makedirs(Analysis)
        
        #Create the Output data frame
        Parameters = ('ID n°', 'Data', 'AUC', 'Max df', 'Data raw')
        Plot_param = ('Means AUC', 'SEM AUC', 'Means dF/F', 'SEM dF/F')

        
        print('='*30, '\n'*2, condition, '\n'*2, '='*30)
        
        return file_glob, Analysis, Parameters, Plot_param
         
    def DataExtractor(self, file):
        
        #Extract file name and data from excel sheet
        file_name = file.split('\\')[-1]   
        data_raw = (pd.read_excel(file, sheet_name=0, header=None, 
                              usecols = 'B')).to_numpy()
        
        print('='*30, '\n'*2, file_name, '\n'*2, '='*30)
        return file_name, data_raw
    

class DataManager():
    def __init__(self, stim_time, Analysis, file_name, data):
        self.stim_time = stim_time
        self.Analysis, self.file_name = Analysis, file_name
        self.data = data
        
    def FitFinder(self, data_raw):
        
        # Make the data have the same format
        data_raw = data_raw.ravel()
        self.data = data_raw[120:1737]
        self.data = self.data - min(self.data)
        self.xdata = np.arange(len(self.data))
        def exp_func(x, a, b, c):
            return a * np.exp(-b * x) + c*x

        
        popt, pcov = curve_fit(exp_func, self.xdata[np.r_[0:self.stim_time, 
                                                          1100:len(self.data)]], 
                                self.data[np.r_[0:self.stim_time, 1100:len(self.data)]], 
                                p0=[1,0.00001,1], maxfev = 1000000)


        exp_inv = exp_func(self.xdata, *popt)
        plt.figure()
        plt.plot(self.data)
        plt.plot(exp_inv)
        plt.savefig(rf'{self.Analysis}\{self.file_name}_+fit.pdf')
        plt.close()
        
        self.data = self.data-exp_inv 
        index = [x for x in range(475,790)]
        self.data = np.delete(self.data, index)
        self.xdata = np.arange(len(self.data))

        return self.data, self.xdata
    
    def TheMeasurer(self, data):
        
        #Find the AUC in baseline and after light-stimulation
        auc_cell = data.clip(0)
        auc = (np.trapz(auc_cell[:self.stim_time]),
                    np.trapz(auc_cell[self.stim_time:self.stim_time+600]))

        #Find the maximum value of df/F0 during baseline and after light-stim
        max_df = (max(data[:self.stim_time-10]), max(data[self.stim_time+50:self.stim_time+self.stim_time]))

        return auc, max_df, data
        
