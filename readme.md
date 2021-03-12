Scrape viewed movies on imdb to identify the most viewed actors.

Using Selenium we access the first page with rated movies on a personal IMDB account and scrape through all the pages to find the individual links for each movie. Looping through the list of links, we will access each one of them and get the title, year and the main actors from the page (not the cast page).

We can write the data into an excel file using openpyxl. The file will have 3 columns: actor name, number of movies, the movie list in a chronological order.