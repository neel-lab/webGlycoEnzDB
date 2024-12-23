"""
Use genomic and coding sequences to create visual representation of gene, showing start and end positions with CRISPR
sequences. CRISPR Sequences derived from : https://portals.broadinstitute.org/gppx/crispick/public
To download specific ENSEMBL version type at terminal: pyensembl install --release 109 --species human

Functions:
- transcript_ensembl(ensembl, ID): Obtain information about the strand direction, exon intervals, transcript sequence,
and coding sequence excluding 5' UTR
    -Input: EnsemblRelease version and transcript ID of gene
    -Output: Information on the strand direction,exon intervals, and sequences of the given gene
- get_gene_data(dir, infile, outfile): Takes the information extracted from transcript_ensembl to create a data file
representing the extracted data in a .csv file format
    -Input: File directory(dir), File containing genes and their respective transcript IDs(infile) and the name of the
    .csv file created by the function(outfile)
    -Output: .csv file whose name is determined by the outfile parameter and stored in the given file directory
-extract_CRISPR_sequences(ensembl): Processes the CRISPR sequences obtained from CRIsPick and formats them into a
usable format that will allow for them to be searched for in the genomic sequences
    - Input: EnsemblRelease version(ensembl), picking results file obtained from CRISPick.com(crispr_data), data file
    containing all the genes and their respective transcript ids(gene_transcripts)
    - Output: New data file containing formatted version of the gene_name followed by the CRISPR Sequences to be
    searched for(reverse complemented if found on the antisense strand) in a list format
-draw_CRISPR_site_for_ko(ensembl, geneID): Creates visual representation for models using a CRISPR knockout mechanism
    -Inputs: EnsemblRelease version(ensembl), gene ID of gene(geneID), data file created from get_gene_data(gene_data),
    picking result file from CRISPick(crispr_data), data file created from extract_CRISPR_sequences(crispr_seq_data)
    -Output: Visual representation of gene, showing exon positions as well as the positions of the gene's respective
    CRISPR knockout sequences denoted by C1-C5 followed by the number exon on which they lie
-draw_CRISPR_site_for_activated_deactivated(ensembl, geneID, mechanism): Creates visual representation for models using
a CRISPR inactivation or activation mechanism
    -Inputs: EnsemblRelease version(ensembl), gene ID of gene(geneID), mechanism parameter which is either 'CRISPRi'
    if using an inactivation mechanism or 'CRISPRa' if using an activation mechanism, data file created from
    get_gene_data (gene_data), picking result file from CRISPick(crispr_data), data file created from
    extract_CRISPR_sequences (crispr_seq_data)
    -Output: Visual representation of gene, showing exon positions as well as the python3 -m pip --version
positions of the gene's respective
    CRISPR knockout sequences denoted by C1-C5 relative to the transcription start site , as well as the location of
    the transcription start site(TSS)

Both the drawing functions import the sub_seq function from NCBI_getGRCh38.py which uses Biopython's Entrez to search
the NCBI database to obtain a gene's full genomic sequence, transcription start site, sub sequence determined by the
minus and plus parameters, and the start and end positions of the gene

"""
import ast

from pyensembl import EnsemblRelease
import pandas as pd
import random
from dna_features_viewer import GraphicFeature, GraphicRecord
# import mpld3
from math import isnan
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from Bio.Seq import Seq
from matplotlib.table import Table
import random
import textwrap
from NCBI_getGRCh38 import sub_seq
import numpy as np


def transcript_ensembl(ensembl, ID):
    transcript = ensembl.transcript_by_id(ID)
    header = '>gene:', transcript.gene_name, ' transcriptID:', transcript.transcript_id
    if transcript.complete:
        cod_sequence = transcript.coding_sequence
        exons = transcript.exon_intervals
        nexon = len(exons)
        strand_dir = transcript.strand
        transcript_seq = transcript.sequence
        return header, exons, strand_dir, transcript_seq, cod_sequence
    else:
        sequence = ''
        exons = ()
        strand_dir = ''
        gene_seq = ''
        return header, exons, strand_dir, gene_seq, sequence


