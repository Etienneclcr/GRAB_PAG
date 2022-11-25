# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 15:22:26 2022

@author: Etienne.CLAUSS
"""

import numpy as np, matplotlib.pyplot as plt
import scipy.stats as Stat, seaborn as sns


class PlotFactory():
    def __init__(self, data, xdata, stim_time, Analysis, file_name, Paired):
      self.data, self.xdata, self.stim_time = data, xdata, stim_time
      self.Analysis, self.file_name = Analysis, file_name
      self.Paired = Paired
        
    def TracePloter(self, show_fig = False):
        plt.figure()
        plt.plot(self.data)
        plt.savefig(rf'{self.Analysis}\{self.file_name}_df.pdf')
        if not show_fig: plt.close()
        
        
    def Histo(self, Output, param_name, show_fig = False):
        
        Parameter = Output[f'{param_name}']
        plt.figure()
        bl, dr = [],[]
        for param in Parameter:
            bl.append(param[0])
            dr.append(param[1])
        meanz = np.asarray((np.mean(bl), np.mean(dr)))
        val_stat = np.asarray((bl, dr))
        indiv_val_hz = val_stat.transpose()            
        bl_sem, dr_sem = (Stat.sem(bl), Stat.sem(dr))  
        semz = np.asarray((np.mean(bl_sem), np.mean(dr_sem)))
        x_ax = (0,0.2)
        plt.bar(x_ax, meanz, width = 0.1,
                yerr=semz, capsize=10, zorder=0)
        for x in indiv_val_hz:
            [plt.scatter(x_ax[i], x, s=20, c='w', marker='o',
                            edgecolor='k', zorder=2) for i,x in enumerate(x)]  
            plt.plot(x_ax, x, c='k', lw=0.5, zorder=1) 
            
        plt.plot(1,0)
        
        plt.savefig(rf'{self.Analysis}\{param_name}.pdf')
        if not show_fig: plt.close()        
        
        
    def HeatMap(self, data_tot, show_fig = False):
        
        def Sorter(data_tot):
            stim = sum(data_tot[self.stim_time:])
            return stim 
        data_tot = sorted(data_tot, key=Sorter)
        
        maxi, mini = [], []
        maxi.append([max(x) for x in data_tot])
        mini.append([min(x) for x in data_tot])
        
        plt.figure()
        fig = sns.heatmap(data_tot, vmin = -30, vmax = 30, cmap = 'seismic')
        fig.axvline(self.stim_time, c='Black', lw = 2)
        
        plt.savefig(rf'{self.Analysis}\HeatMap.pdf')
        if not show_fig: plt.close()
        
    def TimeCourse(self, data_tot, show_fig = False):
    
        mean_bin = np.nanmean(data_tot, axis = 0)
        sem_bin = Stat.sem(data_tot)
        
        plt.figure()
        plt.fill_between(self.xdata, mean_bin-sem_bin, mean_bin+sem_bin)

        plt.axvline(self.stim_time, c='Black', lw = 2)
        
        plt.plot(self.xdata, mean_bin, c='r', zorder=2)    
    
        plt.savefig(rf'{self.Analysis}\TC.pdf')
        if not show_fig: plt.close()
    
    def TimeCourseCombined(self, TC_comb, folder_exp, show_fig = False):
        
        plt.figure()
        for data_total in TC_comb:
            data_tot = []
            data_tot.append([[np.nanmean(data_total[i][j:j+20]) 
                              for j,_ in enumerate(data_total[i])] 
                              for i,_ in enumerate(data_total)])
            mean_bin = np.nanmean(data_tot[0], axis = 0)
            sem_bin = Stat.sem(data_tot[0])
            
            
            plt.fill_between(self.xdata, mean_bin-sem_bin, mean_bin+sem_bin)
            plt.axvline(self.stim_time, c='Black', lw = 2)
            
            plt.plot(self.xdata, mean_bin, c='r', zorder=2)    
        
        plt.savefig(rf'{folder_exp}\TC_comb.pdf')
        if not show_fig: plt.close()
            
        
    
    def HistoDelta(self, delta, folder_exp, param_name, show_fig = False):
        
        x_ax = (0, 0.2, 0.4)
        val_stat = []
        plt.figure()
        for i, condition in enumerate(delta):
            delta_list = [] 
            for data in condition:
                delta_list.append(data[1]-data[0])
                
            val_stat.append(delta_list)
            indiv_val_hz = np.asarray(delta_list)  
            meanz = np.asarray(np.nanmean(delta_list))          
            sem = (Stat.sem(delta_list))  
            semz = np.asarray(np.mean(sem))
            
            plt.bar(x_ax[i], meanz, width = 0.1,
                    yerr=semz, capsize=10, zorder=0)
            for x in indiv_val_hz:
                plt.scatter(x_ax[i], x, s=20, c='w', marker='o',
                                edgecolor='k', zorder=2)   
                
            plt.plot(1,0)

        plt.savefig(rf'{folder_exp}\{param_name}.pdf')
        if not show_fig: plt.close()                