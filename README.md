# GlycoEnzDB

**Reference: Y. Zhou, V. Ghosh, S. Sriram, S. Venkatesan, T. Groth, D. Huang, E. Sobczak, S. Setlur, R.D. Cummings, A. Varki, R. Gunawan, S. Neelamegham, "GlycoEnzDB: A comprehensive database of enzymes involved in mammalian glycosylation", in preparation, 2024.**

The glycan distribution on cells is governed by the stochastic activity of different families of enzymes that are together called ‘glycoEnzymes’. These include ~400 gene products or 2% of the proteome, that have been recently curated in an ontology called GlycoEnzOnto (Groth et al., Bioinformatics, 38(24): 5413–5420, 2022). With the goal of making this ontology more accessible to the larger biomedical and biotechnology community, we organized a web resource presenting this enzyme classification both in terms of enzyme function and the pathways that they participate in. This information is linked to i) Figures from the The Essentials of Glycobiology textbook, ii) General gene, enzyme and pathway data appearing in external databases, iii) Manual and generative-artificial intelligence (AI) based text describing the function and pathways regulated by these entities, iv) Single-cell expression data across cell lines, normal human cell-types and tissue, and v) CRISPR-knockout/activation/inactivation and Transcription factor activity predictions. Whereas these data are curated for human glycoEnzymes, the knowledge framework may be extended to other species also. The user–friendly web interface is accessible at www.virtualglycome.org/glycoenzdb.

## Contents of this resource:

This repository contains all data files and code used to develop the django web resource. THe following are the locations of relevant data files

### webGlycoEnzDB/dataloader/data/

    GlycoEnzOntoDB: describes hierarchy of otology used in website

### webGlycoEnzDB/uniprotDataScript/

    Scripts used to pull generic enzyme data from Uniprot

### webGlycoEnzDB/djangoProject/data/gpt/

    gpt text created using Dr. Glyco GPT

### webGlycoEnzDB/djangoProject/ webGlycoEnzDB/static/

    reaction_imgs/: enzyme reaction
    pathway_figures/: pathway figures used in rendering

### webGlycoEnzDB/singlecellData/ViolinPlots/inputfiles

    CCLE data

Tabula Sapiens ssingle cell transcriptomics data parsed for the glycogenes

### webGlycoEnzDB/djangoProject/webGlycoEnzDB/static/CRISPR/

    CRISPRa/: figures for CRISPR activation
    CRISPRi/: figures for CRISPR inactivation
    CRISPRko/: figures for CRISPR knockout

### webGlycoEnzDB/geneNetGlyco/

    glycol-TF interaction figures

### webGlycoEnzDB/djangoProject/

Here’s the markdown-formatted version:

### Instructions for Setting Up the Server

After setting up the Django application by following the instructions in `webGlycoEnzDB/djangoProject/README.md`, you can create a new service to manage the starting and stopping of the server.

For example, you can create a `glycoenzdb` service using the following command:

```bash
gunicorn -b 0.0.0.0:8000 -w 4 -D djangoProject.wsgi:application
```

Once the service is created, you can start the server with:

```bash
sudo systemctl start glycoenzdb
```

**Collect Static files:** Navigate to the /webGlycoEnzDB/djangoProject/ directory and collect static files by running the following command:

```bash
python manage.py collectstatic
```

Restart the server by running the following command:

```bash
sudo systemctl restart glycoenzdb
```

Licensing: CC BY 4.0. You are fee to copy, redistribute, remix, transform and build upon this material for commercial and non-commercial purposes, provided source of information is attributed/credited.
