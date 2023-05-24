# Envision

## Motivation for the Project
This is a project done under IEEE NITK where the goal is to identify the irrelevant tweets with respect to a particular trend and removing them from the User's feed.
It helps in keeping the feed clean and improves the User experience while using the application.

An external twitter scraper is being which scrapes the tweets using Golang. The steps to install it are as follows:
## Requirements before downloading the Twitter Scraper
Install Go from the website

### Enable dependency tracking for your code
For enabling dependency tracking of the code you have to create a go.mod file
Run the command 
```
go mod init [path-to-module]
```
path-to-module needs to be the location of a remote repository from where Go can download the source code.
Typically, it's of the format
```
<prefix>/<descriptive-text>
```
Example: github.com/<project-name>

## Installation of the scraper

```shell
go get -u github.com/n0madic/twitter-scraper
```
## Setting up the Project
Clone the repository using the HTTPS key:
```
  https://github.com/helios2003/Twitter-Feed-Filter.git
```
Or you can fork the repository and git clone it from there.

Navigate to the root directory and do the following:
### For Windows
```
  python -m venv venv
  venv/Scripts/activate
  pip install -r src/python/requirements.txt
```
### For Linux
```
  python -m venv venv
  source venv/bin/activate
  pip install -r src/python/requirements.txt
``` 
Navigate to ``flask`` directory for how to run the web app. 
  
