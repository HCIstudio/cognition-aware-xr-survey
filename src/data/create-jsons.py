import csv
import json
import argparse
import logging
import os

# properties without a filter or view
excludeProp = ["Name", "Authors", "Year", "DOI", "Bibtex"]

optionals = []

# categories that will be shown in the website
includeProp = {
  # fixed
  "Name":"String",
  "Authors": "MultiSelect",
  "Bibtex": "String",
  "DOI": "String",
  "Year": "Timeline",
  
  # custom categories
  "AR/VR": "MultiSelect",
  "Device Type": "MultiSelect",
  "Device": "MultiSelect",

  "Input": "MultiSelect",

  "Cognitive State": "MultiSelect",

  "Adaptation": "MultiSelect",

  "Application": "MultiSelect",

  "Method": "MultiSelect",
  "Outcomes": "MultiSelect",

  "System Maturity": "MultiSelect",
  "Open Source": "MultiSelect"
}

# properties that will be read from the csv, indexed to their supergroups
categories = {
  "Augmented Reality (AR)": "AR/VR",
  "Virtual Reality (VR)": "AR/VR",
  
  "Head-Mounted Display (HMD)": "Device Type", 
  "Handheld Display (HHD)": "Device Type",
  "Desktop": "Device Type",
  "Cave Automatic Virtual Environment (CAVE)": "Device Type",
  "Miscellaneous": "Device Type",

  "HoloLens 1": "Device",
  "HoloLens 2": "Device",
  "Meta Quest 3": "Device",
  "Meta Quest Pro": "Device",
  "Apple Vision Pro": "Device",
  "HTC Vive Pro": "Device",
  "HTC Vive": "Device",
  "HP Omnicept": "Device",
  "Google Cardboard": "Device",
  "Pico Neo3 Pro Eye": "Device",
  "Valve Index VR": "Device",
  "Meta Quest 2": "Device",
  "Google Daydream VR headset": "Device",
  "HoloLens": "Device",
  "Oculus Rift": "Device",
  "Brother AirScouter": "Device",
  "FOVE 0": "Device",
  "None": "Device",
  "No Info": "Device",
  "Novel Prototype": "Device",

  "Electrocardiogram (ECG)": "Input",
  "Electrodermal Activity (EDA)": "Input",
  "Electroencephalography (EEG)": "Input",
  "Electromyography (EMG)": "Input",
  "Eye-Tracking: Gaze": "Input",
  "Eye-Tracking: Pupil Dilation": "Input",
  "Eye-Tracking: Blink Rate": "Input",
  "Functional Near-Infrared Spectroscopy (fNIRS)": "Input",
  "Galvanic Skin Response (GSR)": "Input",
  "Heart Rate (HR)": "Input",
  "Heart Rate Variability (HRV)": "Input",
  "Photoplethysmogram (PPG)": "Input",
  "Respiration": "Input",
  "Self-Report": "Input",

  "Arousal": "Cognitive State",
  "Stress": "Cognitive State",
  "Attention": "Cognitive State",
  "Emotions/Affect": "Cognitive State",
  "Cognitive Load/Workload": "Cognitive State",
  "Confusion": "Cognitive State",
  "Presence": "Cognitive State",
  "Relaxation": "Cognitive State",
  "Discomfort": "Cognitive State",
  "Engagement": "Cognitive State",

  "Task Adjustment": "Adaptation",
  "FoV/Rendering": "Adaptation",
  "Guidance/Notification": "Adaptation",
  "Information": "Adaptation",
  "Event": "Adaptation",
  "Stimuli": "Adaptation",

  "Education": "Application",
  "Recreation": "Application",
  "Health/Rehabilitation": "Application",
  "Work/Performance": "Application",
  "Miscellaneous": "Application",

  "Qualitative (Participant Study)": "Method",
  "Quantitative (Participant Study)": "Method",
  "Requirement Analysis": "Method",
  "Inference Statistics": "Method",
  "Descriptive Statistics": "Method",
  "None": "Method",
          
  "Usability": "Outcomes",
  "Effectiveness": "Outcomes",
  "None": "Outcomes",

  "Proposal": "System Maturity",
  "Subsystem": "System Maturity",
  "Prototype": "System Maturity",

  "No Info": "Open Source",
  "Data Available": "Open Source",
  "Code Available": "Open Source"
}

groups = { 
  "AR/VR": "Technology",
  "Device Type": "Technology",
  "Device": "Technology",

  "Input": "Input",

  "Cognitive State": "Cognitive State",

  "Adaptation": "Adaptation",

  "Application": "Application",
  
  "Method": "Evaluation",
  "Outcomes": "Evaluation",

  "System Maturity": "Meta",
  "Open Source": "Meta"
}

def get_arguments():
    """ Get parsed CLI arguments """
    parser = argparse.ArgumentParser(description='Python script for converting csv to JSON for Indy.'
                                                 'Generates a config and data file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input-file', type=str, default="raw-data.csv",
                        dest="filename", help='The file that gets parsed.')
    parser.add_argument('-o','--only-data', action='store_true', default=False,
                        dest="onlydata", help='generate only the data file')
    parser.add_argument('-m','--meta', type=str, default="survey-meta.json",
                        dest="metafile", help='JSON file with survey name, description, authors, and github URL')
    parser.add_argument('-n','--name', type=str, default=None,
                        dest="surveyname", help='overrides the survey title from the meta file')
    parser.add_argument('-d','--desc', type=str, default=None,
                        dest="surveydesc", help='overrides the survey description from the meta file')
    parser.add_argument('-a','--authors', type=str, default=None,
                        dest="surveyauthors", help='overrides the survey authors from the meta file')
    parser.add_argument('-g','--github', type=str, default=None,
                        dest="github", help='overrides the GitHub URL from the meta file')

    return parser.parse_args()


