# SND-LHC
Hadronic shower reconstruction for the SND@LHC experiment.

In this project, the first procedure for hadronic shower energy and vertex position reconstruction is 
developed for the SND detector. Shower propagation is profiled using PDFs
and a log-likelihood function is built to reconstruct energy and vertex. 

<h3><b>Key Jupyter notebooks to obtain final plots (useful summary of the reco process):</b></h3>
<ul>
  <li><b>Energy reco plots (summary reco plots)</b></li>
  <li><b>Energy reco diagnostics (single event energy reco breakdown)</b></li>
  <li><b>Depth reco and diagnostics (full depth reco, summary plots, single event reco breakdown)</b></li>
</ul>

<h3><b>Reproducing the results</b></h3>

**To reproduce the results you need to have all the files from this repository**

<b>Steps to prepare the files:</b>

1. Run <code>make_depth_dirs.sh</code>
2. Run <code>generate_energy_reco.sh</code>, while selecting "n" to submit to condor, "n" to runPG and "n" to createPDFs

<b>Steps to generate results:</b>

1. Run <code>generate_energy_reco.sh</code> and select "n" to submit to condor, "y" to runPG and "n" to createPDFs (simulate 1000 events per depth and energy)
2. Run <code>generate_energy_reco.sh</code> once the condor jobs have finished and select "n" to submit to condor, "n" to runPG and "y" to createPDFs (create the PDFs for each station of each depth and energy)
3. Run <code>generate_energy_reco.sh</code> once the PDFs have been created and select "y" to submit to condor, "n" to runPG and "n" to createPDFs (reconstruct the energy for each event)
4. Run the reconstruction code in jupyter notebook "Depth reco and diagnostics.ipynb" (reconstruct the depth for each event)

<!--- 
1. Create all the depth dirs (z_295,z_304,...,z_347) containing the dir e_50 from z_291
2. For each depth dir create all energy sub dirs (e_50,e_100,...,e_2000)
3. Make sure each dir and sub-dir has empty folders with the names error, log, output
4. Run generate_energy_reco.sh with the last line commented out. This will copy the scripts of the z_291 dir.
5. For each depth dir run generate_PDF.sh to fill the energy dirs, update them and generate the PDFs
6. Run generate_energy_reco.sh again but with the last line uncommented to run the Energy_reco_code.py and obtain the log-likelihood 
-->

<h3>Explanation of the scripts</h3>

<b>Steps taken by the scripts to prepare the results:</b>

1. All the depth dirs are created from <code>make_depth_dirs.sh</code>
2. <code>generate_energy_reco.sh</code> copies the file contents of z_291 to all the other depths and updates the parameters of the execution files

<b>Steps taken by the scripts to generate results:</b>

1. Run the GEANT4 simulation in <code>run_simSND.py</code>, for every depth and energy

2. Run the <code>PDF_python_code.py</code> to use the GEANT4 simulation results and create a PDF for each SciFi station for every depth and energy

3. Run the <code>Energy_reco_code.py</code> which takes individual events and performs a log-likelihood scan over all the SciFi PDFs for each energy and a fixed depth. For each scan, the log-likelihood is summed over all 5 SciFi stations. The maximum of the log-likelihood corresponds to the reconstructed energy.

(4.) Depth reco needs to be run manually via the jupyter notebook "Depth reco and diagnostics.ipynb". The reconstruction code works similarly to the code in <code>Energy_reco_code.py</code>.




<!---
4. Run the Depth_reco_code.py which takes individual events and performs a log-likelihood scan over all the SciFi PDFs for each depth at a fixed energy. For each scan, the log-likelihood is summed over all 5 SciFi stations. The maximum of the log-likelihood corresponds to the reconstructed depth.
-->


