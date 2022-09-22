# League_of_Legends_ML
This project was developped by John Payne as a final project for Lighthouse Labs
-- Project Status [Active]

### Project Intro
League of Legends(LoL) has around 117 million active players per month and is played in places such as Korea, North America, Europe and China. Venues such as Madison Square Garden and the Scotiabank Arena have hosted LoL tournaments to great success and Riot Games, the developers of LoL, have managed to stay the most played MOBA for over 10 years. In this project I aimed to analyze the best players in North America to see which strategies boasted the most success. Furthermore, I applied Machine Learning Techniques to predict the winners of high level games. Over the years betting has increased in popularity and I believe a ML model that can predict game outcomes will become increasingly valuable. 

### Methods Used
* Inferential Statistics
* Machine Learning
* Data Visualization
* Predictive Modeling

### Technologies
* Python
* Pandas, Jupyter
* Riot APIs


### Project Description
Before I started coding I needed to find out where and how I was going to get my data. Riot Games spreads out its data in multiple APIs each with their own distinct data types. For example, player data, match data, and overall ranking of players data were all stored in the different APIs. In the Match_History.py file I have the code that joined together data returned from the League V4 API(Held Rank data), Summoner V4 (Held Player data), and Match V5 (Held Match data) APIs. All the functions and classes used can be found in the Functions_Classes folder. 

Because my Project could not be approved by Riot Games for a professional API key due to it potentially solving the game I had to gather data using the free tier key. This key only allowed me to make 100 requests every 2 minutes which greatly slowed my data gathering. Fortunately, for my initial modeling phase I was still able to gather 1200+ unique games using my script. Furthermore, merging the data together was a difficult task as I didn't want to mix up games. To solve this problem I used a match class to hold all information pertaining to a specific match. Every call of the match class would call the Match V5 API once and then parsed through the json response for the data I specified. This allowed me to easily make changes to the script and ensure match data stayed contained. Once all data was parsed I then dumped it into multiple CSV files which can be found in the data folder. I split up the CSV files because I wasn't sure what data I needed for my initial features and knew the order was preserved as the index for each file was the game ID.

Once my data was gathered I imported my files into pandas. Each cell in pandas contained a list with specific data such as wins/losses, player names etc. I created loops to parse out this information and then merged it into a large dataframe. My project was a binary prediciton (win/loss) and thus, I had to find a way to store all data pertaining to a game into a single row. At the time I had 10 rows dedicated for a game with each row representing a single player. One possible solution was pivoting all 10 of the rows into new columns; however, this made me uneasy as I didn't want to have too many features. My final solution was to instead take aggregation scores for each team and then find the difference. For example, winrate was a feature I wanted to capture in my model. To do this I took the mean winrate for each team and then found the difference and used that as the score for each team.

I created the following features for my final predictive model:
* Difference in rank
* Difference in winrate
* Difference in number of veterans
* Difference in number of players on a winstreak
* Difference in number of players playing popular champions

With this model I achieved 65% accuracy which was a 20% increase from just picking team1 or team2 winning every game.
In the Steps.ipynb file I have all my steps in the project listed.

### Next Steps
In the Steps.ipynb I created a model using features it shouldn't have access to such as Cs/Min, Vision_score/Min and KDA. The model had an accuracy of 97.2 and I think a model using those features as an aggreagate of their stats over the year instead of just the specific game could yield much better results than 65%. I have attempted to create a webscraper to take aggregated player data from the popular site opgg.com; however, some of their html code looks to be protected. This leaves me with the option of either scrapping off a lesser known site or generating my own SQL database to hold player data. Unfortunately, with riots rate limits and the fact I would have to store all matches played by a player and then aggregate thier stats and then repeat this for the 1000+ players in high ranking it may not be possible. 

Whether or not the aggregated stats feature becomes a reality I still plan on deploying my model onto a website so the general public can predict their own games.
The following are tasks to do:
* More data mining using webscraping from popular sites
* SQL database creation
* Model deployment

### Getting Started
* Clone the repo
* Run the match_history.py script to collect your own data (Some data is already stored in the data folder)
* Use grid.predict on the final cell in Steps.ipynb with your data in the format (LP difference, Winrate difference, Veteran difference, Winstreak difference, Meta Champions difference) to see your chances of winning!

### Contact
* [John Payne](https://github.com/JDPayne11)
* Email paynejohn888@gmail.com 

