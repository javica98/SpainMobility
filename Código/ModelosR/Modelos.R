#Meter Base de datos 
library(datasets)
library(pscl)
library(readr)
require(ggplot2)
require(sandwich)
require(msm)
library(MASS)
library("ggpubr")

#TODOS LOS DISTINTOS DATA SET QUE USAMOS

#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madrid7NN.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridCapital7.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridMunicipios7.csv")

#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madrid14NN.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridCapital14.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridMunicipios14.csv")

#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madridcon0.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madridcon0Capital.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madridcon0Municipios.csv")


#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madridsin0.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madridsin0Capital.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/Madridsin0Municipios.csv")

#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridTotalCorregido.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridDistritosCorregido.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridMunicipiosCorregido.csv")

data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridTotalCorregidoSin0.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridDistritosCorregidoSin0.csv")
#data <- read_csv("C:/Users/Asus/Desktop/mis cosas/TFM/R/data/MadridMunicipiosCorregidoSin0.csv")

data$Casos=(data$Casos*100.000)/data$Poblacion


#TODAS LAS TRANSFORMACIONES USADAS

#data$Inc14=log(data$Inc14)
#data$Inc=log(data$Inc)
#data$Casos=log(data$Casos)

data$Inc14=log10(data$Inc14)
data$Inc=log10(data$Inc)
#data$Casos=log10(data$Casos)

#data$Inc14=(data$Inc14)^1/3
#data$Inc=(data$Inc)^1/3
#data$Casos=(data$Casos)^1/3

#data$Inc14=(data$Inc14)^1/5
#data$Inc=(data$Inc)^1/5
#data$Casos=(data$Casos)^1/5




#DIVISION DEL DATASET
dt = sort(sample(nrow(data), nrow(data)*.8))
train<-data[dt,]
test<-data[-dt,]
#data<-read.csv(".csv")
#data<-warpbreaks
head(data,10)


#Mostrar columnas
columns<-names(data)
columns



#Media y varianza
print('Media y Varianza Variable Objetivo')
mean(train$Inc14) # calculate mean
var(train$Inc14) # calculate variance



#MEDIA Y VARIANZA DE VARIABLES
print('Media y Varianza Variable Incidencia')
mean(train$Inc) # calculate mean
var(train$Inc) # calculate variance

print('Media y Varianza Variable Casos')
mean(train$Casos) # calculate mean
var(train$Casos) # calculate variance

#MODELOS CON MOVILIDAD
model<-glm(Inc14 ~ Casos+Inc, data=train, family = poisson(link = "log"))
#model<-glm(Inc14 ~ Casos+Inc, data = data, family = quasipoisson)
#model<-glm.nb(Inc14 ~ Casos+Inc,data=data,control = glm.control(maxit=1000))
#model = zeroinfl(Inc14 ~ Casos+Inc,data = data,dist = "poisson")

print('MODELO CON MOVILIDAD')
summary(model)

#MODELOS SIN MOVILIDAD
#model2<-glm(Inc14 ~ Inc, data=train, family = poisson(link = "log"))
model2<-glm(Inc14 ~ Inc, data = data, family = quasipoisson)
#model2<-glm.nb(Inc14 ~ Inc,data=data,control = glm.control(maxit=1000))
#model = zeroinfl(Inc14 ~ Inc,data = data,dist = "poisson")

print('MODELO SIN MOVILIDAD')
summary(model2)

test
predict=predict(model, newdata = test, type = "response")
predict
predict2=predict(model2, newdata = test, type = "response")
predict2

plot(predict,test$Inc14, main="Predicción", col="blue", pch="o")
points(predict2,test$Inc14, col="red", pch="*")
lines(test$Inc14,test$Inc14,col="green", lty=1)


print('ERROR CON MOVILIDAD')
sqrt(mean((test$Inc14 - predict)^2))
mean(abs((test$Inc14-predict)/test$Inc14)) * 100

print('ERROR SIN MOVILIDAD')
sqrt(mean((test$Inc14 - predict2)^2))
mean(abs((test$Inc14-predict2)/test$Inc14)) * 100


print('CORRELACION CON MOVILIDAD')
res <- cor.test(test$Inc14, predict, 
                method = "pearson")
res
print('CORRELACION SIN MOVILIDAD')
res2 <- cor.test(test$Inc14, predict2, 
                method = "pearson")
res2