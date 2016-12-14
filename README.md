# maxent_cv
maximum entropy for NLP in Japanese

you need csv file which includes..
text in Japanese to analyze and Tag(ex. "good" & "bad")

I used original csv file which includes..
-companyname #each name of comapny
#preparation
ntlk(Natural Language Toolkit) from http://www.nltk.org/

#texts
-message_top #message for public on each comapny's website
-message_president #message for stock holders on each comapny's website

#scores
-company_score #score for company obtained from https://en-hyouban.com/
-president_score #score for president obtained from https://en-hyouban.com/
-votes #number of votes for scores obtained from https://en-hyouban.com/

#created tags from scores (companyes&presidents with higher scores :"good", companyes&presidents with lower scores :"bad")
-comapny_tag20 #top 20% of companies in comapny_score and lowest 20% of companies in comapny_score
-president_tag20 #top 20% of companies in president_score and lowest 20% of companies in president_score
-comapny_tag10 #top 10% of companies in comapny_score and lowest 10% of companies in comapny_score
-president_tag10 #top 10% of companies in president_score and lowest 10% of companies in president_score
