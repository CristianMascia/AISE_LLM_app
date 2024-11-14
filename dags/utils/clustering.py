import os
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)


model_params = {
    'eps': 0.3,
    'min_samples': 10,
}


class Clusterer:
    def __init__(self, file_name: str, model_params: dict = model_params) -> None:
        self.model_params = model_params
        self.file_name = file_name

    def cluster_and_label(self, features: list) -> None:
        df = pd.read_json(os.path.join('./data/source', self.file_name))
        df_features = df[features]
        df_features = StandardScaler().fit_transform(df_features)
        db = DBSCAN(**self.model_params).fit(df_features)

        # Find labels from the clustering
        core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        core_samples_mask[db.core_sample_indices_] = True
        labels = db.labels_

        # Add labels to the dataset and return.
        df['label'] = labels
        df.to_json(path_or_buf=os.path.join('./data/cdata/',
                                            self.file_name), orient='records')
