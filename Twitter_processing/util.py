import json
import re

alcohol_tokens = "alcohol|drinking|drunk|beer|wine|liquor|cocktail|pub|bar|nightclub|spirit|brewery|distillery|shot|alcoholism"
alcohol_tags = "alcohol|drinkresponsibly|beeroclock|winelover|drinkup|pubcrawl|heineken|budweiser|jackdaniels|absolutvodka|wine|beerlover|drinkspecials|drinkoftheday|cocktailhour|mixology|craftbeer|winetime|bartenderlife|happyhour|booze|tequila|rum|whiskey|gin"
crash_tokens = "crash|accident|wreckage|rollover|pileup|fender-bender"
crash_tags = "carcrash|trafficaccident|driving|drivesafe|roadaccident|carcollision|trafficsafety|crashscene|drivingtips|insurance|accidentreport|vehicledamage"
crime_tokens = "crime|police|justice|arrest|suspect|victim|offender|robbery|theft|burglary|assault|homicide|prison|parole|probation|court"
crime_tags = "crime|policebrutality|justiceforvictims|lawenforcement|criminaljustice|prisonreform|crimestoppers"

def preprocess_data(line):
    if line.startswith('{'):
        if line.endswith('},\n'):
            return line[:-2]
        elif line.endswith('}\n'):
            return line[:-1]
    print("invalid line:", line, end="")
    return None

def read_data_line_by_line(path):
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line

def read_num_of_lines(path):
    with open(path, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        first_line = first_line[:-10] + "}"
        first_line = json.loads(first_line)
        return first_line["total_rows"] - first_line["offset"]

def process_tokens(tokens):
    labels = []
    alcohol_keywords = re.compile(r'({0})'.format(alcohol_tokens))
    crash_keywords = re.compile(r'({0})'.format(crash_tokens))
    crime_keywords = re.compile(r'({0})'.format(crime_tokens))
    if alcohol_keywords.search(tokens.lower()):
        labels.append("alcohol")
    if crime_keywords.search(tokens.lower()):
        labels.append("crime")
    if crash_keywords.search(tokens.lower()):
        labels.append("crash")
    return labels

def process_tags(tags):
    labels = []
    alcohol_keywords = re.compile(r'({0})'.format(alcohol_tags))
    crash_keywords = re.compile(r'({0})'.format(crash_tags))
    crime_keywords = re.compile(r'({0})'.format(crime_tags))
    if alcohol_keywords.search(tags.lower()):
        labels.append("alcohol")
    if crime_keywords.search(tags.lower()):
        labels.append("crime")
    if crash_keywords.search(tags.lower()):
        labels.append("crash")
    return labels

