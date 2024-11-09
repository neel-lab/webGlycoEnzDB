// Mapping to slide number (box number) in the pathway map image to the ontology tree seperated by '_' like 'Root_subtree' (same as element id)
const slide_to_pathway_mapping = {
    1:['Donor synthesis_Nucleotide-sugar synthesis_NULL_NULL_NULL_NULL'],
    2:['Transport_Donor transport_NULL_NULL_NULL_NULL'],
    3:['Biosynthesis_Core_N-linked_Dolichol_NULL_NULL'],
    4:['Biosynthesis_Core_N-linked_Trimming_NULL_NULL'],
    5:['Biosynthesis_Core_N-linked_Branching_NULL_NULL'],
    6:['Biosynthesis_Core_O-linked_O-GalNAc_NULL_NULL'],
    7:['Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_NULL'],
    8:['Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_Ganglioside', 'Biosynthesis_Capping_Terminal sialylation_NULL_NULL_NULL'],
    9:['Biosynthesis_Core_GAG_O-Xyl_NULL_NULL'],
    10:['Biosynthesis_Core_GAG_Hyaluronan_NULL_NULL'],
    11:['Biosynthesis_Core_O-linked_O-GlcNAc_NULL_NULL'],
    12:['Biosynthesis_Core_Glycolipid_GPI-linked_NULL_NULL'],
    13:['Biosynthesis_Core_O-linked_O-Mannose_TMTC-type_NULL'],
    14:['Biosynthesis_Core_O-linked_O-Mannose_POMT-type_NULL'],
    15:['Biosynthesis_Core_O-linked_O-Fucose_POFUT1-type_NULL'],
    16:['Biosynthesis_Core_O-linked_O-Glucose_NULL_NULL'],
    17:['Biosynthesis_Core_O-linked_EOGT_NULL_NULL'],
    18:['Biosynthesis_Core_O-linked_O-Fucose_POFUT2-type_NULL'],
    19:['Biosynthesis_Core_c-Mannose_NULL_NULL_NULL'],
    20:['Biosynthesis_Elongation_Heparin sulfate elongation_NULL_NULL_NULL'],
    21:['Biosynthesis_Elongation_Chondroitin/Dermatan sulfate elongation_NULL_NULL_NULL'],
    22:['Biosynthesis_Elongation_Keratan sulfate elongation_NULL_NULL_NULL'],
    23:['Biosynthesis_Elongation_LacdiNAc_NULL_NULL_NULL'],
    24:['Biosynthesis_Elongation_LacNAc chain_NULL_NULL_NULL'],
    25:['Biosynthesis_Capping_Sda_NULL_NULL_NULL'],
    26:['Biosynthesis_Core_Glycolipid_GSL core_GlcCer-related_NULL'],
    27:['Biosynthesis_Capping_Terminal fucosylation_NULL_NULL_NULL'],
    28:['Biosynthesis_Capping_Terminal sialylation_NULL_NULL_NULL'],
    29:['Biosynthesis_Capping_Terminal sulfation_NULL_NULL_NULL'],
    30:['Degradation_N-linked_NULL_NULL_NULL_NULL'],
    31:['Degradation_GAG_NULL_NULL_NULL_NULL'],
    32:['Degradation_Glycolipid_NULL_NULL_NULL_NULL']
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