def get_gene_data(ensembl,dir, infile, outfile):
    # infile contains the gene, transcript mapping
    exons_s = []
    strands =[]
    gene_seqs = []
    seqs = []
    headings = []
    data = pd.read_excel(dir+infile)
    genes = data['Gene']
    transcripts = data['ENSEMBL']
    for transcriptID in transcripts:
        header, exons, strand_dir, gene_seq, sequence = transcript_ensembl(ensembl, transcriptID)
        exons_s.append(exons)
        strands.append(strand_dir)
        gene_seqs.append(gene_seq)
        seqs.append(sequence)
        headings.append(header)
        print(header)
    print('done')
    save_dict = {'Header':headings, 'Gene Sequence':gene_seqs, 'Transcript Sequence':seqs, 'Exon Intervals':exons_s,
                 'Strand Direction':strands}
    save_df = pd.DataFrame(save_dict)
    save_df.to_csv(outfile)


def extract_CRISPR_sequences(ensembl):
    gene_transcripts = pd.read_excel('gene_transcript.xlsx')
    transcript_ids = list(gene_transcripts['ENSEMBL'])
    genes = list(gene_transcripts['Gene'])
    crispr_data = pd.read_csv('crispr_new_a.csv', encoding='utf-8')
    oriented_sequences_all = []
    for transcriptID in transcript_ids:
        transcript = ensembl.transcript_by_id(transcriptID)
        input_nums = []
        gene_name = transcript.gene_name
        inputs = list(crispr_data['Input'])
        for row, input in enumerate(inputs):
            if input == gene_name:
                input_nums.append(row)
        orientations = []
        for num in input_nums:
            orientation = crispr_data.loc[num, 'Orientation']
            orientations.append(orientation)
        sgRNA_seqs = []
        for num in input_nums:
            seq = crispr_data.loc[num, 'sgRNA Sequence']
            sgRNA_seqs.append(seq)
        oriented_sequences = []
        for row in range(len(sgRNA_seqs)):
            seq = sgRNA_seqs[row]
            orient = orientations[row]
            if orient == 'sense':
                oriented_sequences.append(seq)
            else:
                converted_seq = Seq(seq)
                converted_seq = converted_seq.reverse_complement()
                oriented_sequences.append(converted_seq)
        oriented_sequences_all.append(oriented_sequences)
    crispr_dict = {'Gene':genes, 'CRISPR Sequences': oriented_sequences_all}
    crispr_df = pd.DataFrame(crispr_dict)
    crispr_df.to_csv('CRISPR_Data_correct_Activated_new.csv',encoding='utf-8', index=True)


def makeplot(gene_name, mechanism, chromosome_num, graph_start, gene_start, graph_end, gene_end, full_sequence,
             cell_text, columns, record, strand_dir, end=0):
    fig = plt.figure(figsize=(17, 6))
    gs = GridSpec(3, 1, height_ratios=[2, 0.5, 1])  # 3 rows: 2/3 for figure, 1/3 for table
    ax1 = fig.add_subplot(gs[0])
    ax1.set_title((gene_name + '(' + mechanism + '), Chromosome ' + str(chromosome_num)), x=0.5, y=0.85)
    #    fig, (ax1, ax2) = plt.subplots(nrows=2,ncols=1, figsize=(8,4))
    graph_width = abs(graph_start - graph_end)
    if mechanism == 'CRISPRa-SpyoCas9':
        record.plot(ax=ax1, figure_width=6, x_lim=(0, 400 + 100))
        ax1.set_xticks([0, 300, end])
        ax1.set_xticklabels([-300, 0, 300])
    elif mechanism == 'CRISPRi-SpyoCas9':
        record.plot(ax=ax1, figure_width=6, x_lim=(0, 400 + 10))
        ax1.set_xticks([0, 50, end])
        ax1.set_xticklabels([-50, 0, 300])
    else:
        record.plot(ax=ax1, figure_width=6, x_lim=(-1000, gene_end - gene_start + 1000))
        ax1.set_xticks([0, len(full_sequence) - 1])
        if (strand_dir == 1):
            ax1.set_xticklabels([gene_start, gene_end])
        else:
            ax1.set_xticklabels([gene_end, gene_start])
    ax2 = fig.add_subplot(gs[2])
    table = ax2.table(cellText=cell_text, colLabels=columns, colWidths=[0.3, 0.1, 0.1, .15],
                      cellLoc='center', edges='horizontal', bbox=[0, 0, 1, 1.2])
    # Set the font size
    #    table.auto_set_font_size(False)
    #    table.set_fontsize(12)
    # table.auto_set_column_width(col=list(range(len(table_data[0]))))
    ax2.set_axis_off()
