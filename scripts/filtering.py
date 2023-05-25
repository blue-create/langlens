import pandas as pd
import re


def _exact_matches(text, keywords):
    """ function to check if text is an exact match to list of keywords
  the check is case insensitive and ignores preceding/  following whitespaces
  Parameters:
    - text (str): string that is checked
    - keywords (list of str): words that are searched for
  Returns:
    - boolean: returns False if either
        - there is no text, ie. text is NA
        - the text DOES NOT contain any of the words in keywords
  """
    if type(text) != str:
        return False

    text = text.lower().strip()
    return text in keywords


def _keyword_filter(text, keywords, first_words=False):
    """ function to check if keywords occur in a text, the check is case insensitive
  Parameters:
    - text (str/ list of str): text that is searched in
    - keywords (list of str): words that are searched for
  Returns:
    - boolean: returns True if any word occurs in text, False otherwise
  """
    if type(text) != str:
        if type(text) == list:
            text = " ".join(text)
        else:
            return False
    text = text.lower()
    text = re.sub("[/\\-!@#$%^&*:\".]", " ", text)
    if first_words:
        text = text.split()[:first_words]
        text = " ".join(text)
    for word in keywords:
        if len(re.findall(word, text)) > 0:
            return True
    return False


def filter_data(df: pd.DataFrame, column: str, keywords, exact_match=True, first_words=False):
    """ function to perform keyword search or exact match search to filter column of dataframe
    Parameters:
    - df (pd.DataFrame): dataframe in which a column is filtered
    - column (str): column name that by which is filtered
    - keywords (list of str): words that are searched for
    - exact_match (bool): if an exact match or keyword search is performed
    - first_words (int): False if the whole text is searched, number of first words that are looked at
    Returns:
    - df (pd.DataFrame): filtered dataframe
    """
    keywords = [keyword.lower().strip() for keyword in keywords]
    if exact_match:
        filtered_df = df[~df[column].apply(_exact_matches, args=[keywords])]
    else:
        filtered_df = df[~df[column].apply(_keyword_filter, args=[keywords, first_words])]
    print(filtered_df.shape)
    return filtered_df


def regex_filter(df: pd.DataFrame, column: str, phone=True, time=True, weekday=True, stats=True, streets=True,
                 link=True):
    filtered_df = df[~df[column].apply(_regex_search, args=[phone, time, weekday, stats, streets, link])]
    return filtered_df


def _regex_search(text: str, phone=True, time=True, weekday=True, stats=True, streets=True, link=True, email=True):
    phone_regex = '\(?\d{4,5}\)?[/\s]*\d{1,5}\s*\d{1,5}'
    if phone and len(re.findall(phone_regex, text)) > 0:
        return True

    time_regex = '\d{1,2}[:\/.]\d{1,2}[:\/.]\d{2,4}'
    hours_regex = "(\d{1,2}.\d{2}, \d{1})+"
    if time and ((len(re.findall(time_regex, text)) > 0) | (len(re.findall(hours_regex, text)) > 0)):
        return True

    weekday_regex = '(Mo|Di|Mi|Do|Fr|Sa|So)[-\\,s–\ ./]+((Mo|Di|Mi|Do|Fr|Sa|So)[-–./ ]+)?\d{1,2}'
    if weekday and len(re.findall(weekday_regex, text)) > 0:
        return True

    street_regex = "[\S]+(str|straße|weg| Str|allee|gasse| Gasse|platz| Straße| straße)[. ]+\d+"
    if streets and len(re.findall(street_regex, text)) > 0:
        return True

    link_regex = "(www\.)\S+\.\S+"
    if link and len(re.findall(link_regex, text)) > 0:
        return True

    stats_regex = "\d*([\.,]\d*)?[ ](Prozent|%)"
    stats_regex2 = "\d+ (Fälle|Opfer|Frauen|Kinder|Personen|Betroffene|Morde|Plätze)"
    if stats and ((len(re.findall(stats_regex, text)) > 0) | (len(re.findall(stats_regex2, text)) > 0)):
        return True
    email_regex = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    if email and len(re.findall(email_regex, text)) > 0:
        return True
    return False
