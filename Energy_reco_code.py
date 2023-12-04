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
-- INSERT --                                                                                                                                                                   75,4           2%
