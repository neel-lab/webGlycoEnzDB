// Mapping to slide number (box number) in the pathway map image to the ontology tree seperated by '_' like 'Root_subtree' (same as element id)
const slide_to_pathway_mapping = {
    1: ['Donor synthesis_Nucleotide-sugar synthesis_NULL_NULL_NULL_NULL'],
    2: ['Transport_Donor transport_NULL_NULL_NULL_NULL'],
    3: ['Biosynthesis_Core_N-linked_Dolichol_NULL_NULL'],
    4: ['Biosynthesis_Core_N-linked_Trimming_NULL_NULL'],
    5: ['Biosynthesis_Core_N-linked_Branching_NULL_NULL'],
    6: ['Biosynthesis_Core_O-linked_O-GalNAc_NULL_NULL'],
    7: ['Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_NULL'],
    8: ['Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_Ganglioside'],
    9: ['Biosynthesis_Core_GAG_O-Xyl_NULL_NULL'],
    10: ['Biosynthesis_Core_GAG_Hyaluronan_NULL_NULL'],
    11: ['Biosynthesis_Core_O-linked_O-GlcNAc_NULL_NULL'],
    12: ['Biosynthesis_Core_Glycolipid_GPI-linked_NULL_NULL'],
    13: ['Biosynthesis_Core_O-linked_O-Mannose_TMTC-type_NULL'],
    14: ['Biosynthesis_Core_O-linked_O-Mannose_POMT-type_NULL'],
    15: ['Biosynthesis_Core_O-linked_O-Fucose_POFUT1-type_NULL'],
    16: ['Biosynthesis_Core_O-linked_O-Glucose_NULL_NULL'],
    17: ['Biosynthesis_Core_O-linked_EOGT_NULL_NULL'],
    18: ['Biosynthesis_Core_O-linked_O-Fucose_POFUT2-type_NULL'],
    19: ['Biosynthesis_Core_c-Mannose_NULL_NULL_NULL'],
    20: ['Biosynthesis_Elongation_Heparin sulfate elongation_NULL_NULL_NULL'],
    21: ['Biosynthesis_Elongation_Chondroitin/Dermatan sulfate elongation_NULL_NULL_NULL'],
    22: ['Biosynthesis_Elongation_Keratan sulfate elongation_NULL_NULL_NULL'],
    23: ['Biosynthesis_Elongation_LacdiNAc_NULL_NULL_NULL'],
    24: ['Biosynthesis_Elongation_LacNAc chain_NULL_NULL_NULL'],
    25: ['Biosynthesis_Capping_Sda_NULL_NULL_NULL'],
    26: ['Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_NULL'],
    27: ['Biosynthesis_Capping_Terminal fucosylation_NULL_NULL_NULL'],
    28: ['Biosynthesis_Capping_Terminal sialylation_NULL_NULL_NULL'],
    29: ['Biosynthesis_Capping_Terminal sulfation_NULL_NULL_NULL'],
    30: ['Degradation_N-linked_NULL_NULL_NULL_NULL'],
    31: ['Degradation_GAG_NULL_NULL_NULL_NULL'],
    32: ['Degradation_Glycolipid_NULL_NULL_NULL_NULL']
}
// Mapping the pathway to the pathway image html (generated from ppt to html tool (http://zamzar.com/) by converting individual slides) path in static/pathway_figures
// const pathway_image_map = {
//     'Donor synthesis_Nucleotide-sugar synthesis_NULL_NULL_NULL_NULL':['Nucleotide/Nucleotide.html'],
//     'Transport_Donor transport_NULL_NULL_NULL_NULL':['Nucleotide_Sugar_transport/Nucleotide_Sugar_transport.html'],
//     'Biosynthesis_Core_N-linked_Dolichol_NULL_NULL': ['Dolichol/Dolichol.html'],
//     'Biosynthesis_Core_N-linked_Trimming_NULL_NULL': ['N-linked/N-linked.html'],
//     'Biosynthesis_Core_N-linked_Branching_NULL_NULL': ['N-linked_Branching/N-linked_Branching.html'],
//     'Biosynthesis_Core_O-linked_O-GalNAc_NULL_NULL': ['O-linked_O-GalNAc/O-linked_O-GalNAc.html'],
//     'Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_NULL': ['Glycolipid/Glycolipid.html'],
//     'Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_Ganglioside':['Glycolipid_ganglioside/Glycolipid_ganglioside.html'],
//     'Biosynthesis_Core_GAG_O-Xyl_NULL_NULL':['cs_hs/cs_hs.html'],
//     'Biosynthesis_Core_GAG_Hyaluronan_NULL_NULL':['HAS/HAS.html'],
// };

