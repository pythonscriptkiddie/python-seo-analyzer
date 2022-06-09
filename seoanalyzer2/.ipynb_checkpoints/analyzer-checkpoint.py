import json
import time

from operator import itemgetter
from seoanalyzer2.website import Website

def analyze(url, sitemap_url=None, analyze_headings=False,
    analyze_extra_tags=False, follow_links=True,
    min_title_length=10, max_title_length=70,
    min_description_length=120, max_description_length=255):
    print(min_description_length)
    print(max_description_length)
    print(min_title_length)
    print(max_title_length)
    start_time = time.time()

    def calc_total_time():
        return time.time() - start_time

    output = {'pages': [], 'keywords': [], 'errors': [], 'total_time': calc_total_time()}

    site = Website(url, sitemap_url, analyze_headings, analyze_extra_tags, follow_links,
                  min_title_length, max_title_length, min_description_length,
                  max_description_length)

    site.crawl()

    for p in site.crawled_pages:
        output['pages'].append(p.talk())

    output['duplicate_pages'] = [list(site.content_hashes[p]) for p in site.content_hashes if len(site.content_hashes[p]) > 1]

    sorted_words = sorted(site.wordcount.items(), key=itemgetter(1), reverse=True)
    sorted_bigrams = sorted(site.bigrams.items(), key=itemgetter(1), reverse=True)
    sorted_trigrams = sorted(site.trigrams.items(), key=itemgetter(1), reverse=True)

    output['keywords'] = []

    for w in sorted_words:
        if w[1] > 4:
            output['keywords'].append({
                'word': w[0],
                'count': w[1],
            })

    for w, v in sorted_bigrams:
        if v > 4:
            output['keywords'].append({
                'word': w,
                'count': v,
            })

    for w, v in sorted_trigrams:
        if v > 4:
            output['keywords'].append({
                'word': w,
                'count': v,
            })

    # Sort one last time...
    output['keywords'] = sorted(output['keywords'], key=itemgetter('count'), reverse=True)

    output['total_time'] = calc_total_time()

    return output
