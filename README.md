# Phenoscript Species Descriptions for the Dung Beetle Genus _Grebennikovius_

This repository is associated with the manuscript:

_Computable Species Descriptions and Nanopublications: Applying Ontology-based Technologies to Dung Beetles (Coleoptera: Scarabaeinae), Biodiversity Data Journal. (in preparation)_

It contains all data files and scripts necessary to reproduce the results. For detailed information, please refer to the original paper. The repository has been tested on Mac and should work on Linux without issues. Windows users may need to make some modifications.

## Content of the Directories

- `materials`, main character patterns.
- `main`, contains the pipeline:
    - `Makefile`, the makefile to run the full pipeline.           
    - `merged_ontologies`, contains `tbox.owl` file representing merged ontologies.         
    - `phenotypes`, the input files (Phenoscript descriptions, `phs-config.yaml`, and snippets).
    - `source_ontologies`, the ontologies used.
    - `source_queries`, helper files.
    - `sparql`, SPARQL queries: `query.sparqlbook` for running queries from the paper; `debug.sparqlbook` for debugging the descriptions.
    - `output`, main outputs, including:
        - `grebennikovius.owl`, Phenoscript descriptions converted into OWL.
        - `grebennikovius-all.ttl`, the full OWL file after running reasoning (i.e., after Step 4).
        - `NL`, generated NL descriptions.
        - `shacl.log`, SHACL output file.

## Running the Pipeline

### Install the Following Software

To run the pipeline, ensure the following software is preinstalled and globally accessible for execution. Installation instructions are provided for Mac. For Linux or Windows, please refer to the original software guidelines.

- [Phenospy](https://pypi.org/project/phenospy/)
    ```bash
    pip install phenospy
    ```
- [ROBOT](https://robot.obolibrary.org/)
    - Read this [installation instruction](https://robot.obolibrary.org/).
- [Apache Jena tools](https://jena.apache.org/index.html). This suite includes commands such as riot, arq, update, shacl.
    ```bash
    brew install jena
    ```
- [Materializer](https://github.com/balhoff/materializer/releases/tag/v0.2.7)
    - Download and unpack the `tgz` file. Make `/bin/materializer` globally accessible for execution.
- [SPARQL Notebook for VS Code](https://marketplace.visualstudio.com/items?itemName=Zazuko.sparql-notebook)
    - Install this extension within VS Code from the Marketplace tab.



### Execute the pipeline

Download the present repository and execute the following commands in your terminal: 

```bash
cd main
make
````

Note, the current content of the repository was generated after running the pipeline and contains files and folders created by the pipeline. To run the full pipeline with only initial files, remove all folders in `main` except these:

- `phenotypes`
- `source_queries`
- `sparql`

Then, execute the `make` command again.


## Validation
To ensure that the created descriptions are consistent and include correct data models, check the following:

- The SHACL output file `main/output/shacl.log` should contain `sh:conforms true` if the validation is successful.
- The output in the terminal when executing the `materializer` software should be similar to the one below. There should be NO lines indicating that the ontology is inconsistent. In that case, the ontology is consistent.

```bash
STEP: reason using materializer
materializer file --ontology-file merged_ontologies/tbox.owl --input output/grebennikovius.owl --output output/grebennikovius-reasoned.ttl --reasoner whelk
2023.12.22 16:23:47 [INFO] org.renci.materializer.Main.:86:33 - Loaded ontology
2023.12.22 16:24:02 [INFO] org.renci.materializer.Main.:36:39 - Prepared reasoner
2023.12.22 16:24:04 [INFO] org.renci.materializer.Main.:50:39 - Reasoning done in: 2.184s
```