const slide_file_path = {
    1: 'Nucleotide/Nucleotide.html',
    2: 'Nucleotide_Sugar_transport/Nucleotide_Sugar_transport.html',
    3: 'Dolichol/Dolichol.html',
    4: 'N-linked/N-linked.html',
    5: 'N-linked_Branching/N-linked_Branching.html',
    6: 'O-linked_O-GalNAc/O-linked_O-GalNAc.html',
    7: 'Glycolipid/Glycolipid.html',
    8: 'Glycolipid_ganglioside/Glycolipid_ganglioside.html',
    9: 'cs_hs/cs_hs.html',
    10: 'HAS/HAS.html',
    11: 'O-GlcNAc/O-GlcNAc.html',
    12: 'GPI-Biosynthetic_pathway/GPI-Biosynthetic_pathway.html',
    13: 'O-mannose/O-mannose.html',
    14: 'POMT/POMT.html',
    15: 'EGF/EGF.html',
    16: 'POFUT2/POFUT2.html',
    17: 'TSR/TSR.html',
    18: 'chondroitin_dermatan_sulfate/chondroitin_dermatan_sulfate.html',
    19: 'KS_bio/KS_bio.html',
    20: 'LacNac_chains/LacNac_chains.html',
    21: 'blood_group_i_antigen/blood_group_i_antigen.html',
    22: 'CT_Antigen/CT_Antigen.html',
    23: 'p1pk/p1pk.html',
    24: 'fucosylated_LacNAc/fucosylated_LacNAc.html',
    25: 'sialoglycans/sialoglycans.html',
    26: 'glycoproteins/glycoproteins.html',
    27: 'N-glycoproteins/N-glycoproteins.html',
    28: 'glycosaminoglycan/glycosaminoglycan.html',
    29: 'glycolipid_degradation/glycolipid_degradation.html'
};




// Gene Details = Welcome to GlycoEnzDB​
// Slide 1 = Cover slide with pathways listed​
// ​
// Box Number = Slide number [Pathway name]​
// 1=2 [Donor synthesis-> Nucleotide-sugar synthesis]​
// 2=3 [Pathway->Transport->Donor transport]​
// 3=4 [Pathway->Biosynthesis->Core-> N-linked->Dolichol]​
// 4=5 [Pathway->Biosynthesis->Core-> N-linked->Trimming]​
// 5=6 [Pathway->Biosynthesis->Core-> N-linked->Branching]​
// 6=7 [Pathway->Biosynthesis->Core-> O-linked->O-GalNAc]​
// 7=8 [Pathway->Biosynthesis->Core-> Glycolipid->GSL core->GlcCer related]​
// 8=9 [Pathway->Biosynthesis->Core-> Glycolipid->GSL core->GlcCer related->Ganglioside] [Pathway->Biosynthesis->Capping> Terminal sialic acid]  # I am not sure how to handle this as this figure has genes from two different pathways. Also, in Pathway, please change ‘Terminal sialic acid’ to ‘Terminal sialylation’​
// 9=10 [Pathway->Biosynthesis->Core-> GAG->O-Xyl]​
// 10=11 [Pathway->Biosynthesis->Core-> GAG->Hyaluronan]​
// 11=12 [Pathway->Biosynthesis->Core-> O-linked->O-GlcNAc]​
// 12=13 [Pathway->Biosynthesis->Core-> Glycolipid->GPI-linked]​
// 13=14 [Pathway->Biosynthesis->Core-> O-linked->O-Mannose->TMTC-type]​
// 14=15 [Pathway->Biosynthesis->Core-> O-linked->O-Mannose->POMT-type]​
// 15=16 [Pathway->Biosynthesis->Core-> O-linked->O-Fucose->POFUT1-type]​
// 16=16 [Pathway->Biosynthesis->Core-> O-linked->O-Glucose]​
// 17=16 [Pathway->Biosynthesis->Core-> O-linked->EOGT]​
// 18=17 [Pathway->Biosynthesis->Core-> O-linked->O-Fucose->POFUT2-type]​
// 19=18 [Pathway->Biosynthesis->Core->c-Mannose]​
// 20=19 [Pathway->Biosynthesis->Elongation>Heparan sulfate elongation] [Pathway->Biosynthesis->Capping> Terminal sulfation]  * Note in pathway menu it should be ‘Heparan’ and not ‘Heparin’ (there is a spelling error at the website)​
// 21=19 [Pathway->Biosynthesis->Elongation>Chondroitin/Dermatan sulfate elongation] [Pathway->Biosynthesis->Capping> Terminal sulfation] ​
// 22=20 [Pathway->Biosynthesis->Elongation>Keratan sulfate elongation] [Pathway->Biosynthesis->Capping> Terminal sulfation] ​
// 23=21 [Pathway->Biosynthesis->Elongation>LacNAc] [Pathway->Elongation>LacdiNAc]​
// 24=22 [Pathway->Biosynthesis->Elongation>LacNAc]​
// 25=23 [Pathway->Biosynthesis->Capping>Sda]​
// 26=24 [Pathway->Biosynthesis->Core-> Glycolipid->GSL core->GlcCer related]​
// 27=25 [Pathway->Biosynthesis->Capping>Terminal fucosylation]​
// 28=26 [Pathway->Biosynthesis->Capping>Terminal sialylation]​
// 29=27 [Pathway->Biosynthesis->Capping>Terminal sulfation]​
// 30=28 [Pathway->Degradation->N-linked]​
// 31=29 [Pathway->Biosynthesis->GAG]​
// 32=30 [Pathway->Biosynthesis->Glycolipid]  * Need to change ‘GSL’ to ‘Glycolipid’ in Pathway menu​
// ​
// Gene name  Figures <scroll>

