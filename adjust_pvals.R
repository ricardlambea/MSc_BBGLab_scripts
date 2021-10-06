# Script used to calculate the adjusted Pvalue of the expression data by FDR method. This script takes as first argument the file name of the DESeq2 outfile file, and as second argument the file name of the output that will be generated.

library(tidyverse)

deseq2_output <- commandArgs(trailingOnly = TRUE)[1]

deseq2_output <- read.table(deseq2_output, header = FALSE, sep = "\t")
colnames(deseq2_output) <- c("ENSG", "baseMean", "log2FoldChange", "lfcSE", "stat", "pvalue", "padj", "symbol")

deseq2_output <- select(deseq2_output, -padj) # get rid of the current padj col cause it is not FDR 

deseq2_output$adjPval <- p.adjust(as.numeric(unlist(deseq2_output %>% select(pvalue))), "BH") # Calculate corrected Pvalues by FDR method and add column 
deseq2_output <- deseq2_output[,c(1,7,2,3,4,5,6,8)] # rearrange columns

deseq2_output_filt <- which(deseq2_output[,'adjPval'] < 0.05) # creates a vector with the indices of the rows that meet the criteria
deseq2_output_filt <- deseq2_output[deseq2_output_filt, ]

output_file_name <- commandArgs(trailingOnly = TRUE)[2]
#cat("ENSG\tsymbol\tbaseMean\tlog2FoldChange\tlfcSE\tstat\tpvalue\tAdjPval\n",file=output_file_name)
write.table(deseq2_output_filt, col.names = TRUE, row.names = FALSE, file = output_file_name, sep="\t")