#    plt.tight_layout()
#    plt.subplots_adjust(left=0.1, bottom=0.1)
    plt.show()
    return fig


def draw_CRISPR_site_for_ko(folder_path, ensembl, geneID):
    gene_data = pd.read_csv('gene_data.csv', encoding='utf-8')
    crispr_data = pd.read_csv('crispr_konew.csv', encoding='utf-8')
    crispr_seq_data = pd.read_csv('CRISPR_Data_correct_KO_new.csv', encoding='utf-8')
    gene_name = ensembl.gene_name_of_gene_id(geneID)
    row_num = 0
    for row in range(gene_data.shape[0]):
        header = gene_data.loc[row,'Header']
        search_header = "('>gene:', "+"'"+gene_name+"'"
        if search_header in header:
            row_num = row
    exon_intervals = gene_data.loc[row_num, 'Exon Intervals']
    exon_intervals = ast.literal_eval(exon_intervals)
    exon_length = 0
    for interval in exon_intervals:
        exon_length += abs(interval[0]-interval[1])

    strand_dir = gene_data.loc[row_num, 'Strand Direction']
    strand = strand_dir
    if(strand_dir != strand_dir):
        return
    sub_sequence, tss_sequence, full_sequence, gene_start, gene_end = sub_seq(gene_symbol=gene_name)
    strand_dir += '1'
    strand_dir = int(strand_dir)
    transcript_seq = gene_data.loc[row_num, 'Gene Sequence']
    crispr_genes = list(crispr_seq_data['Gene'])
    row_crispr = 0
    for row in range(len(crispr_genes)):
        if crispr_genes[row] == gene_name:
            row_crispr = row
    crispr_list = crispr_seq_data.loc[row_crispr, 'CRISPR Sequences'].split()
    crispr_list_new = []
    for elem in crispr_list:
        if '[' in elem:
            elem = elem.replace('[', '')
        if ',' in elem:
            elem = elem.replace(',', '')
        if ']' in elem:
            elem = elem.replace(']','')
        if elem[0:1] == 'S':
            start_index = elem.find("'")+1
            end_index = elem.rfind("'")
            elem = elem[start_index:end_index]
        if elem[0:1] == "'":
            elem = elem.replace("'", "")
        crispr_list_new.append(elem)
    features = []
    inputs = list(crispr_data['Input'])
    input_nums = []
    for row,input in enumerate(inputs):
        if input == gene_name:
            input_nums.append(row)
    crispr_exon_numbers = []
    for num in input_nums:
        exon_num = crispr_data.loc[num, 'Exon Number']
        crispr_exon_numbers.append(exon_num)
    if len(input_nums) == 0:
        return
    crispr_mechanism = crispr_data.loc[input_nums[0], 'CRISPR Mechanism']
    pam_policy = crispr_data.loc[input_nums[0], 'PAM Policy']
    mechanism_pam = crispr_mechanism + '-'+pam_policy
    sgrna_seqs = []
    for num in input_nums:
        sgrna_seq = crispr_data.loc[num, 'sgRNA Sequence']
        sgrna_seqs.append(sgrna_seq)
    pam_sequences = [
    ]
    for num in input_nums:
        pam_sequence = crispr_data.loc[num, 'PAM Sequence']
        pam_sequences.append(pam_sequence)
    target_cuts = []
    for num in input_nums:
        target_cut = crispr_data.loc[num, 'Target Cut %']
        target_cuts.append(target_cut)
    eff_scores = []
    for num in input_nums:
        eff_score = crispr_data.loc[num, 'On-Target Efficacy Score']
        eff_scores.append(eff_score)
    strands = []
    for num in input_nums:
        stra = crispr_data.loc[num, 'Strand of sgRNA']
        strands.append(stra)
    ref_seq = crispr_data.loc[input_nums[0], 'Reference Sequence']
    ref_start = ref_seq.find('_')
    ref_end = ref_seq.find('.')
    chromosome_num = ref_seq[ref_start + 1:ref_end]
    chromosome_num = int(chromosome_num)
    table_data = [
        ['C1: '+sgrna_seqs[0]+' + '+pam_sequences[0], strands[0],target_cuts[0], eff_scores[0]],
        ['C2: '+sgrna_seqs[1]+' + '+pam_sequences[1], strands[1],target_cuts[1], eff_scores[1]],
        ['C3: '+sgrna_seqs[2]+' + '+pam_sequences[2],strands[2],target_cuts[2], eff_scores[2]],
        ['C4: '+sgrna_seqs[3]+' + '+pam_sequences[3], strands[3], target_cuts[3],eff_scores[3]],
        ['C5: '+sgrna_seqs[4]+' + '+pam_sequences[4], strands[4], target_cuts[4], eff_scores[4]]
    ]
    columns = (textwrap.fill('sgRNA Sequence + PAM'), textwrap.fill('Strand'),textwrap.fill('Target Cut %'),
               textwrap.fill('On-Target Score'))
    rows = [gene_name, gene_name, gene_name, gene_name, gene_name]
    cell_text = []
    for row in range(len(rows)):
        y_offset = table_data[row]
        cell_text.append([x for x in y_offset])
    graph_start = 0
    graph_end = 0
    if(strand_dir == 1):
        graph_start = exon_intervals[0][0]
        graph_end = exon_intervals[-1][-1]
    else:
        graph_start = exon_intervals[-1][0]
        graph_end = exon_intervals[0][1]
    graph_width = abs(graph_start-graph_end)
    start = 0
    gene_start = int(gene_start)
    gene_end = int(gene_end)
    for count, exon_interval in enumerate(exon_intervals):
        exon_start = exon_interval[0]
        exon_end = exon_interval[1]
        if(strand_dir == -1):
            exon_graph_start = gene_end - exon_end
            exon_graph_end = gene_end - exon_start
        else:
            exon_graph_start = exon_start-gene_start
            exon_graph_end = exon_end - gene_start
        feature = GraphicFeature(start=exon_graph_start, end=exon_graph_end, strand=1, color='#ffd700')
        features.append(feature)
    for index,sequence in enumerate(crispr_list_new):
        strand = strands[index]
        exon_num = crispr_exon_numbers[index]
        seq_start = full_sequence.find(sequence)
        seq_end = seq_start + len(sequence)
        crispr_feature = GraphicFeature(start=seq_start, end=seq_end, strand=strand, color="#ff66ff",
                                        label='C'+str(index+1)+': ex'+str(exon_num), label_link_color='auto')
        features.append(crispr_feature)
