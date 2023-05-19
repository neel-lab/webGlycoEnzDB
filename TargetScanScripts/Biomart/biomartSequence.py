import pandas as pd
from dna_features_viewer import GraphicFeature, GraphicRecord
import numpy as np
import os
from Bio.Seq import Seq


def graphicfeaturecreation(sequencestartend):
    featuresReturn = []
    start = list(map(lambda x: int(x), sequencestartend["cDNA Coding Start"].split(';')))
    end = list(map(lambda x: int(x), sequencestartend["cDNA Coding End"].split(';')))
    sorted_start = np.sort(start)
    sorted_end = np.sort(end)
    indexForEnd = 0
    for position in sorted_end:
        if indexForEnd == 0:
            #Starting Codon
            graphicFeatureHolder = GraphicFeature(start=int(sorted_start[indexForEnd]),
                                                  end=int(sorted_start[indexForEnd]) + 2,
                                                  label="Start", color="#ccccff", strand=+1)
            featuresReturn.append(graphicFeatureHolder)
            #Starting Exon
            graphicFeatureHolder = GraphicFeature(start=0,
                                                  end=int(sorted_end[indexForEnd]),
                                                  label="1", color="#ccccff", strand=+1)
            featuresReturn.append(graphicFeatureHolder)
            indexForEnd += 1
        elif indexForEnd == len(sorted_end) - 1:
            # End Codon
            graphicFeatureHolder = GraphicFeature(start=int(sorted_end[indexForEnd]) - 2,
                                                  end=int(sorted_end[indexForEnd]),
                                                  label="End", color="#ccccff", strand=+1)
            featuresReturn.append(graphicFeatureHolder)
            #Ending Exon
            graphicFeatureHolder = GraphicFeature(start=int(sorted_end[indexForEnd]) + 1,
                                                  end=int(sequencestartend["Transcript Length"]),
                                                  label=str(indexForEnd + 1), color="#ccccff", strand=+1)
            featuresReturn.append(graphicFeatureHolder)
        else:
            graphicFeatureHolder = GraphicFeature(start=sorted_start[indexForEnd], end=sorted_end[indexForEnd],
                                                  label=str(indexForEnd + 1), color="#ccccff", strand=+1)
            featuresReturn.append(graphicFeatureHolder)
            indexForEnd += 1

    return featuresReturn


if __name__ == '__main__':
    mirnaSequence = ""
    allSequences = []
    sequenceInfo = pd.DataFrame(columns=["Transcript Stable ID Version", "Gene Name", "Gene Stable ID",
                                               "Transcript Length", "cDNA Coding Start", "cDNA Coding End"])
    firstCount = 0
    with open("export_test.txt") as mytext:
        for line in mytext:
            trimmedlineNoNewLine = line.replace("\n", "")
            trimmedlineNoSymbol = trimmedlineNoNewLine.replace(">", "")
            splittedline = trimmedlineNoSymbol.split('|')
            if line[0] == '>':
                if firstCount == 0:
                    sequenceInfo.loc[len(sequenceInfo)] = [splittedline[0], splittedline[1],
                                                                       splittedline[2], splittedline[3],
                                                                       splittedline[4], splittedline[5]]
                    firstCount = 1
                    continue
                sequenceInfo.loc[len(sequenceInfo)] = [splittedline[0], splittedline[1], splittedline[2],
                                                       splittedline[3], splittedline[4], splittedline[5]]
                allSequences.append(mirnaSequence)
                mirnaSequence = ""
            else:
                mirnaSequence += trimmedlineNoSymbol
        allSequences.append(mirnaSequence)

    index = 0
    currentDirectory = os.getcwd()
    os.path.dirname(currentDirectory)

    mergedValues = pd.read_csv("..//TrimmedDataFiles//mergedValues.csv")
    dnaSequenceHolder = pd.DataFrame(columns=["DNA Seq"])
    for seedMatch in mergedValues["Seed+m8"]:
        rna_seq = Seq(seedMatch)
        dna_seq = rna_seq.back_transcribe().reverse_complement()
        dnaSequenceHolder.loc[len(dnaSequenceHolder)] = str(dna_seq)

    mergedValues['DNA Sequence'] = dnaSequenceHolder["DNA Seq"]

    features = graphicfeaturecreation(sequenceInfo.loc[index])
    record = GraphicRecord(sequence_length=len(allSequences[0]), features=features)
    ax, _ = record.plot(figure_width=20)
    record.plot_sequence(ax)
    ax.figure.savefig('sequencePlots//sequence ' + sequenceInfo.loc[index]["Transcript Stable ID Version"] + ".png")
    #record.plot_on_multiple_pages(
    #    "sequencePlots//multipage_plot.pdf",
    #    nucl_per_line=100,
    #    lines_per_page=7,
    #    plot_sequence=True
    #)


    #for sequence in allSequences:
    #    features = graphicfeaturecreation(sequenceInfo.loc[index])
    #    record = GraphicRecord(sequence=allSequences[0][0:10], features=features[0:1])
    #    ax, _ = record.plot()
    #    record.plot_sequence(ax)
    #    ax.figure.savefig("\sequencePlots\sequence_and_translation" + sequenceInfo.loc[index]["Gene Name"] + ".png",
    #                      bbox_inches='tight')
    #    index += 1

    # record = GraphicRecord(sequence=allSequences[0], features=features)
    # ax, _ = record.plot(figure_width=6)
    # ax.figure.savefig("testing.png")
