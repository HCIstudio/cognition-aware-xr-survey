# Cognition-Aware Virtual and Augmented Reality - Survey Overview Website<!-- omit from toc -->

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/HCIstudio/cognition-aware-xr-survey/deploy.yml?label=Github%20Actions%20Deployment)

This repository hosts the survey data and website from the WIP survey paper "Cognition-Aware Virtual and Augmented Reality". More information regarding this publication will be added over time.

## Building and Running the Webpage

1. `npm install` installs all the libraries you need to get the app running using the list from `package.json`.
2. `python create-jsons.py` (in `/src/data`) creates the necessary JSON files from the survey data (see below).
3. `npm run build` updates and exports `index.html`, and the files in `dist/assets` for a static website. 
4. `npm run dev` the site locally (see link to localhost) in development mode (updates to src files reload the site).
5. GitHub Actions (see the related [workflow](/.github/workflows/deploy.yml)) is used to automatically redeploy the website anytime a new commit is made on the `main`-branch.

## Importing Original Survey Data in Bulk
1. The [`raw-data.csv`](/src/data/raw-data.csv) file contains the core corpus described in the paper. 
   1. The taxonomy columns accept lists of strings (comma-separated), or marks ("x") for values that apply. 
   2. `Name`, `Year`, `Authors` (comma separated), `DOI`, `Bibtex`, and `Source` are required.
2. Create the config and data JSON files: 
   1. [create-jsons.py](/src/data/create-jsons.py) describes the survey categories using the `includeProp`, `categories`, and `groups` dictionaries. 
   2. Running the script generates [survey-data.json](src/data/survey-data.json) and [survey-config.json](src/data/survey-config.json). 
   WARNING: The script overwrites the existing files; any manual edits to these JSON files will be lost. 
        ```bash
        python create-jsons.py
        ```
   3. The script prints out warnings for empty fields from the `includeProp` dictionary. You may use this to enforce value combinations (e.g., "at least one column from group A and one from group B") or to identify edge cases. 
3. Note that the "topView" entry of `survey-config.json` must be updated to include Orcids and further details about citation (see existing versions in the repository).  
4. Build the website as explained in [Running the Webpage](#building-and-running-the-webpage) to see the created entries. 

## Manually Adding Papers Afterward
 __TODO: Add GitHub Action step to append `survey-data-additions.json` to `survey-data.json`.__

To manually add papers one-by-one after the cutoff date, open [src/data/survey-data-additions.json](src/data/survey-data-additions.json). Then, add a new paper object to the list under the `"data"` tag using the template below as a guide. Note that the `"Name"`, `"Year"`, `"Authors"`, `"DOI"`, and `"Bibtex"` tags are required, but more can be added.
```json
"data": [  // array of paper objects
    {
        "Name"   : "[Poster] Visualization of solar radiation data in augmented reality",
        "Year"   : "2014",
        "Bibtex" : "'@INPROCEEDINGS{6948437,\n  author={Beatriz Carmo, Maria and Cl\u00e1udio, ....",
        "DOI"    : "10.1109/ISMAR.2014.6948437",
        "Authors": [
            "M. Beatriz Carmo; A. P. Cl\u00e1udio; A. Ferreira; A. P. Afonso; ...."
        ]
    },
]
```

We welcome such updates via pull requests (which can be generated directly on the website, too)!

## Acknowledgements
This repository is based on and forks the [Survey Tool](https://github.com/imldresden/survey-tool) by the [Interactive Media Lab Dresden](https://github.com/imldresden), which itself is a fork from the [Indy Survey Tool](https://github.com/VisDunneRight/Indy-Survey-Tool) made by the [Khoury Vis Lab](https://github.com/VisDunneRight). Thanks a lot to both teams for creating and improving upon this tool. Definitely check them both out! 
