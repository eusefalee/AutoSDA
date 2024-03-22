# Script that performs the loss assessment from the EDPs

import os
from pathlib import Path
import pandas as pd
import numpy as np
from pelicun.base import set_options, convert_to_MultiIndex
from pelicun.assessment import Assessment

# define directories
lossDirectory = os.getcwd()
baseDirectory = os.path.join(Path(lossDirectory,'..'))

# Get the buildings to estimate EDPs for
from main_program import inputs


def preprocessPelicun(pfa,sdr):

    """
    Function that formats the data to be used in pelicun
    """
    index_name = []
    median = []
    log_std = []
    #1-PFA-0-1
    for stripe in pfa[0].unique():
        churn_df = pfa[pfa[0]==stripe]
        story_name = 0 
        for story in churn_df.columns:
            for uniq_dir in pfa[1].unique():
                if story >=3:
                    story_name = story - 3
                    index_name.append('%s-PFA-%s-%s'%(stripe, story_name, uniq_dir))
                    median.append(pfa[(pfa[0]==stripe) & (pfa[1]==uniq_dir)][story].median())
                    log_std.append(pfa[(pfa[0]==stripe) & (pfa[1]==uniq_dir)][story].std())
    d = {
        'idx': index_name, 
        'median': median, 
        'log_std': log_std
    }
    df_pfa = pd.DataFrame(d)
    df_pfa = df_pfa.set_index('idx')

    ## PID
    index_name = []
    median = []
    log_std = []
    #1-PID-0-1
    for stripe in sdr[0].unique():
        churn_df = sdr[sdr[0]==stripe]
        story_name = 0 
        for story in churn_df.columns:
            for uniq_dir in sdr[1].unique():
                if story >=3:
                    story_name = story - 2
                    index_name.append('%s-PID-%s-%s'%(stripe, story_name, uniq_dir))
                    median.append(sdr[(sdr[0]==stripe) & (sdr[1]==uniq_dir)][story].median())
                    log_std.append(sdr[(sdr[0]==stripe) & (sdr[1]==uniq_dir)][story].std())
    d = {
        'idx': index_name, 
        'median': median, 
        'log_std': log_std
    }
    df_sdr = pd.DataFrame(d)
    df_sdr = df_sdr.set_index('idx')

    ## combine two dfs 
    df_comb = pd.concat([df_pfa, df_sdr])
    df_comb.head()

    return df_comb


