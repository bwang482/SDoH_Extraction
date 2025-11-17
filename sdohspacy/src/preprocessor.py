"""
Clinical Text Preprocessor - Simple Template.
Handles questionnaires, lists, and other structured text formats.
"""

import re


class ClinicalTextPreprocessor:
    """
    Preprocessor template for clinical text.
    
    Usage:
        preprocessor = ClinicalTextPreprocessor()
        clean_text = preprocessor.preprocess(raw_text)
    """

    def __init__(self):
        """Initialize the preprocessor."""
        # Store your preprocessing patterns here
        self.rules = []
        self._initialize_rules()

    def _initialize_rules(self):
        """
        Initialize your preprocessing rules.
        
        This method is intentionally empty - add your own rules
        based on your data and requirements.
        
        Example structure (uncomment and modify):
        
        self.rules.append({
            'name': 'rule_name',
            'pattern': re.compile(r'your_pattern'),
            'replacement': 'your_replacement'
        })
        """
        # Example: Format question-answer pairs
        # Clinical questionnaires often have Q&A patterns that need cleaning
        # This example handles simple yes/no responses
        self.add_rule(
            name='format_simple_qa',
            pattern=r'(\?|:|\?:|\? :)\s+(Yes|No|Y|N)\b',
            replacement=r': \2'
        )

    def preprocess(self, text):
        """
        Main preprocessing function for clinical text.
        
        Args:
            text: Raw clinical note text.
            
        Returns:
            Preprocessed text.
        """
        if not text:
            return ""
        
        for rule in self.rules:
            if 'pattern' in rule and 'replacement' in rule:
                processed_text = rule['pattern'].sub(
                    rule['replacement'], 
                    text
                )
            elif 'function' in rule:
                processed_text = rule['function'](processed_text)
        
        return processed_text
    
    def add_rule(self, name: str, pattern: str, replacement: str):
        """
        Add a preprocessing rule.
        
        Args:
            name: Rule identifier
            pattern: Regex pattern
            replacement: Replacement string
        """
        self.rules.append({
            'name': name,
            'pattern': re.compile(pattern),
            'replacement': replacement
        })
    
    def add_function_rule(self, name: str, function):
        """
        Add a custom function as a preprocessing rule.
        
        Args:
            name: Rule identifier
            function: Function that takes and returns a string

        Example:
            def custom_cleaner(text):
                # Your custom logic here
                return text.replace('  ', ' ')
            
            preprocessor.add_function_rule('custom_clean', custom_cleaner)
        """
        self.rules.append({
            'name': name,
            'function': function
        })

    def remove_rule(self, name: str):
        """Remove a rule by name."""
        self.rules = [r for r in self.rules if r.get('name') != name]
    
    def list_rules(self):
        """List all active rules."""
        for rule in self.rules:
            print(f"- {rule.get('name', 'unnamed')}")


