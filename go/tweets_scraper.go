package main

import (
    "bufio"
    "context"
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
    scraper := twitterscraper.New()

    // Read the queries from a text file named "queries.txt"
    queryFile, err := os.Open("files/required_trends.txt")
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
        for tweet := range scraper.SearchTweets(context.Background(), query, 10) {
            if tweet.Error != nil {
                continue
            }
            // Extract only the text part of the tweet and exclude the links
            text := strings.Split(tweet.Text, "http")[0]

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
        file, err := os.Create("files/" + trend + ".txt")
        if err != nil {
            panic(err)
        }
        defer file.Close()

        // Write each tweet to a new line in the file
        for i, tweet := range tweets {
            _, err = file.WriteString(fmt.Sprintf("%d. %s\n", i+1, tweet))
            if err != nil {
                panic(err)
            }
        }
    }
}