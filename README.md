# playdimplomacy_database

This repository contains a large database of the game logs of the [Diplomacy](https://en.wikipedia.org/wiki/Diplomacy_(game)) board game. The data originates from the [playdiplomacy.com](http://playdiplomacy.com) website, which is the biggest platform offering an opportunity to play Diplomacy online. Playdiplomacy.com stores the logs of all of the games played through this platform and they are publically available for registered users. I have scraped most of the games from this site.

The main directory contains the scripts used to clean the data and the configuration file for the spider. The "diplomacy"  folder contains the spider. The "database" folder contains the data itself. The GitHub repository restricts the data size, that's why the full database can not be found in this repository. It can be downloaded from [Google Drive](https://drive.google.com/open?id=0BwwtOX84gTgFdGtQSk5oQmVsbWM) and should be put into the "database" folder in order for everything to work correctly. The "database" folder also contains some portions of the data, that can be of interest and fit the file size constraints: the full list of the games with full information except for the turns made, the subsample of ranked classic games with random choice of the countries and no anonimity or negotiation constraints.

This README contains a short introduction into Diplomacy as well as into the history of statistical an strategical analysis of the game. Next I give my motivation of why this database can be of use for Diplomacy fans and probably for more serious researchers. Then I describe the sample, the data scraping process and document my code. Then I give some simple discriptive statistics which can give an idea of the balance of the game. Finally, I indicate the ways of future improvements of the database.

# Diplomacy and the Postal ages datasets
To be written

# What can I do with it?
Richard Sharp's analysis relies on his own experience of playing Diplomacy as well as on Postal statistics, which he was disposing. However, his biggest database was no more than 1000 observations, which 1) is probably not enough for his extensive use of observed conditional probabilities 2) doesn't allow to inspect some interesting observations one can consider. 

One could be interested to compare the figures used by Sharp to the same statistics based on this database. However, Sharp presents his figures in a messy way and it takes time and work with text, to bring them into order. I hope at some point you will see the results in the 'comparison to the existing databases' section.

Going further, we can take some of Sharp's observations and test them against the data we have. Is Austria indeed strong given that it survived several first turns? Is Germany the most powerful nation in the game, given that an experienced player controls it? Do England gain more than France from the firecease in the English Channel? The dataset also allows us to pose some questions beyond Sharp's observations.

For now I don't think the database is of use for empirical research in Economics/Game Theory. But why not to give it a try? Probably, the data could be used for a do-people-maximize kind of research. This question has been inspected on a wide range of gamified settings including soccer (Chiappori et al., 2002), tennis (Walker & Wooders, 2001), cycling (Mignot, 2016), TV Shows (Metrick, 1995, Gertner, 1998), Blackjack (Carlin & Robinson, 2009). As far as search took me I couldn't find any use of board game data in social sciences.

Another possible way is to use Varian's (1982) approach to analyse predictive power of solution concepts considered in Game Theory. This of course won't give us an idea of why people are playing equilibrium, but at least we'll have a chance to reject some solution concepts in certain settings.

There are several possible modes of the game, which either restrict or not the negotiation between the countries and either provides or not anonimity to the players. This variation could also be used to test some hypotheses.

# Data and Code description

The repository contains the code I used to scrap the data from the playdiplomacy.com website along with the data itself. This is done for transperency and replicability. However, I urge you not to use the scraper if you have not a good reason to do so. It took my computer two weeks of pure time to complete the scraping task. Scraping is always costly for the server you are crawling. It is strongly recommended to be gentle and respectful to the data owner's server or he could restrict the data access or corrupt the work of scrapers in any other way. For this reason I do not document the scraper itself. I want to create some costs of usage and to ensure that the user have a good reason to run the spider.

I did my best to make the code itself as clear as possible. You are also welcome to read the documentation of the framework I've been using (https://scrapy.org/).

![alt tag](https://github.com/go95/playdimplomacy_database/blob/master/sample.jpg)

To be written: fields, sample, scraping process, data organisation in the database, playdiplomcay specifics, online gaming specifics

# Descriptive statistics and comparison to the existing databases

To be written.

To start with let us take a look at the overall game balance. This is the survival rate of the countries in the ranked classic games with random choice of the countries. It shows, at what rate each of the country survives till the end of the game.

| Country | Survival rate |
| ------- | ------------- | 
| Turkey  |	0,328         |
| France  |	0,312         |
| England |	0,300         |
| Germany |	0,264         |
| Russia  |	0,263         |
| Austria |	0,236         |
| Italy   | 0,214         |
| N Games | 13124         |
Here are the winning rates. How often a country wins in a single winner game.

| Country | Winning rate  |
| ------- | ------------- | 
| Russia  |	0,187         |
| Turkey  |	0,174         |
| France  |	0,153         |
| Germany |	0,142         |
| England |	0,123         |
| Austria |	0,121         |
| Italy   |	0,096         |
| N Games | 6148          |

# Further improvements

To be written

# References

Carlin, B. I., & Robinson, D. T. (2009). Fear and loathing in Las Vegas: Evidence from blackjack tables (No. w14955). National Bureau of Economic Research.

Chiappori, P. A., Levitt, S., & Groseclose, T. (2002). Testing mixed-strategy equilibria when players are heterogeneous: The case of penalty kicks in soccer. American Economic Review, 1138-115

Gertner, R. (1993). Game shows and economic behavior: risk-taking on" Card Sharks". The Quarterly Journal of Economics, 108(2), 507-521.

Metrick, A. (1995). A natural experiment in" Jeopardy!". The American Economic Review, 240-253.

Mignot, J. F. (2016). Strategic Behavior in Road Cycling Competitions. In The Economics of Professional Road Cycling (pp. 207-231). Springer International Publishing.

Selten, R. (1991). Properties of a measure of predictive success. Mathematical Social Sciences, 21(2), 153-167.

Sharp, R. (1978). The Game of Diplomacy. A. Barker. (http://www.diplomacy-archive.com/god.htm)

Walker, M., & Wooders, J. (2001). Minimax play at Wimbledon. The American Economic Review, 91(5), 1521-1538.
