#!/usr/bin/env python

import sys
import psycopg2 as psycopg2

DATABASE_NAME = 'news'


def popular_articles():
    connection = psycopg2.connect(database=DATABASE_NAME)
    cursor = connection.cursor()
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
    cursor.execute(query=query)
    result = cursor.fetchall()
    connection.close()
    return result


def popular_article_authors():
    connection = psycopg2.connect(database=DATABASE_NAME)
    cursor = connection.cursor()
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
    cursor.execute(query=query)
    result = cursor.fetchall()
    connection.close()
    return result


def day_requests_error_percentage():
    connection = psycopg2.connect(database=DATABASE_NAME)
    cursor = connection.cursor()
    query = '''
    SELECT
        to_char(day, 'Month DD, YYYY'),
        (error_count * 100.0 / total_count) AS percentage
    FROM
      per_day_log_count
    WHERE
      (error_count * 100.0 / total_count) > 1.0
    '''
    cursor.execute(query=query)
    result = cursor.fetchall()
    connection.close()
    return result


if __name__ == '__main__':
    action = sys.argv[1]
    if action == '1':
        print('\n Computing the most popular three articles of all time...')
        articles = popular_articles()
        count = 1
        for article in articles:
            print('\n %d. "%s" - %d' % (count, article[1], article[2]))
            count = count + 1

        print('\n Done printing %d results.\n' % (count - 1))

    elif action == '2':
        print('\n Computing the most popular article authors of all time...')
        article_authors = popular_article_authors()
        count = 1
        for article_author in article_authors:
            print('\n %d. "%s" - %d' % (count, article_author[1],
                                        article_author[2]))
            count = count + 1

        print('\n Done printing %d results.\n' % (count - 1))

    elif action == '3':
        print('\n Computing the days with more than 1% of requests'
              ' leading to error...')
        days = day_requests_error_percentage()
        count = 1
        for day in days:
            print('\n %d. %s - %.1f%% errors' % (count, day[0], day[1]))
            count = count + 1

        print('\n Done printing %d results.\n' % (count - 1))

    else:
        print('\n Invalid action!\n\n Actions which can be performed are:'
              '\n\n 1 - Compute the most popular three articles of all time'
              '\n\n 2 - Compute the most popular article authors of all time'
              '\n\n 3 - Compute the days with more than 1% of requests'
              ' leading to error'
              '\n\n NOTE: Before using this module execute the "views.sql"'
              ' in your copy of "news" database to create required views.\n')
