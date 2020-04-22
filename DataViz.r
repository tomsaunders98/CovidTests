library(tidyverse)
library(ggrepel)
library(hrbrthemes)
library(gcookbook)


# Load Data
testnumbers <- read_csv("https://github.com/tomsaunders98/CovidTests/raw/master/Testnumbers.csv")

# Universal Wrangling
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

  
####################################
## Tests Per Thousand (Bar Graph) ##
####################################

# Bar Chart Per Cap Wrangling
Barpercap <- testnumbers
Barpercap$datemax <- colnames(Barpercap[7:ncol(Barpercap)])[apply(Barpercap[7:ncol(Barpercap)],1,which.max)]
Barpercap$max <- apply(Barpercap[7:(ncol(Barpercap)-1)], 1, max,na.rm=TRUE)

testnumbersBar <- Barpercap %>% 
  mutate(
    TestsPerCap = as.double(max)/as.double(Population),
    TestsPerMil = (as.double(max)/as.double(Population))*1000
  ) %>%
  arrange(desc(max)) %>%
  filter(Country != "ICE")

# Aesthetics
maxnum = max(testnumbersBar$TestsPerMil, na.rm=TRUE) + 20


plotPM <- ggplot(data = testnumbersBar, aes(x = reorder(CountryNames, TestsPerMil), y = TestsPerMil, fill = DataType)) +
  geom_bar(stat = "identity") +
  geom_text(aes(label=datemax, colour = DataType),  vjust=0.5, hjust=0, show.legend = FALSE)

plotPM + 
  scale_y_continuous(limits=c(0,maxnum)) +
  xlab("Countries ")+
  ylab("Tests Per Thousand") +
  ggtitle("COVID-19 Tests Completed Per Thousand") +
  labs(fill = "Data Collected As:") +
  coord_flip() +
  scale_color_ipsum() +
  scale_fill_ipsum() +
  theme_ipsum_rc(grid="X", axis="X")


#####################################
## Tests Per Thousand (Line Graph) ##
#####################################

# Line Graph Data Wrangling
LineperCap <- testnumbers
LineperCap$datemax <- colnames(LineperCap[7:ncol(LineperCap)])[apply(LineperCap[7:ncol(LineperCap)],1,which.max)]
LineperCap[7:(ncol(LineperCap)-1)] <- LineperCap[7:(ncol(LineperCap)-1)]/LineperCap$Population
LineperCap[7:(ncol(LineperCap)-1)] <- LineperCap[7:(ncol(LineperCap)-1)]*1000

num = 10 #Add up to 32 Countries

linedata <- LineperCap %>%
  arrange(desc(Population)) %>%
  head(n=num) %>%
  pivot_longer(7:(ncol(testnumbers)-1), names_to="dates", values_to="Total") %>%
  drop_na(Total) %>%
  mutate(dates = as.Date(dates, "%d/%m/%Y")) %>%
  mutate(datemax = as.Date(datemax, "%d/%m/%Y")) %>%
  mutate(label = if_else(dates == datemax, as.character(CountryNames), NA_character_)) %>%
  arrange(desc(dates))

# Aesthetics
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
  ggtitle("COVID-19 Tests Completed Per Thousand") +
  labs(shape = "Data Collected As:") +
  guides(color=FALSE) +
  theme_minimal()
  

##################################
## UK 100,000 target evaluation ##
##################################
  
# Data Wrangling
countries <- list( "UK")
df0 <- testnumbers[7:(ncol(testnumbers)-11)]
TestingTories <- cbind(testnumbers[1], df0[-length(df0)] - df0[-1])
TestingTories[TestingTories < 0] <- NA

TestingToriesLine <- TestingTories %>%
  filter(Country %in% countries) %>%
  pivot_longer(2:ncol(TestingTories), names_to="dates", values_to="Total") %>%
  drop_na(Total) %>%
  mutate(dates = as.Date(dates, "%d/%m/%Y")) %>%
  arrange(desc(dates)) 

latestvalue = as.double(TestingToriesLine[1, "Total"])

# Aesthetics
TestTheT <- ggplot(data = TestingToriesLine, aes(x = dates, y = Total, color=Country), cex.lab=1.5, cex.axis=1.5 ) +
  geom_line(col="#003f5c") +
  geom_point(col="#003f5c") +
  scale_y_continuous(limits=c(0,120000)) +
  scale_x_date(limits = as.Date(c("2020-04-07","2020-05-01")))+
  xlab("Dates")+
  ylab("Tests Per Day") +
  guides(color=FALSE) +
  theme_minimal(base_size = 20) +
  theme(legend.position="none") +
  annotate("segment", x = min(TestingToriesLine$dates), y = 100000, xend =as.Date("2020-05-01"), yend = 100000, colour = "#333333", alpha = .8, size=1) +
  annotate("text", x = median(TestingToriesLine$dates), y = 105000, label = "100,000 Tests Per Day", colour = "#333333", size=6) +
  annotate("segment", x = max(TestingToriesLine$dates), linetype = "dashed", y = latestvalue, xend =as.Date("2020-05-01"), yend = 100000, colour = "#bc5090", size=1) +
  annotate("text", x = sort(TestingToriesLine$dates,T)[2], y = (max(TestingToriesLine$Total) + 10000), label = paste("Current Tests: ", latestvalue), colour = "#003f5c", size=5) +
  annotate("rect", xmin = max(TestingToriesLine$dates), xmax = as.Date("2020-05-01"), ymin = 0, ymax = 100000,alpha = .1)


