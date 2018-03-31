# PYTHONPATH= tu vlozit cestu k balickom, ak nebude fungovat anakonda
export PATH=$PATH:~/project_afm_cryoem_actual/project_afm_cryoem/project_python3/
module add anaconda3
source activate python35_numpy_matplotlib
docker.py 1hzh.pdb 1hzh_bcr_from_pdb.bcr psubmit_test_exportpath --rots_count 1000 --rots_count_z 40 --best_fits_count 30

