# Cognition-Aware Virtual and Augmented Reality - Survey Overview Website<!-- omit from toc -->

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/HCIstudio/cognition-aware-xr-survey/deploy.yml?label=Github%20Actions%20Deployment)

This repository hosts the survey data and website from the WIP survey paper "Cognition-Aware Virtual and Augmented Reality". More information regarding this publication will be added over time.

## Building and Running the Webpage

1. `npm install` installs all the libraries you need to get the app running using the list from `package.json`.
2. `python3 create-jsons.py` (in `/src/data`) creates the necessary JSON files from the survey data (see below).
3. `npm run build` updates and exports `index.html`, and the files in `dist/assets` for a static website.
4. `npm run dev` runs the site locally (see link to localhost) in development mode (updates to src files reload the site).
5. GitHub Actions (see the related [workflow](/.github/workflows/deploy.yml)) is used to automatically redeploy the website anytime a new commit is made on the `main`-branch.

## Importing Original Survey Data in Bulk

1. The [`raw-data.csv`](/src/data/raw-data.csv) file contains the core corpus described in the paper.
   1. The taxonomy columns accept lists of strings (comma-separated), or marks ("x") for values that apply.
   2. `Name`, `Year`, `Authors` (comma separated), `DOI`, `Publisher`, and `Bibtex` are required.
2. Edit [`survey-meta.json`](/src/data/survey-meta.json) to set the survey title, description, authors (with ORCIDs), and GitHub URL. This file is read by the script and committed to the repository.
   ```json
   {
       "name": "My Survey Title",
       "description": "Supplementary Website to the Literature Survey",
       "authors": [
           { "name": "Jane Doe", "orcid": "https://orcid.org/0000-0000-0000-0000" }
       ],
       "github": "https://github.com/your-org/your-repo"
   }
   ```
3. Create the config and data JSON files:
   1. [create-jsons.py](/src/data/create-jsons.py) describes the survey categories using the `includeProp`, `categories`, and `groups` dictionaries.
   2. Running the script reads `survey-meta.json` and generates [survey-data.json](src/data/survey-data.json) and [survey-config.json](src/data/survey-config.json).
      WARNING: The script overwrites the existing files; any manual edits to these JSON files will be lost.
      ```bash
      cd src/data
      python3 create-jsons.py
      ```
   3. CLI flags (`-n`, `-d`, `-a`, `-g`) can override individual fields from `survey-meta.json` for one-off runs. Use `-m` to point to a different meta file.
   4. The script prints warnings for empty fields from the `includeProp` dictionary. Use this to enforce value combinations or identify edge cases.
4. Build the website as explained in [Building and Running the Webpage](#building-and-running-the-webpage) to see the created entries.

## Manually Adding Papers After the Cutoff Date

To add papers one-by-one after the cutoff date without re-running the script, edit [`src/data/survey-data-append.json`](src/data/survey-data-append.json). Add a new paper object to the `"data"` array. The `_template` key in that file shows all available fields:

```json
{
    "data": [
        {
            "Name": "My Paper Title",
            "Year": "2025",
            "Authors": ["Last, First; Last, First"],
            "DOI": "https://doi.org/10.1000/example",
            "Publisher": ["IEEE"],
            "Bibtex": "@inproceedings{...",
            "AR/VR": ["Augmented Reality (AR)"],
            "Device Type": ["Head-Mounted Display (HMD)"],
            "Device": ["HoloLens 2"],
            "Input": ["Eye-Tracking: Gaze"],
            "Cognitive State": ["Cognitive Load/Workload"],
            "Adaptation": ["Task Adjustment"],
            "Application": ["Work/Performance"],
            "Method": ["Quantitative (Participant Study)"],
            "Outcomes": ["Effectiveness"],
            "System Maturity": ["Prototype"],
            "Open Source": ["No Info"]
        }
    ]
}
```

Values must match exactly those defined in [create-jsons.py](/src/data/create-jsons.py) (`categories` dict). Appended papers are merged with the generated dataset at build time; no other files need to be changed.

We welcome such updates via pull requests (which can be submitted directly on the website too)!

## Acknowledgements
This repository is based on and forks the [Survey Tool](https://github.com/imldresden/survey-tool) by the [Interactive Media Lab Dresden](https://github.com/imldresden), which itself is a fork from the [Indy Survey Tool](https://github.com/VisDunneRight/Indy-Survey-Tool) made by the [Khoury Vis Lab](https://github.com/VisDunneRight). Thanks a lot to both teams for creating and improving upon this tool. Definitely check them both out!
