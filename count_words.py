#!/usr/bin/env python
import io
import csv
import json
import string
import itertools
from datetime import datetime
from collections import Counter
from stop_words import stop_words
from pipeline import Pipeline

pipeline = Pipeline()


def build_csv(lines, header=None, file=None):
    if header:
        lines = itertools.chain([header], lines)
    writer = csv.writer(file, delimiter=',')
    writer.writerows(lines)
    file.seek(0)
    return file


@pipeline.task()
def file_to_json():
    with open('hn_stories_2014.json') as file:
        stories = json.loads(file.read())['stories']
    return stories


@pipeline.task(depends_on=file_to_json)
def filter_stories(stories):
    for story in stories:
        condition = story['points'] > 50 and story['num_comments'] > 1 and not story['title'].startswith('Ask HN')
        if condition:
            yield story


@pipeline.task(depends_on=filter_stories)
def json_to_csv(stories):
    lines = []
    cols = ['objectID', 'created_at_i', 'url', 'points', 'title']
    for story in stories:
        line = [story[col] for col in cols]
        line[1] = datetime.fromtimestamp(line[1] / 1e3)
        lines.append(line)
    return build_csv(lines, header=cols, file=io.StringIO())


@pipeline.task(depends_on=json_to_csv)
def extract_titles(file):
    csv_file = csv.reader(file)
    header = next(csv_file)
    title_idx = header.index('title')
    for line in csv_file:
        yield line[title_idx]


@pipeline.task(depends_on=extract_titles)
def clean_titles(titles):
    for title in titles:
        title = title.lower().translate(str.maketrans('', '', string.punctuation))
        yield title


@pipeline.task(depends_on=clean_titles)
def build_keyword_dictionary(titles):
    for title in titles:
        words = title.split()
        words = [word for word in words if word not in stop_words and word != '']
        counter = Counter(words)
        yield counter


@pipeline.task(depends_on=build_keyword_dictionary)
def top_words(counters):
    top_words_count = Counter()
    for counter in counters:
        top_words_count.update(counter)
    return top_words_count.most_common(100)


count = pipeline.run()
print(count[top_words])
