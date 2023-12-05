import ROOT as r
import numpy as np
import pandas as pd
import pickle
import sys
from ShipGeoConfig import ConfigRegistry
from rootpyPickler import Unpickler
import shipLHC_conf as sndDet_conf
import SndlhcGeo
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from argparse import ArgumentParser

parser = ArgumentParser()
#group = parser.add_mutually_exclusive_group()

parser.add_argument("--Z",   dest="z", required=False, default = 0, type = int)
parser.add_argument("--E",   dest="e", required=False, default = 0, type = int)
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




scifi_x_avg = np.array([])
scifi_y_avg = np.array([])
scifi_z_avg = np.array([])

scifi_plane = np.array([])

event_avg_x = np.array([])

event_avg_y = np.array([])

vertical_hits = np.array([])

evt_idx = np.array([])

particle_name = np.array([])

stat1_x_sipms = np.array([])
            

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

# /eos/experiment/sndlhc/users/marssnd/PGsim/pion_5GeV
# /eos/user/s/skatsaro/PGsim/pions_100/Ntuples/1/sndLHC.PG_211-TGeant4_digCPP.root

from os.path import exists

cbmsim = r.TChain("cbmsim") # Create the TChain

#cbmsim.SetBranchStatus("*", 0)
#cbmsim.SetBranchStatus("Digi_ScifiHits", 1)

n_files_to_read = 20
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
# geofile = '/eos/experiment/sndlhc/users/marssnd/PGsim/pion_5GeV/geofile_full.PG_211-TGeant4.root'
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

#h_hor = r.TH2D('h_hor', 'h_hor;z;y', 500, 280, 380, 120, 0, 60)
#h_ver = r.TH2D('h_ver', 'h_ver;z;x', 500, 280, 380, 100, -50, 0)

#stat1_x = r.TH1D("stat1_x","stat1_x;x",100,-50,0)

#stat1_hits = r.TH1D("stat1_x","stat1_x;hits",100,-50,0)


# Loop over events
for i_event, event in enumerate(cbmsim) :
    if i_event % 100 == 0 :
        print("Reading event number {0}".format(i_event))

    # Truth-level information
#     mcTracks    = event.MCTrack
#     ScifiPoints = event.ScifiPoint
#     MuFilPoints = event.MuFilterPoint

    evt_vertical_hits = np.array([])

    scifi_left_x = np.array([])
    scifi_left_y = np.array([])
    scifi_left_z = np.array([])


    scifi_right_x = np.array([])
    scifi_right_y = np.array([])
    scifi_right_z = np.array([])


#     daughter_charge = []


    # Digitised information
    ScifiDigihits      = event.Digi_ScifiHits
#     MuonFilterDigihits = event.Digi_MuFilterHits

#     # ... looping over Truth-level quantities
#     for idxtrk, track in enumerate(mcTracks):
#         moth_id = track.GetMotherId()
#         if moth_id == -1:
#             # pion
#             evt_weight = track.GetWeight()

#             pi_px.append(track.GetPx())
#             pi_py.append(track.GetPy())
#             pi_pz.append(track.GetPz())
#             pi_E.append(track.GetEnergy())


#         elif ((moth_id==0) & (track.GetP()>0)):
#             # pion daughters
#             partpdgcode = track.GetPdgCode()
#             particle = pdg.GetParticle(partpdgcode)
            
#             # daughter charge and energy

#             if particle:    
#                 pcharge = particle.Charge()/3.
#                 penergy = track.GetEnergy()
#                 pmom = track.GetP()
#                 daughter_charge.append(pcharge)

#                 ds_e = np.append(ds_e,penergy)
#                 if pcharge != 0:
#                     ds_e_charged = np.append(ds_e_charged,penergy)
#                 else:
#                     ds_e_neutral = np.append(ds_e_neutral,penergy)  
                    
#             # check if proton or neutron
                    
#             if partpdgcode == 2212 or partpdgcode == -2212:
#                 ds_e_proton = np.append(ds_e_proton,penergy)
#                 ds_mom_proton= np.append(ds_mom_proton,pmom)
                    
#             elif partpdgcode == 2112 or partpdgcode == -2112:
#                 ds_e_neutron = np.append(ds_e_neutron,penergy)
#                 ds_mom_neutron = np.append(ds_mom_neutron,pmom)
                
#             # save particle name
            
#             particle_name = np.append(particle_name, GetParticleName(partpdgcode,pdg))


    if (i_event%10)==0:
        print(i_event)

#     ds_mul_charged = np.append(ds_mul_charged,np.sum(np.array(daughter_charge) != 0, axis=0))
# #     print(np.sum(np.array(daughter_charge) != 0, axis=0))

#     ds_mul_neutral = np.append(ds_mul_neutral,np.sum(np.array(daughter_charge) == 0, axis=0))
# #     print(np.sum(np.array(daughter_charge) == 0, axis=0))