#    line_feature = GraphicFeature(start=graph_start, end=graph_end, strand=strand_dir, color="#000000",
#                                  line_thickness=0.5)
#    features.append(line_feature)
    length = len(transcript_seq)
    record = GraphicRecord(sequence_length=len(full_sequence), features=features)
    fig = makeplot(gene_name, mechanism_pam, chromosome_num, graph_start, gene_start, graph_end, gene_end,
                   full_sequence, cell_text, columns, record, strand_dir)
    fig.savefig(folder_path + 'CRISPRko' + '/' + (gene_name + '-' + 'CRISPRko') + '.png')
    return


def draw_CRISPR_site_for_activated_deactivated(folder_path, ensembl, geneID, mechanism):
    gene_data = pd.read_csv('gene_data.csv', encoding='utf-8')
    gene_name = ensembl.gene_name_of_gene_id(geneID)
    if mechanism == 'CRISPRa':
        crispr_data = pd.read_csv('crispr_new_a.csv')
        crispr_seq_data = pd.read_csv('CRISPR_Data_correct_Activated_new.csv')
        sequence_length = 700
        end = 700
    else:
        crispr_data = pd.read_csv('crispr_new_i.csv')
        crispr_seq_data = pd.read_csv('CRISPR_Data_correct_Inactivated_new.csv')
        sequence_length = 400
        end = 400
    row_num = 0
    for row in range(gene_data.shape[0]):
        header = gene_data.loc[row, 'Header']
        search_header = "('>gene:', " + "'" + gene_name + "'"
        if search_header in header:
            row_num = row
    exon_intervals = gene_data.loc[row_num, 'Exon Intervals']
    exon_intervals = ast.literal_eval(exon_intervals)
    strand_dir = gene_data.loc[row_num, 'Strand Direction']
    exon_intervals = gene_data.loc[row_num, 'Exon Intervals']
    exon_intervals = ast.literal_eval(exon_intervals)
    crispr_genes = list(crispr_seq_data['Gene'])
    if (strand_dir != strand_dir):
        return
    if mechanism == 'CRISPRa':
        sub_sequence, tss_sequence, full_sequence, gene_start, gene_end = sub_seq(gene_symbol=gene_name, minus=-300, ko=False)
    else:
        sub_sequence, tss_sequence, full_sequence, gene_start, gene_end = sub_seq(gene_symbol=gene_name, ko=False)
    row_crispr = 0
    for row in range(len(crispr_genes)):
        if crispr_genes[row] == gene_name:
            row_crispr = row
    crispr_list = crispr_seq_data.loc[row_crispr, 'CRISPR Sequences'].split()
    crispr_list_new = []
    for elem in crispr_list:
        if '[' in elem:
            elem = elem.replace('[', '')
        if ',' in elem:
            elem = elem.replace(',', '')
        if ']' in elem:
            elem = elem.replace(']', '')
        if elem[0:1] == 'S':
            start_index = elem.find("'") + 1
            end_index = elem.rfind("'")
            elem = elem[start_index:end_index]
        if elem[0:1] == "'":
            elem = elem.replace("'", "")
        crispr_list_new.append(elem)
    inputs = list(crispr_data['Input'])
    input_nums = []
    for row, input in enumerate(inputs):
        if input == gene_name:
            input_nums.append(row)
    if len(input_nums) == 0:
        return
    if strand_dir != strand_dir:
        return
    sgrna_seqs = []
    for num in input_nums:
        sgrna_seq = crispr_data.loc[num, 'sgRNA Sequence']
        sgrna_seqs.append(sgrna_seq)
    pam_sequences = [
    ]
    for num in input_nums:
        pam_sequence = crispr_data.loc[num, 'PAM Sequence']
        pam_sequences.append(pam_sequence)
    eff_scores = []
    for num in input_nums:
        eff_score = crispr_data.loc[num, 'On-Target Efficacy Score']
        eff_scores.append(eff_score)
    strands = []
    for num in input_nums:
        stra = crispr_data.loc[num, 'Strand of sgRNA']
        strands.append(stra)
    cut_sites = []
    for num in input_nums:
        if mechanism == 'CRISPRa':
            cut_site = crispr_data.loc[num, "sgRNA 'Cut' Site TSS Offset"]
        else:
            cut_site = crispr_data.loc[num, "sgRNA 'Cut' Site TSS Offset"]
        cut_sites.append(cut_site)
    ref_seq = crispr_data.loc[input_nums[0], 'Reference Sequence']
    ref_start = ref_seq.find('_')
    ref_end = ref_seq.find('.')
    chromosome_num = ref_seq[ref_start+1:ref_end]
    chromosome_num = int(chromosome_num)
    crispr_mechanism = crispr_data.loc[input_nums[0], 'CRISPR Mechanism']
    pam_policy = crispr_data.loc[input_nums[0], 'PAM Policy']
    mechanism_pam = crispr_mechanism + '-' + pam_policy
    table_data = []
    for x in range(len(sgrna_seqs)):
        data = ['C'+str(x+1) + ':' + sgrna_seqs[x]+ '+' + pam_sequences[x], strands[x], cut_sites[x], eff_scores[x]]
        table_data.append(data)
    columns = (textwrap.fill('sgRNA Sequence + PAM'), textwrap.fill('Strand'),textwrap.fill('sgRNA Cut Offset'),
               textwrap.fill('On-Target Score'))
    rows = []
    for x in range(len(sgrna_seqs)):
        rows.append(gene_name)
    cell_text = []
    for row in range(len(rows)):
        y_offset = table_data[row]
        cell_text.append([x for x in y_offset])
    cell_text.reverse()
    features = []
    tss_start = sub_sequence.find(tss_sequence)
    tss_end = tss_start + 1
    tss_feature = GraphicFeature(start=tss_start, end=tss_end, strand=strand_dir, color="#ff66ff", label='TSS',
                                 label_link_color='auto')
    features.append(tss_feature)
    for index, sequence in enumerate(crispr_list_new):
        strand = strands[index]
        seq_start = sub_sequence.find(sequence)
        seq_end = seq_start + len(sequence)
        feature = GraphicFeature(start=seq_start, end=seq_end, strand=strand,color="#ff66ff", label='C'+str(index+1), label_link_color='auto')
        features.append(feature)

    graph_start = 0
    graph_end = 0
    if (strand_dir == 1):
        graph_start = exon_intervals[0][0]
        graph_end = exon_intervals[-1][-1]
    else:
        graph_start = exon_intervals[-1][0]
        graph_end = exon_intervals[0][1]
    record = GraphicRecord(sequence_length=sequence_length, features=features)
    fig = makeplot(gene_name, mechanism_pam, chromosome_num, graph_start, gene_start, graph_end, gene_end,
                   full_sequence, cell_text, columns, record, strand_dir, end=end)
    fig.savefig(folder_path+mechanism+'/'+(gene_name+'-'+mechanism)+'.png')


