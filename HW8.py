# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    dict = {}
    cur.execute('SELECT restaurants.name, restaurants.rating, categories.category, buildings.building FROM restaurants JOIN categories ON restaurants.category_id = categories.id JOIN buildings ON restaurants.building_id = buildings.id')
    for restaurant in cur: 
        dict[restaurant[0]] = {'rating': restaurant[1], 'category': restaurant[2], 'building': restaurant[3]}
    return dict

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    dict = {}
    cur.execute('SELECT categories.category FROM restaurants JOIN categories ON restaurants.category_id = categories.id')
    for restaurant in cur:
        if not restaurant[0] in dict:
            dict[restaurant[0]] = 1
        else:
            dict[restaurant[0]] += 1
    names = []
    values = []
    for restaurant in dict:
        names.append(restaurant)
        values.append(dict[restaurant])
    fig, ax = plt.subplots()
    ax.barh(names, values)
    ax.set_xlabel('Average Rating')
    ax.set_autoscale_on
    fig.savefig('categories.png')
    return dict

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    list = []
    cur.execute('SELECT restaurants.name FROM restaurants JOIN buildings ON restaurants.building_id = buildings.id WHERE buildings.building = ? ORDER BY restaurants.rating DESC', (building_num, ))
    for restaurant in cur:
        list.append(restaurant[0])
    return list

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    data = load_rest_data(db)
    categories_dict = {} #key = category name, value = sum of ratings
    building_dict = {} #key = building name, value = sum of ratings
    for restaurant in data:
        if not data[restaurant]['category'] in categories_dict:
            categories_dict[data[restaurant]['category']] = data[restaurant]['rating']
        else:
            categories_dict[data[restaurant]['category']] += data[restaurant]['rating']
        if not data[restaurant]['building'] in building_dict:
            building_dict[data[restaurant]['building']] = data[restaurant]['rating']
        else:
            building_dict[data[restaurant]['building']] += data[restaurant]['rating']
    #divide by num in category/building to get average + find max category/building
    num_in_categories = plot_rest_categories(db)
    max_category = ""
    max_category_rating = 0
    max_building = ""
    max_building_rating = 0
    category_names = []
    category_ratings = []
    building_names = []
    building_ratings = []
    for category in categories_dict:
        categories_dict[category] /= num_in_categories[category]
        category_names.append(category)
        category_ratings.append(categories_dict[category])
        if categories_dict[category] > max_category_rating:
            max_category_rating = categories_dict[category]
            max_category = category
    for building in building_dict:
        num_in_building = len(find_rest_in_building(building, db))
        building_dict[building] /= num_in_building
        building_names.append(building)
        building_ratings.append(building_dict[building])
        if building_dict[building] > max_building_rating:
            max_building_rating = building_dict[building]
            max_building = building
    list = []
    list.append((max_category, max_category_rating))
    list.append((max_building, max_building_rating))
    sorted_categories = sorted(categories_dict, reverse = True)
    sorted_buildings = sorted(building_dict, reverse = True)
    for category in sorted_categories:
        category_names.append(category)
        category_ratings.append(categories_dict[category])
    for building in sorted_buildings:
        building_names.append(str(building))
        building_ratings.append(building_dict[building])
    plt.figure(1, figsize = (8,8))
    plt.subplot(131)
    plt.barh(category_names, category_ratings)
    plt.subplot(132)
    plt.barh(building_names, building_ratings)
    plt.show()
    return list

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
