# If you get an error on reading the csv, replace the file path with the absolute path

# Read dataset
dataset = read.csv(file = 'perry_winter_2017_iconicity.csv')

# Group by POS and sum across frequency
frequencies = aggregate(dataset$Freq, by=list(POS=dataset$POS), FUN=sum)

# Add plot
barplot(
    frequencies$x, 
    names.arg = frequencies$POS, 
    horiz = T, 
    las = 2, 
    cex.names = 0.7, 
    col = 7,
    main = "Grammatical is by far the most frequent part of speech"
)

# Add vertical grid
grid(
    nx = NULL, 
    ny = NA,
    lty = 1,
    col = "gray",
    lwd = 2
)
