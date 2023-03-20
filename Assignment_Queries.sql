use food_delivery;

-- Customer login query
SELECT * FROM Customers WHERE email = 'leon82@example.org'  AND password = '965478'; 

-- Delivery agent login query
SELECT * FROM delivery_agent WHERE email = 'roselyn.durgan@example.org' AND password = 'Kathryn';

-- Restaurant login query
SELECT * FROM restaurant WHERE email = 'skylar.dach@example.com' AND password = 'skylar.dach';

-- Signup query for customer
-- For getting max ID and then increment it by one
select max(customer_ID) from customers;
insert into customers(customer_ID, first_name, last_name, email, phone_no, password, DOB) values('1001', 'Vishal', 'Ghoniya', 'vishal@example.com', '9727270199' , 'Break', '2019-02-07');

-- Signup queries for restaurant
select max(restaurant_ID) from restaurant;
insert into restaurant(restaurant_ID, name, email, phone_number, rest_address, password) values('61','Meera', 'meera@gmail.com', '8989758653', '2', 'meerabutani');

-- Signup queries for delivery agent
select max(agent_ID) from delivery_agent;
insert into delivery_agent(agent_ID, first_name, middle_name, last_name, phone_no, email, DOB, password) values('101', 'vishal','hello','patel','789456123','deliver@gmail.com','2011-12-03', 'deliver');

-- Renmame queries in About us file for team_details table
-- to get column names of team_details table
SELECT column_name FROM information_schema.columns WHERE table_name = 'team_details';
-- Example of rename functionality
ALTER TABLE `team_details` RENAME COLUMN `roll_number` TO `student_ID`;
SELECT `student_ID`, `first_name`, `last_name`, `email_id` FROM `team_details`;

-- Queries for delivery agent view
select agent_ID, first_name, last_name, email, phone_no from delivery_agent where agent_ID='1';
SELECT order_ID, order_status, delivery_ID, restaurant_ID, customer_ID FROM orders WHERE order_id IN (SELECT order_id FROM delivery_agent WHERE agent_id = '1') ORDER BY order_placed_time DESC limit 10;
SELECT phone_no from customers where customer_ID='1';
SELECT building_name, street_name, city, state, pin_code from address where address_ID='5';
SELECT delivery_address, delivery_charges, pickup_time, delivery_time from delivery_detail where delivery_ID='1';

-- Queries for customer view

-- Dashboard Get distinct cuisine types
select distinct type from cuisine_type;

-- Userprofile page
-- delete the order provided in userprofile
DELETE FROM orders WHERE order_ID = '5';
-- get userdetails
SELECT * FROM Customers WHERE customer_ID = '1';
-- get order details of a customer
SELECT Orders.order_ID, Orders.order_placed_time, Orders.order_status, restaurant.name as restaurant_name, order_totals.net_price 
FROM Orders 
	inner join restaurant on Orders.restaurant_ID = restaurant.restaurant_ID 
	inner join ( SELECT Orders.order_ID, SUM(Menu_Item.unit_price * Order_Items.quantity) AS net_price 
		FROM Orders 
			JOIN Order_Items ON Orders.order_ID = Order_Items.order_ID 
			JOIN Menu_Item ON Order_Items.item_ID = Menu_Item.item_ID GROUP BY Orders.order_ID ) 
            order_totals on Orders.order_ID = order_totals.order_ID 
WHERE customer_ID = ('1') 
ORDER BY order_placed_time DESC;

-- Restlist page
-- to get list of restaurant with rating >= average rating of particular cuisine
select distinct r.restaurant_ID, r.name, r.email, r.phone_number, r.rating, address.city, address.pin_code, address.state 
from restaurant r 
	inner join address on r.rest_address = address.address_ID 
    inner join cuisine_type ct on r.restaurant_ID = ct.restaurant_ID 
where ct.type = 'Italian' and r.rating >= (select avg(rating) from restaurant inner join cuisine_type on restaurant.restaurant_ID = cuisine_type.restaurant_ID where cuisine_type.type = 'Italian' ) 
order by r.rating DESC;

-- to get list of restaurants of particular search query
select r.restaurant_ID, r.name, r.email, r.phone_number, r.rating, address.city, address.pin_code, address.state 
from restaurant r 
	inner join address on r.rest_address = address.address_ID 
where r.name like '%ra%' ;

-- Menu page
-- get menu_items details of selected restaurant which are available to be ordered
select name, unit_price, veg, item_type, item_ID from menu_item where restaurant_ID = '1' and menu_item.availability='1';
-- placing the order and add records of order_items containing the items being ordered with its quantities
select max(order_ID) from orders;
insert into orders(order_ID, order_placed_time, order_status, restaurant_ID, customer_ID) values('10000', '2023-03-11 12:47:05', 'placed', '1', '1');
insert into order_items(order_ID, item_ID, quantity) values ('10000', '3', '3');

-- Restaurant view
-- restdetail page query to get restaurant details
select name, email, phone_number, rating from restaurant where restaurant_ID='1';
-- get latest 10 orders for the given restaurant where latest is first
SELECT Orders.order_ID, Orders.order_placed_time, Orders.order_status, order_totals.net_price FROM Orders inner join restaurant on Orders.restaurant_ID = restaurant.restaurant_ID inner join ( SELECT Orders.order_ID, SUM(Menu_Item.unit_price * Order_Items.quantity) AS net_price FROM Orders JOIN Order_Items ON Orders.order_ID = Order_Items.order_ID JOIN Menu_Item ON Order_Items.item_ID = Menu_Item.item_ID GROUP BY Orders.order_ID ) order_totals on Orders.order_ID = order_totals.order_ID WHERE Orders.restaurant_ID = '1' ORDER BY order_placed_time DESC LIMIT 10;
-- query to get the order_items list out of particular order
select name, unit_price, quantity from order_items left join menu_item on order_items.item_ID=menu_item.item_ID where order_items.order_ID='642';

-- Restmenu page get items of this restaurant
select name, unit_price, veg, item_type, item_ID, availability from menu_item where restaurant_ID = '1';

-- inserting new item after incrementing item_ID by 1 and updating an item 
select max(item_ID) from menu_item;
insert into menu_item(item_ID, name, unit_price, availability, veg, item_type, restaurant_ID) values('1000','aloo paratha','25','0','0','main_course','1');
UPDATE menu_item SET veg = '0', availability='1', name='aloo paratha', unit_price ='40.00', item_type='snack' where item_ID = '1000';