# SND-LHC
Hadronic shower reconstruction for the SND@LHC experiment

In this project, the first procedure for hadronic shower energy and vertex position reconstruction is 
developed for the SND detector. Shower propagation is profiled using PDFs
and a log-likelihood function is built to reconstruct energy and vertex. 

Steps to prepare the files:

1. Run make_depth_dirs.sh
2. Run generate_energy_reco.sh, while selecting "n" to runPG and "n" to createPDFs

Steps to generate results:

1. Run generate_energy_reco.sh and select "y" to runPG and "n" to createPDFs
2. Run generate_energy_reco.sh once the condor jobs have finished and select "n" to runPG and "y" to createPDFs

<!--- 
1. Create all the depth dirs (z_295,z_304,...,z_347) containing the dir e_50 from z_291
2. For each depth dir create all energy sub dirs (e_50,e_100,...,e_2000)
3. Make sure each dir and sub-dir has empty folders with the names error, log, output
4. Run generate_energy_reco.sh with the last line commented out. This will copy the scripts of the z_291 dir.
5. For each depth dir run generate_PDF.sh to fill the energy dirs, update them and generate the PDFs
6. Run generate_energy_reco.sh again but with the last line uncommented to run the Energy_reco_code.py and obtain the log-likelihood 
-->

Steps taken by the scripts to generate results:

1. Run the GEANT4 simulation in run_simSND.py, for every depth and energy

2. Run the PDF_python_code.py to use the GEANT4 simulation results and create a PDF for each SciFi station for every depth and energy

3. Run the Energy_reco_code.py which takes individual events and performs a log-likelihood scan over all the SciFi PDFs for each energy and a fixed depth. For each scan, the log-likelihood is summed over all 5 SciFi stations. The maximum of the log-likelihood corresponds to the reconstructed energy.

4. Run the Depth_reco_code.py which takes individual events and performs a log-likelihood scan over all the SciFi PDFs for each depth at a fixed energy. For each scan, the log-likelihood is summed over all 5 SciFi stations. The maximum of the log-likelihood corresponds to the reconstructed depth.


