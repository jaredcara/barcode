## rnaseq barcode example
source("rnaseq_barcode.R")
load("geoMeans.rda")
load("barcode_params.rda")
load(file="e_test.rda")

## object should be a vector of unnormalized counts 
## with the same length and names as geoMeans
e_test <- e_test[names(geoMeans),,drop=FALSE]
identical(names(geoMeans), rownames(e_test))
tst <- rnaseq_barcode(object=e_test, gmeans=geoMeans, mu=params$mu_r2, tau=sqrt(params$tau2_r2),
                      cutoff = 6.5, output = "binary")
  