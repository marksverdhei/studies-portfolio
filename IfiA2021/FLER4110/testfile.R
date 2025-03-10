library(tcltk)
library(datasets)
library(dplyr)

X11()

data(iris)
names(iris) <- tolower(names(iris))
# summary(iris)

size = nrow(iris)
train_size = size * 0.7
iris_train = iris[0:train_size, ]
iris_test = iris[train_size:size, ]


# X_train = select(iris_train, sepal.length:petal.width)
# y_train = select(iris_train, species)
#
# X_test = select(iris_test, sepal.length:petal.width)
# y_test = select(iris_test, species)

model <- glm(species ~., family=binomial(link='logit'), data=iris_train)

# summary(model)

fitted.results = predict(model, data=iris_test)
print(fitted.results)

sl = select(iris, sepal.length)
pl = select(iris, petal.length)

plot(sl[,1], pl[,1])
sys.sleep(5)
