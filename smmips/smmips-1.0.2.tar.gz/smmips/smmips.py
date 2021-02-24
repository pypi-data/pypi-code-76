# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 12:54:35 2020

@author: rjovelin
"""

import argparse
import os
import json
import pysam
import time

from smmips.smmips_libs import align_fastqs, assign_reads_to_smmips, create_tree, read_panel, \
count_alleles_across_panel, write_table_variants, parse_cosmic, get_genomic_positions, remove_bam_extension, \
sort_index_bam, merge_smmip_counts, merge_stats, merge_bams




def align_reads(outdir, fastq1, fastq2, reference, bwa, prefix, remove):
    '''
    (str, str, str, str, str, str, str, bool) -> None 
     
    Parameters
    ----------
    - outdir (str): Path to directory where directory structure is created
    - fastq1 (str): Path to Fastq1
    - fastq2 (str): Path to Fastq2
    - reference (str): Path to the reference genome
    - bwa (str): Path to the bwa script
    - prefix (str): Prefix used to name the output files
    - remove (bool): Remove intermediate files if True                     
 
    Align fastq1 and fastq2 using bwa mem into coordinate-sorted and indexed bam in outdir/out.
    '''
    
    # use current directory if outdir not provided
    if outdir is None:
        outdir = os.getcwd()
    else:
        outdir = outdir
    # align fastqs
    prefix = os.path.basename(prefix)
    align_fastqs(fastq1, fastq2, reference, outdir, bwa, prefix, remove)


def assign_smmips(outdir, sortedbam, prefix, chromosome, remove, panel, upstream_nucleotides,
                  umi_length, max_subs, match, mismatch, gap_opening, gap_extension,
                  alignment_overlap_threshold, matches_threshold):
    '''
    (str, str, str, str, bool, str, int, int, int, float | int, float | int, float | int, float | int, float | int , float | int) -> None
    
    Parameters
    ----------
    - outdir (str): Path to directory where directory structure is created
    - sortedbam (str): Coordinate-sorted bam with all reads
    - prefix (str): Prefix used to name the output files
    - chromosome (str): Specifies the genomic region in the alignment file where reads are mapped 
                        Valid values:
                        - all: loop through all chromosomes in the bam
                        - chrA: specific chromosome. Format must correspond to the chromosome format in the bam file
    - remove (bool): Remove intermediate files if True                     
    - panel (str): Path to file with smmip information
    - upstream_nucleotides (int): Maximum number of nucleotides upstream the UMI sequence
    - umi_length (int): Length of the UMI    
    - max_subs (int): Maximum number of substitutions allowed in the probe sequence
    - match (float or int): Score of identical characters
    - mismatch (float or int): Score of non-identical characters
    - gap_opening (float or int): Score for opening a gap
    - gap_extension (float or int): Score for extending an open gap
    - alignment_overlap_threshold (float or int): Cut-off value for the length of the de-gapped overlap between read1 and read2 
    - matches_threshold (float or int): Cut-off value for the number of matching positions within the de-gapped overlap between read1 and read2 
 
    Write assigned reads, assigned but empty smmips and unassigned
    reads to 3 separate output bams, coordinate-sorted and indexed.
    Assigned reads are tagged with the smMip name and the extracted UMI sequence.
    Also write 2 json files in outdir/stats for QC
    with counts of total, assigned and unassigned read along with empty smmips,
    and read count for each smmip in the panel
    '''
    
    # record time spent smmip assignment
    start_time = time.time()
    
    # use current directory if outdir not provided
    if outdir is None:
        outdir = os.getcwd()
    else:
        outdir = outdir
    # create directory structure within outdir, including outdir if doesn't exist
    finaldir, statsdir, aligndir = create_tree(outdir)
    
    # align fastqs
    prefix = os.path.basename(prefix)
    
    # open files for writing
    
    # create AlignmentFile object to read input bam
    infile = pysam.AlignmentFile(sortedbam, 'rb')
    # create AlignmentFile objects for writing reads
    if chromosome == 'all':
        # create a new file, use header from bamfile
        assigned_filename = remove_bam_extension(sortedbam) + '.assigned_reads.bam'
        # open bams for writing unassigned reads. use header from bamfile
        unassigned_filename = remove_bam_extension(sortedbam) + '.unassigned_reads.bam'
        # open bam for writing assigned but empty reads
        empty_filename = remove_bam_extension(sortedbam) + '.empty_reads.bam'
    else:
        # create a new file, use header from bamfile
        assigned_filename = remove_bam_extension(sortedbam) + '.{0}.temp.assigned_reads.bam'.format(chromosome)
        # open bams for writing unassigned reads. use header from bamfile
        unassigned_filename = remove_bam_extension(sortedbam) + '.{0}.temp.unassigned_reads.bam'.format(chromosome)
        # open bam for writing assigned but empty reads
        empty_filename = remove_bam_extension(sortedbam) + '.{0}.temp.empty_reads.bam'.format(chromosome)
    assigned_file = pysam.AlignmentFile(assigned_filename, 'wb', template=infile)
    unassigned_file = pysam.AlignmentFile(unassigned_filename, 'wb', template=infile)
    empty_file = pysam.AlignmentFile(empty_filename, 'wb', template=infile)
    
    # close sortedbam
    infile.close()
    
    # assign reads to smmips
    metrics, smmip_counts = assign_reads_to_smmips(sortedbam, assigned_file, unassigned_file, empty_file, chromosome, read_panel(panel), upstream_nucleotides, umi_length, max_subs, match, mismatch, gap_opening, gap_extension, alignment_overlap_threshold, matches_threshold)
    
    # close bams    
    for i in [assigned_file, unassigned_file, empty_file]:
        i.close()
        
    # sort and index bams
    if chromosome == 'all':
        sort_index_bam(assigned_filename, '.assigned_reads.sorted.bam')
        sort_index_bam(unassigned_filename, '.unassigned_reads.sorted.bam')
        sort_index_bam(empty_filename, '.empty_reads.sorted.bam')
    else:
        sort_index_bam(assigned_filename, '.temp.assigned_reads.sorted.bam')
        sort_index_bam(unassigned_filename, '.temp.unassigned_reads.sorted.bam')
        sort_index_bam(empty_filename, '.temp.empty_reads.sorted.bam')
    
    # remove intermediate files
    if remove:
        os.remove(assigned_filename)
        os.remove(unassigned_filename)
        os.remove(empty_filename)
    
    # record time after smmip assignment and update QC metrics
    end_time = time.time()
    run_time = round(end_time - start_time, 3)
    metrics.update({'run_time': run_time})
    
    # write json to files
    if chromosome == 'all':
        statsfile1 = os.path.join(statsdir, '{0}_extraction_metrics.json'.format(prefix))
        statsfile2 = os.path.join(statsdir, '{0}_smmip_counts.json'.format(prefix))
    else:
        statsfile1 = os.path.join(statsdir, '{0}_temp.{1}.extraction_metrics.json'.format(prefix, chromosome))
        statsfile2 = os.path.join(statsdir, '{0}_temp.{1}.smmip_counts.json'.format(prefix, chromosome))
    with open(statsfile1, 'w') as newfile:
        json.dump(metrics, newfile, indent=4)
    with open(statsfile2, 'w') as newfile:
        json.dump(smmip_counts, newfile, indent=4)
   

def merge_chromosome_files(outdir, remove):
    '''
    (str, bool) -> None

    Merges all the stats files and the alignment files for each chromosome into
    single stats files and a single bam. The bam is indexed and coordinate-sorted
    
    Parameters
    ----------
    - outdir (str): Path to directory where directory structure is created
    - remove (bool): Remove intermediate files if True                     
    '''
    
    # merge stats files
    statsDir = os.path.join(outdir, 'stats')
    
    # merge smmips counts
    F1 = [os.path.join(statsDir, i) for i in os.listdir(statsDir) if 'temp' in i and 'smmip_counts.json' in i]
    L1 = []
    for i in F1:
        infile = open(i)
        L1.append(json.load(infile))
        infile.close()
    smmip_counts = merge_smmip_counts(L1)

    # merge read counts
    F2 = [os.path.join(statsDir, i) for i in os.listdir(statsDir) if 'temp' in i and 'extraction_metrics.json' in i]
    L2= []
    for i in F2:
        infile = open(i)
        L2.append(json.load(infile))
        infile.close()
    read_counts = merge_stats(L2)

    # get prefix name
    prefix = os.path.basename(F2[0][:F2[0].index('_temp')])
    
    statsfile1 = os.path.join(statsDir, '{0}_smmip_counts.json'.format(prefix))
    statsfile2 = os.path.join(statsDir, '{0}_extraction_metrics.json'.format(prefix))
        
    with open(statsfile1, 'w') as newfile:
        json.dump(smmip_counts, newfile, indent=4)
    with open(statsfile2, 'w') as newfile:
        json.dump(read_counts, newfile, indent=4)

    # merge bam files
    finalDir = os.path.join(outdir, 'out')
    assigned = [os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.assigned_reads.sorted.bam' in i and i[i.index('temp.assigned_reads.sorted.bam'):] == 'temp.assigned_reads.sorted.bam']
    unassigned = [os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.unassigned_reads.sorted.bam' in i and i[i.index('temp.unassigned_reads.sorted.bam'):] == 'temp.unassigned_reads.sorted.bam']
    empty = [os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.empty_reads.sorted.bam' in i and i[i.index('temp.empty_reads.sorted.bam'):] == 'temp.empty_reads.sorted.bam']
    
    assigned_filename = os.path.join(finalDir, prefix + '.assigned_reads.bam')
    unassigned_filename = os.path.join(finalDir, prefix + '.unassigned_reads.bam')
    empty_filename = os.path.join(finalDir, prefix + '.empty_reads.bam')
    
    merge_bams(assigned_filename, assigned)
    merge_bams(unassigned_filename, unassigned)
    merge_bams(empty_filename, empty)
    
    # sort and index merged bams
    sort_index_bam(assigned_filename, '.assigned_reads.sorted.bam')
    sort_index_bam(unassigned_filename, '.unassigned_reads.sorted.bam')
    sort_index_bam(empty_filename, '.empty_reads.sorted.bam')
    
    # remove intermediate files
    if remove:
        # make a list of intermediate files:
        L = [os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.assigned_reads.bam' in i]
        L.extend([os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.unassigned_reads.bam' in i])
        L.extend([os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.empty_reads.bam' in i])
        L.extend([os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.assigned_reads.sorted.bam' in i])
        L.extend([os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.unassigned_reads.sorted.bam' in i])
        L.extend([os.path.join(finalDir, i) for i in os.listdir(finalDir) if 'temp.empty_reads.sorted.bam' in i])
        for i in F1 + F2 + L + [assigned_filename, unassigned_filename, empty_filename]:
            os.remove(i)
        
   
def count_variants(bamfile, panel, outdir, max_depth, truncate, ignore_orphans,
                   stepper, prefix, reference, cosmicfile):
    '''
    (str, str, str, int, bool, bool, str, str, str) -> None
   
    Parameters
    ----------
    - bamfile (str): Path to the coordinate-sorted and indexed bam file with annotated reads with smMIP and UMI tags
    - panel (str): Path to panel file with smMIP information
    - outdir (str): Path to output directory where out directory is written
    - max_depth (int): Maximum read depth
    - truncate: Consider only pileup columns within interval defined by region start and end if True
    - ignore_orphans: Ignore orphan reads (paired reads not in proper pair) if True
    - stepper: Controls how the iterator advances. Accepted values:
               'all': skip reads with following flags: BAM_FUNMAP, BAM_FSECONDARY, BAM_FQCFAIL, BAM_FDUP
               'nofilter': uses every single read turning off any filtering
    - prefix (str): Prefix used to name the output bam file
    - reference (str): Reference genome. Must be the same reference used in panel. Accepted values: 37 or 38
    - cosmicfile (str): Cosmic file. Tab separated table of all COSMIC coding
                        point mutations from targeted and genome wide screens
    
    Write a summary table with nucleotide and indel counts at each unique position of
    the target regions in panel.
    '''
    
    # use current directory if outdir not provided
    if outdir == None:
        outdir = os.getcwd()
    else:
        outdir = outdir
    # create directory structure within outdir, including outdir if doesn't exist
    finaldir, statsdir, aligndir = create_tree(outdir)

    # get the allele counts at each position across all target regions
    Counts = count_alleles_across_panel(bamfile, read_panel(panel), max_depth, truncate, ignore_orphans, stepper)
    # get positions at each chromosome with variant information
    positions = get_genomic_positions(Counts)
    # get cosmic mutation information
    mutations = parse_cosmic(reference, cosmicfile, positions)

    # write base counts to file
    outputfile = os.path.join(finaldir, '{0}_Variant_Counts.txt'.format(prefix))
    write_table_variants(Counts, outputfile, mutations)


def main():
    '''
    main function to run the smmips script
    '''
    
    # create main parser    
    parser = argparse.ArgumentParser(prog='smmip.py', description="A tool to analyse smMIP libraries")
    subparsers = parser.add_subparsers(help='sub-command help', dest='subparser_name')
       		
    
    # align reads
    al_parser = subparsers.add_parser('align', help='Align reads to reference genome')
    al_parser.add_argument('-f1', '--Fastq1', dest='fastq1', help = 'Path to Fastq1', required=True)
    al_parser.add_argument('-f2', '--Fastq2', dest='fastq2', help = 'Path to Fastq2', required=True)
    al_parser.add_argument('-o', '--Outdir', dest='outdir', help = 'Path to outputd directory. Current directory if not provided')
    al_parser.add_argument('-r', '--Reference', dest='reference', help = 'Path to the reference genome', required=True)
    al_parser.add_argument('-bwa', '--Bwa', dest='bwa', help = 'Path to the bwa script', required=True)
    al_parser.add_argument('--remove', dest='remove', action='store_true', help = 'Remove intermediate files. Default is False, becomes True if used')
    al_parser.add_argument('-pf', '--Prefix', dest='prefix', help = 'Prefix used to name the output files', required=True)
    
    
    # assign smMips to reads
    a_parser = subparsers.add_parser('assign', help='Extract UMIs from reads and assign reads to smmips')
    a_parser.add_argument('-pa', '--Panel', dest='panel', help = 'Path to panel file with smmip information', required=True)
    a_parser.add_argument('-o', '--Outdir', dest='outdir', help = 'Path to outputd directory. Current directory if not provided')
    a_parser.add_argument('-c', '--Chromosome', dest='chromosome', default='all', help = 'Considers only the reads mapped to chromosome. Default is all chromosomes. Accepted values are "all", "chrA"')
    a_parser.add_argument('-b', '--BamFile', dest='sortedbam', help = 'Coordinate-sorted and indexed bam with all reads', required=True)
    a_parser.add_argument('--remove', dest='remove', action='store_true', help = 'Remove intermediate files. Default is False, becomes True if used')
    a_parser.add_argument('-pf', '--Prefix', dest='prefix', help = 'Prefix used to name the output files', required=True)
    a_parser.add_argument('-s', '--Subs', dest='max_subs', type=int, default=0, help = 'Maximum number of substitutions allowed in the probe sequence. Default is 0')
    a_parser.add_argument('-up', '--Upstream', dest='upstream_nucleotides', type=int, default=0, help = 'Maximum number of nucleotides upstream the UMI sequence. Default is 0')
    a_parser.add_argument('-umi', '--Umi', dest='umi_length', type=int, default=4, help = 'Length of the UMI sequence in bp. Default is 4')
    a_parser.add_argument('-m', '--Matches', dest='match', type=float, default=2, \
                          help = 'Score of identical characters during local alignment. Used only if report is True. Default is 2')
    a_parser.add_argument('-mm', '--Mismatches', dest='mismatch', type=float, default=-1, \
                          help = 'Score of non-identical characters during local alignment. Used only if report is True. Default is -1')
    a_parser.add_argument('-go', '--Gap_opening', dest='gap_opening', type=float, default=-5, \
                          help = 'Score for opening a gap during local alignment. Used only if report is True. Default is -5')
    a_parser.add_argument('-ge', '--Gap_extension', dest='gap_extension', type=float, default=-1, \
                          help = 'Score for extending an open gap during local alignment. Used only if report is True. Default is -1')
    a_parser.add_argument('-ao', '--Alignment_overlap', dest='alignment_overlap_threshold', type=int, default=60, \
                          help = 'Cut-off value for the length of the de-gapped overlap between read1 and read2. Default is 60bp')
    a_parser.add_argument('-mt', '--Matches_threshold', dest='matches_threshold', type=float, default=0.7, \
                          help = 'Cut-off value for the number of matching positions within the de-gapped overlap between read1 and read2. Used only if report is True. Default is 0.7')
    
    # merge chromosome-level files
    m_parser = subparsers.add_parser('merge', help='Merges all the chromosome-level stats and alignment files')
    m_parser.add_argument('-o', '--Outdir', dest='outdir', help = 'Path to outputd directory. Current directory if not provided')
    m_parser.add_argument('--remove', dest='remove', action='store_true', help = 'Remove intermediate files. Default is False, becomes True if used')
    
    ## Variant counts command
    v_parser = subparsers.add_parser('variant', help='Write table with variant counts across target regions')
    v_parser.add_argument('-b', '--Bam', dest='bamfile', help = 'Path to the coordinate-sorted and indexed input bam with UMI and smmip tags', required=True)
    v_parser.add_argument('-p', '--Panel', dest='panel', help = 'Path to panel file with smmip information', required=True)
    v_parser.add_argument('-o', '--Outdir', dest='outdir', help = 'Path to outputd directory. Current directory if not provided')
    v_parser.add_argument('-m', '--MaxDepth', dest='max_depth', default=1000000, type=int, help = 'Maximum read depth. Default is 1000000')
    v_parser.add_argument('-io', '--IgnoreOrphans', dest='ignore_orphans', action='store_true', help='Ignore orphans (paired reads that are not in a proper pair). Default is False, becomes True if used')
    v_parser.add_argument('-t', '--Truncate', dest='truncate', action='store_true', help='Only pileup columns in the exact region specificied are returned. Default is False, becomes True is used')
    v_parser.add_argument('-stp', '--Stepper', dest='stepper', choices=['all', 'nofilter'], default='nofilter',
                          help='Filter or include reads in the pileup. See pysam doc for behavior of the all or nofilter options. Default is nofilter')
    v_parser.add_argument('-pf', '--Prefix', dest='prefix', help = 'Prefix used to name the variant count table', required=True)
    v_parser.add_argument('-rf', '--Reference', dest='reference', type=str, choices=['37', '38'], help = 'Reference genome. Must be the same reference used in panel. Accepted values: 37 or 38', required=True)
    v_parser.add_argument('-c', '--Cosmic', dest='cosmicfile', help = 'Tab separated table of all COSMIC coding point mutations from targeted and genome wide screens', required=True)
    
    args = parser.parse_args()

    if args.subparser_name == 'align':
        try:
            align_reads(args.outdir, args.fastq1, args.fastq2, args.reference, args.bwa, args.prefix, args.remove)
        except AttributeError as e:
            print('#############\n')
            print('AttributeError: {0}\n'.format(e))
            print('#############\n\n')
            print(parser.format_help())
    elif args.subparser_name == 'assign':
        try:
            assign_smmips(args.outdir, args.sortedbam, args.prefix, args.chromosome, args.remove,
                          args.panel, args.upstream_nucleotides, args.umi_length, args.max_subs,
                          args.match, args.mismatch, args.gap_opening, args.gap_extension,
                          args.alignment_overlap_threshold, args.matches_threshold)
        except AttributeError as e:
            print('#############\n')
            print('AttributeError: {0}\n'.format(e))
            print('#############\n\n')
            print(parser.format_help())
    elif args.subparser_name == 'merge':
        try:
            merge_chromosome_files(args.outdir, args.remove)
        except AttributeError as e:
            print('#############\n')
            print('AttributeError: {0}\n'.format(e))
            print('#############\n\n')
            print(parser.format_help())
    elif args.subparser_name == 'variant':
        try:
            count_variants(args.bamfile, args.panel, args.outdir, args.max_depth, args.truncate, args.ignore_orphans,
                   args.stepper, args.prefix, args.reference, args.cosmicfile)
        except AttributeError as e:
            print('#############\n')
            print('AttributeError: {0}\n'.format(e))
            print('#############\n\n')
            print(parser.format_help())
    elif args.subparser_name is None:
        print(parser.format_help())