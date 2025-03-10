# knitr::opts_chunk$set(echo = TRUE)

# nifty code using the pacman package
# it checks if the packages specified below are installed, if not, they will be installed, if yes, they will be loaded
# if (!require("pacman")) install.packages("pacman")
# pacman::p_load(rstudioapi, tidyverse)

# set the current working directory to the one where this file is
# current_working_dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
# setwd(current_working_dir)

library("dplyr")
library("ggplot2")
df = read.csv("ELP_frequency.csv")
df

df = mutate(df, Freq=log10(Freq))
df

# The log10 function is already applied in-place on the dataframe
# So we dont need ot apply it again
model = lm(df$RT ~ df$Freq, data=df)

ggplot(df, aes(x=Freq, y=RT)) + geom_point()

ggplot(df, aes(x=Freq, y=RT)) + geom_point() + geom_hline(yintercept=mean(df$RT))

coefs = coefficients(model)
intercept = coefs[["(Intercept)"]]
slope = coefs[["df$Freq"]]

ggplot(df, aes(x=Freq, y=RT)) + geom_point(colour="blue") + 
geom_hline(yintercept=mean(df$RT), color="red") + 
geom_abline(intercept=intercept, slope=slope)
