
###	AMPLIFICATIONS
#for i in $(ls -d /workspace/projects/cndrivers/hartwig/*/)

#do

#echo $i
#project=$(echo $i | cut -d'/' -f6)
#project_short=$(echo $i | cut -f2- -d'_' | cut -f1 -d'/')

#cut -f2 /workspace/projects/cndrivers/hartwig/${project}/${project_short}_adjusted_amp.tsv | sed 's/"//g' > /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_firstfile_amp.tsv
#sed -i '1d' /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_firstfile_amp.tsv

#python3 scripts/run_deseq2.py ./extract_exp_values.R /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_firstfile_amp.tsv /workspace/projects/cndrivers/hartwig/ensg_and_symbols_exp.tsv /workspace/projects/cndrivers/hartwig/${project}/gistic_output/all_thresholded.by_genes.txt /workspace/projects/cndrivers/hartwig/${project}/expression_matrix.tsv /workspace/projects/cndrivers/hartwig/hartwig_2colsdict.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_secondfile_amp.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/qmap_${project_short}_amp.map

#echo $project finished.

#done

###	DELETIONS
for i in $(ls -d /workspace/projects/cndrivers/hartwig/*/)

do

echo $i
project=$(echo $i | cut -d'/' -f6)
project_short=$(echo $i | cut -f2- -d'_' | cut -f1 -d'/')

cut -f2 /workspace/projects/cndrivers/hartwig/${project}/${project_short}_adjusted_del.tsv | sed 's/"//g' > /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_firstfile_del.tsv
sed -i '1d' /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_firstfile_del.tsv

python3 scripts/run_deseq2.py ./extract_exp_values.R /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_firstfile_del.tsv /workspace/projects/cndrivers/hartwig/ensg_and_symbols_exp.tsv /workspace/projects/cndrivers/hartwig/${project}/gistic_output/all_thresholded.by_genes.txt /workspace/projects/cndrivers/hartwig/${project}/expression_matrix.tsv /workspace/projects/cndrivers/hartwig/hartwig_2colsdict.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/${project_short}_secondfile_del.tsv /workspace/projects/cndrivers/cgi_df/cgi_df_hmf/qmap_${project_short}_del.map

echo $project finished.

done

