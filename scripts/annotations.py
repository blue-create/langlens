import numpy as np
import pandas as pd

def extract_annotations(test):
  ann_dict=dict()
  for ann in test:
    ### FOR NOW: later change to id
    name=ann["annotator"]["name"][0]
    # Remane old label names
    label=update_label(ann["concept"]["preferred_label"]["name"])
    if name in ann_dict.keys():
      ann_dict[name].append(label)
    else:
      ann_dict[name]=[label]
  #remove duplicates
  for key in ann_dict.keys():
    ann_dict[key]=set(ann_dict[key])
    ann_dict[key]=clean_annotation(ann_dict[key])
  return ann_dict


def update_label(label):
  if label=="NA":
    return "Domestic Violence"
  elif label=="Victim blaming":
    return 'Statement of responsibility'
  else:
    return label
  

def jaccard_similarity(sets):
# Calculate the intersection
    intersection = set.intersection(*sets)

    # Calculate the union
    union = set.union(*sets)

    # Compute the Jaccard similarity
    similarity = len(intersection) / len(union)

    return similarity

def calculate_similarity(annotations: dict, sim="jaccard"):
  #if no co-annotation
  if len(annotations)==1:
    return np.nan
  else:
    if sim=="jaccard":
      return jaccard_similarity(list(annotations.values()))
    elif sim=="dice":
      return dice_similarity_multiple(list(annotations.values()))
    
def dice_similarity_multiple(sets):
    num_sets = len(sets)
    similarity_sum = 0

    # Pairwise comparisons
    for i in range(num_sets - 1):
        for j in range(i + 1, num_sets):
            set1 = sets[i]
            set2 = sets[j]
            
            # Calculate the intersection
            intersection = set1.intersection(set2)
            
            # Calculate the sum of set sizes
            set_sum = len(set1) + len(set2)
            
            # Compute the Dice similarity coefficient
            similarity = 2 * len(intersection) / set_sum
            
            similarity_sum += similarity

    # Calculate the average similarity
    average_similarity = similarity_sum / (num_sets * (num_sets - 1) / 2)
    
    return average_similarity


def ground_truth_filter(entry, min_coannotation=1, min_similarity=0.5, similarity="jaccard"):
  """
      Extracts ground truth value of the annotated sample based on two filters:
      - a minimum number of people that annotated a text
      - a minimum of similarity between all annotations of a text

      Args:
      - annotations (dict): a dictionary containing all annotations of a text with the annotator initial as key
      - min_coannotation (int): minimum number of co-annotations of a text, by default 1, so all annotations are considered
      - min_similarity (int): if more than one annotator, the value minimum value of similarity so that a value is considered ground truth

      Returns:
      - either:
        - most_common (set): containing a set of the most common label(s) that are considered ground truth
        - NaN: if the annotation does not fulfill the conditions set for ground truth
  """
  if len(entry["annotations"])<min_coannotation or entry[similarity]<min_similarity:
    return np.nan
  else:
    all_values = [value for s in entry["annotations"].values() for value in s]
    most_common=pd.DataFrame(all_values).mode().values
    most_common=[i[0]for i in most_common]
    if len(most_common)>1 and "Domestic Violence" in most_common:
      most_common.remove("Domestic Violence")
    return set(most_common)
  

def clean_annotation(ann):
  # removes the label "domestic violence" if it has been chosen in combination with a second label
  if len(ann)>1:
    ann.discard("Domestic Violence")
  return ann