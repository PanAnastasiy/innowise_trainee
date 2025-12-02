
-- 1. Display the number of films in each category, sorted in descending order.

EXPLAIN ANALYZE
SELECT name AS name_of_category,
       COUNT(film_id) AS count_of_films
FROM category
         LEFT JOIN film_category USING (category_id)
GROUP BY category_id
ORDER BY count_of_films DESC;

-- 2.1 Display the top 10 actors whose films were rented the most,
-- sorted in descending order.

EXPLAIN ANALYZE
SELECT CONCAT(last_name, ' ', first_name) AS full_name,
       COUNT(rental_id) AS rentals
FROM actor
         LEFT JOIN film_actor USING (actor_id)
         LEFT JOIN inventory USING (film_id)
         LEFT JOIN rental USING(inventory_id)
GROUP BY actor_id, full_name
ORDER BY 2 DESC
LIMIT 10;

-- 2.2 Display the top 10 actors whose films were rented the most,
-- sorted in descending order.

WITH actor_rental_stats AS (
    SELECT
        actor_id,
        CONCAT(last_name, ' ', first_name) AS full_name,
        COUNT(rental_id) AS rentals,
        DENSE_RANK() OVER (ORDER BY COUNT(rental_id) DESC) AS rnk
    FROM actor
             LEFT JOIN film_actor USING (actor_id)
             LEFT JOIN inventory USING (film_id)
             LEFT JOIN rental USING(inventory_id)
    GROUP BY actor_id, full_name
)
SELECT full_name,
       rentals
FROM actor_rental_stats
WHERE rnk <= 10
ORDER BY rentals DESC, full_name;

-- 3.1 Display the category of films that generated the highest revenue.

EXPLAIN ANALYZE
SELECT name AS name_of_category,
       COALESCE(SUM(amount), 0) AS revenue_of_category
FROM category
         LEFT JOIN film_category USING(category_id)
         LEFT JOIN inventory USING(film_id)
         LEFT JOIN rental USING (inventory_id)
         LEFT JOIN payment USING(rental_id)
GROUP BY category_id
ORDER BY revenue_of_category DESC;

-- 3.2 Display the category of films that generated the highest revenue.
EXPLAIN ANALYZE
WITH revenue AS (
    SELECT category_id,
           name,
           COALESCE(SUM(amount), 0) AS revenue,
           RANK() OVER (ORDER BY SUM(amount) DESC) AS rnk
    FROM category
             LEFT JOIN film_category USING(category_id)
             LEFT JOIN inventory USING(film_id)
             LEFT JOIN rental USING (inventory_id)
             LEFT JOIN payment USING(rental_id)
    GROUP BY category_id, name
)
SELECT name AS name_of_category,
       revenue AS revenue_of_category
FROM revenue
WHERE rnk = 1
ORDER BY name;

-- 4. Display the titles of films not present in the inventory.
-- Write the query without using the IN operator.

EXPLAIN ANALYZE
SELECT title AS films_not_presented
FROM film
         LEFT JOIN inventory USING (film_id)
WHERE inventory_id IS NULL;

-- 5. Display the top 3 actors who appeared the most in films within the "Children" category.
-- If multiple actors have the same count, include all.

EXPLAIN ANALYZE
SELECT full_name_of_actor,
       total_count_of_films,
       place_in_top
FROM (
         SELECT
             CONCAT(a.last_name, ' ', a.first_name) AS full_name_of_actor,
             COUNT(*) AS total_count_of_films,
             DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS place_in_top
         FROM actor a
                  JOIN film_actor fa USING(actor_id)
                  JOIN film_category fc USING(film_id)
                  JOIN category c USING(category_id)
         WHERE c.name = 'Children'
         GROUP BY a.actor_id, full_name_of_actor
     ) ranked
WHERE place_in_top < 4
ORDER BY total_count_of_films DESC;

-- 6. Display cities with the count of active and inactive customers (active = 1).
-- Sort by the count of inactive customers in descending order.

EXPLAIN ANALYZE
SELECT city AS name_of_city,
       COUNT(*) FILTER (WHERE active = 1) AS active_count,
       COUNT(*) FILTER (WHERE active = 0) AS inactive_count
FROM customer
         JOIN address USING(address_id)
         JOIN city USING (city_id)
GROUP BY city_id, city
ORDER BY inactive_count DESC;

-- 7.1 Display the film category with the highest total rental hours in cities
-- where customer.address_id belongs to that city and starts with the letter "a".
-- Do the same for cities containing the symbol "-". Write this in a single query.

-- Больно... Тут join-ны столько хавают... (Nested Loop) Но подругому пока не знаю как это сделать. На досуге поищу.

EXPLAIN ANALYZE
(
    SELECT
        name AS "Name of category",
        'Cities starting with A' AS group_name,
        ROUND(SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)), 2) AS Total
    FROM category
             JOIN film_category USING (category_id)
             JOIN inventory USING(film_id)
             JOIN rental USING(inventory_id)
             JOIN customer USING(customer_id)
             JOIN address USING(address_id)
             JOIN city USING(city_id)
    WHERE city ILIKE 'a%'
    GROUP BY category_id
    ORDER BY Total DESC
)
UNION ALL
(
    SELECT
        name AS "Name of category",
        'Cities with -' AS group_name,
        ROUND(SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)), 2) AS Total
    FROM category
             JOIN film_category USING (category_id)
             JOIN inventory USING(film_id)
             JOIN rental USING(inventory_id)
             JOIN customer USING(customer_id)
             JOIN address USING(address_id)
             JOIN city USING(city_id)
    WHERE city LIKE '%-%'
    GROUP BY category_id
    ORDER BY Total DESC
);

-- 7.2 Display the film category with the highest total rental hours in cities
-- where customer.address_id belongs to that city and starts with the letter "a".
-- Do the same for cities containing the symbol "-". Write this in a single query.

WITH ranked AS (
    SELECT
        name AS category,
        'Cities starting with A' AS group_name,
        ROUND(SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)), 2) AS total,
        RANK() OVER (
            PARTITION BY 'Cities starting with A'
            ORDER BY SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)) DESC
            ) AS rnk
    FROM category
             JOIN film_category USING (category_id)
             JOIN inventory USING (film_id)
             JOIN rental USING (inventory_id)
             JOIN customer USING (customer_id)
             JOIN address USING (address_id)
             JOIN city USING (city_id)
    WHERE city ILIKE 'a%'
    GROUP BY category_id, name

    UNION ALL

    SELECT
        name AS category,
        'Cities with -' AS group_name,
        ROUND(SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)), 2) AS total,
        RANK() OVER (
            PARTITION BY 'Cities with -'
            ORDER BY SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)) DESC
            ) AS rnk
    FROM category
             JOIN film_category USING (category_id)
             JOIN inventory USING (film_id)
             JOIN rental USING (inventory_id)
             JOIN customer USING (customer_id)
             JOIN address USING (address_id)
             JOIN city USING (city_id)
    WHERE city LIKE '%-%'
    GROUP BY category_id, name
)
SELECT category,
       group_name,
       total
FROM ranked
WHERE rnk = 1
ORDER BY group_name, total DESC;
