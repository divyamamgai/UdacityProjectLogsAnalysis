CREATE VIEW articles_path AS
  SELECT
    id,
    ('/article/' || slug) AS path
  FROM articles;

CREATE VIEW per_day_log_count AS
    SELECT
      date_trunc('day', time) AS day,
      count(*) AS total_count,
      count(CASE WHEN status != '200 OK' THEN 1 END) AS error_count
    FROM
      log
    GROUP BY day;