def load_meta(args):
    """ Load survey metadata from file, with CLI args as overrides """
    meta = {
        "name": "Example Title",
        "description": "Example Description",
        "authors": "<anonymized for submission>",
        "github": "<anonymized for submission>"
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))
    meta_path = os.path.join(script_dir, args.metafile)
    if os.path.exists(meta_path):
        with open(meta_path, encoding='utf-8') as f:
            meta.update(json.load(f))
    else:
        print(f"Note: meta file '{meta_path}' not found, using defaults.")
    if args.surveyname is not None:
        meta["name"] = args.surveyname
    if args.surveydesc is not None:
        meta["description"] = args.surveydesc
    if args.surveyauthors is not None:
        meta["authors"] = args.surveyauthors
    if args.github is not None:
        meta["github"] = args.github
    return meta

class CustomFormatter(logging.Formatter):    
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def main():
  args = get_arguments()
  meta = load_meta(args)

  logger = logging.getLogger(__name__)
  
  stdout_handler = logging.StreamHandler()
  stdout_handler.setFormatter(CustomFormatter('%(levelname)8s | %(message)s'))
  logger.addHandler(stdout_handler)

  with open(args.filename, encoding='utf-8-sig') as csvfile:
    spamreader = csv.reader(csvfile)
    jsonfile = {"meta":[], "data":[]}
    configfile = {"filterBy":[], "filterBy":[], "detailView":{
        "view" : "normal",
        "show":[] #Add properties that you want to view on summary view
      }, 
      "summaryView": {
        "view": "text",
        "showImg": True,
        "show":[] #Add properties that you want to view on summary view
      },
      "topView":{
        "title":meta["name"],
        "description":meta["description"],
        "authors":meta["authors"],
        "addEntry": {
          "description":[
            "If you know a peer-reviewed published work that presents a contribution missing in our browser, please submit an entry!",
            "Filling out the form below will create a json entry that can be added to an issue in our Github repository."],
          "github":meta["github"]
        }
      }
    }

    header = []
    uniques = set()

    # get header information
    for row in spamreader:
      for name in row:
        header.append(name)
        if name in includeProp:
          jsonfile["meta"].append({'name': name, "type":includeProp[name]})
          if (includeProp[name] == 'MultiSelect' or includeProp[name] == 'String') and name not in excludeProp :
            configfile["filterBy"].append(name)
          if name not in excludeProp:
            configfile["detailView"]["show"].append(name)
        elif name in categories: 
          catname = categories[name]
          nametype = includeProp[catname]
          
          if catname not in uniques: 
            uniques.add(catname)
            jsonfile["meta"].append({'name': catname, "type": nametype})
            if (nametype == 'MultiSelect' or nametype == 'String') and catname not in excludeProp :
              configfile["filterBy"].append(catname)
            if catname not in excludeProp:
              configfile["detailView"]["show"].append(catname)
      break

    propStructure = {}
    for prop in includeProp:
      propStructure[prop] = {"name":prop, "values":set()}

    # reads every paper 
    for row in spamreader:
      entry = {}
      for index, prop in enumerate(row):

        # read and collect values with "x" in them 
        if header[index] in categories:  
          catname = categories[header[index]]
          nametype = includeProp[catname]

          if catname not in entry: 
            entry[catname] = set()
          
          if (prop != ""):
            entry[catname].add(header[index])
                
          for doc in entry[catname]:
            propStructure[catname]['values'].add(doc)
        
        # read as lists of strings (comma separated)
        elif header[index] in includeProp:
            catname = header[index]

            # handle edge cases
            if (catname == "Edge Case"): 
              if (prop == "x"): 
                entry[catname] = ["Yes"]
              elif (prop == ""):       
                entry[catname] = ["No"]
            
            else: 
              if includeProp[catname] == "MultiSelect":
                entry[catname] = [x.strip() for x in prop.split(",")]
              else:
                entry[catname] = prop.strip()
              
            if includeProp[catname] == "MultiSelect":
              propList = entry[catname]
              for doc in propList:
                propStructure[catname]['values'].add(doc)

        
        
      for k in entry: 
        if isinstance(entry[k], set):
          entry[k] = list(entry[k])

      for k in includeProp: 
        if (not k in entry or (len(entry[k]) == 0)) and (not k in optionals):
          logger.warning(
            "Prop: \"" + k + "\" empty for: \"" + entry["Name"] + "\". " + 
            "Check for duplicate headings, or this may be an edge case."
          )
      jsonfile["data"].append(entry)
    
    dataObject = json.dumps(jsonfile, indent=4)
    
    # writing to survey-data.json
    with open("survey-data.json", "w") as outfile:
        outfile.write(dataObject)
    
    filterGroups = {}
    if args.onlydata == False:
      for i in range(len(configfile["filterBy"])):
        name = configfile["filterBy"][i]
        propStructure[name]['values'] = list(propStructure[name]['values'] )

        
        if not groups[name] in filterGroups: 
          filterGroups[groups[name]] = { "groupName": groups[name], "categories": [] }
        filterGroups[groups[name]]["categories"].append(propStructure[name])

      configfile["filterBy"] = [x for x in filterGroups.values()]

      with open("survey-config.json", "w") as outfile:
          configObject= json.dumps(configfile, indent=4)
          outfile.write(configObject)

if __name__ == '__main__':
  main()