from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from random import shuffle
import random
from copy import deepcopy
import math
import HttpBot

import json

def garden_of_eden(cities):
    """ Step 1 """
    population = []
    #individual = randomly create a list of cities using every city from the master city list
    #insert this individual into your population
    #repeat 20 times to create a population of size 20
    for i in range(20):
        shuffle(cities)
        population.append(deepcopy(cities))
        
    return population

def calculate_cost_for_individual(city_1, city_2, city_coordinates):
    """ Step 2 """
        #Break up the cities into long and lat
    city_1 = city_coordinates[city_1]
    lat1 = city_1[0]
    long1 = city_1[1]
    
    city_2 = city_coordinates[city_2]
    lat2 = city_2[0]
    long2 = city_2[1]
    
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    #Multiply arc by the radius of the earth in miles
    distance_btwn_cities = arc * 3963.1676
    
    return distance_btwn_cities

def calc_cost_for_solution(solution, city_coordinates):
    solution_cost = 0
    for i in range(len(solution) - 1):
        solution_cost = solution_cost + calculate_cost_for_individual(solution[i], solution[i+1], city_coordinates)
    return solution_cost

    
def sort_population_by_cost(population, city_coordinates):
    """ Step 3 """
    #loop through population passed in, calculate cost for each solution
    #return population of solutions sorted by cost
    temp_population = []
    sorted_population = []
    for solution in population:
        solution_cost = calc_cost_for_solution(solution, city_coordinates)
        solution_dictionary = {"solution": solution, "cost": solution_cost}
        temp_population.append(solution_dictionary)

    temp_population = sorted(temp_population, key = lambda k : k ["cost"])
    for temp in temp_population:
        sorted_population.append(temp["solution"])
        
    return sorted_population
    

def create_new_generation(sorted_population):
    """ Step 4 """
    #Clone the top five solutions in the sorted population
    new_generation = deepcopy(sorted_population[:5])
    
    #Mate top 5 solutions with the second top 5 solutions
    for i in range(5):
        new_baby = make_babies(deepcopy(sorted_population[i]), deepcopy(sorted_population[i + 5]))
        if new_baby in new_generation:
            shuffle(new_baby)
        new_generation.append(new_baby)
    
    #Mate bottom 5 solutions with the second bottom 5 solutions
    #for i in range(5):
    #    new_baby = make_babies(deepcopy(sorted_population[-i - 1]), deepcopy(sorted_population[-i - 6]))
    #    if new_baby in new_generation:
    #        shuffle(new_baby)
    #    new_generation.append(new_baby)
        
    #Mutate top 5 solutions by randomly swapping two cities
    for i in range(5):
        #swap_1 = random.choice(deepcopy(sorted_population[i]))
        #swap_2 = random.choice(deepcopy(sorted_population[i]))
        #sorted_population[i][sorted_population[i].index(swap_1)] = swap_2
        #sorted_population[i][sorted_population[i].index(swap_2)] = swap_1
        #new_generation.append(sorted_population[i])
        
        clone = deepcopy(sorted_population[i])
        base = random.randrange(0, len(clone)-2)
        tmp = clone[base]
        clone[base] = clone[base+1]
        clone[base+1] = tmp
        new_generation.append(clone)
        
    for i in range(5):
        clone = deepcopy(sorted_population[i])
        clone.append(clone.pop(0))
        new_generation.append(clone)

    return new_generation

#TODO NEW asexual make babies function
#TODO:
# Extract best gene pairs, randomize them.

def make_babies(solution_1, solution_2):
    new_solution = []
    flag = 1
    for i in range(len(solution_1)/2):
        if flag == 1:
            new_solution.extend(solution_1[0:2])
            for city in solution_1[0:2]:
                solution_1.remove(city)
                solution_2.remove(city)
            flag = 2
        elif flag == 2:
            new_solution.extend(solution_2[0:2])
            for city in solution_2[0:2]:
                solution_1.remove(city)
                solution_2.remove(city)
            flag = 1
        
    if len(solution_1) % 2 == 1:
        if flag == 1:
            new_solution.append(solution_1[-1])
        if flag == 2:
            new_solution.append(solution_2[-1])
        
    return new_solution



@csrf_exempt
def index(request):
    return render(request, 'index.html', {})

@csrf_exempt
def calculate(request):
    all_solutions = []
    best_cost = -1
    cities_data = json.loads(request.POST['data']) #[{u'ioTAKs9TH9AZAwO': [36.66156684576627, -109.89201118749983]}, {u'PUcFKCe1COqaxNQ': [38.64452685562811, -115.73673774999826]}, {u'VfmJAEfYdOfNZfE': [33.49763591978297, -116.04435493749818]}, {u'msE8ejGzqiZImxq': [33.42431215833266, -105.1019721250011]}]
    
    cities = []
    city_coordinates = {}
    for c in cities_data:
        for k,v in c.items():
            cities.append(k)
            city_coordinates[k] = v
    generation = garden_of_eden(cities)

    for i in range(10000):
        generation = sort_population_by_cost(deepcopy(generation), city_coordinates)
        tmp_cost = calc_cost_for_solution(deepcopy(generation[0]), city_coordinates)
        if tmp_cost < best_cost or best_cost == -1:
            best_cost = tmp_cost
            all_solutions.append({"solution":deepcopy(generation[0]), "cost":best_cost})
        generation = create_new_generation(deepcopy(generation))
        
    print "TOTAL=", len(all_solutions)
        
    return HttpResponse(json.dumps({"status": "success", "data": all_solutions}), content_type="application/json")


##############GEOCHAT


@csrf_exempt
def geochat(request):
    return render(request, 'geochat.html', {})

@csrf_exempt
def geochat_post(request):
    latitude = request.POST['lat']
    longitude = request.POST['long']
    bot = HttpBot.HttpBot()
    url = "https://api.geofeedia.com/v1/search/latlon/"+latitude+","+longitude+",1.6?appId=f6d01234&appKey=f484f1093b303a0b6903d7df5cf8e494&sources=twitter&take=30"
    print url
    html = bot.POST(url, {})
    
    return HttpResponse(html, content_type="application/json")


