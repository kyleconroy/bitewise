load the files in RStudio

    attach(asian_percents)
    attach(asian_ratings)
    plot(percents, jitter(ratings))
    reg1 <- lm(ratings~percents)
    abline(reg1)
    reg1

