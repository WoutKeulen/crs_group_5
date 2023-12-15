install.packages('fitdistrplus')
install.packages('MASS')
install.packages('survival')
install.packages('logspline')
install.packages('car')
install.packages('carData')
install.packages('ggpubr')
library(ggpubr)
library(carData)
library(car)
library(logspline)
library(fitdistrplus)
library(MASS)
library(survival)
library(ggplot2)
require(ggplot)
###################################################
##Import the data and check if imported correctly##
###################################################
f <- file.choose()
data <- read.csv( f, sep =",", stringsAsFactors = FALSE)
View(data)


##Create seperate table for Type 1 patients and Type 2 patients
data_type1 <- subset(data, data$PatientType=='Type 1')
data_type2 <- subset(data,data$PatientType=="Type 2")

mean(data_type1$Time)

#Create Sample mean for Exponential distribution between arrival times
summary(data_type1$Time)
plot(data_type1$Time)

set.seed(123)

#Doing the analysis for mean and sd of interarrival time
mean(interArrive_clean)

k <- 10000
simsamples <- replicate(k, rexp(379, arrive_rate))
mean_expdist <- apply(simsamples, 2, mean)
quantile(simmeans, c(0.025,0.975))

mean(simmeans)
hist(mean_expdist, col='blue', nclass=30)

sd(interArrive_clean)

simstandard_deviation <- apply(simsamples, 2, sd)
var_expdist <- simstandard_deviation*simstandard_deviation
quantile(simstandard_deviation*simstandard_deviation, c(0.025, 0.975))

hist(var_expdist, nclass= 30)
mean(simstandard_deviation*simstandard_deviation)

#Doing the analysis for mean and standard deviation of normal distribution
mean(data_type1$Duration)
sd(data_type1$Duration)

simsamples_1 <- replicate(k,rnorm(379, 0.4326608, 0.09777424))
mean_normaldist <- apply(simsamples_1, 2, mean)
quantile(mean_normaldist, c(0.025,0.975))

mean(mean_normaldist)
hist(mean_normaldist, col='red', nclass=30)

sd_normaldist <- apply(simsamples_1, 2, sd)
quantile(var_normaldist, c(0.025,0.975))
mean(sd_normaldist*sd_normaldist)

var_normaldist <- sd_normaldist*sd_normaldist

hist(var_normaldist, col='blue', nclass=30)


#Trying to fit with the graph
#first test it for duration
descdist(data_type2$Duration, boot = 10000)

min(data_type2$Duration)
max(data_type2$Duration)

descdist(data_type2$Duration, discrete = FALSE, boot=100000)
fitdist(data_type2$Duration,"gamma")
fitdist(data_type2$Duration, "chisq")

fitdist(data_type2$Duration, "norm" )
fitdist(data_type2$Duration, "weibull")
fitdist(data_type2$Duration, "unif")


normal_ = fitdist(data_type2$Duration, "norm")
gamma_ = fitdist(data_type2$Duration, "gamma")
weibull_ = fitdist(data_type2$Duration, "weibull")
uniform_ = fitdist(data_type2$Duration, "unif")

plot(normal_)
plot(gamma_)
plot(weibull_)
plot(uniform_)



#Interarrival time tests
interArrive <- diff(data_type1$Time)
interArrive_clean = subset(interArrive, interArrive >= 0)
hist(interArrive_clean)
arrive_rate <- 1/mean(interArrive_clean)


interArrive2 <- diff(data_type2$Time)
interarrive2_clean = subset(interArrive2, interArrive2 >= 0)
hist(interarrive2_clean)

descdist(interarrive2_clean, boot=10000)
fitdist(interarrive2_clean, "norm")
normal2_ = fitdist(interarrive2_clean, 'norm')
plot(normal2_)

fitdist(interarrive2_clean, "weibull")
weibull2_ = fitdist(interarrive2_clean, "weibull")
plot(weibull2_)


fitdist(interarrive2_clean,'lnorm')
lognormal2_ = fitdist(interarrive2_clean, 'lnorm')
plot(lognormal2_)

fitdist(interarrive2_clean, "gamma")
gamma2_ = fitdist(interarrive2_clean, "gamma")

weibull2_$aic
lognormal2_$aic
gamma2_$aic




#mean and sd for weibull type 2 interarrival time
simsamples5 <- replicate(k, rweibull(239, 3.04586, 0.95142))
simmeans5 <- apply(simsamples5, 2, mean)
hist(simmeans5)
mean(simmeans5)
quantile(simmeans5, c(0.025,0.975))

mean(interarrive2_clean)
sd(interarrive2_clean)

simsd_3 <- apply(simsamples5,2,sd)
mean(simsd_3*simsd_3)
quantile(simsd_3*simsd_3, c(0.025,0.975))


#Exploring type 2 distributions

descdist(data_type2$Duration, discrete = FALSE, boot=30000)
fit.gamma <- fitdist(data_type2$Duration, "gamma")
fit.normal <- fitdist(data_type2$Duration, "norm")
fit.lognormal <- fitdist(data_type2$Duration, "lnorm")


#Doing the bootstrap analysis for the duration of type 2 using gamma distribution
simsamples6 <- replicate(k,rgamma(239, 12.5837,18.8003))
simmeans6 <- apply(simsamples6, 2, mean)
hist(simmeans6)
mean(simmeans6)
quantile(simmeans6, c(0.025,0.975))

mean(data_type2$Duration)

simsd6 <- apply(simsamples6, 2, sd)
var6 <- simsd6*simsd6
hist(var6)
mean(var6)
quantile(var6, c(0.025,0.975))


#Plot all candidate distributions
plot(fit.gamma)
plot(fit.lognormal)
plot(fit.normal)

#AIC from gamma is lowest
fit.gamma$aic
fit.normal$aic
fit.lognormal$aic

