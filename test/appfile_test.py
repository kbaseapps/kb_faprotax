import os

from kb_faprotax.util.debug import dprint
from kb_faprotax.util.varstash import Var
from kb_faprotax.impl.workflow import parse_tax2groups, parse_tax_and_groups
from mock import TEST_DATA_DIR


def test_parse_tax2groups():
    """Test function used to parse FAPROTAX's predicted functions from its output"""

    fp = os.path.join(
        TEST_DATA_DIR,
        "return/refseq/return/FAPROTAX_output",
        Var.GROUPS2RECORDS_TABLE_DENSE_FN,
    )

    tax2groups_d = parse_tax2groups(fp)

    taxonomy = "\
cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Pseudomonadales; Moraxellaceae; \
Acinetobacter; Acinetobacter calcoaceticus/baumannii complex; Acinetobacter pittii"
    functions = "\
aerobic_chemoheterotrophy,human_pathogens_septicemia,human_pathogens_pneumonia,human_pathogens_nosocomia,\
human_pathogens_all,animal_parasites_or_symbionts,aromatic_compound_degradation,chemoheterotrophy"

    assert tax2groups_d[taxonomy] == functions


def test_parse_tax_and_groups():

    fp = os.path.join(
        TEST_DATA_DIR,
        "return/refseq/return/FAPROTAX_output",
        Var.GROUPS2RECORDS_TABLE_DENSE_FN,
    )

    tax, groups = parse_tax_and_groups(fp)

    assert tax == [
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Pseudomonadales; Moraxellaceae; Acinetobacter; Acinetobacter calcoaceticus/baumannii complex; Acinetobacter pittii",
        "cellular organisms; Bacteria; Terrabacteria group; Firmicutes; Bacilli; Bacillales; Bacillaceae; Bacillus; Bacillus subtilis group; Bacillus subtilis; Bacillus subtilis subsp. subtilis",
        "cellular organisms; Bacteria; Proteobacteria; delta/epsilon subdivisions; Epsilonproteobacteria; Campylobacterales; Campylobacteraceae; Campylobacter; Campylobacter jejuni; Campylobacter jejuni subsp. jejuni",
        "cellular organisms; Bacteria; Proteobacteria; Alphaproteobacteria; Caulobacterales; Caulobacteraceae; Caulobacter; Caulobacter vibrioides; Caulobacter vibrioides CB15",
        "cellular organisms; Bacteria; PVC group; Chlamydiae; Chlamydiia; Chlamydiales; Chlamydiaceae; Chlamydia/Chlamydophila group; Chlamydia; Chlamydia trachomatis",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Legionellales; Coxiellaceae; Coxiella; Coxiella burnetii",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Escherichia; Escherichia coli",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Escherichia; Escherichia coli; Escherichia coli O157:H7",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Klebsiella; Klebsiella pneumoniae; Klebsiella pneumoniae subsp. pneumoniae",
        "cellular organisms; Bacteria; Terrabacteria group; Firmicutes; Bacilli; Bacillales; Listeriaceae; Listeria; Listeria monocytogenes",
        "cellular organisms; Bacteria; Terrabacteria group; Actinobacteria; Actinobacteria; Corynebacteriales; Mycobacteriaceae; Mycobacterium; Mycobacterium tuberculosis complex; Mycobacterium tuberculosis",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Pseudomonadales; Pseudomonadaceae; Pseudomonas; Pseudomonas aeruginosa group; Pseudomonas aeruginosa",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Salmonella; Salmonella enterica; Salmonella enterica subsp. enterica; Salmonella enterica subsp. enterica serovar Typhimurium",
        "cellular organisms; Bacteria; Proteobacteria; Gammaproteobacteria; Enterobacterales; Enterobacteriaceae; Shigella; Shigella flexneri; Shigella flexneri 2a",
        "cellular organisms; Bacteria; Terrabacteria group; Firmicutes; Bacilli; Bacillales; Staphylococcaceae; Staphylococcus; Staphylococcus aureus; Staphylococcus aureus subsp. aureus",
    ]
    assert groups == [
        "aerobic_chemoheterotrophy,human_pathogens_septicemia,human_pathogens_pneumonia,human_pathogens_nosocomia,human_pathogens_all,animal_parasites_or_symbionts,aromatic_compound_degradation,chemoheterotrophy",
        "nitrate_ammonification,nitrite_ammonification,nitrite_respiration,cellulolysis,xylanolysis,ligninolysis,plant_pathogen,nitrate_respiration,nitrate_reduction,nitrogen_respiration,chemoheterotrophy",
        "human_pathogens_meningitis,human_pathogens_gastroenteritis,human_pathogens_diarrhea,human_pathogens_all,animal_parasites_or_symbionts,nitrate_respiration,nitrate_reduction,nitrogen_respiration,fumarate_respiration",
        "aerobic_chemoheterotrophy,chemoheterotrophy",
        "human_pathogens_all,animal_parasites_or_symbionts,intracellular_parasites",
        "human_pathogens_all,animal_parasites_or_symbionts,intracellular_parasites",
        "nitrite_ammonification,nitrite_respiration,fermentation,aerobic_chemoheterotrophy,human_pathogens_gastroenteritis,human_pathogens_diarrhea,human_pathogens_all,human_gut,mammal_gut,animal_parasites_or_symbionts,nitrate_respiration,nitrate_reduction,nitrogen_respiration,fumarate_respiration,chemoheterotrophy",
        "nitrite_ammonification,nitrite_respiration,fermentation,aerobic_chemoheterotrophy,human_pathogens_gastroenteritis,human_pathogens_diarrhea,human_pathogens_all,human_gut,mammal_gut,animal_parasites_or_symbionts,plant_pathogen,nitrate_respiration,nitrate_reduction,nitrogen_respiration,fumarate_respiration,chemoheterotrophy",
        "fermentation,aerobic_chemoheterotrophy,human_pathogens_septicemia,human_pathogens_pneumonia,human_pathogens_nosocomia,human_pathogens_all,human_gut,mammal_gut,animal_parasites_or_symbionts,nitrate_reduction,chemoheterotrophy",
        "fermentation,human_pathogens_all,animal_parasites_or_symbionts,chemoheterotrophy",
        "aerobic_chemoheterotrophy,human_pathogens_all,animal_parasites_or_symbionts,chemoheterotrophy",
        "nitrate_denitrification,nitrite_denitrification,nitrous_oxide_denitrification,denitrification,nitrite_respiration,dark_thiosulfate_oxidation,dark_oxidation_of_sulfur_compounds,aerobic_chemoheterotrophy,human_pathogens_septicemia,human_pathogens_pneumonia,human_pathogens_all,animal_parasites_or_symbionts,plant_pathogen,aromatic_hydrocarbon_degradation,aromatic_compound_degradation,hydrocarbon_degradation,nitrate_respiration,nitrate_reduction,nitrogen_respiration,plastic_degradation,chemoheterotrophy",
        "sulfite_respiration,thiosulfate_respiration,respiration_of_sulfur_compounds,fermentation,human_pathogens_gastroenteritis,human_pathogens_all,animal_parasites_or_symbionts,nitrate_reduction,chemoheterotrophy",
        "fermentation,human_pathogens_gastroenteritis,human_pathogens_all,animal_parasites_or_symbionts,nitrate_reduction,chemoheterotrophy",
        "human_pathogens_septicemia,human_pathogens_pneumonia,human_pathogens_gastroenteritis,human_pathogens_all,human_gut,mammal_gut,animal_parasites_or_symbionts,plant_pathogen,nitrate_reduction,ureolysis",
    ]
