package main

import (
	"bufio"
	"context"
	"encoding/csv"
	"fmt"
	"os"
	"strings"

	twitterscraper "github.com/n0madic/twitter-scraper"
)

func not_main() {
	scraper := twitterscraper.New()
	trends, err := scraper.GetTrends()
	if err != nil {
		panic(err)
	}

	// Create a new file named "trends.txt" and open it for writing
	file, err := os.Create("files/trends.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	// Write each trend to a new line in the file
	for _, trend := range trends {
		_, err = file.WriteString(fmt.Sprintf("%v\n", trend))
		if err != nil {
			panic(err)
		}
	}
}

func main() {
	not_main()
	scraper := twitterscraper.New()
	// Read the queries from a text file named "trends.txt"
	queryFile, err := os.Open("files/trends.txt")
	if err != nil {
		panic(err)
	}
	defer queryFile.Close()

	// Create a map to store tweets for each trend
	trendTweets := make(map[string][]string)
	// Read each query from the file and run Twitter search for it
	scanner := bufio.NewScanner(queryFile)
	for scanner.Scan() {
		query := strings.TrimSpace(scanner.Text())
		// Search for tweets for the current query
		scraper.SetSearchMode(twitterscraper.SearchLatest)
		for tweet := range scraper.GetTweets(context.Background(), query, 20) {
			if tweet.Error != nil {
				continue
			}

			// Extract only the text part of the tweet and exclude the links
			text := strings.Split(tweet.Text, "http")[0]
			// Remove "@" symbols from the tweet text
			text = strings.ReplaceAll(text, "@", "")

			// Add the tweet to the corresponding trend in the map
			trendTweets[query] = append(trendTweets[query], text)
		}
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}
	
	// Create a new file for each trend and write the tweets to it
	for trend, tweets := range trendTweets {
		// Create a new file for the current trend and open it for writing
		file, err := os.Create("files/" + trend + ".csv")
		if err != nil {
			panic(err)
		}

		// Create a CSV writer for the file
		writer := csv.NewWriter(file)

		 // Write the header row
		writer.Write([]string{"tweet"})

		// Write each tweet to a new row in the CSV file
		for _, tweet := range tweets {
			err := writer.Write([]string{tweet})
			if err != nil {
				panic(err)
			}
		}

		// Flush the data to the file and close the writer
		writer.Flush()
		if err := writer.Error(); err != nil {
			panic(err)
		}
		file.Close()
	}
}
