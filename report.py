#!/usr/bin/env python

import sys
import psycopg2 as psycopg2

DATABASE_NAME = 'news'


def get_query_results(query):
    try:
        connection = psycopg2.connect(database=DATABASE_NAME)
    except psycopg2.Error as error:
        print('\n Cannot connect to the "%s" database!\n\n Error - %s'
              % (DATABASE_NAME, error))
        sys.exit(1)
    else:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result


def popular_articles():
    query = '''
    SELECT
      articles.id,
      articles.title,
      count(*) AS views
    FROM
      articles
      JOIN articles_path
        ON articles_path.id = articles.id
      JOIN log
        ON log.path = articles_path.path
    WHERE LOG.status = '200 OK'
    GROUP BY articles.id, articles.title
    ORDER BY views DESC
    LIMIT 3
    '''
    return get_query_results(query)


def popular_article_authors():
    query = '''
    SELECT
      authors.id,
      authors.bio,
      count(*) AS views
    FROM
      authors
      JOIN articles
        ON articles.author = authors.id
      JOIN articles_path
        ON articles_path.id = articles.id
      JOIN log
        ON log.path = articles_path.path
    WHERE LOG.status = '200 OK'
    GROUP BY authors.id, authors.bio
    ORDER BY views DESC
    LIMIT 4
    '''
    return get_query_results(query)


def relevant_day_error_percentages():
    query = '''
    SELECT
        to_char(day, 'Month DD, YYYY'),
        (error_count * 100.0 / total_count) AS percentage
    FROM
      per_day_log_count
    WHERE
      (error_count * 100.0 / total_count) > 1.0
    '''
    return get_query_results(query)


def print_popular_articles(articles):
    print('\n The most popular three articles of all time are:')
    count = 1
    for article in articles:
        print('\n %d. "%s" - %d' % (count, article[1], article[2]))
        count = count + 1
    return count - 1


def print_popular_article_authors(article_authors):
    print('\n The most popular article authors of all time are:')
    count = 1
    for article_author in article_authors:
        print('\n %d. "%s" - %d' % (count, article_author[1],
                                    article_author[2]))
        count = count + 1
    return count - 1


def print_day_requests_error_percentage(day_error_percentages):
    print('\n The days with more than 1% of requests  leading to error are:')
    count = 1
    for day_error_percentage in day_error_percentages:
        print('\n %d. %s - %.1f%% errors'
              % (count, day_error_percentage[0], day_error_percentage[1]))
        count = count + 1
    return count - 1


def print_actions():
    print('\n Invalid action!\n\n Actions which can be performed are:'
          '\n\n 1 - Compute the most popular three articles of all time'
          '\n\n 2 - Compute the most popular article authors of all time'
          '\n\n 3 - Compute the days with more than 1% of requests'
          ' leading to error'
          '\n\n NOTE: Before using this module execute the "views.sql"'
          ' in your copy of "news" database to create required views.\n')


def perform_action(number):
    print('\n Computing...')
    count = 0
    if number == '1':
        count = print_popular_articles(popular_articles())
    elif number == '2':
        count = print_popular_article_authors(popular_article_authors())
    elif number == '3':
        count = print_day_requests_error_percentage(
            relevant_day_error_percentages())
    print('\n Done printing %d results.\n' % count)


if __name__ == '__main__':
    action = sys.argv[1]
    if '1' <= action <= '3':
        perform_action(action)
    else:
        print_actions()
