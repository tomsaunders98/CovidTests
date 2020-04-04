library(tidyverse)
library(ggrepel)
library(hrbrthemes)
library(gcookbook)
testnumbers <- read_csv("Testnumbers.csv")

#Number of countries to graph:
num = 10

# Descriptive Sample Explaners
for(i in 1:nrow(testnumbers)){
  val = toString(testnumbers$DataType[i])
  if (val == "People"){
    temp = "Number of People Tested"
  }
  if (val == "Unclear"){
    temp = "Unclear Measuremt (see notes)"
  }
  if (val == "Samples"){
    temp = "Number of Laboratory Samples Analysed"
  }
  if (val == "Cases"){
    temp = "Number of Cases Tested"
  }
  testnumbers$DataType[i] = temp
}

# Develop Universal Columns
testnumbers$datemax <- colnames(testnumbers[7:ncol(testnumbers)])[apply(testnumbers[7:ncol(testnumbers)],1,which.max)]
testnumbers$max <- apply(testnumbers[7:(ncol(testnumbers)-1)], 1, max,na.rm=TRUE)

# Develop Bar Chart Columns
testnumbersBar <- testnumbers %>% 
  mutate(
    TestsPerCap = as.double(max)/as.double(Population),
    TestsPerMil = as.double(max)/1000000
  ) %>%
  arrange(desc(Population)) %>%
  head(n=num)

update_geom_font_defaults(font_rc_light)
## Tests Per Capita (bar)

plotPC <- ggplot(data = testnumbersBar, aes(x = reorder(CountryNames, TestsPerCap), y = TestsPerCap, fill = DataType)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label=datemax, colour = DataType),  vjust=0.5, hjust=0, show.legend = FALSE)

plotPC + 
  scale_y_continuous(limits=c(0,0.015)) +
  xlab("Countries ")+
  ylab("Tests Per Capita") +
  ggtitle("COVID-19 Tests Completed Per Capita") +
  labs(fill = "Data Collected As:") +
  coord_flip() +
  scale_color_ipsum() +
  scale_fill_ipsum() +
  theme_ipsum_rc(grid="X", axis="X")


## Tests Per Million (Bar)


plotPM <- ggplot(data = testnumbersBar, aes(x = reorder(CountryNames, TestsPerMil), y = TestsPerMil, fill = DataType)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label=datemax, colour = DataType),  vjust=0.5, hjust=0, show.legend = FALSE)

plotPM + 
  scale_y_continuous(limits=c(0,1.9)) +
  xlab("Countries ")+
  ylab("Tests Per Million") +
  ggtitle("COVID-19 Tests Completed Per Million") +
  labs(fill = "Data Collected As:") +
  coord_flip() +
  scale_color_ipsum() +
  scale_fill_ipsum() +
  theme_ipsum_rc(grid="X", axis="X")


## Line Graph, Tests Per Million
# Remove Max as not needed for now
testnumbers$max <- NULL

#develop line columns
testnumbers[7:(ncol(testnumbers)-1)] <- testnumbers[7:(ncol(testnumbers)-1)]/1000000 
linedata <- testnumbers %>%
  arrange(desc(Population)) %>%
  head(n=num) %>%
  pivot_longer(7:(ncol(testnumbers)-1), names_to="dates", values_to="Total") %>%
  drop_na(Total) %>%
  mutate(dates = as.Date(dates, "%d/%m/%Y")) %>%
  mutate(datemax = as.Date(datemax, "%d/%m/%Y")) %>%
  mutate(label = if_else(dates == datemax, as.character(CountryNames), NA_character_)) %>%
  arrange(desc(dates))

# Develop Line Graph

LinePM <- ggplot(data = linedata, aes(x = dates, y = Total, group = CountryNames, color=CountryNames)) +
  geom_smooth() +
  geom_point(aes(shape=DataType)) +
  geom_label_repel(aes(label = label),
                 nudge_x=0.01,
                 na.rm = TRUE,
                 nudge_y=0.01,
                 min.segment.length = Inf)

LinePM + 
  xlab("Dates")+
  ylab("Tests Per Million") +
  ggtitle("COVID-19 Tests Completed Per Million") +
  labs(shape = "Data Collected As:") +
  guides(color=FALSE) +
  #scale_color_ipsum() +
  theme_ipsum_rc(grid="XY", axis="xy")

