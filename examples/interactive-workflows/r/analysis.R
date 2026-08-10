dir.create("results", showWarnings = FALSE)
x <- data.frame(x = 1:100)
x$x_squared <- x$x ^ 2
write.csv(x, "results/r-results.csv", row.names = FALSE)
print(tail(x))
