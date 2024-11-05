---
Title: Electoral College Data Scraper (270toWin)
Author: Sam Lee
---

# Electoral College Data Scraper and Analysis

This repository provides tools to scrape, process, and analyze U.S. Electoral College data from electoral maps. The project leverages Selenium for web scraping and custom JavaScript to extract electoral vote data for each state. The data is then analyzed using Python to calculate party metrics, including total electoral votes.

## Project Structure

- **`fips.py`**: This script downloads and preprocesses FIPS codes (Federal Information Processing Standards) for U.S. states. It maps state names to their abbreviations and saves the resulting data as `fips.csv`, which is used in data analysis and merging with electoral data.

- **`analyze.py`**: Contains the `Analysis` class, which takes scraped electoral data and performs metrics calculations. It reads saved electoral maps, processes vote counts for each party, and prepares data for further insights.

- **`ec.js`**: A JavaScript file injected into the electoral map webpage to extract relevant data. It defines three main functions:
  - `getElectoralCollegeData`: Collects electoral votes for each state from HTML elements on the page.
  - `getPathData`: Extracts voting data by detecting path colors for each state, associating colors with either the Democratic or Republican party.
  - `getSpecial`: Specifically handles Maine and Nebraska, which split electoral votes by district, retrieving party-specific vote counts based on district color coding.

- **`ec_scraper.py`**: The main scraping and data processing script. It uses Selenium to navigate the electoral map site, injects `ec.js` to extract data, and merges it with FIPS codes and electoral vote data. The `Scraper` class includes methods for accessing, processing, and saving data, while handling special cases like Maine and Nebraska. It also initiates an analysis on the scraped data.
