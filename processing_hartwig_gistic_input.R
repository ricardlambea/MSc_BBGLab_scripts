
c_project <- commandArgs(trailingOnly = TRUE)[1]
c_file <- commandArgs(trailingOnly = TRUE)[2]
# c_file <- "/workspace/projects/cndrivers/hartwig/hartwig_Mesothelium/unformatted_input_Mesothelium.tsv"
# c_project <- "hartwig_Mesothelium"
print(paste("Parsing Hartwig project:", c_project, sep = " "))

input = read.csv(file = c_file, header = 0, sep = "\t", )
colnames(input) <- c("patientID","chromosome", "start", "end", "copyNumber")

input_mod <- input
input_mod$logCN <- log2(input_mod$copyNumber) - 1 # NAs and Inf values are produced
input_mod$markers <- 500
input_mod <- input_mod[input_mod$copyNumber > 0,] # NAs and Inf values are removed
print("All values < 0 are filtered out.")
output <- input_mod[, c(1,2,3,4,7,6)]
out_path <- paste("/workspace/projects/cndrivers/hartwig/", c_project, "/gistic_input_", c_project, ".tsv", sep = "")

write.table(output, col.names = FALSE, row.names = FALSE, file = out_path, sep="\t", quote = FALSE)
print(paste(c_project, "done. Output stored in", out_path, sep = " "))

