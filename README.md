# Food Delivery website
Video_link: https://drive.google.com/file/d/1BrPiArpvNygDpygwt5aaDxWbDvjJVzE1/view?usp=sharing \
We have developed a food delivery website that allows users to log in or sign up as customers, restaurants, or delivery agents. To launch the website, please follow the steps below.
1. Clone this repository.
2. Run the Food_Delivery.sql file in your sql workbench.
3. Open the file ```fooddelivery/db.yaml``` and update the mysql_password to your sql root database password.
4. Create a virtual environment and activate it by using the following commands:
\
  4.1 ```cd <location to the cloned repo>```
  \
  4.2 ```py -3 -m venv venv```
  \
  4.3 ```venv\Scripts\activate```
  \
  4.4 ```Install all the dependencies from the requirements.txt file using pip command as below:```
    \
      &ensp;&ensp;&ensp;&ensp;4.4.1 ```pip install flask```
      \
      &ensp;&ensp;&ensp;&ensp;4.4.2```pip install flask-mysqldb```
      \
      &ensp;&ensp;&ensp;&ensp;4.4.3 ```pip install flask-wtf```
      \
      &ensp;&ensp;&ensp;&ensp;4.4.4```pip install pyyaml```
    \
  4.5 ```python app.py```
  \
  4.6 ```go to the hyperlink created in the terminal```
5. Enjoy using the website!


# Insert & Delete

When a customer orders food, the order is added and the added order can be seen in the orders page. When a customer deletes a delivered order, the deleted order is no longer visible in the ordered list of that customer.
| Before Insert | After Insert | After Delete |
| :-: | :-: | :-: |
|![image](https://user-images.githubusercontent.com/76422222/226303469-53f6c77c-7123-47c8-a731-287bd23f2be4.png)|![image](https://user-images.githubusercontent.com/76422222/226303859-1273f6ac-c7ed-40a1-af92-a4931211823d.png)|![image](https://user-images.githubusercontent.com/76422222/226304035-7101b759-db24-4fd5-a2e0-c1a00a758ff9.png)|

# Update
Here we can see the price of the first item in the menu is updated.
| Before Update | After Update |
| :-: | :-: |
|![image](https://user-images.githubusercontent.com/76422222/226306066-58e0d23e-7511-43eb-a3f1-8a21102acf71.png)|![image](https://user-images.githubusercontent.com/76422222/226306434-564005ac-b534-4148-93fe-d1e4e68f184f.png)|

# Rename
Here we can see that the column name with last_name has been renmaed to surname. 
| Before Rename | After Rename | 
| :-: | :-: |
|![image](https://user-images.githubusercontent.com/76422222/226305315-8092ebc2-470d-426c-a357-8550a2427a2f.png)|![image](https://user-images.githubusercontent.com/76422222/226305680-aa6d528d-0d2a-43ed-875d-34850e7dd6bc.png)|
# Where
| Provides a list of orders delivered by a particular restaurant on restaurant's dashboard page|
| :-: |
|![image](https://user-images.githubusercontent.com/76422222/226307233-40b2a826-1d3e-45e7-85a2-4374a8b6fea2.png)|
