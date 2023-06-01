import sentiment_analysis.analysis
import reddit.scraper
import instagram.scraper
import twitter.scraper

def scrapeSites(location, topic, limit=50):
    # text.append(reddit.scraper.scrape(location, topic, limit))
    final = instagram.scraper.scraper(location, topic, limit) + twitter.scraper.scrape(location, topic, limit)
    print(final)
    return analyse(final)

def analyse(text):
    return sentiment_analysis.analysis.analyse(text)
