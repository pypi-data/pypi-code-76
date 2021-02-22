#!/usr/bin/env python
# coding: utf-8

# import modules
import pysam
import pandas as pd
import numpy as np
import re
import os
import sys
import collections
import scipy
from scipy import stats
import statsmodels
import subprocess
import logging
from statsmodels.stats.multitest import fdrcorrection
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio import Seq


pd.options.mode.chained_assignment = None  # default='warn', this is used to remove warning from pandas chain assignment
np.seterr(divide = 'ignore') 
# np.seterr(divide = 'warn') 

try:
    from . import global_para
except ImportError:
    import global_para

try:
    from .consensus_seq import *
except ImportError:
    from consensus_seq import *

try:
    from .math_stat import *
except ImportError:
    from math_stat import *

try:
    from .unaligned_reads import *
except ImportError:
    from unaligned_reads import *

try:
    from .multi_processor import *
except ImportError:
    from multi_processor import *

try:
    from .set_log import *
except ImportError:
    from set_log import *

try:
    from .clipped_seq_source_inference import *
except ImportError:
    from clipped_seq_source_inference import *

os.chdir(global_para.output_dir)


def detect_cdna(global_para):
# 1. check if bam index exist
check_bam_index(global_para.genome_bam_file)
global_para.genome_bam_paired = bam_ispair()
# 1.1 check output directory exist, if not, create it
if os.path.isdir(global_para.output_dir):
    pass
else:
    os.makedirs(global_para.output_dir)
# 1.2 use the logger file
logger = set_logger()
logger.info('Begin to process sample: %s'%global_para.genome_bam_file)

# 2. load gene module file
df_gene_exon_unique = read_gene_model(global_para.gtf_gene_unique_file)
df_gene_exon_unique = df_gene_exon_unique.astype({'seqname': 'str'})
df_gene_exon_unique = df_gene_exon_unique.fillna('')
overlap_reference = f_overlap_reference(global_para.genome_bam_file,df_gene_exon_unique)
if len(overlap_reference)==0:
    logger.error('chromosome names are note matched between gene model and bam file')
    exit(1)
df_gene_exon_unique = df_gene_exon_unique.query('seqname in @overlap_reference')
df_gene_exon_unique = f_exon_group_by_distance(df_gene_exon_unique)

## 3. get background information unaligned list
logger.info('Start scanning exon regions...')
x = apply_parallel(df_gene_exon_unique.groupby('read_group'),f_find_unalign_readlist_multi)
global_para.num_total_read_exon = sum([i[0] for i in x]) 
global_para.num_unalign_read = sum([i[1] for i in x]) 

## if no reads satisfy the cutoff, then exit the program
if global_para.num_total_read_exon>0:
    p_unalign_read = global_para.num_unalign_read/global_para.num_total_read_exon
else:
    f_0cdna(logger)        
if p_unalign_read>=0.2:
    logger.warning("Warning: Proportion of clipped reads in exon regions is high! Pay attention to detected cDNAs (if detected).")
logger.info('Proportion of soft-clipped reads is: %0.3f\n'%(p_unalign_read))

## 4. filter gene exon regions which unaligned reads around edge information are suitable
df_gene_exon_unique['num_unalign_read'] = [i for sublist in x for i in sublist[2]]
df_gene_exon_unique['num_unalign_read_exon_edge'] = [i for sublist in x for i in sublist[3]]
df_gene_exon_unique['num_all_read_exon_edge'] = [i for sublist in x for i in sublist[4]]
df_gene_exon_unique['num_bg_total_read_exon'] = global_para.num_total_read_exon
df_gene_exon_unique['num_bg_unalign_read_exon'] = global_para.num_unalign_read
df_gene_exon_unique['pvalue'] = df_gene_exon_unique.apply(lambda x:beta_binomial_significance(x.num_unalign_read_exon_edge, x.num_all_read_exon_edge, x.num_bg_unalign_read_exon, x.num_bg_total_read_exon),axis = 1)
df_gene_exon_unique['region'] = df_gene_exon_unique.apply(lambda x:x['gene_name'] + "|" + x['seqname'] + ':' + str(x['start']) + "-" + str(x['end']), axis = 1)

