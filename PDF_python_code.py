import ROOT as r
import numpy as np
import pandas as pd
#import pickle
#import sys
#from ShipGeoConfig import ConfigRegistry
from rootpyPickler import Unpickler
import shipLHC_conf as sndDet_conf
import SndlhcGeo
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from argparse import ArgumentParser
import time
from itertools import chain


parser = ArgumentParser()

parser.add_argument("--Z",   dest="z", required=False, default = 0, type = int)
parser.add_argument("--E",   dest="e", required=False, default = 0, type = int)
parser.add_argument("--N",   dest="n", required=False, default = 0, type = int)
parser.add_argument("-o", "--output",dest="outputDir",  help="Output directory", required=False,  default=".")


options = parser.parse_args()

print(options.e,options.z)


def GetParticleCharge (pdgcode, pdgdatabase):

  #from PDG, get charge
    charge = 0.
    if (pdgdatabase.GetParticle(pdgcode)): 
        charge = pdgdatabase.GetParticle(pdgcode).Charge()
    elif (pdgcode > 1e+8):
        charge = 1. #these are heavy nuclei, for now we give them charge 1.Add a decode function with info from (https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf)
    return charge


def GetParticleName(pdgcode, pdgdatabase):

  #from PDG, get charge
    name = "zero"
    if (pdgdatabase.GetParticle(pdgcode)): 
        name = pdgdatabase.GetParticle(pdgcode).GetName()
    elif (pdgcode > 1e+8):
        name = "heavy nuclei" #these are heavy nuclei, for now we give them charge 1.Add a decode function with info from (https://pdg.lbl.gov/2007/reviews/montecarlorpp.pdf)
    return name


t1 = time.perf_counter()


scifi_x_avg = []
scifi_y_avg = []
scifi_z_avg = []

scifi_plane = []

vertical_hits = []

evt_idx = []


stat1_x_sipms = np.array([])
stat2_x_sipms = np.array([])
stat3_x_sipms = np.array([])
stat4_x_sipms = np.array([])
stat5_x_sipms = np.array([])

stat1_y_sipms = np.array([])
stat2_y_sipms = np.array([])
stat3_y_sipms = np.array([])
stat4_y_sipms = np.array([])
stat5_y_sipms = np.array([])
            

def get_QDC_US(hit):
    sig_left = 0; sig_right = 0

    # US or DS Muon Filter: save the QDC (NOT CALIBRATED as of 06.11.22)
    if hit.GetSystem() in [2, 3]:
        for ch in hit.GetAllSignals(False):
            if (hit.GetnSiPMs() > ch[0]):  # left side
                sig_left += ch[1]
            else:                           # right side
                sig_right += ch[1]
    
    return (sig_left, sig_right)

def MuFiGetStation(detID):
        return r.TMath.Floor(detID/1000)-r.TMath.Floor(detID/10000)*10

# define your functions/main here

from os.path import exists

cbmsim = r.TChain("cbmsim") # Create the TChain
cbmsim.SetBranchStatus("MCTrack", 0)

print("Starting chain")


n_files_to_read = options.n
n_files_read = 0
for i in range(n_files_to_read) :
    file_name = '/eos/user/s/skatsaro/PGsim/depth_{}/pions_{}/Ntuples/{}/sndLHC.PG_211-TGeant4_digCPP.root'.format(options.z,options.e,i+1)
    
    # Combine the root files
    if not exists(file_name) :
        continue # Combine only existing root files
    this_read = cbmsim.Add(file_name)

    if this_read > 0 :
        n_files_read += 1
    
print(cbmsim.GetEntries()) # Check if all 1000 events were simulated and combined

pdg  = r.TDatabasePDG.Instance()

geofile = '/eos/user/s/skatsaro/PGsim/depth_{}/pions_{}/Ntuples/1/geofile_full.PG_211-TGeant4.root'.format(options.z,options.e)
fgeo    = r.TFile.Open(geofile)
upkl    = Unpickler(fgeo)
snd_geo = upkl.load('ShipGeo')
geo     = SndlhcGeo.GeoInterface(geofile)
run     = r.FairRunSim()
modules = sndDet_conf.configure(run, snd_geo)
r.gGeoManager.Import(geofile)
lsOfGlobals = r.gROOT.GetListOfGlobals()
lsOfGlobals.Add(geo.modules['Scifi'])
lsOfGlobals.Add(geo.modules['MuFilter'])
scifiDet    = lsOfGlobals.FindObject('Scifi')
muonfiltDet = lsOfGlobals.FindObject('MuFilter')

