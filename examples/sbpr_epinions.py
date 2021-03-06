# Copyright 2018 The Cornac Authors. All Rights Reserved.
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
# ============================================================================
"""Example for Social Bayesian Personalized Ranking (SBPR) with Epinions dataset"""

import cornac
from cornac.data import Reader, GraphModality
from cornac.datasets import epinions
from cornac.eval_methods import RatioSplit


# SBPR integrates user social network into Bayesian Personalized Ranking.
# The necessary data can be loaded as follows
feedback = epinions.load_feedback(
    Reader(bin_threshold=4.0)
)  # feedback is binarised (turned into implicit) using Reader.
trust = epinions.load_trust()

# Instantiate a GraphModality, it makes it convenient to work with graph (network) auxiliary information
# For more details, please refer to the tutorial on how to work with auxiliary data
user_graph_modality = GraphModality(data=trust)

# Define an evaluation method to split feedback into train and test sets
ratio_split = RatioSplit(
    data=feedback,
    test_size=0.1,
    rating_threshold=0.5,
    exclude_unknowns=True,
    verbose=True,
    user_graph=user_graph_modality,
)

# Instantiate SBPR model
sbpr = cornac.models.SBPR(
    k=10,
    max_iter=50,
    learning_rate=0.001,
    lambda_u=0.015,
    lambda_v=0.025,
    lambda_b=0.01,
    verbose=True,
)

# Use Recall@10 for evaluation
rec_10 = cornac.metrics.Recall(k=10)

# Put everything together into an experiment and run it
cornac.Experiment(eval_method=ratio_split, models=[sbpr], metrics=[rec_10]).run()
