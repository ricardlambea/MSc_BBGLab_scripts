#for i in 'acc' 'blca' 'brca' 'cesc' 'chol' 'coad' 'dlbc' 'esca' 'gbm' 'hnsc' 'kirc' 'kirp' 'laml' 'lgg' 'lihc' 'luad' 'lusc' 'meso' 'ov' 'paad' 'pcpg' 'prad' 'read' 'sarc' 'skcm' 'stad' 'tgct' 'thca' 'thym' 'ucec' 'ucs' 'uvm' # there is one project missing KICH, because there was an error when running GISTIC on that porject

#do 

#project=${i}

#cut -f2 /workspace/projects/cndrivers/tcga/tcga_${project}/${project}_adjusted_amp.tsv | sed 's/"//g' > /workspace/projects/cndrivers/${project}_firstfile_amp.tsv

#python3 scripts/run_deseq2.py ./extract_exp_values.R /workspace/projects/cndrivers/${project}_firstfile_amp.tsv /workspace/projects/cndrivers/tcga/ensg_symbol.tsv /workspace/projects/cndrivers/tcga/tcga_${project}/gistic_output/all_thresholded.by_genes.txt /workspace/projects/cndrivers/tcga/tcga_${project}/${project}_expression_mtx.tsv /workspace/projects/cndrivers/tcga/tcga_${project}/tcga_${project}_2colsdict.tsv /workspace/projects/cndrivers/${project}_secondfile_amp.tsv /workspace/projects/cndrivers/qmap_${project}_amp.map

#echo $project finished.

#done





for i in 'acc' 'blca' 'brca' 'cesc' 'chol' 'coad' 'dlbc' 'esca' 'gbm' 'hnsc' 'kirc' 'kirp' 'laml' 'lgg' 'lihc' 'luad' 'lusc' 'meso' 'ov' 'paad' 'pcpg' 'prad' 'read' 'sarc' 'skcm' 'stad' 'tgct' 'thca' 'thym' 'ucec' 'ucs' 'uvm' # there is one project missing KICH, because there was an error when running GISTIC on that porject

do

project=${i}

cut -f2 /workspace/projects/cndrivers/tcga/tcga_${project}/${project}_adjusted_del.tsv | sed 's/"//g' > /workspace/projects/cndrivers/${project}_firstfile_del.tsv

python3 scripts/run_deseq2.py ./extract_exp_values.R /workspace/projects/cndrivers/${project}_firstfile_del.tsv /workspace/projects/cndrivers/tcga/ensg_symbol.tsv /workspace/projects/cndrivers/tcga/tcga_${project}/gistic_output/all_thresholded.by_genes.txt /workspace/projects/cndrivers/tcga/tcga_${project}/${project}_expression_mtx.tsv /workspace/projects/cndrivers/tcga/tcga_${project}/tcga_${project}_2colsdict.tsv /workspace/projects/cndrivers/${project}_secondfile_del.tsv /workspace/projects/cndrivers/qmap_${project}_del.map

echo $project finished.

done


