# QT-GILD
#### QT-GILD (version 1.0)
This repository contains the official implementation of ***QT-GILD*** <!--code and helper scripts of--> <!-- our paper [**"wQFM: Highly Accurate Genome-scale Species Tree Estimation from Weighted Quartets"**](https://academic.oup.com/bioinformatics/advance-article-abstract/doi/10.1093/bioinformatics/btab428/6292084) accepted in ***Bioinformatics, 2021***. -->

<!-- ## Notice to all the users
- Codebase has been slightly updated **(on June 12, 2021)** to fix some precision related bugs.
- New version (i.e. the current stable version **v-1.3**) has it fixed. Please use the current version if you have used the jar file/codebase before the aforementioned date.
- New version also includes quartet score outputs (please see below **"To infer quartet scores"** section).
 -->
## Short Description

**QT-GILD** is a quartet imputation technique for estimating species trees despite the presence of missing data. 

QT-GILD is an  automated  and specially tailored unsupervised deep learning technique, accompanied by cues from natural languageprocessing (NLP), which learns the quartet distribution in a given set of incomplete gene trees andgenerates a complete set of quartets accordingly.

<!--wQFM uses a two-step technique in which we first use the input set of estimated gene trees to produce a set of weighted four-taxon trees (*weighted quartets*).-->

## Installing QT-GILD

Before installing QT-GILD, please sure that you have the following programs installed:

- Python: Version >= 3.7
- Pip: Version >= 21.0
- Java: Version >= 11.0 (if you want to generate the species trees using [wQFM](https://academic.oup.com/bioinformatics/advance-article-abstract/doi/10.1093/bioinformatics/btab428/6292084))

To install the python packages, use the following command

```bash
pip install -r requirements.txt
``` 

The authors recommend using seperate conda environment to install QT-GILD.

If you use wQFM, please cite the paper ["wQFM: Highly Accurate Genome-scale Species Tree Estimation from Weighted Quartets"](https://academic.oup.com/bioinformatics/advance-article-abstract/doi/10.1093/bioinformatics/btab428/6292084)


## Usage

####  For imputing and generating the imputed weighted quartets distribution, use -i and -o flag.
   
<!-- Code Blocks -->
```bash
python QT-GILD.py -i <input-gene-tree-file> -o <output-folder>
``` 
OR
<!-- Code Blocks -->
```bash
python QT-GILD.py --input <input-gene-tree-file> --output <output-folder>
``` 
#### To generate the species trees using wQFM, just use a --st flag alongside usual input. 
```bash
python QT-GILD.py -i <input-gene-tree-file> -o <output-folder> --st
``` 

## Example

There are two gene tree files provided in the repository to test QT-GILD

```bash
python QT-GILD.py --input test/aminota_gt.tre --output output
``` 
