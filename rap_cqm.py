# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, Binary
import numpy as np

def get_token():
    '''Returns personal access token. Only required if submitting to autograder.'''
    
    return 'Z209-1503c4d4535589d031a8a15337373b4657a620b5'

def get_cqm(n_max, n_min, Rs, C, cs):
    """Returns a dictionary representing a QUBO.

    Args:
        n_max(integer): maximum number of components
    """

    ln_Rs = ln(Rs)
    bs_name, bs_weight = bin(n_max, len(cs))
    F_weight = update_weight(bs_weight, ln_Rs, n_max)
    C_weight = update_weight(bs_weight, cs, n_max)
    
    cqm = ConstrainedQuadraticModel()
    length = len(bs_name)
    
    # equation 10
    cqm.set_objective(sum(bs_name[i]*F_weight[i] for i in range(length)))
    
    # equation 11
    cqm.add_constraint(sum(bs_name[i]*C_weight[i] for i in range(length)) <= C, label = 'budget_limitation')

    # equation 12
    cqm.add_constraint(sum(bs_name[i]*bs_weight[i] for i in range(length)) <= n_max, label = 'upper_limit')
    cqm.add_constraint(sum(bs_name[i]*bs_weight[i] for i in range(length)) >= n_min, label = 'bound_limit')
    
    return cqm

def ln(Rs):
    """Returns a list with Ln(1 - R_k).

    Args:
        Rs(integer list): reability list of k-components
    """

    aux = [1-x for x in Rs]
    return list(np.log(aux))
	
def bin(max, n):
    """Returns two list with variable names and binary weight.

    Args:
        max(integer): maximum number of components
	n(integer): number of types of components
	
    Example:
        max = 2 means that 2 bits are necessary to represents (00, 01 and 10)
        n = 2 means that 2 types of components are allowed
                
        The list will be:
	name = ['b_0,1', 'b_1,1', 'b_0,2', 'b_1,2']
	weight = [1, 2, 1, 2]

    """

    name = list()
    weight = list()
    
    # how many bits are necessary to represent max
    bits = max.bit_length()
    

    for k in range(n):
        for i in range(bits):
            name.append(Binary(f"b_{i},{k+1}"))
            weight.append(2**i)
	
    return (name, weight)

def update_weight(weight, factor, max):
    """Returns a list where weight[i]*factor[i//bits of max].

    Args:
        weight(integer list): reability list of k-components
        factor(float list): values to update weight list
	max(integer): maximum number of components
    """

    new_weight = list()
    bits = max.bit_length()
    
    for i, w in enumerate(weight):
        new_weight.append(w*factor[i//bits])

    return new_weight

def run_on_qpu(cqm, sampler):
    """Runs the BQM on the sampler provided.

    Args:
        bqm (BinaryQuadraticModel): a BQM for the problem;
        sampler (dimod.Sampler): a sampler that uses the QPU
    """

    sample_set = sampler.sample_cqm(cqm,label='RAP')

    return sample_set

## ------- Main program -------
if __name__ == "__main__":

    cs = [3,2]
    Rs = [0.98, 0.95]
    n_min = 0
    n_max = 2
    C = 5
    
    cqm = get_cqm(n_max, n_min, Rs, C, cs)
    #print(cqm)
    #TODO:  Write code to define your sampler
    cqm_sampler = LeapHybridCQMSampler()

    #TODO:  Write code to run your problem
    result = run_on_qpu(cqm, cqm_sampler)


    #TODO:  Write code to look at the solutions returned
    print(result)
