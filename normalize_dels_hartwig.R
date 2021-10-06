### Script used to normalize the expression data corresponding to one single gene for all the samples from the same TCGA project. DESeq2 method is used to normalize and afterwards compare between the groups of wild-type vs mutated. This script is used for deletions

# c_gene <- "AADAT"
c_gene <- commandArgs(trailingOnly = TRUE)[1] # take first argument after script's name
print(paste("Chosen gene is", c_gene, sep=" "))
# gene2ensembl <-  "/workspace/projects/cndrivers/hartwig/ensg_and_symbols_exp.tsv"
gene2ensembl <-  commandArgs(trailingOnly = TRUE)[2]
# f_patients <- "/workspace/projects/cndrivers/hartwig/hartwig_Anus/gistic_output_Anus/all_thresholded.by_genes.txt"
f_patients <- commandArgs(trailingOnly = TRUE)[3]
# f_expression <- "/workspace/projects/cndrivers/hartwig/hartwig_Anus/expression_matrix.tsv"
f_expression <- commandArgs(trailingOnly = TRUE)[4]
# new_dict <- "/workspace/projects/cndrivers/hartwig/hartwig_2colsdict.tsv"
new_dict <- commandArgs(trailingOnly = TRUE)[5]
# out_file <- "/workspace/projects/cndrivers/hartwig/hartwig_Anus/tmp_deseq2_dels.tsv"
out_file <- commandArgs(trailingOnly = TRUE)[6]

gene2ensembl <- read.table(gene2ensembl, header = FALSE, stringsAsFactors = FALSE, sep = "\t") 
all_patients <- read.table(f_patients, header = TRUE, row.names = 1, stringsAsFactors = FALSE, sep = "\t", check.names = FALSE) 
all_patients <- all_patients[,c(-1,-2)] 
all_expression <- read.table(f_expression, header = TRUE, row.names = 1, stringsAsFactors = FALSE, sep = "\t", check.names = FALSE)
new_dict <- read.table(new_dict, header = FALSE, stringsAsFactors = FALSE, sep = "\t", check.names = FALSE)
print("Data laoded.")

rownames(all_expression) <- sub("\\.[0-9]*", "", rownames(all_expression)) 

# If the gene is not found in either the gene2ensembl file or the expression file or the all_thresholded.by_genes file, quit the script
if (!c_gene %in% gene2ensembl[,2]){
  print(paste(c_gene, "is not found in gene2ensembl"))
  quit(save = "no", status = 0)
} else if (!c_gene %in% rownames(all_patients)){
  print(paste(c_gene, "is not found in all_thresholded.by_genes.txt"))
  quit(save = "no", status = 0)
} else {
  ensembl_id <- gene2ensembl[gene2ensembl[, 2] == c_gene, 1]
  if (!(ensembl_id %in% rownames(all_expression))){
    print(paste(c_gene, "is not found in the expression matrix."))
    quit(save = "no", status = 0)
  }
}

c_patients <- colnames(all_patients)[all_patients[c_gene,] < 1] # get rid of amplifications
c_patients <- as.data.frame(c_patients) # for now these are aliquot_UUIDs, but we want to transform them to sample_IDs
colnames(c_patients) <- c("Aliquot_UUID")

expression_gene <- all_expression[, colnames(all_expression) %in% new_dict$V1] # submatrix with the patients to evaluate for a given gene

c_patients <- colnames(all_patients)[all_patients[c_gene,] == 0] # store only diploid patients
c_patients <- as.data.frame(c_patients) # for now these are aliquot_UUIDs, but we want to transform them to sample_IDs
colnames(c_patients) <- c("Aliquot_UUID")
c_patients$Sample_ID <- sapply(c_patients[,1], function(x) {
  c_out <- new_dict[new_dict[,2] == x, 1]
  if (length(c_out) > 1){
    c_out <- grep(".*01A$", c_out, perl = TRUE, value = TRUE) 
  }
  c_out
})

colData <- data.frame(cases = factor(colnames(expression_gene) %in% c_patients$Sample_ID), row.names = colnames(expression_gene)) # for 'cases' variable: true if diploid, false if either deleted or amplified (depending on what we are analysing)

levels(colData$cases) <- c("FALSE" = "DELETED", "TRUE" = "DIPLOID")

library("DESeq2", "ggplot2", quietly = TRUE)
library("tidyverse", quietly = TRUE)

# normalizing by DESeq2
print("Performing normalization by DESeq2...")
dds <- DESeqDataSetFromMatrix(countData = expression_gene, colData = colData, design = ~ cases)
dds <- DESeq(dds)
res <- results(dds)
print("Normalization finished.")

c_gene_res <- res[gene2ensembl[gene2ensembl[,2] == c_gene,1],]
c_log2FC <- res[gene2ensembl[gene2ensembl[,2] == c_gene,1], 2]
c_pvalue <- res[gene2ensembl[gene2ensembl[,2] == c_gene,1], 5]

gene_plot <- plotCounts(dds, gene = gene2ensembl[gene2ensembl[,2] == c_gene,1][1], intgroup = "cases", returnData = TRUE)
gplot <- ggplot(data = gene_plot) + 
  aes(x = gene_plot$cases, y = gene_plot$count, fill = gene_plot$cases) + 
  geom_boxplot() + 
  geom_jitter(color="black", size=0.4, alpha=0.4) + 
  theme_bw() + 
  theme(legend.position="right", plot.title = element_text(size=14)) + 
  ggtitle(paste("Boxplot of gene", c_gene, sep = " ")) + xlab("Cases") + ylab("Normalized counts") + labs(fill = "Cases")
#gplot

c_gene_res$symbol <- c_gene
write.table(c_gene_res, col.names = FALSE, append = TRUE, row.names = TRUE, file = out_file, sep="\t")
# header = baseMean log2FoldChange     lfcSE      stat      pvalue       padj      symbol  # headers used in write.table, but they are not printed into the generated file

#save(c_gene_res, gplot, file = paste(c_gene, "deseq2.Rdata", sep = ".")) # if we want to explore the result for a single gene


