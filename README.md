# SND-LHC
Hadronic shower reconstruction for the SND@LHC experiment

In this project, the first procedure for hadronic shower energy and vertex position reconstruction is 
developed for the SND detector. Shower propagation is profiled using PDFs
and a log-likelihood function is built to reconstruct energy and vertex. 

Steps to generate the results:

1. Run the GEANT4 simulation for every depth and energy

2. Run the PDF_python_code.py to use the GEANT4 simulation results and create a PDF for each SciFi station for every depth and energy

3. Run the Energy_reco_code.py which takes individual events and performs a log-likelihood scan over all the SciFi PDFs for each energy and a fixed depth. For each scan, the log-likelihood is summed over all 5 SciFi stations. The maximum of the log-likelihood corresponds to the reconstructed energy.

4. Run the Depth_reco_code.py which takes individual events and performs a log-likelihood scan over all the SciFi PDFs for each depth at a fixed energy. For each scan, the log-likelihood is summed over all 5 SciFi stations. The maximum of the log-likelihood corresponds to the reconstructed depth.


