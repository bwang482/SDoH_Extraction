"""
NLP Matcher module for SDoH entity extraction using MedSpaCy.
"""

import logging
logger = logging.getLogger("medspacy")
logger.setLevel(logging.ERROR)
import spacy
from spacy.tokens import Doc, Span
from medspacy.custom_tokenizer import create_medspacy_tokenizer
from medspacy.postprocess import Postprocessor, PostprocessingRule, PostprocessingPattern
from medspacy.postprocess import postprocessing_functions

from preprocessor import ClinicalTextPreprocessor


class NLPMatcher:
    """
    Identifies predefined SDoH terms in clinical notes using MedSpaCy.

    Tokenization -> Sentence splitting -> Section recognition -> Note preprocessing
                                                                        |
                                                                        V
    Returns entities <- Postprocessing <- Context recognition <- Entity matching
    """
    def __init__(self, target_rules, max_len, sentencizer="pysbd"):
        """
        Initialize the NLP matcher with MedSpaCy pipeline.

        args: 
            target_rules: MedSpaCy target rules with query terms.
            max_len: Maximum number of chars allowed per note.
            sentencizer: Sentence splitter to use ("pysbd" or "pyrush")
        """
        self.nlp = spacy.blank("en")
        self.nlp.max_length = max_len
        self.preprocessor = ClinicalTextPreprocessor()

        # Tokenization
        self.nlp.tokenizer = create_medspacy_tokenizer(self.nlp)

        # Sentence splitting using pysbd or pyrush
        if sentencizer == "pysbd":
            self.nlp.add_pipe('medspacy_pysbd')
        elif sentencizer == "pyrush":
            self.nlp.add_pipe('medspacy_pyrush', config={"pyrush_path": "../resources/rush_rules.tsv"})
        else:
            raise ValueError(f"Invalid sentencizer: {sentencizer}")
        
        # Section recognition (uses "section_pattern_updated.json")
        self.nlp.add_pipe("medspacy_sectionizer", config={"rules": '../resources/section_pattern_updated.json'})

        # Entity matching
        self.nlp.add_pipe('medspacy_target_matcher')
        target_matcher = self.nlp.get_pipe("medspacy_target_matcher")
        target_matcher.add(target_rules)

        # Context recognition (uses "context_rules_updated.json")
        # ConText algorithm: https://www.sciencedirect.com/science/article/pii/S1532046409000744
        context = self.nlp.add_pipe(
            "medspacy_context", 
            config={"rules": "../resources/context_rules_updated.json",}                         
        )

        # Postprocessing - remove entities from irrelevant sections
        postprocessor = self.nlp.add_pipe("medspacy_postprocessor", config={"debug": False})
        postprocess_rules = [
            PostprocessingRule(
                patterns=[
                    PostprocessingPattern(condition=lambda ent: ent._.section_category == "observation_and_plan"),
                ],
                action=postprocessing_functions.remove_ent,
                description="Remove any entities from the assessment and plan section."
            ),

            PostprocessingRule(
                patterns=[
                    PostprocessingPattern(condition=lambda ent: ent._.section_category == "patient_instructions"),
                ],
                action=postprocessing_functions.remove_ent,
                description="Remove any entities from the instructions sections."
            ),
            
        ]
        postprocessor.add(postprocess_rules)

    def match(self, text):
        """
        Process clinical text and return identified entities.

        Args:
            text: Clinical note text
            
        Returns:
            List of extracted entities and metadata
        """
        # Preprocess text
        processed_text = self.preprocessor.preprocess(text)

        # Process with SpaCy pipeline
        doc = self.nlp(processed_text)

        # Extract entities with attributes
        seen_keys = set()
        unique_entities = []
        for idx, ent in enumerate(doc.ents):

            # Custom filtering -  based on your specific data and requirements
            # See _apply_custom_filters() for current rules, add new filters as needed
            if not self._apply_custom_filters(ent):
                continue
            
            # Create entity dictionary
            matched_entity = {
                "id": idx,
                "entity": ent.text, 
                "target_rule": ent._.target_rule.literal,
                "category": ent.label_,
                "sub-category": ent._.sub_category,
                "sent": ent.sent.text.strip(),
                "start_char": ent.start_char,
                "end_char": ent.sent.end_char,
                "text_segment": doc.text[ent.start_char-150:ent.end_char+150],
                "is_negated": ent._.is_negated,
                "is_family": ent._.is_family,
                "is_historical": ent._.is_historical,
                "is_uncertain": ent._.is_uncertain,
                "is_hypothetical": ent._.is_hypothetical,
            }
            
            key = (matched_entity['entity'], matched_entity['category'], matched_entity['sent'])

            # Add only if not seen before
            if key not in seen_keys:
                seen_keys.add(key)
                unique_entities.append(matched_entity)
        
        return unique_entities

    @staticmethod
    def _include_ent(ent):
        """ 
        Determine if an entity should be included based on context and rules.

        Args:
            ent: SpaCy Span object representing the entity
            
        Returns:
            True if entity should be included, False otherwise
        """
        if ent._.is_negated:
            return False
        if ent._.is_uncertain:
            return False
        if ent._.is_family:
            return False
        if ent._.is_historical:
            return False
        if ent._.is_hypothetical:
            return False
        return True

    @staticmethod
    def _apply_custom_filters(ent):
        """Apply custom filtering rules to an entity."""
        ent_text = ent.text.lower()
        sent_text = " ".join(ent.sent.text.lower().strip().split())

        # Example filter - expand these filters based on your specific data and requirements.
        if (ent_text == "shelter") and ("animal shelter" in sent_text):
            return False
        else:
            return True
        

