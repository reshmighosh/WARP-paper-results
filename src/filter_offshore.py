import pandas as pd 
import numpy as np

origin_results_folder = '../map_results'
destination_results_folder = '../map_results_onshore'

onshore_bounds = pd.read_excel("offshore_bounds/offshore_MERRA_Format_bounds.xlsx",index_col=0).values

def filter_offshore(region,year,capacity,technology,add_on=None):
    elcc_map_file = '%s/%s_%d_%d_MW_%s%s_results_map.csv' % (origin_results_folder,region,year,capacity,technology,'' if add_on is None else '_'+add_on)
    elcc_df = pd.read_csv(elcc_map_file,index_col=0,header=0)
    elcc = elcc_df.to_numpy()
    lats = np.asarray(elcc_df.index.values)
    lons = np.asarray(elcc_df.columns.values).astype(float)

    #if cell is onshore (0) leave value as is, if offshore (1) place value as np.nan
    onshore_map = np.where(onshore_bounds == 0, elcc, np.nan)
    
    elcc = onshore_map

    results_filename = '%s_%d_%d_MW_%s%s_results.csv' % (region,year,capacity,technology,'' if add_on is None else '_'+add_on)
    
    elcc_map = pd.DataFrame(index=lats, columns=lons, data=elcc)
    elcc_map.to_csv('%s/%s' % (destination_results_folder, results_filename))
    return elcc_map

# Base cases
capacity = 500
for region in ['basin','california','mountains','northwest','southwest']:
    for year in [2016, 2017, 2018, 2019]:
        for technology in ['solar', 'wind']:
            for ff in [True, False]:
                try: 
                    filter_offshore(region,year,capacity,technology,'FF' if ff else '')
                except:
                    pass

# Sensitivities
year = 2019
for region in ['basin','california','mountains','northwest','southwest']:
    for technology in ['solar','wind']:
        for capacity in [100,500,2000]:
            # storage
            if capacity == 500:
                try: 
                    filter_offshore(region,year,capacity,technology,'storage')
                except:
                    pass
            # variable size
            else: 
                try: 
                    filter_offshore(region,year,capacity,technology)
                except:
                    pass