df_gene_exon_unique_expand_t = f_expand_by_transcript(df_gene_exon_unique)


tmp_genelist_unaligned_reads_filter1 = df_gene_exon_unique_expand_t.query('read_transcript>=cutoff_transcript_read')['gene_name'].unique().tolist()
# df_gene_exon_unique.to_csv(global_para.out_log + '.xls', sep = '\t')

if len(tmp_genelist_unaligned_reads_filter1)<=1000:
    tmp_genelist_unaligned_reads_filter = tmp_genelist_unaligned_reads_filter1
    if len(tmp_genelist_unaligned_reads_filter)==0:
        f_0cdna(logger)    
    df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t.query('(gene_name in @tmp_genelist_unaligned_reads_filter) and (num_unalign_read_exon_edge>=@global_para.cutoff_num_exon_unaligned_reads)')
    n_transcript_detect = df_gene_exon_unique_expand_t_filter.groupby(['transcript_split'])['transcript_split'].count()
    n_transcript_detect.name = 'n_transcript_detect'
    df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t_filter.merge(pd.DataFrame(n_transcript_detect),left_on = 'transcript_split', right_index = True).merge(pd.DataFrame(n_transcript_detect),left_on = 'transcript_split', right_index = True)
    df_gene_exon_unique_expand_t_filter['ratio'] = df_gene_exon_unique_expand_t_filter.apply(lambda x:x.n_transcript_detect_x/x.n_transcript,axis = 1)
    df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t_filter.query('ratio>=@global_para.cutoff_ratio_gene')
else:
    tmp_genelist_unaligned_reads_filter2 = df_gene_exon_unique_expand_t.query('pvalue<=@global_para.cutoff_pvalue').gene_name.unique().tolist()
    tmp_genelist_unaligned_reads_filter = list(set(tmp_genelist_unaligned_reads_filter1) & set(tmp_genelist_unaligned_reads_filter2))
    if len(tmp_genelist_unaligned_reads_filter)==0:
        f_0cdna(logger)    
    df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t.query('(gene_name in @tmp_genelist_unaligned_reads_filter) and (num_unalign_read_exon_edge>=@global_para.cutoff_num_exon_unaligned_reads) and pvalue<=@global_para.cutoff_pvalue')
    n_transcript_detect = df_gene_exon_unique_expand_t_filter.groupby(['transcript_split'])['transcript_split'].count()
    n_transcript_detect.name = 'n_transcript_detect'
    df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t_filter.merge(pd.DataFrame(n_transcript_detect),left_on = 'transcript_split', right_index = True).merge(pd.DataFrame(n_transcript_detect),left_on = 'transcript_split', right_index = True)
    df_gene_exon_unique_expand_t_filter['ratio'] = df_gene_exon_unique_expand_t_filter.apply(lambda x:x.n_transcript_detect_x/x.n_transcript,axis = 1)
    df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t_filter.query('ratio>=@global_para.cutoff_ratio_gene')
    if len(df_gene_exon_unique_expand_t_filter.gene_name.unique())>=1000:
        tmp_gene_filter = df_gene_exon_unique_expand_t_filter.sort_values('pvalue')['gene_name'].unique()[0:1000]
        df_gene_exon_unique_expand_t_filter = df_gene_exon_unique_expand_t_filter.query('gene_name in @tmp_gene_filter')



df_gene_exon_unique_filter_exon = df_gene_exon_unique.query('region in @df_gene_exon_unique_expand_t_filter.region.unique().tolist()')

