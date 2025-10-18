
-- 1. Display the number of films in each category, sorted in descending order.

SELECT name AS Название_категории, COUNT(*) AS Количество_фильмов
FROM category
    LEFT JOIN film_category USING (category_id)
GROUP BY category_id
ORDER BY 2 DESC;

-- 2. Display the top 10 actors whose films were rented the most,
-- sorted in descending order.

SELECT CONCAT(last_name, ' ', first_name) AS Имя_актёра,  COUNT(*) AS Количество_раз_в_прокате
FROM actor
    LEFT JOIN film_actor USING (actor_id)
    LEFT JOIN inventory USING (film_id)
    LEFT JOIN rental USING(inventory_id)
GROUP BY actor_id
ORDER BY 2 DESC
LIMIT 10;

-- 3. Display the category of films that generated the highest revenue.

SELECT name, SUM(amount) AS Доходность_категории
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

SELECT title
FROM inventory AS inv
    RIGHT JOIN film USING (film_id)
WHERE inventory_id IS NULL;

-- 5. Display the top 3 actors who appeared the most in films within the "Children" category.
-- If multiple actors have the same count, include all.

SELECT CONCAT(last_name, ' ', first_name) AS Имя_актёра, COUNT(*) AS Количество_фильмов
FROM actor
    LEFT JOIN film_actor USING(actor_id)
    LEFT JOIN film_category USING (film_id)
WHERE category_id NOT IN (SELECT category_id FROM category WHERE name <> 'Children')
GROUP BY actor_id
ORDER BY 2 DESC
LIMIT 3;


-- 6. Display cities with the count of active and inactive customers (active = 1).
-- Sort by the count of inactive customers in descending order.

SELECT city, SUM(CASE WHEN customer.active = 1 THEN 1 ELSE 0 END) AS Active,
             SUM(CASE WHEN customer.active = 0 THEN 1 ELSE 0 END) AS Not_active
FROM customer
    LEFT JOIN address USING(address_id)
    INNER JOIN city USING (city_id)
GROUP BY city_id, city
ORDER BY 3 DESC;

-- 7. Display the film category with the highest total rental hours in cities
-- where customer.address_id belongs to that city and starts with the letter "a".
-- Do the same for cities containing the symbol "-". Write this in a single query.

SELECT name, ROUND(SUM(EXTRACT(EPOCH FROM (return_date - rental_date) / 3600)), 2) AS Total
FROM category
    JOIN film_category USING (category_id)
    LEFT JOIN inventory USING(film_id)
    JOIN rental USING(inventory_id)
    JOIN customer USING(customer_id)
    JOIN address USING(address_id)
    JOIN city USING(city_id)
WHERE city LIKE 'a%' OR city LIKE '%-%'
GROUP BY category_id, name
ORDER BY Total DESC
LIMIT 1;