scifiDet.SetConfPar('Scifi/scifimat_length' , 39.0)
scifiDet.SetConfPar('Scifi/channel_width'   , (0.25/10))
scifiDet.SetConfPar('Scifi/epoxymat_z'      , 0.17)
scifiDet.SetConfPar('Scifi/nsipm_channels'  , 128)
scifiDet.SetConfPar('Scifi/nsipm_mat'       , 4)
scifiDet.SetConfPar('Scifi/nmats'           , 3)
scifiDet.SetConfPar('Scifi/sipm_edge'       , (0.17/10))
scifiDet.SetConfPar('Scifi/charr_width'     , (64 * 0.25/10))
scifiDet.SetConfPar('Scifi/charr_gap'       , (0.2/10))
scifiDet.SetConfPar('Scifi/sipm_diegap'     , (0.06/10))
scifiDet.SetConfPar('Scifi/firstChannelX'   , -19.528)
scifiDet.SiPMmapping()


# Loop over events
for i_event, event in enumerate(cbmsim) :
    if i_event % 100 == 0 :
        print("Reading event number {0}".format(i_event))

    # Truth-level information
#     mcTracks    = event.MCTrack
#     ScifiPoints = event.ScifiPoint
#     MuFilPoints = event.MuFilterPoint

    evt_vertical_hits = []
    
    scifi_left_x = []
    scifi_left_y = []
    scifi_left_z = []

    
    scifi_right_x = []
    scifi_right_y = []
    scifi_right_z = []


    # Digitised information
    ScifiDigihits = event.Digi_ScifiHits


    if (i_event%10)==0:
        print(i_event)


    # ... looping over digitised quantities

    if ScifiDigihits:
        for idxscifihits, scifihit in enumerate(ScifiDigihits):
            if scifihit.isValid():
                vLeft, vRight = r.TVector3(), r.TVector3()
                scifiDet.GetSiPMPosition(scifihit.GetDetectorID(), vLeft, vRight)
                stat_nr_scifi  = scifihit.GetStation()
                
                scifi_left_x.append(vLeft.X())
                scifi_left_y.append(vLeft.Y())
                scifi_left_z.append(vLeft.Z())
                
                
                scifi_right_x.append(vRight.X())
                scifi_right_y.append(vRight.Y())
                scifi_right_z.append(vRight.Z())

                scifi_plane.append(stat_nr_scifi)

                evt_vertical_hits.append(scifihit.isVertical())

                evt_idx.append(i_event)


        scifi_x_avg.append((np.array(scifi_left_x)+np.array(scifi_right_x))/2)
        scifi_y_avg.append((np.array(scifi_left_y)+np.array(scifi_right_y))/2)
        scifi_z_avg.append((np.array(scifi_left_z)+(scifi_right_z))/2)

        vertical_hits.append(evt_vertical_hits)
        
    a, b = r.TVector3(), r.TVector3()

    if i_event == 1:
        for i_sta in range(1,6):
            for i_mat in range(0,3):
                for i_sipm in range(0,4):
                    for i_chan in range(0, 128):

                        id = i_sta*1000000 + i_mat*10000 + i_sipm*1000 + i_chan

                        # Horizontal
                        scifiDet.GetSiPMPosition(id, a, b);

                        if i_sta == 1:
                            stat1_y_sipms = np.append(stat1_y_sipms,(a.Y() + b.Y())/2.)
                        if i_sta == 2:
                            stat2_y_sipms = np.append(stat2_y_sipms,(a.Y() + b.Y())/2.)
                        if i_sta == 3:
                            stat3_y_sipms = np.append(stat3_y_sipms,(a.Y() + b.Y())/2.)
                        if i_sta == 4:
                            stat4_y_sipms = np.append(stat4_y_sipms,(a.Y() + b.Y())/2.)
                        if i_sta == 5:
                            stat5_y_sipms = np.append(stat5_y_sipms,(a.Y() + b.Y())/2.)

                        # Vertical
                        id += 100000 
                        scifiDet.GetSiPMPosition(id, a, b)

                        if i_sta == 1:
                            stat1_x_sipms = np.append(stat1_x_sipms,(a.X() + b.X())/2.)
                        if i_sta == 2:
                            stat2_x_sipms = np.append(stat2_x_sipms,(a.X() + b.X())/2.)
                        if i_sta == 3:
                            stat3_x_sipms = np.append(stat3_x_sipms,(a.X() + b.X())/2.)
                        if i_sta == 4:
                            stat4_x_sipms = np.append(stat4_x_sipms,(a.X() + b.X())/2.)
                        if i_sta == 5:
                            stat5_x_sipms = np.append(stat5_x_sipms,(a.X() + b.X())/2.)
                            
                            
