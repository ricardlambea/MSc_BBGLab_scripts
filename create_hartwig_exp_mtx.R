
ensg_df <- read.csv("/workspace/projects/cndrivers/hartwig/ensg_and_symbols_exp.tsv", header = 0, sep = "\t")

files <- list.files(path="/workspace/datasets/hartwig/20201120/isofox", pattern="CPCT*", full.names=TRUE, recursive=FALSE) # all directories corresponding to all patients' gene data
patient_ids <- sapply(files, function(x) strsplit(x, "/")[[1]][7]) # obtain patients_ids

library("data.table")
for (file in files) {
  transcript_f <- list.files(path=file, pattern = "*isf.gene_data.csv.gz", full.names = TRUE, recursive = FALSE) # gene file for the current patient
  # gzfile <- read.table(gzfile(transcript_f), sep = ",", header = 1) # reads the whole file
  gzfile <- fread(cmd = paste("zcat", transcript_f, sep = " "), select = c("GeneId","SplicedFragments"), sep = ",", header = TRUE) # reads only the two columns of our interest
  ensg_df <- cbind(ensg_df, gzfile[,2])
  print(paste(transcript_f, "processed.", sep = " "))
}
colnames(ensg_df) <- c("ENSG", "GeneSymbol", patient_ids)
print("Dataframe created. Time to write the output file.")

print("Creating gzip file 'hartwig_expression_data.gz'...")
gz1 <- gzfile("/workspace/projects/cndrivers/hartwig/hartwig_expression_data.gz", "w")
write.table(ensg_df, gz1, sep = "\t", row.names = FALSE)
close(gz1)
print("Gzip file created.")