logger.info('Evaluating %d potential candidate cDNA(s) ......'%len(df_gene_exon_unique_filter_exon.gene_name.unique()))
## 5. stat reads around exon edges for each regions.
list_stat_all_region = list()
list_stat_all_region_fdr = list()
for gene, df_gene in df_gene_exon_unique_filter_exon.groupby(['gene_name']):
    print(gene)
    df_gene = df_gene_exon_unique_filter_exon.query('gene_name==@gene')
    list_stat_start = list()
    list_stat_end = list();
    for region, df_exon in df_gene.groupby('region'):
        list_stat_start.append(f_df_exon_start_stat(df_exon))
        list_stat_end.append(f_df_exon_end_stat(df_exon))
    df_stat_start = pd.concat(list_stat_start)
    df_stat_end = pd.concat(list_stat_end)
    if len(df_stat_start)==0 or len(df_stat_end)==0:
        continue
    df_stat_start = f_df_gene_start_stat_remove_dup(df_stat_start)
    df_stat_end = f_df_gene_end_stat_remove_dup(df_stat_end)
    # 5.2 merge reads in start/end to whole exons
    df_gene = df_gene.merge(df_stat_start, left_on = "region",right_on = "region_start" ,suffixes = ("","_start"), how = "left")
    df_gene = df_gene.merge(df_stat_end, left_on = "region",right_on = "region_end", suffixes = ("","_end"), how = "left")
    # 5.2.1 remove duplication information
    df_gene = f_df_gene_merge_removedup(df_gene)
    if len(df_gene)==0:
        continue
    # adjust most-left position
    df_exon_start = df_gene.query('is_exon_boundary_start=="1"')
    for tmp_index_start in df_exon_start.index.tolist():
        tmp_df_exon_start = df_gene.loc[tmp_index_start]
        if tmp_df_exon_start.is_exon_match_end and tmp_df_exon_start.bbinom_p_end <= global_para.cutoff_pvalue and tmp_df_exon_start.bbinom_p_start >=0.05:
            df_gene.loc[tmp_index_start] = exon_start_adj(tmp_df_exon_start)
    # ajust for exon end position
    df_exon_end = df_gene.query('is_exon_boundary_end=="1"')
    for tmp_index_end in df_exon_end.index.tolist():
        tmp_df_exon_end = df_gene.loc[tmp_index_end]
        if tmp_df_exon_end.is_exon_match_start and tmp_df_exon_end.bbinom_p_start <= global_para.cutoff_pvalue and tmp_df_exon_end.bbinom_p_end >=0.05:
            df_gene.loc[tmp_index_end] = exon_end_adj(tmp_df_exon_end)
    # generate clipped sequences for gene
    df_gene['combine_pvalue'] = df_gene.apply(lambda x:f_combin_p([x.bbinom_p_start,x.bbinom_p_end]),axis = 1)
    df_gene['clipped_seq_start'] = df_gene.apply(lambda x:x.consensus_seq_start[::-1],axis = 1)
    df_gene['clipped_seq_end'] = df_gene.consensus_seq_end
    list_stat_all_region_fdr.append(df_gene)




是我的代码变了吗？怎么结果是OK的。
。。。。



if len(list_stat_all_region_fdr)==0:
    f_0cdna(logger)
df_gene_fdr = pd.concat(list_stat_all_region_fdr)
df_gene_fdr['combine_qvalue'] = fdrcorrection(df_gene_fdr['combine_pvalue'])[1]
# for gene, df_gene in df_gene_fdr.groupby(['gene_name']):
#     df_gene['is_exon_keep'] = df_gene.apply(lambda x:f_exon_filter(x, global_para),axis = 1)
#     select_columns =        ['seqname', 'start', 'end', 'pos_start',          'pos_end','gene_id', 'gene_name','transcript','num_bad_reads_ajust_start', 'num_all_reads_ajust_start',  'bbinom_p_start', 'num_bad_reads_ajust_end', 'num_all_reads_ajust_end','bbinom_p_end','bg_unalign_start', 'bg_total_start','combine_pvalue', 'combine_qvalue']
#     select_columns_rename = ['seqname', 'exon_start', 'exon_end', 'pos_start','pos_end','gene_id', 'gene_name','transcript','num_clipped_start', 'num_total_start',  'bbinom_pvalue_start','num_clipped_end', 'num_total_end',  'bbinom_pvalue_end','num_bg_clipped', 'num_bg_total','combine_pvalue', 'combine_qvalue']
#     df_gene_filter = df_gene.query('is_exon_keep==True').filter(select_columns)
#     df_gene_filter.columns = select_columns_rename
#     list_stat_all_region.append(df_gene_filter)