scifi_x_avg = np.array(list(chain.from_iterable(scifi_x_avg))) 
scifi_y_avg = np.array(list(chain.from_iterable(scifi_y_avg)))
scifi_z_avg = np.array(list(chain.from_iterable(scifi_z_avg)))

vertical_hits = np.array(list(chain.from_iterable(vertical_hits)))

scifi_plane = np.array(scifi_plane)
evt_idx = np.array(evt_idx)

np.savetxt("{}scifi_plane.txt".format(options.outputDir), scifi_plane, delimiter=',')
np.savetxt("{}evt_idx.txt".format(options.outputDir), evt_idx, delimiter=',')
np.savetxt("{}vertical_hits.txt".format(options.outputDir), vertical_hits, delimiter=',')

                
for plane, sipm_counts in enumerate([stat1_x_sipms,stat2_x_sipms,stat3_x_sipms,stat4_x_sipms,stat5_x_sipms],start=1):
    plane_idx = np.where(scifi_plane==plane)[0]
    
    # stat_x_hits = np.histogram(scifi_x_avg[plane_idx][vertical_hits[plane_idx]==1],bins = np.linspace(-50,-0,101))
    # np.savetxt("{}hits_x_{}.txt".format(options.outputDir,plane), stat_x_hits[0], delimiter=',')
    
    x_size = np.shape(scifi_x_avg[plane_idx][vertical_hits[plane_idx]==1])[0]
    stat_x_scaled = np.histogram(scifi_x_avg[plane_idx][vertical_hits[plane_idx]==1],bins = np.linspace(-50,-0,101),
                             weights=np.ones(x_size)/(n_files_to_read*10))
    
    # np.savetxt("{}hits_x_{}.txt".format(options.outputDir,plane), stat_x_scaled[0], delimiter=',')
    
    stat_x_sipm_counts = np.histogram(sipm_counts,bins = np.linspace(-50,0,101))
    
    # np.savetxt("{}SiPM_x_{}.txt".format(options.outputDir,plane), stat_x_sipm_counts[0], delimiter=',')
    
    PDF = np.nan_to_num(stat_x_scaled[0]/stat_x_sipm_counts[0],nan=0.0)
    np.savetxt("{}PDF_x_{}.txt".format(options.outputDir,plane), PDF, delimiter=',')
    

for plane, sipm_counts in enumerate([stat1_y_sipms,stat2_y_sipms,stat3_y_sipms,stat4_y_sipms,stat5_y_sipms],start=1):
    plane_idx = np.where(scifi_plane==plane)[0]
    
    # stat_y_hits = np.histogram(scifi_y_avg[plane_idx][vertical_hits[plane_idx]==0],bins = np.linspace(10,60,101))
    # np.savetxt("{}hits_y_{}.txt".format(options.outputDir,plane), stat_y_hits[0], delimiter=',')
    
    y_size = np.shape(scifi_y_avg[plane_idx][vertical_hits[plane_idx]==0])[0]
    stat_y_scaled = np.histogram(scifi_y_avg[plane_idx][vertical_hits[plane_idx]==0],bins = np.linspace(10,60,101),
                             weights=np.ones(y_size)/(n_files_to_read*10))
    
    # np.savetxt("{}hits_y_{}.txt".format(options.outputDir,plane), stat_y_scaled[0], delimiter=',')

    stat_y_sipm_counts = np.histogram(sipm_counts,bins = np.linspace(10,60,101))
    
    # np.savetxt("{}SiPM_y_{}.txt".format(options.outputDir,plane), stat_y_sipm_counts[0], delimiter=',')

    PDF = np.nan_to_num(stat_y_scaled[0]/stat_y_sipm_counts[0],nan=0.0)
    np.savetxt("{}PDF_y_{}.txt".format(options.outputDir,plane), PDF, delimiter=',')
    
    