def performAssessment(pelicundf,nstory,sample_size = 10000, delta_y = 0.0075,stripe = '3'):

    """
    Function that performs the loss assessment with pelicun

    sample_size
    delta_y
    stripe - hazard level
    """

    # initialize a pelicun Assessment
    PAL = Assessment({"PrintLog": True, "Seed": 415,})

    # load the demand model
    PAL.demand.load_model({'marginals': stripe_demands,
                        'correlation': perfect_CORR})

    # generate samples
    PAL.demand.generate_sample({"SampleSize": sample_size})

    # add residual drift and Sa
    demand_sample = PAL.demand.save_sample()

    RID = PAL.demand.estimate_RID(demand_sample['PID'], {'yield_drift': delta_y})
    demand_sample_ext = pd.concat([demand_sample, RID], axis=1)

    Sa_vals = [0.158, 0.387, 0.615, 0.843, 1.071, 1.299, 1.528, 1.756]
    demand_sample_ext[('SA_1.13',0,1)] = Sa_vals[int(stripe)-1]

    # add units to the data 
    demand_sample_ext.T.insert(0, 'Units',"")

    # PFA and SA are in "g" in this example, while PID and RID are "rad"
    demand_sample_ext.loc['Units', ['PFA', 'SA_1.13']] = 'g'
    demand_sample_ext.loc['Units',['PID', 'RID']] = 'rad'

    PAL.demand.load_sample(demand_sample_ext)

    #############################

    # prepare demand input
    raw_demands = convert_to_MultiIndex(pelicundf, axis=0)
    raw_demands.index.names = ['stripe','type','loc','dir']

    # prepare the demand input for pelicun
    stripe_demands = raw_demands.loc[stripe,:]

    # units - - - - - - - - - - - - - - - - - - - - - - - -  
    stripe_demands.insert(0, 'Units',"")
    stripe_demands.loc['PFA','Units'] = 'g'
    stripe_demands.loc['PID','Units'] = 'rad'

    # distribution family  - - - - - - - - - - - - - - - - -  
    stripe_demands.insert(1, 'Family',"")
    stripe_demands['Family'] = 'lognormal'

    # distribution parameters  - - - - - - - - - - - - - - -
    stripe_demands.rename(columns = {'median': 'Theta_0'}, inplace=True)
    stripe_demands.rename(columns = {'log_std': 'Theta_1'}, inplace=True)

    # prepare a correlation matrix that represents perfect correlation
    ndims = stripe_demands.shape[0]
    demand_types = stripe_demands.index 

    perfect_CORR = pd.DataFrame(
        np.ones((ndims, ndims)),
        columns = demand_types,
        index = demand_types)

    # prepare additional fragility and consequence data ahead of time
    cmp_marginals = pd.read_csv('CMP_marginals.csv', index_col=0)

    # add missing data to P58 damage model
    P58_data = PAL.get_default_data('fragility_DB_FEMA_P58_2nd')
    cmp_list = cmp_marginals.index.unique().values[:-3]

    # now take those components that are incomplete, and add the missing information
    additional_fragility_db = P58_data.loc[cmp_list,:].loc[P58_data.loc[cmp_list,'Incomplete'] == 1].sort_index()

    # D2022.013a, 023a, 023b - Heating, hot water piping and bracing
    # dispersion values are missing, we use 0.5
    additional_fragility_db.loc[['D.20.22.013a','D.20.22.023a','D.20.22.023b'],
                                [('LS1','Theta_1'),('LS2','Theta_1')]] = 0.5

    # D2031.013b - Sanitary Waste piping
    # dispersion values are missing, we use 0.5
    additional_fragility_db.loc['D.20.31.013b',('LS1','Theta_1')] = 0.5

    # D2061.013b - Steam piping
    # dispersion values are missing, we use 0.5
    additional_fragility_db.loc['D.20.61.013b',('LS1','Theta_1')] = 0.5

    # D3031.013i - Chiller
    # use a placeholder of 3.0|0.5
    additional_fragility_db.loc['D.30.31.013i',('LS1','Theta_0')] = 3.0
    additional_fragility_db.loc['D.30.31.013i',('LS1','Theta_1')] = 0.5

    # D3031.023i - Cooling Tower
    # use a placeholder of 3.0|0.5
    additional_fragility_db.loc['D.30.31.023i',('LS1','Theta_0')] = 3.0
    additional_fragility_db.loc['D.30.31.023i',('LS1','Theta_1')] = 0.5

    # D3052.013i - Air Handling Unit
    # use a placeholder of 3.0|0.5
    additional_fragility_db.loc['D.30.52.013i',('LS1','Theta_0')] = 3.0
    additional_fragility_db.loc['D.30.52.013i',('LS1','Theta_1')] = 0.5

    # prepare the extra damage models for collapse and irreparable damage
    additional_fragility_db.loc[
        'excessiveRID', [('Demand','Directional'),
                        ('Demand','Offset'),
                        ('Demand','Type'), 
                        ('Demand','Unit')]] = [1, 0, 'Residual Interstory Drift Ratio', 'rad']   

    additional_fragility_db.loc[
        'excessiveRID', [('LS1','Family'),
                        ('LS1','Theta_0'),
                        ('LS1','Theta_1')]] = ['lognormal', 0.01, 0.3]   

    additional_fragility_db.loc[
        'irreparable', [('Demand','Directional'),
                        ('Demand','Offset'),
                        ('Demand','Type'), 
                        ('Demand','Unit')]] = [1, 0, 'Peak Spectral Acceleration|1.13', 'g']   

    additional_fragility_db.loc[
        'irreparable', ('LS1','Theta_0')] = 1e10

    additional_fragility_db.loc[
        'collapse', [('Demand','Directional'),
                    ('Demand','Offset'),
                    ('Demand','Type'), 
                    ('Demand','Unit')]] = [1, 0, 'Peak Spectral Acceleration|1.13', 'g']   

    additional_fragility_db.loc[
        'collapse', [('LS1','Family'),
                    ('LS1','Theta_0'),
                    ('LS1','Theta_1')]] = ['lognormal', 1.35, 0.5]  

    # Now we can set the incomplete flag to 0 for these components
    additional_fragility_db['Incomplete'] = 0

    # create the additional consequence models
    additional_consequences = pd.DataFrame(
        columns = pd.MultiIndex.from_tuples([
            ('Incomplete',''), ('Quantity','Unit'), ('DV', 'Unit'), ('DS1', 'Theta_0')]),
        index=pd.MultiIndex.from_tuples([
            ('replacement','Cost'), ('replacement','Time')])
    )

    additional_consequences.loc[('replacement', 'Cost')] = [0, '1 EA', 'USD_2011', 21600000]
    additional_consequences.loc[('replacement', 'Time')] = [0, '1 EA', 'worker_day', 12500]


    ################################
    # specify number of stories
    PAL.stories = nstory

    # load component definitions
    cmp_marginals = pd.read_csv('CMP_marginals.csv', index_col=0)
    PAL.asset.load_cmp_model({'marginals': cmp_marginals})

    # generate sample
    PAL.asset.generate_cmp_sample(sample_size)

    # load the models into pelicun
    PAL.damage.load_damage_model([
        additional_fragility_db,  # This is the extra fragility data we've just created
        'PelicunDefault/fragility_DB_FEMA_P58_2nd.csv' # and this is a table with the default P58 data    
    ])

    # prescribe the damage process
    dmg_process = {
        "1_collapse": {
            "DS1": "ALL_NA"
        },
        "2_excessiveRID": {
            "DS1": "irreparable_DS1"
        }
    }

    # calculate damages
    PAL.damage.calculate(dmg_process=dmg_process)

    #########################

    # create the loss map
    drivers = [f'DMG-{cmp}' for cmp in cmp_marginals.index.unique()]
    drivers = drivers[:-3]+drivers[-2:]

    loss_models = cmp_marginals.index.unique().tolist()[:-3] +['replacement',]*2

    loss_map = pd.DataFrame(loss_models, columns=['BldgRepair'], index=drivers)

    # load the loss model
    PAL.bldg_repair.load_model(
        [additional_consequences,
        "PelicunDefault/bldg_repair_DB_FEMA_P58_2nd.csv"], 
        loss_map)

    # perform the calculation
    PAL.bldg_repair.calculate()

    # get the aggregate losses
    agg_DF = PAL.bldg_repair.aggregate_losses()

    agg_DF.describe([0.1, 0.5, 0.9])

    return agg_DF