# for gene_name, df_gene in df_gene_fdr.groupby('gene_name'):
#     df_gene['is_exon_keep'] = df_gene.apply(lambda x:f_exon_filter(x, global_para),axis = 1)
#     df_gene_filter = df_gene.query('is_exon_keep==True')
#     if len(df_gene_filter)>=1:
#         tmp1= df_gene.query('is_exon_boundary_start=="1"').query('is_exon_match_end==True').query('combine_qvalue<@global_para.cutoff_pvalue')
#         tmp2= df_gene.query('is_exon_boundary_end=="1"').query('is_exon_match_start==True').query('combine_qvalue<@global_para.cutoff_pvalue')
#         df_gene_filter = pd.concat([df_gene_filter,tmp1,tmp2])
#         df_gene_filter = df_gene_filter.drop_duplicates()
#     list_stat_all_region.append(df_gene_filter)


for gene_name, df_gene in df_gene_fdr.groupby('gene_name'):
    df_gene['is_exon_keep'] = df_gene.apply(lambda x:f_exon_filter(x, global_para),axis = 1)
    df_gene_filter = df_gene.query('is_exon_keep==True')
    if len(df_gene_filter)>=1:
        tmp1= df_gene.query('is_exon_boundary_start=="1"').query('is_exon_match_end==True').query('bbinom_p_end<@global_para.cutoff_pvalue')
        tmp2= df_gene.query('is_exon_boundary_end=="1"').query('is_exon_match_start==True').query('bbinom_p_start<@global_para.cutoff_pvalue')
        df_gene_filter = pd.concat([df_gene_filter,tmp1,tmp2])
        df_gene_filter = df_gene_filter.drop_duplicates()
    list_stat_all_region.append(df_gene_filter)


# 5.3 merge all info for all genes
if len(list_stat_all_region)==0:
    f_0cdna(logger)
# 5.3 merge all info for all genes
df_stat_all_region = pd.concat(list_stat_all_region)
if len(df_stat_all_region) == 0:
    f_0cdna(logger)


# identify source;
records = list()
# global_para.out_blastn_seq = os.path.join(global_para.output_dir, (global_para.sampleid + '.clipped_seq'))
# global_para.out_blastn_seq_table = global_para.out_blastn_seq + ".blastn.xls"
for gene_name, df_gene in df_stat_all_region.groupby('gene_name'):
    tmp_df_seq_start = df_gene.query('is_exon_boundary_start=="1"').query('q_value_start<@global_para.cutoff_pvalue').filter(['gene_name','clipped_seq_start'])
    if len(tmp_df_seq_start)>=1:
        tmp_df_seq_start['name'] = tmp_df_seq_start.apply(lambda x:x.gene_name + ":start",axis = 1)
        tmp_df_seq_start.columns = ['gene_name','clipped_seq','name']
    tmp_df_seq_end = df_gene.query('is_exon_boundary_end=="1"').query('q_value_end<@global_para.cutoff_pvalue').filter(['gene_name','clipped_seq_end'])
    if len(tmp_df_seq_end)>=1:
        tmp_df_seq_end['name'] = tmp_df_seq_end.apply(lambda x:x.gene_name + ":end",axis = 1)
        tmp_df_seq_end.columns = ['gene_name','clipped_seq','name']
    tmp_df_seq = pd.concat([tmp_df_seq_start, tmp_df_seq_end], sort = False)
    if len(tmp_df_seq)>=1:
        for i in range(len(tmp_df_seq)):
          if len(tmp_df_seq.iloc[i]['clipped_seq']) >=6:
            record = SeqRecord(Seq.Seq(tmp_df_seq.iloc[i]['clipped_seq']),id=tmp_df_seq.iloc[i]['name'])
            records.append(record)
    del(tmp_df_seq_start)
    del(tmp_df_seq_end)
    del(tmp_df_seq)


