# Programming languages for bioinformatics
The idea of this project is to solidify my learning experience on programming languages by coding a core set of bioinformartics procedures and data models in each programming language I am learning.


## Tasks
The following are the data models and procedures that I will be implementing in each language

### Data models
All these data types will be based on a space and memory efficient way to store biological sequence data

- Nucleotide (including indel)
- Nucleotide sequence
- Codon
- Protein sequence
- Alignment (protein, codon, and nucleotide)
- Annotation
    - GFF
    - BED
    - VCF
    - BAM
- Phylogenetic tree (with branch lengths, support values, and annotations)

### Parsers
- GFF
- VCF
- BED
- BAM
- Fasta
- Fastq
- Newick

### Functions
- Spectrum analysis of fasta file
- Display phred quality score across squence length of fastq file
- Convert nucleotide to protein
- Convert protein to codons (given nuceotide and protein sequence)
- Calculate most recent common ancestor between two leaves of a phylogenetic tree
- NW alignment of two sequences