# Write a function for getting loss of a single building
def calculateLoss(building):

    # Get path to building folder
    buildingFolder = Path(baseDirectory,"Outputs",str(building.ID))

    # Get the EDPs for building based on LFRS type
    if building.lfrs == "steelmf":
        folderNames = ["PeakFloorAcceleration.csv","PeakStoryDrift.csv","ResidualDrift.csv"]
        numstories = pd.read_csv(Path(buildingFolder,"Geometry.csv"))["number of story"][0].item()


    elif building.lfrs == "woodframe":
        folderNames = ["PFA.csv","SDR.csv","RDR.csv"]
        numstories = pd.read_csv(Path(baseDirectory,"BuildingInfo",str(building.ID),"Geometry","numberOfStories.txt"))[0].item()
    
    elif building.lfrs == "rcwall":
        folderNames = []
        numstories = pd.read_csv(Path(baseDirectory,"BuildingInfo","Building_" + str(building.ID) + ".csv"))["number of story"][0].item()

    # Get EDPs
    pfa = pd.read_csv(Path(buildingFolder,folderNames[0]), header=None)
    sdr = pd.read_csv(Path(buildingFolder,folderNames[1]), header=None)
    rdr = pd.read_csv(Path(buildingFolder,folderNames[2]), header=None)

    # Preprocess data for pelicun
    pelicundf = preprocessPelicun(pfa,sdr)
    
    # Calculate losses
    losses = performAssessment(pelicundf,numstories)

    return losses