list_blastn_columns = ["query_acc.ver", "subject_acc.ver", "pct_identity", "alignment_length", "mismatches", "gap_opens", "q._start", "q._end", "s._start", "s._end", "evalue", "bit_score"]
if len(records)>=1:
    SeqIO.write(records, global_para.out_blastn_seq, "fasta")
    blastn_command = "bash " + os.path.join(global_para.script_path, "scripts/detect/f_blastn_source_inference.sh") + " " +  global_para.out_blastn_seq + " " + global_para.blastn_database
    logger.info("Running blastn for inferring sources")
    subprocess.call(blastn_command,shell = True)
    if os.path.isfile(global_para.out_blastn_seq_table) and os.path.getsize(global_para.out_blastn_seq_table):
        table_blastn = pd.read_csv(global_para.out_blastn_seq_table, header = 0, sep = '\t')
        table_blastn.columns = list_blastn_columns
    else:
        table_blastn = pd.DataFrame(columns = list_blastn_columns)
else:
    table_blastn = pd.DataFrame(columns = list_blastn_columns)
table_blastn_source = f_source_inference(df_stat_all_region, table_blastn)
table_blastn_source.to_csv(global_para.out_blastn_seq_source,sep = '\t', index = False)



tmp_table_blastn_source = table_blastn_source.filter(['gene_name','source_inference'])


df_stat_all_region = df_stat_all_region.rename(columns = {'num_bad_reads_ajust_start':'num_clipped_start', 'num_all_reads_ajust_start':'num_total_start', 'bbinom_p_start':'bbinom_pvalue_start', 'num_bad_reads_ajust_end':'num_clipped_end', 'num_all_reads_ajust_end':'num_total_end', 'bbinom_p_end':'bbinom_pvalue_end', 'bg_unalign_start':'num_bg_clipped', 'bg_total_start':'num_bg_total'})
# df_stat_all_region = df_stat_all_region.astype({'pos_start':int,'pos_end':int,'num_clipped_start':int,'num_total_start':int,'num_clipped_end':int,'num_total_end':int,'num_bg_clipped':int,'num_bg_total':int})
select_columns_rename = ['seqname', 'exon_start', 'exon_end', 'pos_start','pos_end','gene_id', 'gene_name','transcript','num_clipped_start', 'num_total_start',  'bbinom_pvalue_start','num_clipped_end', 'num_total_end',  'bbinom_pvalue_end','num_bg_clipped', 'num_bg_total','combine_pvalue', 'combine_qvalue']
df_stat_all_region = df_stat_all_region.astype({'pos_start':int,'pos_end':int,'num_clipped_start':int,'num_total_start':int,'num_clipped_end':int,'num_total_end':int,'num_bg_clipped':int,'num_bg_total':int})

## 6. generate output files
## 6.1 exon stat
df_stat_all_region.reset_index(inplace = True,drop = True)
df_stat_all_region_full = df_stat_all_region.copy()
df_stat_all_region = df_stat_all_region.filter(select_columns_rename)
df_stat_all_region['exon_start'] = df_stat_all_region['exon_start'] -1
df_stat_all_region['pos_start'] = df_stat_all_region['pos_start'] -1