if __name__ == "__main__":
    mode = 'draw_gene_for_ko'   # CHOICES: 'get_gene_data', 'draw_gene_for_ko', 'draw_gene_seq_for_activation_mechs',
    dir = r'C:\Users\neel\Documents\GitHub\webGlycoEnzDB\djangoProject\webGlycoEnzDB\static\CRISPR' + '/'
    ensembl = EnsemblRelease(109)
    infile = ('gene_transcript.xlsx')
    outfile = 'introns2.csv'
    if mode == 'get_gene_data':
        get_gene_data(ensembl, dir, infile, outfile)
    elif mode == 'draw_gene_for_ko':
        data = pd.read_excel(dir + infile)
        transcripts = data['ENSEMBL']
        for num in range(380, len(transcripts)):
            print(num)
            transcriptID = transcripts[num]
            transcript = ensembl.transcript_by_id(transcriptID)
            gene_id = transcript.gene_id
            draw_CRISPR_site_for_ko(dir, ensembl, gene_id)

    elif mode == 'draw_gene_seq_for_activation_mechs':
        data = pd.read_excel(dir + infile)
        transcripts = data['ENSEMBL']
        for num in range(180, len(transcripts)):
#        num = random.randint(0, len(transcripts) - 1)
            print(num)
            transcriptID = transcripts[num]
            transcript = ensembl.transcript_by_id(transcriptID)
            geneID = transcript.gene_id
            draw_CRISPR_site_for_activated_deactivated(dir, ensembl, geneID, 'CRISPRi')  # can be 'CRISPRi' or 'CRISPRa'


    elif mode == 'extract_CRISPR_data':
        extract_CRISPR_sequences(ensembl=ensembl)
    else:
        print('Incorrect mode')