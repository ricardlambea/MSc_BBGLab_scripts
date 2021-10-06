#### DELETIONS
for i in $(ls -d /workspace/projects/cndrivers/pcawg_open/*/)

do

echo $i
project=$(echo $i | cut -d'/' -f6)

cut -f2 /workspace/projects/cndrivers/pcawg_open/${project}/${project}_adjusted_del.tsv | sed 's/"//g' > /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_firstfile_del.tsv
sed -i '1d' /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_firstfile_del.tsv

python3 /workspace/projects/cndrivers/scripts/run_deseq2.py /workspace/projects/cndrivers/scripts/extract_exp_values.R /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_firstfile_del.tsv /workspace/projects/cndrivers/pcawg_open/ensg_enst_symbol.txt /workspace/projects/cndrivers/pcawg_open/${project}/gistic_output/all_thresholded.by_genes.txt /workspace/projects/cndrivers/pcawg_open/${project}/expression_matrix.tsv /workspace/projects/cndrivers/pcawg_open/2colsdict.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_secondfile_del.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/qmap_${project}_del.map

echo $project finished.

done

exit ####################### THIS LINE HAS TO BE REMOVED TO RUN THE SCRIPT FOR AMPLIFICATIONS


#### AMPLIFICATIONS
for i in $(ls -d /workspace/projects/cndrivers/pcawg_open/*/)

do

echo $i
project=$(echo $i | cut -d'/' -f6)

cut -f2 /workspace/projects/cndrivers/pcawg_open/${project}/${project}_adjusted_amp.tsv | sed 's/"//g' > /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_firstfile_amp.tsv
sed -i '1d' /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_firstfile_amp.tsv

python /workspace/projects/cndrivers/scripts/run_deseq2.py /workspace/projects/cndrivers/scripts/extract_exp_values.R /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_firstfile_amp.tsv /workspace/projects/cndrivers/pcawg_open/ensg_enst_symbol.txt /workspace/projects/cndrivers/pcawg_open/${project}/gistic_output/all_thresholded.by_genes.txt /workspace/projects/cndrivers/pcawg_open/${project}/expression_matrix.tsv /workspace/projects/cndrivers/pcawg_open/2colsdict.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/${project}_secondfile_amp.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_pcawg/qmap_${project}_amp.map

echo $project finished.

done


