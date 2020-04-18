library(tidyverse)
library(ggrepel)
library(hrbrthemes)
library(gcookbook)
testnumbers <- read_csv("Testnumbers.csv")

#Number of countries to graph:
num = 20
countries <- list( "UK")

# Descriptive Sample Explaners
for(i in 1:nrow(testnumbers)){
  val = toString(testnumbers$DataType[i])
  if (val == "People"){
    temp = "Number of People Tested"
  }
  if (val == "Unclear"){
    temp = "Measurement Not Specified"
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
  #filter(Country %in% countries) %>%
  mutate(
    TestsPerCap = as.double(max)/as.double(Population),
    TestsPerMil = as.double(max)/1000000
  ) %>%
  arrange(desc(max)) %>%
  head(n=num)
  

update_geom_font_defaults(font_rc_light)
## Tests Per Capita (bar)
maxnum = max(testnumbersBar$TestsPerCap, na.rm=TRUE) + 0.005

plotPC <- ggplot(data = testnumbersBar, aes(x = reorder(CountryNames, TestsPerCap), y = TestsPerCap, fill = DataType)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label=datemax, colour = DataType),  vjust=0.5, hjust=0, show.legend = FALSE)

plotPC + 
  scale_y_continuous(limits=c(0,maxnum)) +
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
  scale_y_continuous(limits=c(0,4.5)) +
  xlab("Countries ")+
  ylab("Tests Per Million") +
  ggtitle("COVID-19 Tests Completed Per Million") +
  labs(fill = "Data Collected As:") +
  coord_flip() +
  scale_color_ipsum() +
  scale_fill_ipsum() +
  theme_ipsum_rc(grid="X", axis="X")

num = 10
## Line Graph, Tests Per Million
# Remove Max as not needed for now
testnumbers$max <- NULL

#develop line columns
testnumbers[7:(ncol(testnumbers)-1)] <- testnumbers[7:(ncol(testnumbers)-1)]/1000000#testnumbers$Population


linedata <- testnumbers %>%
  arrange(desc(Population)) %>%
  head(n=num) %>%
  #filter(Country %in% countries) %>%
  pivot_longer(7:(ncol(testnumbers)-1), names_to="dates", values_to="Total") %>%
  drop_na(Total) %>%
  mutate(dates = as.Date(dates, "%d/%m/%Y")) %>%
  mutate(datemax = as.Date(datemax, "%d/%m/%Y")) %>%
  mutate(label = if_else(dates == datemax, as.character(CountryNames), NA_character_)) %>%
  arrange(desc(dates))

# Develop Line Graph

LinePM <- ggplot(data = linedata, aes(x = dates, y = Total, group = CountryNames,color=CountryNames)) +
  geom_point(aes(shape=DataType)) +
  geom_line() +
  geom_label_repel(aes(label = label),
                 nudge_x=1,
                 na.rm = TRUE,
                 nudge_y=0.01,
                 min.segment.length = Inf)


LinePM + 
  #scale_y_continuous(limits=c(0,1.2)) +
  xlab("Dates")+
  ylab("Tests Per Million") +
  ggtitle("COVID-19 Tests Completed Per Million") +
  labs(shape = "Data Collected As:") +
  guides(color=FALSE) +
  scale_color_ipsum() +
  theme_ipsum_rc(grid="XY", axis="xy")



#geom_smooth( method='lm') +

 # theme(legend.position="none")
#labs(caption="What does 100,000 tests a day look like ?") +

# annotate("segment", x = as.Date("2020-03-30"), y = 0.125, xend = as.Date("2020-04-08"), yend = 1.025,
#    colour = "#8fd175", alpha = .8, size=1)
# annotate("text", x = as.Date("2020-04-03"), y = 0.75, label = "100,000 Tests Per Day", colour = "#8fd175", size=6)
#geom_abline(intercept = 37, slope = 0.1, color="red", 
#      linetype="dashed", size=1.5)+