df_stat_all_region.to_csv(global_para.out_exon_stat, sep = "\t", index = False)
## 6.2 gene stat
list_transcript = list(set([x for sublist in df_stat_all_region.transcript.tolist() for x in sublist.split(',')]))
# tmp_num_bg_exon_detected = df_stat_all_region.iloc[:,0:3].drop_duplicates().shape[0]
# tmp_num_bg_exon_transcript = df_gene_exon_unique.iloc[:,0:3].drop_duplicates().shape[0]
df_stat_all_transcript = pd.DataFrame({"transcript":list_transcript}).apply(lambda x:f_transcript_stat(x.transcript,df_stat_all_region,df_gene_exon_unique),axis = 1,result_type = "expand")
df_stat_all_transcript.columns = ['gene_id','gene_name','transcript','num_exon_detected','num_exon_transcript']

df_stat_all_transcript['ratio'] = df_stat_all_transcript.apply(lambda x: round(x.num_exon_detected/x.num_exon_transcript, 3), axis=1)
df_stat_all_transcript = df_stat_all_transcript.merge(tmp_table_blastn_source, how = 'left') # merge transcript results.
df_stat_all_transcript.to_csv(global_para.out_gene_stat,index = False, sep = "\t")

## 6.3 filter gene and exon information
# df_stat_all_transcript_filter = df_stat_all_transcript.query('ratio>=@global_para.cutoff_ratio_gene')
# df_stat_all_transcript_filter.to_csv(global_para.out_gene_stat_filter,index = False, sep = "\t")
# list_transcript_filter = df_stat_all_transcript_filter.transcript.unique().tolist()
# df_stat_all_region_filter = df_stat_all_region[df_stat_all_region.apply(lambda x:str_list_compare(list_transcript_filter, x.transcript),axis = 1)]
# df_stat_all_region_filter.to_csv(global_para.out_exon_stat_filter, sep = '\t', index = False)
df_stat_all_transcript_filter = df_stat_all_transcript.query('ratio>=@global_para.cutoff_ratio_gene')
list_transcript_filter = df_stat_all_transcript_filter.transcript.unique().tolist()
df_stat_all_region_filter = df_stat_all_region[df_stat_all_region.apply(lambda x:str_list_compare(list_transcript_filter, x.transcript),axis = 1)]


df_stat_possible_transcript = pd.DataFrame({'gene_name':df_stat_all_transcript_filter.gene_name.unique().tolist(), 'possible_transcript':"unknown"})
df_stat_possible_transcript['possible_transcript'] = df_stat_possible_transcript.apply(lambda x:f_transcript_source(x.gene_name, df_stat_all_transcript_filter, df_gene_fdr, df_gene_exon_unique_filter_exon), axis = 1)
df_stat_all_transcript_filter = df_stat_all_transcript_filter.merge(df_stat_possible_transcript, how = "left").query('transcript==possible_transcript')
# df_stat_all_region_filter_full = df_stat_all_region_filter.copy() # used in the merge section



del(df_stat_all_transcript_filter['possible_transcript'])
df_stat_all_region_filter.to_csv(global_para.out_exon_stat_filter, sep = '\t', index = False)
df_stat_all_transcript_filter.to_csv(global_para.out_gene_stat_filter,index = False, sep = "\t")

## 6.4 generate region information: need to merge some regions
select_columns = ['seqname','pos_start','pos_end','gene_id','gene_name','region']
select_columns_rename = ['seqname','start','end','gene_id','gene_name','region','filter']
df_stat_all_region_filter['region'] = df_stat_all_region_full.loc[df_stat_all_region_filter.index].region.tolist()
df_region_stat_bed = df_stat_all_region_filter.filter(select_columns)
## 6.4.1 merge interval
list_merge = list()
for gene_name, sub_df_pass in df_region_stat_bed.groupby('gene_name'):
    
