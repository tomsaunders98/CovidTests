library(tidyverse)
testnumbers <- read_csv("Testnumbers.csv")
testnumbers <- mutate(testnumbers,
       testsCP = tests2days/Population
)
plot <- ggplot(data = testnumbers) +
  geom_bar(mapping = aes(x = CountryNames, y = testsCP, fill = CountryNames), stat = "identity", show.legend = FALSE
)
plot + 
  xlab("Countries ")+
  ylab("Tests Per Capita") +
  ggtitle("COVID-19 Tests Completed Per Capita (30/3/2020 - 1/4/2020)")
