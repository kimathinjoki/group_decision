from flask import Flask, request, jsonify
import numpy as np
import os

from ast import Assign
from urllib import response
import numpyro
import pandas as pd
import numpy as np
import argparse
import pickle
import time
import jax.numpy as jnp
from jax import random, vmap
from jax.scipy.special import logit
from numpyro.distributions import Gamma, Beta, Normal, Categorical
from numpyro.distributions.transforms import StickBreakingTransform
from numpyro.infer import MCMC, NUTS, DiscreteHMCGibbs
from scipy.special import logit, expit
from scipy import stats
from math import sqrt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)

@app.route('/group_decision', methods=['POST'])


def group_decision():
    # data = request.get_json()

    # results = {}

    # for column, values in data.items():
    #     num_val = [float(i) for i in values if isinstance(i, (int, float))]
    #     if num_val:
    #         avg = np.mean(num_val)
    #         results[column] = f"{avg:.6f}"
    # return jsonify(results)
     # test_excel = pd.read_excel('test_excel.xlsx')
    data = request.get_json()
    df = pd.DataFrame(data)
    stacked = df.stack().reset_index()
    
    stacked.columns = ['Row', 'Column', 'Value']
    result = stacked.apply(lambda x: [x['Row'], df.columns.get_loc(x['Column']), x['Value']], axis=1).tolist()

    # Convert list to numpy array
    response_matrix = np.array(result, dtype=float)
    response_matrix[response_matrix[:, 2] == 10, 2] = 9.99
    response_matrix[response_matrix[:, 2] == 0, 2] = 0.01



    # Model
    def model():
        # no_cultures = 3
        # alpha = numpyro.sample('alpha', Gamma(1, 1))
        # with numpyro.plate('weights', no_cultures - 1):
        #     v = numpyro.sample('v', Beta(1, alpha))
            
        # with numpyro.plate('ind', participants):
        #     sb_trans = StickBreakingTransform()
        #     culture_id = numpyro.sample("culture_id", Categorical(sb_trans(v)))
            
        # with numpyro.plate("data_loop", participants):
        #     culture_assignment = culture_id[features[:, 0]]
            
        # with numpyro.plate('parameters', no_cultures):
        competence_mean = numpyro.sample('competence_mean', Normal(0, 4))
        competence_precision = numpyro.sample('competence_precision', Gamma(0.01, 0.01))
        scale_prior_precision = numpyro.sample("scale_prior_precision", Gamma(0.01, 0.01))
        bias_prior_variance = numpyro.sample("bias_prior_variance", Gamma(0.01, 0.01))
        consensus_mean = numpyro.sample('consensus_mean', Normal(0, 4))
        consensus_precision = numpyro.sample('consensus_precision', Gamma(0.01, 0.01))
        itemDiff_precision = numpyro.sample('itemDiff_precision', Gamma(0.01, 0.01))
        with numpyro.plate('culture_ind', participants):
            LogCompetence = numpyro.sample('LogCompetence', Normal(competence_mean, 1/competence_precision))
            bias = numpyro.sample('bias', Normal(0, 1/bias_prior_variance))
            LogScale = numpyro.sample('LogScale', Normal(0, 1/scale_prior_precision))
        with numpyro.plate('stimplate', stimuli):
            consensus = numpyro.sample('consensus', Normal(consensus_mean, 1/consensus_precision))
            itemDiff = numpyro.sample('itemDiff', Normal(0, 1/itemDiff_precision))
        competence = jnp.exp(LogCompetence[features[:, 0]])    
        scale = jnp.exp(LogScale[features[:, 0]])
        item_difficulty = jnp.exp(itemDiff[features[:, 1]])
        ratingMu = vmap(lambda scale, cons, bias: scale * cons + bias)(scale, consensus[features[:, 1]], bias[features[:, 0]])
        ratingVariance = (scale * competence * item_difficulty)**2
        
        numpyro.sample("rating", Normal(ratingMu, ratingVariance), obs=rates)

    # Data features
    features, rates = response_matrix[:, :].astype(int), logit(response_matrix[:, 2].astype(float)/10)
    participants = len(jnp.unique(response_matrix[:, 0]))
    stimuli = len(jnp.unique(response_matrix[:, 1]))
    rng_key, rng_key_predict = random.split(random.PRNGKey(0))

    # Model specifications
    kernel = NUTS(model, target_accept_prob = 0.80, max_tree_depth=6)
    mcmc = MCMC(
        kernel,
        num_warmup= 1000,
        num_samples= 1000,
        num_chains= 1,
        chain_method= "sequential",
        progress_bar=True
    )
    # Run the model
    mcmc.run(rng_key)

    # Get the results
    diagnos = numpyro.diagnostics.summary(mcmc.get_samples(group_by_chain=True))
    # with open('intervention-test.pickle', 'wb') as handle:
    #     pickle.dump(diagnos, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    
    # Save cultural assignment
    samples = mcmc.get_samples()
    # np.save('cultural_assignments.npy', samples['culture_id'])
    # culture_assignment = np.load('cultural_assignments.npy')
    # mode_culture_assignment = culture_assignment
    # mode_cultures = stats.mode(mode_culture_assignment)
    # assigment_mode_culture = mode_cultures[0][0]
    # assigment_mode_culture includes cultural assignments that matches with participant id index from 0....N. 
    # print(assigment_mode_culture)

    # with open('intervention-test.pickle', 'rb') as handle:
    #     posterior_inference = pickle.load(handle)
        
    consensus = expit(samples['consensus']['mean'])
    # Candidate 1 corresponds to consensus[0], Candidate 2 corresponds to consensus[1]
    print(consensus)
    
    return jsonify({'consensus': consensus.tolist()})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
