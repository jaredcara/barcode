source("rnaseq_barcode.R")
load("geoMeans.rda")
load("barcode_params.rda")

files <- list.files(path='/media/jared/Drive/test/star_counts', full.names = T)
files1 <- list.files(path='/media/jared/Drive/test/star_counts', full.names = F)

for (i in 1:length(files1)){
  counts <- read.table(files[i], header = F)
  rownames(counts) <- counts[,1]
  counts[,c(1,3,4)] <- NULL
  counts <- tail(counts, -4)
  
  e_counts <- counts[names(geoMeans),, drop=FALSE]
  identical(names(geoMeans), rownames(e_counts))
  
  e_counts <- data.matrix(e_counts)
  barcode <- rnaseq_barcode(object=e_counts, gmeans=geoMeans, mu=params$mu_r2, tau=sqrt(params$tau2_r2), 
                            cutoff = 6.5, output = 'binary')
  
  write.table(barcode, file=paste('/media/jared/Drive/test/barcode_out/', 
                                  sub(".ReadsPerGene.out.tab", "", files1[i]), '.barcode', sep=''), 
              col.names = F, sep ='\t', quote = F)
  
}

counts <- read.table('/media/jared/Drive/test/star_counts/SRR577581.ReadsPerGene.out.tab', header = F)
rownames(counts) <- counts[,1]
counts[,c(1,3,4)] <- NULL
counts <- tail(counts, -4)

e_counts <- counts[names(geoMeans),, drop=FALSE]
identical(names(geoMeans), rownames(e_counts))

e_counts <- data.matrix(e_counts)
barcode <- rnaseq_barcode(object=e_counts, gmeans=geoMeans, mu=params$mu_r2, tau=sqrt(params$tau2_r2), 
                       cutoff = 6.5, output = 'binary')

write.table(barcode, file='/media/jared/Drive/test/barcode_out/SRR577581.barcode', col.names = F, sep ='\t', quote = F)

