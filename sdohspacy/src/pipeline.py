"""
The main pipeline run file.
"""

import logging
logging.captureWarnings(True)
import os
import time
import pandas as pd
from tqdm import tqdm
from loguru import logger
from datetime import datetime

from config import params
from utils import load_pickle
from nlp_matcher import NLPMatcher

from spacy.tokens import Span
Span.set_extension("sub_category", default="")


# Load SDoH terms as target rules
social_terms = load_pickle(os.path.join(params['rules_dir'], "social_terms.pk")) # 336 target rules
physical_terms = load_pickle(os.path.join(params['rules_dir'], "physical_terms.pk")) # 256 target rules
finance_terms = load_pickle(os.path.join(params['rules_dir'], "finance_terms.pk")) # 42 target rules
housing_terms = load_pickle(os.path.join(params['rules_dir'], "housing_terms.pk")) # 41 target rules
emp_terms = load_pickle(os.path.join(params['rules_dir'], "employment_terms.pk")) # 50 target rules
food_terms = load_pickle(os.path.join(params['rules_dir'], "food_terms.pk")) # 19 target rules
insur_terms = load_pickle(os.path.join(params['rules_dir'], "insurance_terms.pk")) # 23 target rules
all_terms = social_terms + physical_terms + finance_terms + housing_terms + emp_terms + food_terms + insur_terms


class SDoHExtractionPipeline:
    """
    Main pipeline for extracting SDoH entities from clinical notes.

    Important parameters: note types, data directory, output directory, output file name
    are in "config.py".
    
    args: 
        save_output: whether or not to save resulted dataframe.
    """
    def __init__(self, save_output=True):
        """ 
        Initializes the notes processing pipeline.
        """
        self.params = params
        self.output_path = os.path.join(self.params['output_dir'], self.params['output_fname'])
        
        # Create NLP matcher
        nlp_model = NLPMatcher(
            target_rules=all_terms, # setting which query terms to use
            max_len=3000000 # max number of chars per note = 3000000
        ) 
        self.results_df = self.apply_nlp(nlp_model)

        # SAVE RESULTING DATAFRAME
        if save_output:
            self.save_results()

    def apply_nlp(self, nlpmodel):
        """ 
        Process all note files in the input directory.

        Args: a NLP matcher model

        Returns: 
            Dataframe containing:
                - patient ID
                - Note ID
                - Note type
                - Note date
                - Extracted entities
                - Note text
        """
        results = []
        for filename in os.listdir(self.params['data_dir']):

            note_type = filename.split(".")[0][-3:]

            if filename.endswith(".csv") and (note_type in self.params['note_types']): # filter by note_types from config
                df = pd.read_csv(os.path.join(self.params['data_dir'], filename))

                logger.info(f"Processing notes from {filename}")
                for i, row in tqdm(df.iterrows(), total=df.shape[0]):
                    if "Lno" in filename:
                        note = row['comments']
                        note_id = row['record_id']
                        note_date = datetime.strptime(row['lmrnote_date'].split(" ")[0],"%m/%d/%Y")
                    else:
                        note = row['report_text']
                        note_id = row['report_number']
                        note_date = datetime.strptime(row['report_date_time'].split(" ")[0],"%m/%d/%Y")

                    # Apply NLP model
                    ents = nlpmodel.match(note)

                    # Only keep notes with entities
                    if ents:
                        results.append({
                            'empi': row['empi'],
                            'note_id': note_id,
                            'note_type': note_type,
                            'note_date': note_date,
                            'entities': ents,
                            'text': note
                        })
                    else: continue

        return pd.DataFrame(results)

    def save_results(self):
        """ 
        Saves resulting dataframe.
        """
        logger.info(f"Saving resulting dataframe")
        self.results_df.to_csv(self.output_path, index=False)
        logger.info(f"Results saved to {self.output_path}")


def main():
    t0 = time.time()
    SDoHExtractionPipeline(save_output=True)
    logger.info(f"Overall took {round((time.time()-t0)/60, 2)} mins")


if __name__ == "__main__":
    main()