sub_df_pass = df_region_stat_bed.query('gene_name==@gene_name')
sub_tmp = df_gene_exon_unique.query('gene_name==@gene_name')
tmp_transcript = df_stat_all_transcript_filter.query('gene_name==@gene_name').iloc[0].transcript
sub_tmp['num'] = sub_tmp.apply(lambda x:str_list_num([x.transcript], tmp_transcript),axis = 1)
sub_tmp['num_pass'] = sub_tmp.apply(lambda x:str_list_num(sub_df_pass.region.tolist(), x.region),axis = 1)
sub_df_fail = sub_tmp.query('num>0').query('num_pass ==0').filter(['seqname','start','end','gene_id','gene_name','region'])
sub_df_fail.columns = select_columns
sub_df_fail['filter'] = 'fail'
sub_df_pass['filter'] = 'pass'
sub_df = pd.concat([sub_df_fail, sub_df_pass])
interval_sub_df = [[sub_df.iloc[i].pos_start,sub_df.iloc[i].pos_end,sub_df.iloc[i]['filter']] for i in range(len(sub_df))]
merge_interval_list = merge_interval(interval_sub_df)
sub_df_new = sub_df.iloc[0:len(merge_interval_list)].copy()
sub_df_new.pos_start = [i[0] for i in merge_interval_list]
sub_df_new.pos_end = [i[1] for i in merge_interval_list]
sub_df_new['filter'] = [i[2] for i in merge_interval_list]
list_merge.append(sub_df_new)
del(sub_df_new)

if len(list_merge)==0:
    f_0cdna(logger)
df_region_stat_bed_merge = pd.concat(list_merge)
# df_region_stat_bed_merge.iloc['pos_start'] = df_region_stat_bed_merge.apply(lambda x:x.pos_start -1, axis = 1)
df_region_stat_bed_merge.columns = select_columns_rename
f_generate_bed(df_region_stat_bed_merge)
del(df_region_stat_bed_merge['region'])
df_region_stat_bed_merge.to_csv(global_para.out_bed_merge, sep = "\t", index = False)

# 7. tell users information
logger.info("Program finished successfully")
logger.info('%d cDNA detected'%(len(df_stat_all_transcript_filter.gene_name.unique())))


if __name__ == "__main__":
pass






感觉是region可能没有对对应上。
重新计算一下。


def f_transcript_source(genename,df_stat_all_transcript_filter, df_gene_fdr, df_gene_exon_unique_filter_exon):

genename = 'ERBB2'
tmp_df_transcript_filter = df_stat_all_transcript_filter.query("gene_name==@genename")
tmp_df_select_max = df_max(tmp_df_transcript_filter, 'num_exon_detected')
tmp_transcript = ''
if len(tmp_df_select_max) == 1:
    tmp_transcript = tmp_df_select_max.iloc[0].transcript
elif len(tmp_df_select_max) >1:
    tmp_df_gene_fdr = df_gene_fdr.query("gene_name==@genename").query('combine_qvalue<0.05')
    tmp_df_select_max['num_tmp_fdr'] = tmp_df_select_max.apply(lambda x:str_list_num(tmp_df_gene_fdr.transcript.tolist(), x.transcript),axis = 1)
    tmp_df_select_max = df_max(tmp_df_select_max,'num_tmp_fdr')
    tmp_transcript = tmp_df_select_max.iloc[0].transcript
    if len(tmp_df_select_max)>1:
        tmp_df_gene_exon_unique = df_gene_exon_unique_filter_exon.query("gene_name==@genename")
        tmp_df_select_max['num_tmp_uniq'] = tmp_df_select_max.apply(lambda x:str_list_num(tmp_df_gene_exon_unique.query('pvalue<0.05').transcript.tolist(), x.transcript),axis = 1)
        tmp_df_select_max = df_max(tmp_df_select_max,'num_tmp_uniq')
        tmp_transcript = tmp_df_select_max.iloc[0].transcript
        if len(tmp_df_select_max)>1:
            tmp_df_select_max = df_max(tmp_df_select_max,'ratio')
            tmp_transcript = tmp_df_select_max.iloc[0].transcript
            if len(tmp_df_select_max)>1:
                tmp_df_select_max = tmp_df_select_max.iloc[[0]]
                tmp_transcript = tmp_df_select_max.iloc[0].transcript
return(tmp_transcript)


这个region选择的结果并不对啊。
