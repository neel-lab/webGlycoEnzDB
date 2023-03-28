Data from tabula sapiens single-cell data split by individual compartments.  

Citation: Tabula Sapiens Consortium*, Jones, R. C., et al. (2022). The Tabula Sapiens: A multiple-organ, single-cell transcriptomic atlas of humans. Science, 376(6594), eabl4896.

The preprocessing steps for the dataset are as follows:
From the decontaminated UMI counts obtained from TS, 
	- Remove cells which have less than 200 genes detected.
	- Remove genes which are detected inless than 3 cells
	- Scale data such that each cell has a total sum of 10000 reads. For each cell, (expr/sum(expr))*10000
	- Log transform data. ln(1+expr)
	- Subset data to glycogenes

In each compartment folder(endothelial, epithelial, stromal, immune), 5 files are available:
1. *_expr.csv files contain gene expression in cellsXglycogenes table format.

2. *_metadata.csv files contain cell metadata in cellsXmetadata format. The most relevant columns for creating the violin plots are: tissue_in_publication, cell_type and compartment to group the cells by.

The following 3 files in each folder are specifically calculated for box plots. To create violin plots, the original *_expr.csv has to be used instead. 

3. *._stats_celltype.csv files contain groupwise summary stats for each celltype in each tissue for each of the 400 glycogenes.  For each combination (tissue, cell_type, gene), the following stats are computed based on the expression:
	- Mean, std, min(minimum expression), 25%(1st quartile), 50%(median), 75%(3rd quartile), max(maximum expression), iqr(inter-quartile range)
	In addition, 2 columns are created specifically for creating the whiskers for box and whisker plots(not required for violin plots):
	- Upper = Minimum value between max expression and (3rdquartile+1.5*iqr)
	- Lower = Maximum value between min expression and (1stquartile-1.5*iqr)

4. *_stats_tissue.csv files contain groupwise summary stats for each tissue for each of the 400 glycogenes. Each row is for a combination of (tissue, gene). The other columns follow same meaning as in _stats_celltype.csv files described above.

5. *_stats_tissue.csv files contain summary stats for the entire compartment for each of the 400 glycogenes. Each row is for a gene. The other columns follow same meaning as in _stats_celltype.csv files described above.

Information for plotting[Vishnu]: 
1. To create Violin/Boxplots, use the plotly-dash python package framework. Instructions for creating violin plots are as explained in the link: https://plotly.com/python/violin/ which takes a dataframe as input.
2. To generate violin plots, combine the *_expr.csv and *_metadata.csv files into a single dataframe. If celltypes relevant to a tissue are to be shown on x-axis, once merging the 2 files, subset dataframe based on 'tissue_in_publication' column to tissue of interest prior to plotting. This could later be provided as an option to users as a dropdown to choose specific tissues.
3. To generate box plots, the *_stats_celltype.csv, *_stats_tissue.csv and *_stats_compartment.csv files provide the median, iqr(for the box) and upper and lower whisker bounds in each row. 

