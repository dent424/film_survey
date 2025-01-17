setwd("C:/Users/Alex/Dropbox/programming projects")
critic_data <- read.csv('dummies.csv', sep = ',')
summary(critic_data)
core.data <- c("country", "poll", "newName", "selectionYear", "selectionDirector","rating","genre","language","country.1")
summary(critic_data[core.data])
library(ggplot2)
library(dplyr)
library(reshape2)
library(RColorBrewer)
library(gridExtra)
critic_data=na.omit(critic_data)
critic_data$Germany.Aggregate <- critic_data$Germany + critic_data$West.Germany

#I first decided to see how many votes per decade to see the distribution
ggplot(aes(x=selectionYear), data=critic_data) +
  geom_histogram(binwidth=10, color="Black", fill="White")+
  ggtitle("Votes by decade")+
  ylab("Votes") +
  xlab("Decade")
#We can see that there is a peak is in the 1960s. This makes sense for several reasons.
#Newer movies from the 1980s on especially are often considered too new to be considered classics
#In addition, we might hypothesize that with ever additional decade, there are more movies to pick from
#Finally, the 1960s is also considered an important time in film with highly influential movements like
#the New Wave in full swing. Anecdotally much classic cinema seems to come from this time period. 

#creates a decade variable for future analysis
critic_data$decade <- floor(critic_data$selectionYear/10)*10
#confirmation that decade is working the way I want it to
ggplot(aes(x=selectionYear,y=decade), data=critic_data) +
  geom_point()

#I next wanted to see whether there were interesting trends in movie votes by country.
#First I had to reshape and prepare the data

#finds countries, languages, and genres with over 100 votes
country_sums <- colSums(Filter(is.numeric, critic_data),na.rm = TRUE, )
keep_vars <- names(country_sums[country_sums > 100])
a <- c("country","poll","selectionName","newName","rating","runtime")
keep_vars <- c(keep_vars, a)
#keeps variables with over 100 votes as well as variables with basic information
new_data <- critic_data[keep_vars]

#creates movie location vote counts by decade
decade_groups <- group_by(new_data, decade)
votesbyDecade<-summarise(decade_groups,
                         Canada = sum(Canada),
                         China = sum(China),
                         Denmark=sum(Denmark),
                         France =sum(France),
                         Germany = sum(Germany),
                         Hong.Kong = sum(Hong.Kong),
                         India = sum(India),
                         Iran = sum(Iran),
                         Italy = sum(Italy),
                         Japan = sum(Japan),
                         Mexico = sum(Mexico),
                         Ussr = sum(Soviet.Union),
                         Spain = sum(Spain),
                         Sweden = sum(Sweden),
                         Switzerland = sum(Switzerland),
                         Taiwan = sum(Taiwan),
                         UK = sum(UK),
                         USA = sum(USA),
                         West.Germany = sum(West.Germany),
                         Germany.Aggregate = sum(Germany.Aggregate))
#converts to long format for analysis
votesbyDecade.long <- melt(votesbyDecade, 
                           id.vars=c("decade"),
                           variable.name="country",
                           value.name="votes")

#This was my first try but the graph was unreadable.
#Votes by Decade by Country
ggplot(aes(y=votes,x=decade, color=country),data=votesbyDecade.long)+
  geom_line() +
  ggtitle("Votes by Decade and Country")

#A facet wrap worked much better
#Votes by Decade by Country Faceted
ggplot(aes(y=votes,x=decade),data=votesbyDecade.long)+
  geom_line() +
  facet_wrap(~country)+
  ggtitle("Votes by Decade and Country")

#We can see that even in this group, the number of movies is dominated by a few countries.
#These countries include USA, Japan, Italy, and France.
#In addition we can see that many countries encounter a distinct peak.
#Notable peaks include France and Italy in the 1960s, Japan in the 1950s, 
#and the USA in the 1950s and the 1970s. Each of these peaks seems to correspond with 
#a few auteurs that worked in those decades. In France in the 1960s we have the French New Wave
#directors including luminaries such as Jean-Luc Godard and Francois Truffaut. In Italy in the 1960s,
#we have Frederico Fellini and Michaelangelo Antonioni.
#In the 1950s in the USA we have directors like Alfred Hitchcock, Billy Wilder, and Elia Kazan, and John Ford
#The 1970s in the US we have Francis Ford Coppola and Martin Scorsese.
#Japan in the 1950s featured major works by Akira Kurosawa and Yasujiro Ozu
#In a later analysis, I will try to see how much of these peaks is attributable to individual auteurs
#rather than a broader trend.


#Next I wanted to see the distribution of votes within a country. I decided to convert each datapoint into a percentage
#of the total votes of country cast for movies of a given decade. This would ideally give a sense of where the peaks and 
#troughs for each country are.

