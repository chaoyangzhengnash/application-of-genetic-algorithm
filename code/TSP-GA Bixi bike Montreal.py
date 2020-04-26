#
# Program: BIXI_bike_tsp_problems_GA
#
# Purpose: 
#
# Written by: Hoa Nguyen  ​
#             Xinyue Tan ​
#             Zhenghao Wang ​
#             Chaoyang zheng ​
# 
# Updated: 1 April 2019
#        
# ------------------------------------------------------.
#
#######################################################################################
###    Part 1:    Data preprocessing                                                ###
###    Purpose :  Based on the net flow trips in each BIXI station (count of        ### 
###               lent trips - count of return trips),We divied each station        ###
###               into balanced and imblanced stations, we only focused on those    ###  
###               imblanced netflow stations(absolute value of net flow higher      ###
###               than 1000)                                                        ###
###    Tips:      This part is not the application of what we leant from this       ### 
###               course, therefore some packages were used                         ###   
#######################################################################################
# Loading dataset and packages
import os
import pandas as pd
import numpy as np
path_bixi_data = os.path.abspath("C:/Users/Zheng Chaoyang/Desktop/projectdu_ algorithum")
files_rentals_2018 = [x for x in os.listdir() if "OD_2018" in x]
stations_2018 = pd.read_csv("C:/Users/Zheng Chaoyang/Desktop/projectdu_ algorithum/Stations_2018.csv")
# Define the Mass Append Table Function:
def mass_append(df_list):
    """ 
    mass_append(df_list)
    
    Description:
        This function appends together all DataFrames withina list.
    
    Argument(s): 
        df_list : List of pandas DataFrame objects. 
    """
    # Instantiate empty DataFrame
    output_df = pd.DataFrame()
    
    for df in df_list:
        # Append each table one by one
        output_df = output_df.append(df)
    return output_df

df_rentals_2018 = mass_append([pd.read_csv(x) for x in files_rentals_2018])
df_rentals_2018 = df_rentals_2018.merge(stations_2018, how='left', 
                                        left_on='start_station_code', right_on='code')
df_rentals_2018.rename({'code':'start_code', 
                        'name':'start_name', 
                        'latitude':'start_latitude', 
                        'longitude':'start_longitude',
                        'neighborhood':'start_neighborhood',
                        'great_park':'start_great_park',
                        'affectation':'start_affectation'}, axis='columns', inplace=True)
df_rentals_2018 = df_rentals_2018.merge(stations_2018, how='left', 
                                        left_on='end_station_code', right_on='code')
df_rentals_2018.rename({'code':'end_code', 
                        'name':'end_name', 
                        'latitude':'end_latitude', 
                        'longitude':'end_longitude',
                        'neighborhood':'end_neighborhood',
                        'great_park':'end_great_park',
                        'affectation':'end_affectation'}, axis='columns', inplace=True)

# Regroup dataset by count of lent and return trips 
station_bystart = pd.DataFrame(df_rentals_2018.groupby(by=["start_station_code","start_latitude","start_longitude"]).size())
station_byend = pd.DataFrame(df_rentals_2018.groupby(by=["end_station_code","end_latitude","end_longitude"]).size())
station_bystart = pd.DataFrame(station_bystart).reset_index()
station_byend = pd.DataFrame(station_byend).reset_index()
station_bystart.rename({'start_station_code':'code', 
                        0:'count of lent trips', 
                       }, axis='columns', inplace=True)
    
station_byend.rename({'end_station_code':'code', 
                        0:'count of return trips', 
                       }, axis='columns', inplace=True)   

# Merging two dataset to caculate the absolute value of net flow of each station    
station_merged = pd.merge(station_bystart,
                 station_byend[['code','count of return trips']],
                 on= 'code')    

station_merged['net_flow'] = abs(station_merged['count of lent trips'] - station_merged['count of return trips'])

# Picking up those stations whose absolute net flow is higher than 1000
station_imbalance = station_merged[station_merged.net_flow > 999]
#station_imbalance.to_csv("station_imbalance.csv" ,index=False)

#######################################################################################
###    Part 2:    Building  Genteic algorithm                                       ###
###    Purpose :  The detailed process of building the Genetic algorithm            ###
###    Tips:      This part is our application of Genetic algorithum, which is      ### 
###               our own contribution                                              ###   
#######################################################################################

# Import basic packages 
import random
import math

SCORE_NONE = -1

class Life(object):
      """Defining each solution as life"""
      def __init__(self, aGene = None):
            self.gene = aGene
            self.score = SCORE_NONE