#     ds_mul = np.append(ds_mul,len(daughter_charge))
# #     print(len(daughter_charge))


    # ... looping over digitised quantities

    if ScifiDigihits:
        for idxscifihits, scifihit in enumerate(ScifiDigihits):
            if scifihit.isValid():
                vLeft, vRight = r.TVector3(), r.TVector3()
#                 mean_position = (vLeft + vRight)*0.5
#                 print(scifiDet.GetnSiPMs(scifihit.GetDetectorID()))
                scifiDet.GetSiPMPosition(scifihit.GetDetectorID(), vLeft, vRight)
                stat_nr_scifi  = scifihit.GetStation()

                scifi_left_x = np.append(scifi_left_x,vLeft.X())
                scifi_left_y = np.append(scifi_left_y,vLeft.Y())
                scifi_left_z = np.append(scifi_left_z,vLeft.Z())


                scifi_right_x = np.append(scifi_right_x,vRight.X())
                scifi_right_y = np.append(scifi_right_y,vRight.Y())
                scifi_right_z = np.append(scifi_right_z,vRight.Z())

                scifi_plane = np.append(scifi_plane,stat_nr_scifi)

                evt_vertical_hits = np.append(evt_vertical_hits,scifihit.isVertical())

                evt_idx = np.append(evt_idx,i_event)
                
                #if stat_nr_scifi == 1 and scifihit.isVertical()==1:
                        #stat1_hits.Fill((vLeft.X() + vRight.X())/2.)


        scifi_x_avg = np.append(scifi_x_avg,(scifi_left_x+scifi_right_x)/2)
        scifi_y_avg = np.append(scifi_y_avg,(scifi_left_y+scifi_right_y)/2)
        scifi_z_avg = np.append(scifi_z_avg,(scifi_left_z+scifi_right_z)/2)

        scifi_evt_x_avg = (scifi_left_x+scifi_right_x)/2
        scifi_evt_y_avg = (scifi_left_y+scifi_right_y)/2
        scifi_evt_z_avg = (scifi_left_z+scifi_right_z)/2

        vertical_hits = np.append(vertical_hits,evt_vertical_hits)
        
    a, b = r.TVector3(), r.TVector3()
#     h_hor = r.TH2D('h_hor', 'h_hor;z;y', 500, 280, 380, 120, 0, 60)
#     h_ver = r.TH2D('h_ver', 'h_ver;z;x', 500, 280, 380, 100, -50, 0)
#     h_

    for i_sta in range(1,6):
        for i_mat in range(0,3):
            for i_sipm in range(0,4):
                for i_chan in range(0, 128):

                    id = i_sta*1000000 + i_mat*10000 + i_sipm*1000 + i_chan

                    # Horizontal
                    scifiDet.GetSiPMPosition(id, a, b);
                    #h_hor.Fill((a.Z() + b.Z())/2., (a.Y() + b.Y())/2.)

                    # Vertical
                    id += 100000 
                    scifiDet.GetSiPMPosition(id, a, b)
                    #h_ver.Fill((a.Z() + b.Z())/2., (a.X() + b.X())/2.)
                    
                    if i_sta == 1 and i_event == 1:
                        #stat1_x.Fill((a.X() + b.X())/2.)
                        
                        stat1_x_sipms = np.append(stat1_x_sipms,(a.X() + b.X())/2.)
                        
                        





    if np.unique(evt_vertical_hits).size==2:


        vert = evt_vertical_hits == 1
        horz = evt_vertical_hits == 0

#         for i in range(0,5):
#             plane1_evt_avg = 


        event_avg_x = np.append(event_avg_x,np.average(scifi_evt_x_avg[vert]))
        event_avg_y = np.append(event_avg_y,np.average(scifi_evt_y_avg[horz]))
        #print(scifi_evt_x_avg[vert].shape,scifi_evt_y_avg[horz].shape,np.average(scifi_evt_x_avg[evt_vertical_hits==1]),\
              #np.average(scifi_evt_y_avg[evt_vertical_hits==0]))

plane_idx = np.where(scifi_plane==1)[0]
x_size = np.shape(scifi_x_avg[plane_idx][vertical_hits[plane_idx]==1])[0]
stat1_x_scaled = plt.hist(scifi_x_avg[plane_idx][vertical_hits[plane_idx]==1],bins = np.linspace(-50,-0,101),histtype="step",
         weights=np.ones(x_size)/(n_files_to_read*10))
stat1_x_sipm_counts = plt.hist(stat1_x_sipms,bins = np.linspace(-50,0,101))

PDF = np.nan_to_num(stat1_x_scaled[0]/stat1_x_sipm_counts[0],nan=0.0)

PDF_bins = plt.hist(np.linspace(-50,0,100),bins=np.linspace(-50,0,101),weights=PDF)

print(PDF)

#with open('PDF.txt', 'w') as f:
#    f.write(PDF)

np.savetxt("{}PDF.txt".format(options.outputDir), PDF, delimiter=',')

print("Done")