#First convert the absolute numbers to percentages
country_groups <- group_by(votesbyDecade.long, country)
votesbyCountry <- summarise(country_groups,
                            Totals = sum(votes))
country_percentages <- merge(votesbyDecade.long, votesbyCountry, by="country")
country_percentages$percentages <- (country_percentages$votes/country_percentages$Totals)*100

#And then we create the charts
ggplot(aes(y=percentages,x=decade),data=country_percentages)+
  geom_line() +
  facet_wrap(~country)+
  ggtitle("Percent Votes by Decade and Country")

#This analysis indicates that most countries seem to be dominated by one or two significant peaks in their history.
#This could indicate the influence of one or two auteurs dominating the movie scene of that country or perhaps a
#particularly influential movement in that time period. 
#As an illustration, it seems likely that the peak in India in the 1950s would be from the movies of Satyajit Ray.
#Similarly it seems likely that the peak in Sweden in the 1960s would be largely the result of Ingmar Bergman movies.
#Notable exceptions to this trend include the UK, the USA, France.

#I next wanted to analyze the voters to see where they are from.
ggplot(aes(x=country), data=critic_data) +
  geom_bar() +
  ggtitle("Directors by Country")
#This chart was obviously not particularly illuminating. I decided to reorder the 
#data by votes to get a general idea of the distribution of voters by country
voter_groups <- group_by(critic_data, country)
votersbyCountry <- summarise(voter_groups,
                             Totals = n())

ggplot(aes(x=reorder(country, -Totals),y=Totals), data=votersbyCountry) +
  geom_point(stat="identity") +
  ggtitle("Votes by Country") +
  ylab("Number of Votes") +
  xlab("Each point represents a country") +
  theme(axis.text.x=element_blank())+
  scale_x_discrete(breaks=NULL)

#It's clear that the votes are note evenly distributed. In fact it seems as though
#there is a floor to the number of voters.
top_vote_countries <- subset(votersbyCountry, Totals >= quantile(Totals,0.9))
ggplot(aes(y=reorder(country,-Totals), x=Totals), data=top_vote_countries) +
  geom_point()+ 
  ggtitle("Top 10% Countries with most votes")+
  xlab("Number of Votes")+
  ylab("Country")
#Unsurprisingly the most votes come from the UK where Sight and Sound, the maker of the poll
#is based. The United States also has a significant number of voters likely due to
#its large size and it's prominent position in the film industry. The remainder of 
#the top 10% is mostly represented by Europe with the exceptions of Argentina,
#Australia, Canada, and Japan. I was interested to see if the top 20% was more diverse
top_vote_countries <- subset(votersbyCountry, Totals >= quantile(Totals,0.8))
ggplot(aes(y=reorder(country,-Totals), x=Totals), data=top_vote_countries) +
  geom_point()+ 
  ggtitle("Top 20% Countries with most votes")+
  xlab("Number of Votes")+
  ylab("Country")
#It was. Notable inclusions are Brazil, India, Turkey, Mexico, and China outside of Europe.

#Next I will look at individual directors to see who is most influential overall. 
#First group by director
director_groups <- group_by(critic_data, selectionDirector)
votesbyDirector <- summarise(director_groups,
                             Totals = n())
#votesbyDirector2 <- votesbyDirector[order(votesbyDirector$Total),] 
#votesbyDirector$ordered.director <- factor(votesbyDirector2$selectionDirector,
#                                          levels=votesbyDirector2[order(votesbyDirector$Totals), 1])

#Next make a chart to see the distribution of votes
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals), data=votesbyDirector) +
  geom_point(alpha=0.5)+ 
  theme(axis.text.x=element_blank())+
  scale_x_discrete(breaks=NULL)+
  ggtitle("Distribution of Votes by Director")+
  ylab("Number of Votes")+
  xlab("Each vote represents a director")

#Create to 5% ranked director lists
top_20_director <- subset(votesbyDirector, Totals >= quantile(Totals,0.95))
ggplot(aes(y=reorder(selectionDirector,-Totals), x=Totals), data=top_20_director) +
  geom_point()+ 
  ggtitle("Distribution of Votes by Director")+
  ylab("Number of Votes")+
  xlab("Each vote represents a director")

#But this was hard to read so I reduced
top_20_director <- subset(votesbyDirector, Totals >= quantile(Totals,0.975))
ggplot(aes(y=reorder(selectionDirector,-Totals), x=Totals), data=top_20_director) +
  geom_point()+ 
  ggtitle("Top 2.5% Most Voted For Directors")+
  xlab("Number of Votes")+
  ylab("Director")

