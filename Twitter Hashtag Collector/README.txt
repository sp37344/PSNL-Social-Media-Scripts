Twitter Hashtag Collector
Author: Sarah Pan 

GENERAL USAGE
--------------------------------------------------------------------------------
To run program, go to terminal and enter folder where program is stored. 
Program requires Python 3. 
To run command: 
 -- python twitter_hashtag.py

Output file is dated and named as trending_hashtags_<date>. Two intermediate 
files trending_hashtags and trending_hashtags_woeid are also created in the 
process.  

PROGRAM OPTIONS
---------------------------------------------------------------------------------
There are Steps 1, 2, and 3 within the main function. 
Step 1 extracts the woeid (identifier) for each region
Step 2 collects hashtags for each region 
Step 3 converts data to csv 

User can comment out step 1 and 2 (woeid_collector() and hashtag_collector()) 
when twitter quota is exceeded. However, step 3 will not extract any twitter 
information.