# Function for preprocessing
def preprocess(doc: str, remove_ent=False):
    """_summary_

    Args:
        doc (str): String text
        remove_ent (bool, optional): If True, removes entities using spaCy. Defaults to False.
        remove_stop (bool, optional): If True, removes stopwords using adapted spaCy stopword list. Defaults to False.

    Returns:
        doc_preprocessed (list): Preprocessed lower-case corpus with punctuation, non-alphanumeric characters, spaCy stopwords and proper nouns removed.
    """
    
    if remove_ent == True:
        doc_no_ent = []
        ents = [e.text for e in doc.ents]
        for item in doc:
            if item.text in ents:
                pass
            else:
                doc_no_ent.append(item)

        doc_preprocessed = [token.lower_ for token in doc_no_ent if
                            # token is not punctuation
                            token.is_punct == False and
                            # token is alphanumeric character
                            token.is_alpha == True and
                            # token is not stop word
                            token.is_stop == False and
                            # token is not proper noun
                            token.pos_ != "PROPN"]
        
    else: # do not remove entities
        doc_preprocessed = [token.lower_ for token in doc if
                            # token is not punctuation
                            token.is_punct == False and
                            # token is alphanumeric character
                            token.is_alpha == True and
                            # token is not stop word
                            token.is_stop == False and
                            # token is not proper noun
                            token.pos_ != "PROPN"]

    return doc_preprocessed

    