PATHWAY_GENE_MAPPING = {
    1: 'HK1,HK2,HK3,GCK,G6PC1,GPI,MPI,PMM1,PMM2,GMPPA,GMPPB,GNPDA1,GNPDA2,NAGK,UAP1,GNPNAT1,GFPT1,GFPT2,GALK2,NANS,CMAS,DPM1,DPM2,DPM3,GMDS,TSTA3,FPGT,FCSK,GNE,GALE,GALK1,GALT,ALG5,UGP2,HGDH,UXS1,PGM1,PGM2,PGM3,CMAH,RENBP, CRPPA',
    2: 'SLC35A1, SLC35C1, SLC35D2, SLC35B4, SLC35D1, SLC35A3, SLC35A2, SLC35B2, SLC35B3',
    3: 'GPI, MPI, PMM2, GMPPA, GMPPB, DPAGT1, ALG13, ALG14, ALG1, ALG2, ALG11, ALG3, ALG9, DPM1, DPM2, DPM3, ALG9, ALG12, ALG6, ALG8, ALG10, STT3A, STT3B, RPN1, RPN2, DDOST, DAD1',
    4: 'MOGS, GANAB, CALR, CANX, EDEM1, EDEM2, EDEM3, UGGT1, UGGT2, MANB1, MAN1A1, MAN1A2, MAN1C1, GNPTAB, GNPTG, MGAT1, MGAT2, FUT8, MAN2A1, MAN2A2, SLC35A1, SLC35C1, NAGPA, ST6GAL1, ST3GAL4, B4GALT1',
    5: 'MGAT1, MGAT2, MGAT3, MGAT4A, MGAT4B, MGAT5, MGAT5B, MAN2A1, MAN2A2, FUT8',
    6: 'GALNT1, GALNT2, GALNT3, GALNT4, GALNT5, GALNT6, GALNT7, GALNT8, GALNT9, GALNT10, GALNT11, GALNT12, GALNT13, GALNT14, GALNT15, GALNT16, GALNT17, GALNT18, GALNT19, GALNT20, C1GALT1, C1GALT1C1, GCNT1, B4GALT1, ST6GALNAC1, ST3GAL1, B3GNT3, GCNT3, B3GALT5',
    7: 'B4GALT6, B4GALNT1, B3GNT5, A4GALT, A3GALT2, B3GALT4, B3GALT5, B4GALT1, B3GALNT1',
    8: 'UGT8, ST3GAL5, GAL3ST1, UGCG, B4GALT6, B4GALNT1, B3GALT4, ST3GAL2, ST3GAL3, ST3GAL4, ST6GALNAC3, ST6GALNAC4, ST6GALNAC5, ST6GALNAC6, ST8SIA1, ST8SIA3, ST8SIA5',
    9: 'XYLT1, XYLT2, B4GALT7, FAM20B, B3GALT6, B3GAT3, CSGALNACT1, CSGALNACT2, EXTL3',
    10: 'HAS1, HAS2, HAS3',
    11: 'OGT, OGA',
    12: 'PIGA, PIGH, PIGC, PIGO, PIGP, PIGY, DPM2, PIGL, PIGW, PIGM, PIGX, PIGV, PIGN, PIGB, PIGZ, PIGO, PIGG, GPAA1, PIGK, PIGT, PIGS, PIGU, PGAP1, PGAP2, PGAP3, PGAP4, PGAP5, B3GALT4',
    13: 'TMTC1, TMTC2, TMTC3, TMTC4',
    14: 'POMT1, POMT2, POMGNT1, POMGNT2, POMK, B3GALNT2, FKTN, FKRP, RXYLT1, B4GAT1, LARGE1, LARGE2, MGAT5B, B4GALT1, B4GALT2, B4GALT3, B3GAT1, B3GAT2, ST3GAL6, FUT4, FUT9',
    15: 'POFUT1, MFNG, LFNG, RFNG, POGLUT1, POGLUT2, POGLUT3, GXYLT1, GXYLT2, XXYLT1, EOGT',
    16: 'POFUT2, B3GLCT',
    17: 'DPY19L1, DPY19L2, DPY19L3, DPY19L4',
    18: 'XYLT1, XYLT2, B4GALT7, FAM20B, B3GALT6, B3GAT3, CSGALNACT1, CSGALNACT2, CHPF, CHPF2, CHSY1, CHSY3, UST, DSE, DSEL, CHST3, CHST7, CHST11, CHST12, CHST13, CHST14, CHST15, EXTL3, GLCE, NDST1, NDST2, NDST3, NDST4, HS2ST, HS3ST1, HS3ST2, HS3ST3a, HS3ST3b, HS3ST4, HS3ST5, HS3ST6, HS6ST1, HS6ST2, HS6ST3, EXTL1, EXT1, EXT2',
    19: 'CHST1, CHST2, CHST5, CHST6, B4GALT1, B4GALT4, B3GNT2, B3GNT7',
    20: 'B4GALT1, B4GALT2, B4GALT3, B4GALT4, B4GALT5, B3GNT2, B3GNT4, B3GNT8, B3GALT1, B3GALT2, B3GALT5, B4GALNT3, B4GALNT4',
    21: 'GCNT2, GCNT3, B3GNT2, B3GNT8, B4GALT1',
    22: 'B4GALNT2, B4GALNT1',
    23: 'A4GALT, B3GALNT1, B3GNT5, B3GALT5',
    24: 'FUT1, FUT2, FUT3, FUT4, FUT5, FUT6, FUT7, FUT9, ABO, ST3GAL3, ST3GAL4, ST3GAL6',
    25: 'ST3GAL1, ST3GAL4, ST6GAL1, ST6GALNAC1, ST6GALNAC2, ST6GALNAC3, ST6GALNAC4, C1GALT1, ST8SIA1, ST8SIA2, ST8SIA3, ST8SIA4, ST8SIA5, ST8SIA6',
    26: 'B3GAT1, B3GAT2, CHST10, CHST2, CHST4, CHST1',
    27: 'FUCA1, FUCA2, ENGASE, AGA, CTBS, NEU1, NEU2, NEU3, HEXA, HEXB, MAN2B1, MAN2B2, MANAB, MAN2C1',
    28: 'HPSE2, ARSG, HPSE, IDS, IDUA, SGSH, HGSNAT, NAGLU, ARSK, GUSB, GNS, IDU, ARSB, HEXA, HEXB, GALNS, GLB1, SULF1, SULF2',
    29: 'NAGA, GLA, GLB1, HEXA, HEXB, NEU1, NEU2, NEU3, NEU4, GBA1, GBA2, GBA3, GALC, ARSA',
}