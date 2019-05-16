## simple barcode function for testing
rnaseq_barcode <- function(object, gmeans, mu, tau, cutoff = 6.5, output = "binary"){
  s_j <- DESeq2::estimateSizeFactorsForMatrix(object, geoMeans = gmeans)
  m <- log2(object / s_j)
  
  if (output %in% c("p-value", "lod", "binary")) {
    pval <- pnorm(m, mean = mu, sd = tau, lower.tail = FALSE)
    if (output == "p-value") {
      colnames(pval) <- colnames(object)
      rownames(pval) <- rownames(object)
      return(pval)
    }
    else {
      lod <- -log10(pval)
      if (output == "lod") {
        colnames(lod) <- colnames(object)
        rownames(lod) <- rownames(object)
        return(lod)
      }
      else {
        bc <- matrix(as.integer(lod > cutoff), ncol = ncol(object))
        colnames(bc) <- colnames(object)
        rownames(bc) <- rownames(object)
        return(bc)
      }
    }
  }
  if (output == "z-score") {
    z <- (object - mu)/tau
    colnames(z) <- colnames(object)
    rownames(z) <- rownames(object)
    return(z)
  }
}