#But I also wanted to see how it would look with the director's most active decade included
director_groups <- group_by(critic_data, selectionDirector)
votesbyDirector <- summarise(director_groups,
                             Active_Decade = median(decade),
                             Totals = n())

votesbyDirector$Active_Decade<- as.factor(votesbyDirector$Active_Decade)

votesbyDirector$Active_Decade <- votesbyDirector$as.factor(Active_Decade)
top_20_director <- subset(votesbyDirector, Totals >= quantile(Totals,0.975))
top.1.perc.director <- subset(votesbyDirector, Totals >= quantile(Totals,0.99))
total20 <- ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=top_20_director) +
  geom_point(size = 5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Top 2.5% Most Voted For Directors")+
  ylab("Number of Votes")+
  xlab("Director")+
  scale_color_brewer(palette = "Paired")+
  scale_fill_brewer(palette = "Paired")+
  coord_flip()

total20

#From these plots we can see who the directors are who have the highest number of votes
#We can also see what decade that they represent.
#In particular, we can see a prevalence of directors that were most active in the 1950s
#and 1960s with a smattering of other decades. The newest director in the set is David Lynch
#active in the 1990s and the earliest are Sergei Eisenstein and F.W. Murnau from the silent 
#era in the 1920s. Also notable is Michael Powell and Emeric Pressburger (Also known as the Archers)
#who are the only duo on this list.

#Due to the highly skewed nature of the voters, I thought it might be interesting to 
#see if the most influential directors differed significantly by country.

Spain.votes <- subset(critic_data, country=="Spain")
director.spain_groups <- group_by(Spain.votes, selectionDirector)
votesbyDirectorSpain <- summarise(director.spain_groups,
                             Active_Decade = median(decade),
                             Totals = n())

votesbyDirectorSpain.Top <- subset(votesbyDirectorSpain, Totals >= quantile(Totals,0.9))
votesbyDirectorSpain.Top$Active_Decade <- as.factor(votesbyDirectorSpain.Top$Active_Decade)
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=votesbyDirectorSpain.Top) +
  geom_point(size=5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Distribution of Spanish Votes by Director")+
  xlab("Number of Votes")+
  ylab("Each vote represents a director")+
  scale_color_brewer(palette = "Dark2")+
  scale_fill_brewer(palette = "Dark2")+
  coord_flip()

#I decided to turn it into a function
top.directors.countries <- function(data, country.name, percentile) {
  votes <- subset(data, country.name==country)
  director.groups <- group_by(votes, selectionDirector)
  votesbyDirector <- summarise(director.groups,
                               Active_Decade = median(decade),
                               Totals = n())
  votesbyDirector.Top <- subset(votesbyDirector, Totals >= quantile(Totals, percentile))
  votesbyDirector.Top$Active_Decade<-as.factor(votesbyDirector.Top$Active_Decade)
  return(data.frame(votesbyDirector.Top)) 
} 

spain.directors <- top.directors.countries(critic_data, "Spain", 0.85)
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=spain.directors) +
  geom_point(size=5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Distribution of Spanish Votes by Director")+
  xlab("Directors")+
  ylab("Number of Votes")+
  scale_color_brewer(palette = "Paired")+
  scale_fill_brewer(palette = "Paired")+
  coord_flip()


#Unsurprisingly Luis Bunuel, an extremely influential Spanish director comes in second
#Even though he comes in 15th in the general poll. Also, John Ford, particularly famous
#For westerns tops the poll, even though he ranks 14th in the original poll.
#Also the Spanish voters seem particularly partial to movies from the 1950s and sixties

France.directors <- top.directors.countries(critic_data, "France", 0.85)
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=France.directors) +
  geom_point(size=5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Distribution of French Votes by Director")+
  xlab("Directors")+
  ylab("Number of Votes")+
  scale_color_brewer(palette = "Paired")+
  scale_fill_brewer(palette = "Paired")+
  coord_flip()

#Compared with the other countries, France has choices representing a wide swath of decades.

UK.directors <- top.directors.countries(critic_data, "UK", 0.95)
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=UK.directors) +
  geom_point(size=5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Distribution of UK Votes by Director")+
  xlab("Directors")+
  ylab("Number of Votes")+
  scale_color_brewer(palette = "Paired")+
  scale_fill_brewer(palette = "Paired")+
  coord_flip()

#Powerll and Pressburger score particularly high in England.

US.directors <- top.directors.countries(critic_data, "US", 0.93)
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=US.directors) +
  geom_point(size=5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Distribution of US Votes by Director")+
  xlab("Directors")+
  ylab("Number of Votes")+
  scale_color_brewer(palette = "Paired")+
  scale_fill_brewer(palette = "Paired")+
  coord_flip()

Germany.directors <- top.directors.countries(critic_data, "Germany", 0.85)
ggplot(aes(x=reorder(selectionDirector,-Totals), y=Totals, color=Active_Decade, fill=Active_Decade), data=Germany.directors) +
  geom_point(size=5)+ 
  geom_bar(stat="identity", width=0.1) +
  ggtitle("Distribution of German Votes by Director")+
  xlab("Directors")+
  ylab("Number of Votes")+
  scale_color_brewer(palette = "Paired")+
  scale_fill_brewer(palette = "Paired")+
  coord_flip()
#F.W. Murnau and Fritz Lang, both early German film makers score high.


#Now I would like to make a chart showing variability in rankings by country

#Groups critic_data by Director and Country and creates 
#a new dataset with the total number of votes per director in each country
director.country.groups <- group_by(critic_data, selectionDirector, country)
votes.by.director.country <- summarise(director.country.groups,
                                  Totals = n())

#Adds a column that ranks directors from most to least number of votes by country
votes.by.director.country <- transform(votes.by.director.country, 
          director.rank = ave(Totals, country, 
                          FUN = function(x) rank(-x, ties.method = "first")))

#These next steps keep only directors in the top 1 percentile of overall votes

#converts the column of directors in top.1.perc.director into a vector
directors <- top.1.perc.director[['selectionDirector']]
#creates a boolean vector with TRUE representing all directors in the list directors
keep <- apply(votes.by.director.country,1,function(x) any(x %in% directors))
#uses the boolean vector to subset the data, keeping only True values
top.votes.by.director.country <- votes.by.director.country[keep,]

top.votes.by.director.country$selectionDirector <- as.factor(top.votes.by.director.country$selectionDirector) 

#This was my first attempt. It was a complete mess.
ggplot(aes(x=country, y=director.rank, color=selectionDirector, group=1), data=top.votes.by.director.country) +
  geom_line()

#So I thought I might look director by director starting at the top
ggplot(aes(x=reorder(country, director.rank), y=director.rank, group=1), data=subset(top.votes.by.director.country,selectionDirector == "Alfred Hitchcock")) +
         geom_line() + 
         coord_flip() +  
  ggtitle("Rankings of Alfred Hitchcock across countries")+
  xlab("Ranking") +
  ylab("Country")

#I thought I would look at the whole set of top directors
ggplot(aes(x=reorder(country, director.rank), y=director.rank, group=1), data=top.votes.by.director.country) +
  geom_line(color='black') +
  coord_flip() +
  facet_wrap(~selectionDirector) +
  theme(axis.text.x=element_blank())+
  scale_x_discrete(breaks=NULL) +
  xlab("Director Rank") +
  ylab("Country")+
  ggtitle("Relative rankings of top directors across countries")
#But this was a bit hard to see so I added some color

#so I decided to create a dataset with just the top 10 countries
top_10_countries <- subset(votersbyCountry, Totals >= quantile(Totals,0.935))[['country']]
keep <- apply(top.votes.by.director.country,1,function(x) any(x %in% top_10_countries))
top.votes.by.director.country <- top.votes.by.director.country[keep,]

ggplot(aes(x=reorder(country, director.rank), y=director.rank, group=1,color=country), data=top.votes.by.director.country) +
  geom_line(color='black') + 
  geom_point(size=5) +
  coord_flip() +
  facet_wrap(~selectionDirector)
#But this looked a bit messy so I changed the background

rects <- data.frame(xstart = seq(0.5,9.5,1), xend = seq(1.5,10.5,1), col = c("US","UK","Sweden","Spain","Italy","Germany","France","Canada","Australia","Argentina"))

ggplot() +
  geom_point(data=top.votes.by.director.country, aes(x=country, y=director.rank, group=1)) +
  geom_line(data=top.votes.by.director.country, color='black', aes(x=country, y=director.rank, group=1)) +
  geom_rect(data=rects,aes(ymin=0,ymax=80,xmin=xstart,xmax=xend,fill=col), alpha=0.5) +
  coord_flip() +
  facet_wrap(~selectionDirector) +
  theme(legend.position="none") +
  scale_fill_brewer(palette = "Set3")
#And this made it much easier to read this chart.  

ggplot(aes(x=reorder(country, director.rank), y=director.rank, group=1,color=country), data=top.votes.by.director.country) +
  geom_line(color='black') + 
  geom_point(size=5) +
  coord_flip() +
  facet_wrap(~selectionDirector)

ggplot(aes(x=country, y=director.rank, color = selectionDirector), data=top.votes.by.director.country) +
  geom_point() + 
  coord_flip() +
  scale_fill_brewer(palette = "Paired")
  
ggplot(aes(country, director.rank, group = selectionDirector, color=selectionDirector), data=top.votes.by.director.country)+
  geom_line()+
  coord_cartesian(ylim = c(0,40))