class GA(object):
      """Defining Genetic algorithum """
      def __init__(self, aCrossRate, aMutationRage, aLifeCount, aGeneLenght, aMatchFun ):
               self.croessRate = aCrossRate
            self.mutationRate = aMutationRage
            self.lifeCount = aLifeCount
            self.geneLenght = aGeneLenght
            self.matchFun = aMatchFun                 # Match function
            self.lives = []                           # Population
            self.best = None                          # Keep the best individual(solution) in this 
                                                      # generation(iteration)
            self.generation = 1
            self.crossCount = 0
            self.mutationCount = 0
            self.bounds = 0.0                         # The sum of each solution's score, used to calculate 
                                                      # the probability for selection
            self.mean = 1.0                           # The avearge score for population
            self.initPopulation()


      def initPopulation(self):
            """Initiating population"""
            self.lives = []
            for i in range(self.lifeCount):
                  gene = [ x for x in range(self.geneLenght) ] 
                  random.shuffle(gene)#Used to randomly reorder a sequence of gene 
                  life = Life(gene)
                  self.lives.append(life)


      def judge(self):
            """Evaluate and calculate the fitness value of each life(solution)"""
            self.bounds = 0.0
            self.best = self.lives[0]
            for life in self.lives:
                  life.score = self.matchFun(life)
                  self.bounds += life.score 
                  if self.best.score < life.score:
                        self.best = life
            self.mean=self.bounds/self.lifeCount


      def cross(self, parent1, parent2):
            """Cross"""
            n=0
            while 1:
                  newGene = []

                  index1 = random.randint(0, self.geneLenght - 1)# Used to randomly generate an 
                                                                 # integer within a specified range
                  index2 = random.randint(index1, self.geneLenght - 1)
                  tempGene = parent2.gene[index1:index2]   # Cross-over gene fragments

                  p1len = 0
                  for g in parent1.gene:
                        if p1len == index1:
                              newGene.extend(tempGene)     # Inseting the gene fragments
                              p1len += 1
                        if g not in tempGene:
                              newGene.append(g)
                              p1len += 1
                  if (self.matchFun(Life(newGene)) > max(self.matchFun(parent1),self.matchFun(parent2))):
                        self.crossCount += 1
                        return newGene
                    "Accept some mutation result which didn't improve performance"
                  # else:
                  #       rate = random.random()
                  #       if rate < math.exp(-100 / math.sqrt(self.generation)):
                  #             self.crossCount += 1
                  #             return newGene
                  if (n>100):
                        self.crossCount += 1
                        return newGene
                  n += 1



      def  mutation(self, egg):
            """mutation"""
            index1 = random.randint(0, self.geneLenght - 1)
            index2 = random.randint(0, self.geneLenght - 1)
            newGene = egg.gene[:]       # create a new gene sequence, so as not
                                        #to affect the parent population during mutation
            newGene[index1], newGene[index2] = newGene[index2],newGene[index1]
            if self.matchFun(Life(newGene)) > self.matchFun(egg):
                  self.mutationCount += 1
                  return newGene
            else:
                  rate = random.random()
                  if rate < math.exp(-10 / math.sqrt(self.generation)) :
                        self.mutationCount += 1
                        return newGene
                  return egg.gene


      def getOne(self):
            """ Get one solution as parent"""
            r = random.uniform(0, self.bounds)  #Random sampling in a uniform distribution
            for life in self.lives:
                  r -= life.score
                  if r <= 0:
                        return life #Roulette selection method

            raise Exception("Selection error", self.bounds)


      def newChild(self):
            """Generating new life(solution)"""
            parent1 = self.getOne()
            rate = random.random()
            # Based on probablity to cross
            if rate < self.croessRate:
                  # Cross
                  parent2 = self.getOne()
                  gene = self.cross(parent1, parent2)
            else:
                  gene = parent1.gene

            # Based on probablity to mutates
            rate = random.random()
            if rate < self.mutationRate:
                  gene = self.mutation(Life(gene))
            return Life(gene)


      def next(self):
            """Get a new generation"""
            self.judge()
            newLives = []
            newLives.append(self.best)            # Directly take the solution with highest score 
                                                  # (the optimal solution) in the present generation 
                                                  # into the next generation ​
            while len(newLives) < self.lifeCount:
                  newLives.append(self.newChild())
            self.lives = newLives
            self.generation 
            1
            
x = range(6)

for n in x:
  print(n)

#######################################################################################
###    Part 3:    Applyting Genteic algorithun to solove tsp problem                ###
###    Purpose :  Applyting Genteic algorithun to found the shortest path which     ###
###               enable one to travel through all imbalanced stations.             ### 
###    Tips:      This part is our application of Genetic algorithum, which is      ### 
###               our own contribution                                              ###   
#######################################################################################
#from GA import GA

class TSP(object):
      def __init__(self, aLifeCount = 100,):
            self.initCitys()
            self.lifeCount = aLifeCount
            self.ga = GA(aCrossRate = 0.7, 
                  aMutationRage = 0.04, 
                  aLifeCount = self.lifeCount, 
                  aGeneLenght = len(self.citys), 
                  aMatchFun = self.matchFun())


      def initCitys(self):
            self.citys = []
            for i in range(0,30):
                self.citys.append(([lat[0][i],log[0][i]]))

            
      def distance(self, order):
            distance = 0.0
            for i in range(-1, len(self.citys) - 1):
                  index1, index2 = order[i], order[i + 1]
                  city1, city2 = self.citys[index1], self.citys[index2]
                  distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
            return distance


      def matchFun(self):
            return lambda life: 1.0 / self.distance(life.gene)


      def run(self, n = 0):
            while n > 0:
                  self.ga.next()
                  distance = self.distance(self.ga.best.gene)
                  print (("%d : %f") % (self.ga.generation, distance))
                  n -= 1
                  print ("After %d th iteration ，the optimal distance is：%f" %(self.ga.generation, distance))
                  print ("The sequence to go through each station is：", self.ga.best.gene)
                  optimal_distance.append(self.distance(self.ga.best.gene))
                  optimal_order.append(self.ga.best.gene)


Bixi_orgin = station_imbalance
code = [Bixi_orgin.ix[:,'code']]
lat = [Bixi_orgin.ix[:,'start_latitude']]
log = [Bixi_orgin.ix[:,'start_longitude']]

if __name__ == '__main__':
      tsp=TSP()
      tsp.run(300)
    
 # Get the result 
df = pd.DataFrame({'optimal_distance':  optimal_distance,
        'optimal_order': optimal_order})
#df.to_csv("result.csv" ,index=False)

  
  
