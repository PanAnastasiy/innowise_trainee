
-- 1. Display the number of films in each category, sorted in descending order.

EXPLAIN ANALYZE
SELECT name AS "Name of category",
       COUNT(film_id) AS "Count of films"
FROM category
    LEFT JOIN film_category USING (category_id)
GROUP BY category_id
ORDER BY 2 DESC;

-- 2. Display the top 10 actors whose films were rented the most,
-- sorted in descending order.

EXPLAIN ANALYZE
SELECT CONCAT(last_name, ' ', first_name) AS "Full name of actor",
       COUNT(rental_id) AS "Number of times rented"
FROM actor
    LEFT JOIN film_actor USING (actor_id)
    LEFT JOIN inventory USING (film_id)
    LEFT JOIN rental USING(inventory_id)
GROUP BY actor_id, "Full name of actor"
ORDER BY 2 DESC
LIMIT 10;

-- 3. Display the category of films that generated the highest revenue.

EXPLAIN ANALYZE
SELECT name AS "Name of category",
       COALESCE(SUM(amount), 0) AS "Revenue of category"
FROM category
    LEFT JOIN film_category USING(category_id)
    LEFT JOIN inventory USING(film_id)
    LEFT JOIN rental USING (inventory_id)
    LEFT JOIN payment USING(rental_id)
GROUP BY category_id
ORDER BY 2 DESC
LIMIT 1;

-- 4. Display the titles of films not present in the inventory.
-- Write the query without using the IN operator.

EXPLAIN ANALYZE
SELECT title AS "Films aren't presented"
FROM inventory AS inv
    RIGHT JOIN film USING (film_id)
WHERE inventory_id IS NULL;

-- 5. Display the top 3 actors who appeared the most in films within the "Children" category.
-- If multiple actors have the same count, include all.

EXPLAIN ANALYZE
SELECT "Full name of actor",
       "Total count of films",
       "Place in top"
FROM (
         SELECT
             CONCAT(a.last_name, ' ', a.first_name) AS "Full name of actor",
             COUNT(*) AS "Total count of films",
             DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS "Place in top"
         FROM actor a
                  JOIN film_actor fa USING(actor_id)
                  JOIN film_category fc USING(film_id)
                  JOIN category c USING(category_id)
         WHERE c.name = 'Children'
         GROUP BY a.actor_id, "Full name of actor"
     ) ranked
WHERE "Place in top" < 4
ORDER BY 2 DESC;

-- 6. Display cities with the count of active and inactive customers (active = 1).
-- Sort by the count of inactive customers in descending order.

EXPLAIN ANALYZE
SELECT city AS "Name of city",
       COUNT(*) FILTER (WHERE active = 1) AS "Active count",
       COUNT(*) FILTER (WHERE active = 0) AS "Inactive count"
FROM customer
    JOIN address USING(address_id)
    JOIN city USING (city_id)
GROUP BY city_id, city
ORDER BY 3 DESC;

-- 7. Display the film category with the highest total rental hours in cities
-- where customer.address_id belongs to that city and starts with the letter "a".
-- Do the same for cities containing the symbol "-". Write this in a single query.

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
    LIMIT 1
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
    LIMIT 1
);
