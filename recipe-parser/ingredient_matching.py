import json
import csv
import difflib
import re
import pprint

class IngredientMatcher():

  def __init__(self, usda_reduced_nouns_file, ingredients):
    pp = pprint.PrettyPrinter(indent=2)
    reg = re.compile(r"[\w']+")
    if usda_reduced_nouns_file != "":
      self.usda_db = IngredientMatcher.load_usda(usda_reduced_nouns_file)
    self.ingredients = ingredients
    self.ratios_NLP = {}
    self.ratios = {}
    self.usda_split_dict = IngredientMatcher.get_split_names(self.usda_db, False)
    self.usda_split_dict_NLP = IngredientMatcher.get_split_names(self.usda_db, True)
    self.ingredients_split = dict((ing_name,reg.findall(ing_name.lower())) for ing_name in ingredients)
    self.methods = {}
    for ing_name, ing_split in self.ingredients_split.iteritems():
      self.ratios_NLP[ing_name] = IngredientMatcher.get_ratios(ing_split, self.usda_split_dict_NLP)
      self.ratios[ing_name] = IngredientMatcher.get_ratios(ing_split, self.usda_split_dict)
      self.methods[ing_name] = {}
    for ing_name, ing_split in self.ingredients_split.iteritems():
      self.methods[ing_name]["get_bests_NLP"] = IngredientMatcher.get_bests(self.ratios_NLP[ing_name])
      self.methods[ing_name]["get_bests"] = IngredientMatcher.get_bests(self.ratios[ing_name])
      self.methods[ing_name]["get_averages_NLP"] = IngredientMatcher.get_averages(self.ratios_NLP[ing_name])
      self.methods[ing_name]["get_averages"] = IngredientMatcher.get_averages(self.ratios[ing_name])
      self.methods[ing_name]["get_bests_above_threshold_NLP"] = IngredientMatcher.get_bests_above_threshold(self.ratios_NLP[ing_name], 0.9)
      self.methods[ing_name]["get_bests_above_threshold"] = IngredientMatcher.get_bests_above_threshold(self.ratios[ing_name], 0.9)
      self.methods[ing_name]["get_averages_above_threshold_NLP"] = IngredientMatcher.get_averages_above_threshold(self.ratios_NLP[ing_name], 0.8)
      self.methods[ing_name]["get_averages_above_threshold"] = IngredientMatcher.get_averages_above_threshold(self.ratios[ing_name], 0.8)
      self.methods[ing_name]["get_weighted_bests_NLP"] = IngredientMatcher.get_weighted_bests(self.ratios_NLP[ing_name])
      self.methods[ing_name]["get_weighted_bests"] = IngredientMatcher.get_weighted_bests(self.ratios[ing_name])
      self.methods[ing_name]["get_weighted_averages_NLP"] = IngredientMatcher.get_weighted_averages(self.ratios_NLP[ing_name])
      self.methods[ing_name]["get_weighted_averages"] = IngredientMatcher.get_weighted_averages(self.ratios[ing_name])
      self.methods[ing_name]["get_weighted_bests_above_threshold_NLP"] = IngredientMatcher.get_weighted_bests_above_threshold(self.ratios_NLP[ing_name], 0.9)
      self.methods[ing_name]["get_weighted_bests_above_threshold"] = IngredientMatcher.get_weighted_bests_above_threshold(self.ratios[ing_name], 0.9)
      self.methods[ing_name]["get_weighted_averages_above_threshold_NLP"] = IngredientMatcher.get_weighted_averages_above_threshold(self.ratios_NLP[ing_name], 0.7)
      self.methods[ing_name]["get_weighted_averages_above_threshold"] = IngredientMatcher.get_weighted_averages_above_threshold(self.ratios[ing_name], 0.7)
    with open('match_results.json', 'wb+') as f:
      for ing_name, method_dict in self.methods.iteritems():
        f.write(json.dumps({ing_name:method_dict})+'\n')

  @staticmethod
  def load_usda(filename):
    usda = []
    with open(filename) as f:
      for line in f:
        usda.append(json.loads(line))
    return usda

  @staticmethod
  def get_split_names(usda_db, nlp=True):
    reg = re.compile(r"[\w']+")
    split_dict = {}
    for ingredient in usda_db:
      usda_name = ingredient["name"]["long"].lower()
      usda_reg = reg.findall(usda_name)
      usda_split = []
      if nlp:
        usda_split = [word for word in usda_reg if word in ingredient["name"]["split"]]
      if usda_split == []:
        usda_split = reg.findall(usda_name)
      split_dict[usda_name] = usda_split
    return split_dict

  @staticmethod
  def get_ratios(ing_split, usda_split_dict):
    ratios = {}
    i = 0.
    for usda_name, usda_split in usda_split_dict.iteritems():
      ratio_list = [((ing_word, usda_word), difflib.SequenceMatcher(None, ing_word, usda_word).ratio()) \
                    for usda_word in usda_split for ing_word in ing_split]
      ratios[usda_name] = {key: value for (key, value) in ratio_list}
      if i%500==0: print i/len(usda_split_dict)
      i+=1
    return ratios

  @staticmethod
  def get_max_ratio_per_usda_word(ratio_dict):
    max_ratio_per_usda_word = {}
    for (ing_word, usda_word),ratio in ratio_dict.iteritems():
      if usda_word in max_ratio_per_usda_word:
        if ratio > max_ratio_per_usda_word[usda_word]:
          max_ratio_per_usda_word[usda_word] = ratio
      else:
        max_ratio_per_usda_word[usda_word] = ratio
    return max_ratio_per_usda_word

  @staticmethod
  def get_weighted_max_ratio_per_usda_word(ratio_dict, usda_name):
    weighted_max_ratio_per_usda_word = {}
    reg = re.compile(r"[\w']+")
    usda_split = reg.findall(usda_name)
    for (ing_word, usda_word),ratio in ratio_dict.iteritems():
      weighted_ratio = ratio/(usda_split.index(usda_word)+1)
      if usda_word in weighted_max_ratio_per_usda_word:
        if weighted_ratio > weighted_max_ratio_per_usda_word[usda_word]:
          weighted_max_ratio_per_usda_word[usda_word] = weighted_ratio
      else:
        weighted_max_ratio_per_usda_word[usda_word] = weighted_ratio
    return weighted_max_ratio_per_usda_word

  @staticmethod
  def get_bests(ratios):
    matches = (0,[])
    for usda_name, ratio_dict in ratios.iteritems():
      m = max(ratio_dict.values())
      if m > matches[0]:
        matches = (m, [usda_name])
      elif m == matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_averages(ratios):
    matches = (0,[])
    for usda_name, ratio_dict in ratios.iteritems():
      max_ratio_per_usda_word = IngredientMatcher.get_max_ratio_per_usda_word(ratio_dict)
      average = sum(max_ratio_per_usda_word.values())/len(max_ratio_per_usda_word)
      if average > matches[0]:
        matches = (average, [usda_name])
      elif average == matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_bests_above_threshold(ratios, threshold):
    matches = (threshold,[])
    for usda_name, ratio_dict in ratios.iteritems():
      m = max(ratio_dict.values())
      if m >= matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_averages_above_threshold(ratios, threshold):
    matches = (threshold,[])
    for usda_name, ratio_dict in ratios.iteritems():
      max_ratio_per_usda_word = IngredientMatcher.get_max_ratio_per_usda_word(ratio_dict)
      average = sum(max_ratio_per_usda_word.values())/len(max_ratio_per_usda_word)
      if average >= matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_weighted_bests(ratios):
    matches = (0,[])
    for usda_name, ratio_dict in ratios.iteritems():
      weighted_max_ratio_per_usda_word = IngredientMatcher.get_weighted_max_ratio_per_usda_word(ratio_dict, usda_name)
      m = max(weighted_max_ratio_per_usda_word.values())
      if m > matches[0]:
        matches = (m, [usda_name])
      elif m == matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_weighted_averages(ratios):
    matches = (0,[])
    for usda_name, ratio_dict in ratios.iteritems():
      weighted_max_ratio_per_usda_word = IngredientMatcher.get_weighted_max_ratio_per_usda_word(ratio_dict, usda_name)
      average = sum(weighted_max_ratio_per_usda_word.values())/len(weighted_max_ratio_per_usda_word)
      if average > matches[0]:
        matches = (average, [usda_name])
      elif average == matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_weighted_bests_above_threshold(ratios, threshold):
    matches = (threshold,[])
    for usda_name, ratio_dict in ratios.iteritems():
      weighted_max_ratio_per_usda_word = IngredientMatcher.get_weighted_max_ratio_per_usda_word(ratio_dict, usda_name)
      m = max(weighted_max_ratio_per_usda_word.values())
      if m >= matches[0]:
        matches[1].append(usda_name)
    return matches

  @staticmethod
  def get_weighted_averages_above_threshold(ratios, threshold):
    matches = (threshold,[])
    for usda_name, ratio_dict in ratios.iteritems():
      weighted_max_ratio_per_usda_word = IngredientMatcher.get_weighted_max_ratio_per_usda_word(ratio_dict, usda_name)
      average = sum(weighted_max_ratio_per_usda_word.values())/len(weighted_max_ratio_per_usda_word)
      if average >= matches[0]:
        matches[1].append(usda_name)
    return matches

def main():
  ingredients = []
  names = {"large flour tortillas":"tortillas, ready-to-bake or -fry, flour, shelf stable","fresh lime juice":"lime juice, raw","small avocado, stone removed, peeled, mashed":"avocados, raw, all commercial varieties","coarsely grated vintage cheddar":"cheese, cheddar","baby spinach leaves":"spinach, raw","Greek-style feta, crumbled":"cheese, feta","smoked chicken breast fillet, thinly sliced":"chicken, broiler or fryers, breast, skinless, boneless, meat only, cooked, grilled"}
  im = IngredientMatcher("USDA-food-db/usda-reduced-nouns.json",names.keys())

if __name__=="__main__":
  main()

