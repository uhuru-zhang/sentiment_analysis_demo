import logging

import numpy as np
import pandas as pd
from pandas._libs import json
from torch.utils.data import Dataset
from collections import Counter


class TextDataSet(Dataset):

    def __init__(self, train=True, skiprows=0, nrows=None, usecols=None):
        csv_file = "trainingset/sentiment_analysis_trainingset.csv" if train else "validationset/sentiment_analysis_validationset.csv"

        self.texts = pd.read_csv(csv_file,
                                 skiprows=skiprows,
                                 nrows=nrows,
                                 header=0,
                                 dtype={"id": np.int, "content": np.str, "location_traffic_convenience": np.int,
                                        "location_distance_from_business_district": np.int,
                                        "location_easy_to_find": np.int, "service_wait_time": np.int,
                                        "service_waiters_attitude": np.int, "service_parking_convenience": np.int,
                                        "service_serving_speed": np.int, "price_level": np.int,
                                        "price_cost_effective": np.int, "price_discount": np.int,
                                        "environment_decoration": np.int, "environment_noise": np.int,
                                        "environment_space": np.int, "environment_cleaness": np.int,
                                        "dish_portion": np.int, "dish_taste": np.int, "dish_look": np.int,
                                        "dish_recommendation": np.int, "others_overall_experience": np.int,
                                        "others_willing_to_consume_again": np.int
                                        },
                                 index_col="id",
                                 usecols=usecols
                                 )
        logging.info("init done! {}".format(len(self.texts)))

    def __getitem__(self, index):
        return {i: self.texts.loc[index, :][i] for i in self.texts.loc[index, :].index}

    def __len__(self):
        return len(self.texts)


def generate_word_index():
    texts = pd.read_csv("trainingset/sentiment_analysis_trainingset.csv",
                        header=0,
                        dtype={"id": np.int, "content": np.str, "location_traffic_convenience": np.int,
                               "location_distance_from_business_district": np.int,
                               "location_easy_to_find": np.int, "service_wait_time": np.int,
                               "service_waiters_attitude": np.int, "service_parking_convenience": np.int,
                               "service_serving_speed": np.int, "price_level": np.int,
                               "price_cost_effective": np.int, "price_discount": np.int,
                               "environment_decoration": np.int, "environment_noise": np.int,
                               "environment_space": np.int, "environment_cleaness": np.int,
                               "dish_portion": np.int, "dish_taste": np.int, "dish_look": np.int,
                               "dish_recommendation": np.int, "others_overall_experience": np.int,
                               "others_willing_to_consume_again": np.int
                               },
                        index_col="id",
                        usecols=["id", "content"])

    contents = texts["content"]

    index = 1
    character_index_dict = {}
    character_counter_dict = {}

    for content in contents:
        for c in content:
            if c not in character_index_dict:
                character_index_dict[c] = index
                index += 1

            character_counter_dict[c] = character_index_dict.get(c, 0) + 1

    character_index_file = open("character_index_file.json", "w")
    character_counter_file = open("character_counter_file.json", "w")

    character_index_file.write(json.dumps(character_index_dict))
    character_index_file.flush()
    character_index_file.close()

    character_counter_file.write(json.dumps(character_counter_dict))
    character_counter_file.flush()
    character_counter_file.close()


if __name__ == '__main__':
    generate_word_index()
