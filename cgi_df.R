### This script needs 4 arguments: 1) input file name; 2) output file name; 3) tumor type; 4) mutation type.

i_file <- commandArgs(trailingOnly = TRUE)[1] # "/workspace/projects/cndrivers/data4cgi_output.tsv"
out_f <- commandArgs(trailingOnly = TRUE)[2] # "/workspace/projects/cndrivers/cgi_df_out.tsv"

# DATA
library(tidyverse)
df <- data.frame()
ttype <- commandArgs(trailingOnly = TRUE)[3] #automatize
mutation <- commandArgs(trailingOnly = TRUE)[4] # automatize
file <- read_tsv(file = i_file, col_names = FALSE)
colnames(file) <- c('sample','count','cases','gene')

last_gene <- toString(file[1,4])
t_df <- data.frame()

for (row in 1:nrow(file)){
  gene <- toString(file[row, 4])
  if (gene == last_gene){ # if the gene is the same as before
    t_df <- rbind(t_df, file[row,]) # add to the new df and continue next line
    last_gene <- gene

  } else { # if the gene has just changed
    ### mut stats
    mask_mut <- t_df[t_df$cases %in% 'AMPLIFIED',] # calculate the stats for the current filled df

    lowestq_mut <- quantile(mask_mut$count, probs = c(0.05), names = FALSE)
    median_mut <- quantile(mask_mut$count, probs = c(0.5), names = FALSE)
    firstq_mut <- quantile(mask_mut$count, probs = c(0.25), names = FALSE)
    thirdq_mut <- quantile(mask_mut$count, probs = c(0.75), names = FALSE)
    highestq_mut <- quantile(mask_mut$count, probs = c(0.95), names = FALSE)
    stddev_mut <- sd(mask_mut$count)
    
    n_mut <- length(mask_mut$cases)
    error_mut <- qnorm(0.975)*stddev_mut/sqrt(n_mut)
    
    ##### wild-type stats
    mask_wt <- t_df[t_df$cases %in% 'DIPLOID',]
    
    lowestq_wt <- quantile(mask_wt$count, probs = c(0.05), names = FALSE)
    median_wt <- quantile(mask_wt$count, probs = c(0.5), names = FALSE)
    firstq_wt <- quantile(mask_wt$count, probs = c(0.25), names = FALSE)
    thirdq_wt <- quantile(mask_wt$count, probs = c(0.75), names = FALSE)
    highestq_wt <- quantile(mask_wt$count, probs = c(0.95), names = FALSE)
    stddev_wt <- sd(mask_wt$count)
    
    n_wt <- length(mask_wt$cases)
    error_wt <- qnorm(0.975)*stddev_wt/sqrt(n_wt)
    
    # insert into new df the generated data
    new_df <- data.frame(last_gene, ttype, mutation, lowestq_mut, firstq_mut, median_mut, thirdq_mut, highestq_mut, n_mut, lowestq_wt, firstq_wt, median_wt, thirdq_wt, highestq_wt, n_wt)
    df <- rbind(df, new_df)
    print(paste(gene,"processed.", sep = " "))
    
    last_gene <- gene
  }
}

write.table(df, col.names = TRUE, append = TRUE, row.names = FALSE, file = out_f, sep="\t")


