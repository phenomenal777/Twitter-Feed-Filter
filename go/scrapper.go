package main

import (
    "fmt"
    "os"
    twitterscraper "github.com/n0madic/twitter-scraper"
)

func main() {
    scraper := twitterscraper.New()
    trends, err := scraper.GetTrends()
    if err != nil {
        panic(err)
    }

    // Create a new file named "trends.txt" and open it for writing
    file, err := os.Create("trends.txt")
    if err != nil {
        panic(err)
    }
    defer file.Close() // Ensure the file is closed at the end of the function

    // Write each trend to a new line in the file
    for _, trend := range trends {
        _, err = file.WriteString(fmt.Sprintf("%v\n", trend))
        if err != nil {
            panic(err)
        }
    }
}