# hits_x = []
# hits_y = []
    
# for event in range(0,n_files_to_read*10):
    
#     for plane, sipm_counts in enumerate([stat1_x_sipms,stat2_x_sipms,stat3_x_sipms,stat4_x_sipms,stat5_x_sipms],start=1):
        
#         plane_idx = np.where(scifi_plane==plane)[0]
        
#         evt = np.where(evt_idx==event)[0]
        
        
#         selection = np.array(list(set(plane_idx).intersection(evt)))
        
        
        
#         if selection.size>0:
#             stat_x_hits = np.histogram(scifi_x_avg[selection][vertical_hits[selection]==1],bins = np.linspace(-50,-0,101))
#             # np.savetxt("{}events/hits_x_{}_{}.txt".format(options.outputDir,plane,event+1), stat_x_hits[0], delimiter=',')
#             hits_x.append(stat_x_hits[0])
#         else:
#             print("no selection")
            
#             stat_x_hits = np.zeros(100)
#             hits_x.append(stat_x_hits)
            
#             # np.histogram(scifi_x_avg[selection][vertical_hits[selection]==1],bins = np.linspace(-50,-0,101))
#             # np.savetxt("{}events/hits_x_{}_{}.txt".format(options.outputDir,plane,event+1), np.zeros(100), delimiter=',')
        
#         # stat_x_scaled = np.histogram(scifi_x_avg[selection][vertical_hits[selection]==1],bins = np.linspace(-50,-0,101))
#         # stat_x_sipm_counts = np.histogram(sipm_counts,bins = np.linspace(-50,0,101))
    
#         # PDF = np.nan_to_num(stat_x_scaled[0]/stat_x_sipm_counts[0],nan=0.0)
#         # np.savetxt("{}events/PDF_x_{}_{}.txt".format(options.outputDir,plane,event+1), PDF, delimiter=',')

        


# for event in range(0,n_files_to_read*10):
    
#     for plane, sipm_counts in enumerate([stat1_y_sipms,stat2_y_sipms,stat3_y_sipms,stat4_y_sipms,stat5_y_sipms],start=1):
        
#         plane_idx = np.where(scifi_plane==plane)[0]
        
#         evt = np.where(evt_idx==event)[0]
        
        
#         selection = np.array(list(set(plane_idx).intersection(evt)))
        
#         if selection.size>0:
#             stat_y_hits = np.histogram(scifi_y_avg[selection][vertical_hits[selection]==0],bins = np.linspace(10,60,101))
#             hits_y.append(stat_y_hits[0])
#             # np.savetxt("{}events/hits_y_{}_{}.txt".format(options.outputDir,plane,event+1), stat_y_hits[0], delimiter=',')
#         else:
#             print("no selection")
#             stat_y_hits = np.zeros(100)
#             hits_y.append(stat_y_hits)
            
#             # np.histogram(scifi_x_avg[selection][vertical_hits[selection]==1],bins = np.linspace(-50,-0,101))
#             # np.savetxt("{}events/hits_y_{}_{}.txt".format(options.outputDir,plane,event+1), np.zeros(100), delimiter=',')
        
        
        
# hits_x_df = pd.DataFrame(hits_x)
# hits_x_df.to_csv("{}events/hits_x.txt".format(options.outputDir), encoding="utf-8", index=False)
        

# hits_y_df = pd.DataFrame(hits_y)
# hits_y_df.to_csv("{}events/hits_y.txt".format(options.outputDir), encoding="utf-8", index=False)

t2 = time.perf_counter()
print(t2-t1)



# for plane in range(1,6):
#     PDF = np.loadtxt("{}PDF_x_{}.txt".format(options.outputDir,plane))
#     PDF_bins = plt.hist(np.linspace(-50,0,100),bins=np.linspace(-50,0,101),weights=PDF)
#     print(PDF)
