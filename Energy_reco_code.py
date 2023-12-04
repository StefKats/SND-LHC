import ROOT as r
import numpy as np
import pandas as pd
# import pickle
# import sys
# from ShipGeoConfig import ConfigRegistry
from rootpyPickler import Unpickler
import shipLHC_conf as sndDet_conf
import SndlhcGeo
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, Normalize
from argparse import ArgumentParser
import time


parser = ArgumentParser()

parser.add_argument("--Z",   dest="z", required=False, default = 0, type = int)
# parser.add_argument("--E",   dest="e", required=False, default = 0, type = int)
parser.add_argument("--N",   dest="n", required=False, default = 0, type = int)
parser.add_argument("-o", "--output",dest="outputDir",  help="Output directory", required=False,  default=".")


options = parser.parse_args()

n_events = options.n

depth = options.z

print(options.z)


simps_x = []
for station in range(1,6):
    data = np.loadtxt("/eos/user/s/skatsaro/PGsim/SiPMs/SiPM_x_{}.txt".format(station))
    simps_x.append(data)

simps_y = []
for station in range(1,6):
    data = np.loadtxt("/eos/user/s/skatsaro/PGsim/SiPMs/SiPM_y_{}.txt".format(station))
    simps_y.append(data)

energies = [50,100,200,300,400,500,750,1000,1250,1500,2000]
PDFs_x = []
for station in range(1,6):
    for energy in energies:
        path = "/eos/user/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/PDF_x_{}.txt".format(depth,energy,station)
        data = np.loadtxt(path)
        PDFs_x.append(data)

energies = [50,100,200,300,400,500,750,1000,1250,1500,2000]
PDFs_y = []
for station in range(1,6):
    for energy in energies:
        path = "/eos/user/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/PDF_y_{}.txt".format(depth,energy,station)
        data = np.loadtxt(path)
        PDFs_y.append(data)
        
PDFs_x = np.array(PDFs_x)

PDFs_x[PDFs_x==0] = 0.00005

PDFs_y = np.array(PDFs_y)

PDFs_y[PDFs_y==0] = 0.00005


t1 = time.perf_counter()
reco_e_x = np.array([])
reco_e_y = np.array([])
reco_e_comb = np.array([])
energies = [50,100,200,300,400,500,750,1000,1250,1500,2000]

for true_e in energies:
    hit_counts_x_list = pd.read_csv("/eos/user/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/events/hits_x.txt".format(depth,true_e))
    hit_counts_x_list = hit_counts_x_list.values.tolist()
    
    hit_counts_y_list = pd.read_csv("/eos/user/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/events/hits_y.txt".format(depth,true_e))
    hit_counts_y_list = hit_counts_y_list.values.tolist()
    for event in range(1,n_events+1):
        
        sum_log_x = np.zeros(11)
        sum_log_y = np.zeros(11)
        sum_log_comb = np.zeros(11)


        for station in range(1,6):
            logL_x = []
            logL_y = []

            SiPM_counts_x = simps_x[station-1]

            hit_counts_x = hit_counts_x_list[(5*(event-1))+(station-1)]
    
            SiPM_counts_y = simps_y[station-1]
        
            hit_counts_y = hit_counts_y_list[(5*(event-1))+(station-1)]

            
            for num_e, energy in enumerate(energies,start=0):
                
                PDF_x = PDFs_x[((station-1)*11)+num_e]
                

                logL_x.append(np.sum(((SiPM_counts_x-hit_counts_x)*np.log(1-PDF_x))+\
                                                       ((hit_counts_x)*np.log(PDF_x))))
    
                PDF_y = PDFs_y[((station-1)*11)+num_e]

                logL_y.append(np.sum(((SiPM_counts_y-hit_counts_y)*np.log(1-PDF_y))+\
                                                       ((hit_counts_y)*np.log(PDF_y))))
                
            sum_log_x += logL_x
            sum_log_y += logL_y

        reco_e_x = np.append(reco_e_x,energies[np.argmax(sum_log_x)])
        reco_e_y = np.append(reco_e_y,energies[np.argmax(sum_log_y)])
        reco_e_comb = np.append(reco_e_comb,energies[np.argmax(sum_log_y+sum_log_x)])


reco_e_x_df = pd.DataFrame(reco_e_x)
reco_e_y_df = pd.DataFrame(reco_e_y)
reco_e_comb_df = pd.DataFrame(reco_e_comb)



reco_e_x_df.to_csv("{}energy_reco/reco_e_x.txt".format(options.outputDir), encoding="utf-8", index=False)
reco_e_y_df.to_csv("{}energy_reco/reco_e_y.txt".format(options.outputDir), encoding="utf-8", index=False)
reco_e_comb_df.to_csv("{}energy_reco/reco_e_comb.txt".format(options.outputDir), encoding="utf-8", index=False)

t2 = time.perf_counter()
print(t2-t1)                                                                                                                         75,4           2%
