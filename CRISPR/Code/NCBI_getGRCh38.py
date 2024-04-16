from pyensembl import EnsemblRelease
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
import xmltodict

def sub_seq(gene_symbol = 'ST3GAL4', minus=-50, plus=300, ko=True):
    """
    Obtain genomic sequence for gene symbol in the region minus to plus from the TSS
    :param gene_symbol: HGNC gene symbol
    :param minus: position prior to the transcription start site
    :param plus: position after the transcription start site
    :param ko: If we are searching for CRISPR-KO then True, else false
    :return: sub_seq: sequence between minus and plus, tss_seq: first 20 bases following TSS, full_seq: full genomic seq,
    gene_start: start position of gene, gene_end: end position of gene on chromosome
    """
    search_term = f"GRCh38[Assembly] AND {gene_symbol}[Gene]"
    handle = Entrez.esearch(db="gene", term=search_term)
    record = Entrez.read(handle)
    ind = 0
    gene_id = record["IdList"][ind]

    # get start and end of gene by searching the "gene" database
    gene_record = Entrez.efetch(db="gene", id=gene_id, rettype="fasta", retmode="text")     # rettype can be 'gb' or 'xml'
    data = gene_record.read()
    Entrez.email = "shysriram206@gmail.com"     # Always tell NCBI who you are
    lines = data.split('\n')
    while(not(gene_symbol in lines[1])):
        ind +=1
        gene_id = record["IdList"][ind]
        gene_record = Entrez.efetch(db="gene", id=gene_id, rettype="fasta",
                                    retmode="text")  # rettype can be 'gb' or 'xml'
        data = gene_record.read()
        lines = data.split('\n')
    for line in lines:
        if line.startswith("Annotation:"):
            # Extract chromosome, db, start, and end from the line
            _, annotation = line.split(': ')
            field = annotation.split()
            chr = field[1]
            db = field[2]
            start_end = field[3]
            positions = start_end.replace('(', '').replace(')', '').replace(',', '')
            gene_start, gene_end = positions.split('..')
            if 'comp' in field[len(field) - 1]:
                strand = '-'
            else:
                strand = '+'
            break
        else:
            print("Annotation line not found.")
    if not(ko):
        gene_start = int(gene_start)
        gene_start -= 600
        gene_start = str(gene_start)
        gene_end = int(gene_end)
        gene_end +=600
        gene_end = str(gene_end)
    handle = Entrez.efetch(db="nucleotide", id=db, rettype="fasta", strand=1, seq_start=gene_start, seq_stop=gene_end)
    record = SeqIO.read(handle, "fasta")
    full_seq = record.seq
    if strand == '-':
        seq_obj = Seq(full_seq)
        full_seq = str(seq_obj.reverse_complement())

    # get transcription start site by looking at MANE transcripts
    search_term = f"{gene_symbol}[Gene] AND Homo sapiens[Organism] AND MANE_select[keyword]"
    handle1 = Entrez.esearch(db="nuccore", term=search_term)
    record1 = Entrez.read(handle1)
    ind_2 = 0
    gene_id = record1["IdList"][ind_2]
    gene_record = Entrez.efetch(db="nuccore", id=gene_id, rettype="xml")  # rettype="gb"
    xml_data = gene_record.read()
    xml_dict = xmltodict.parse(xml_data)
    gene_verification = xml_dict['GBSet']['GBSeq']['GBSeq_definition']
    while(not(gene_symbol in gene_verification)):
        ind_2 += 1
        gene_id = record1["IdList"][ind_2]
        gene_record = Entrez.efetch(db="nuccore", id=gene_id, rettype="xml")  # rettype="gb"
        xml_data = gene_record.read()
        xml_dict = xmltodict.parse(xml_data)
        gene_verification = xml_dict['GBSet']['GBSeq']['GBSeq_definition']

    tss_seq =xml_dict['GBSet']['GBSeq']['GBSeq_sequence'][0:20]
    tss_seq = tss_seq.upper()
    tss = full_seq.find(tss_seq)

    # get sub_seq
    start = max(0, tss + minus)
    end = min(tss + plus, len(full_seq)-1)
    sub_seq = full_seq[start:end]
    return sub_seq, tss_seq, full_seq, gene_start, gene_end
if __name__ == "__main__":
    sub_seq, tss_seq, full_seq, gene_start, gene_end = sub_seq('GLCE')
    print(sub_seq)