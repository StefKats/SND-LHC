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
from scipy import stats


parser = ArgumentParser()

# parser.add_argument("--Z",   dest="z", required=False, default = 0, type = int)
parser.add_argument("--E",   dest="e", required=False, default = 0, type = int)
parser.add_argument("--N",   dest="n", required=False, default = 0, type = int)
parser.add_argument("-o", "--output",dest="outputDir",  help="Output directory", required=False,  default=".")


options = parser.parse_args()

n_events = options.n

energy = options.e

print(options.e)


simps_x = []
for station in range(1,6):
    data = np.loadtxt("/eos/user/s/skatsaro/PGsim/SiPMs/SiPM_x_{}.txt".format(station))
    simps_x.append(data)

simps_y = []
for station in range(1,6):
    data = np.loadtxt("/eos/user/s/skatsaro/PGsim/SiPMs/SiPM_y_{}.txt".format(station))
    simps_y.append(data)

depths = [291,295,304,308,317,321,330,334,343,347]
PDFs_x = []

for depth in depths:
    for station in range(1,6):
        path = "/eos/home-i02/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/PDF_x_{}.txt".format(depth,energy,station)
        data = np.loadtxt(path)
        PDFs_x.append(data)

depths = [291,295,304,308,317,321,330,334,343,347]

PDFs_y = []
for depth in depths:
    for station in range(1,6):
        path = "/eos/home-i02/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/PDF_y_{}.txt".format(depth,energy,station)
        data = np.loadtxt(path)
        PDFs_y.append(data)

t1 = time.perf_counter()
r2_vals = []
reco_z_x_corrs = []
reco_z_y_corrs = []
reco_z_comb_corrs = []

# [0,-25,-50,-100,-400,-1600,-5000]

for correction in [0]:
    reco_z_x = np.array([])
    reco_z_y = np.array([])
    reco_z_comb = np.array([])
    # energies = [50,100,200,300,400,500,750,1000,1250,1500,2000]
    depths = [291,295,304,308,317,321,330,334,343,347]


    for true_z_num, true_z in enumerate(depths):
        hit_counts_x_list = pd.read_csv("/eos/home-i02/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/events/hits_x.txt".format(true_z,energy))
        hit_counts_x_list = hit_counts_x_list.values.tolist()

        hit_counts_y_list = pd.read_csv("/eos/home-i02/s/skatsaro/PGsim/depth_{}/pions_{}/PDF/events/hits_y.txt".format(true_z,energy))
        hit_counts_y_list = hit_counts_y_list.values.tolist()
        for event in range(1,101):

            sum_log_x = np.zeros(10)
            sum_log_y = np.zeros(10)

            for depth_num, starting_depth in enumerate(depths):

                logL_x = 0
                logL_y = 0
                for station in range(1,6):
    #                 logL_x = []
    #                 logL_y = []

                    SiPM_counts_x = simps_x[station-1]

                    hit_counts_x = hit_counts_x_list[(5*(event-1))+(station-1)]

                    SiPM_counts_y = simps_y[station-1]

                    hit_counts_y = hit_counts_y_list[(5*(event-1))+(station-1)]

   

                    PDF_x = PDFs_x[(depth_num*5)+(station-1)]

    
                    logL_x += np.sum(np.nan_to_num(((SiPM_counts_x-hit_counts_x)*np.log(1-PDF_x))+\
                                                           ((hit_counts_x)*np.nan_to_num(np.log(PDF_x),neginf=correction)),nan=0.0))

                    PDF_y = PDFs_y[(depth_num*5)+(station-1)]
                

                    logL_y += np.sum(np.nan_to_num(((SiPM_counts_y-hit_counts_y)*np.log(1-PDF_y))+\
                                                           ((hit_counts_y)*np.nan_to_num(np.log(PDF_y),neginf=correction)),nan=0.0))

                sum_log_x[depth_num] = logL_x


                sum_log_y[depth_num] = logL_y

            reco_z_x = np.append(reco_z_x,depths[np.argmax(sum_log_x)])
            reco_z_y = np.append(reco_z_y,depths[np.argmax(sum_log_y)])
            reco_z_comb = np.append(reco_z_comb,depths[np.argmax(sum_log_y+sum_log_x)])
            
    reco_z_x_corrs.append(reco_z_x)
    reco_z_y_corrs.append(reco_z_y)
    reco_z_comb_corrs.append(reco_z_comb)
    
    true_z = np.array([])
    for z in depths:
        for i in range(0,100):

            true_z = np.append(true_z,z)
            
    r2_vals.append(stats.linregress(reco_z_x, true_z)[2])
    
t2 = time.perf_counter()
print(t2-t1)


reco_z_x_df = pd.DataFrame(reco_z_x_corrs)    
reco_z_y_df = pd.DataFrame(reco_z_y_corrs)
reco_z_comb_df = pd.DataFrame(reco_z_comb_corrs)



reco_z_x_df.to_csv("{}depth_reco/reco_z_x.txt".format(options.outputDir), encoding="utf-8", index=False)
reco_z_y_df.to_csv("{}depth_reco/reco_z_y.txt".format(options.outputDir), encoding="utf-8", index=False)
reco_z_comb_df.to_csv("{}depth_reco/reco_z_comb.txt".format(options.outputDir), encoding="utf-8", index=False)

t2 = time.perf_counter()
print(t2-t1)
