# Application of Genetic Algorithm on a practical case of BIXI Montreal
This is a group project wrote by Chaoyang zheng, Hoa Nguyen, Xinyue Tan and Zhenghao Wang for master course:Algorithms for Optimization and Big Data Analysis in HEC MONTREAL.

## 1.	Introduction 
Bixi bike Montreal is a public sharing system that allows citizens to rent bikes on hourly, daily or monthly basis at a small fee. Bixi Montreal was created in 2014 and by 2018, it owns 552 docking stations and approximately 7,000 vehicles. The majority of the Bixi’s docking stations locates in the downtown area, the Plateau-Mont-Royal area, and near universities. The number of bikes at each station depends on the demand for biking service in the neighborhood where that station locates. When a customer rent a bike from a docking station, he removes a bike from the station, goes on his trip and returns the bike to any of the stations he finds in 30 minutes. Because a bike can be returned to any of the docking station, there often cases that some of the docking stations are empty after some time while the others are full. Thus, Bixi needs redistribute the bikes each day using large trucks. 

For this project, we aim at applying the Genetic Algorithm (GA) for Travel Salesman Problem (TSP) on the Bixi docking stations problem. The goal is to find the shortest path to visit all the chosen docking stations (just one time at each station) by solving an open loop TSP. 

The reminder of the paper is organized as follows: Section 2 will describe the classic TSP and the methodology we will apply. Section 3 we will discuss about the structure of the data we used. Section 4 is to explain how we implement Genetic Algorithm. Section 5 we will present the result of our algorithm and a comparison of the result of our algorithm and the Variable Neighborhood Search’s (VNS). Section 6 is to show the challenges and difficulties we met and takeaways.  Section 7 will be our conclusion. 

## 2.	Literature review and Methodology 
### 2.1.	TSP
TSP is a well-known problem for finding the optimal path which can be solved by various methods. Many algorithms have been developed for TSP but here we are using the concept of genetic algorithm. Other approximation techniques for finding near optimum solutions for TSP based on heuristics are proposed in the literature such as [1] simulated annealing [2], ant colonies [3], genetic algorithms (GA) [4] and [5]. John Holland's pioneering book "Adaptation in natural Artificial System (1975, 1992) showed how the evolutionary process can be applied to solve a wide variety of problems using a highly parallel technique that is now called genetic algorithm. Genetic Algorithms have been applied to a large number of real-world problems. The proposed genetic algorithm in this paper build on much work done by previous researchers [4]. Here we introduce the detailed implementation to solve a practical issue.
### 2.2.	Metaheuristics 
Meta-heuristics can be defined as search algorithms, which were initially designed to find satisfying approximated optimal solutions in a reasonable computation time for several optimization problems. In contrast to conventional algorithms [6]. Metaheuristics do not iteratively visit each element in the search space. They actually guide the search process towards regions that may contain high quality solutions. Meta-heuristics can be classified under two main categories [7]: single solution and population-based search. The former proceeds with one initial solution and try to enhance its quality by repeatedly moving to a better solution. Examples of such type of algorithms are simulated annealing (SA) [8] and tabu search (TS) [9]. However, population-based are meta-heuristics in which a population of solutions is maintained at each iteration. Evolutionary algorithms [10] are good examples for population-based algorithms. 
#### 2.2.1.	Genetic Algorithms (GAs)
Genetic Algorithms (GAs) are known as adaptive heuristic search algorithms. GAs are inspired by biological evolution and they are based on the idea of the survival of the fittest. The power of GAs lies in their ability to avoid randomness search by intelligently exploit historical information to direct the search process towards the regions of better performance within the solution space. GAs ultimately converges to the individual which is the best adapted to the environment and thus obtaining the optimal or a satisfactory solution. After generating a set of initial solutions, GAs evolve through three main genetic operations: Selection, Crossover, and Mutation. 

- Selection: In this phase, the algorithm decides which individual (solution) will survive or pass its genes to the next generation. Better solutions have always more chances to survive. The selection operation is therefore to prevent the loss of effective gene to make high performance individuals survival with greater probability, thereby enhancing the global convergence and computational efficiency.

- Crossover: The crossover operation is used to assemble a new individual and do effective search in the solution space. There are several techniques to accomplish the crossover such as single point, multiple points, and variable point crossovers. The efficiency of those latters depends mostly on the problem. 

- Mutation: This operator is usually used to maintain diversity and to prevent premature convergence. It is often performed with low probability since it results in a random walk through the search space. 


#### 2.2.2.	Variable neighborhood search (VNS)  
VNS is a single solution meta-heuristic that is firstly proposed by Hansen and Meladenovic in 1997. The principle of VNS is to extend a local search routine in order to get out of local optima, by systematically drawing solutions at random within a set of neighborhoods increasingly far from the current best solution, performing descents from there with the local search routine and recentering the search around a better solution if one is found. [11]

VNS has been proved to be very useful for obtaining high quality approximate solutions to wide range of optimization problems. The high performance of VNS is stemmed from its ability to explore distant neighborhoods of the current incumbent solution [10]. VNS can move from a solution to another by repeatedly applying local search improvements to reach local optima. Once a local optimum is detected, VNS is able to jump out of it and eventually find better solutions by dynamically changing the neighborhood‘s structures. Therefore, VNS is more likely to prevent the optimization process from rapidly falling into local optima.

VNS has several advantageous in comparison with conventional metaheuristics such as tabu search, simulated annealing. The algorithm is not only easy to achieve since its structure is simple, but it is also irrelevant to the problem and is suitable for all kinds of optimization problems. Several extensions have been derived from VNS such as Variable Neighborhood Descent (VND), Reduced VNS (RVNS) [10], skewed VNS (SVNS) [12], etc... These variants have been invented in order to enhance the performance of the basic VNS scheme as well as to adapt it for different optimization scenarios.

## 3.	Data structure and conditions
### 3.1.	Data structure
The major input data we used for this project is the historical record of Bixi’s bikes movement in 2018. The data was obtained from an open source called Kaggle. The structure of the raw data includes: index, code, start_latitude, start_longtitude, count of lent trips, and count of return trips. One column was added as net_flow which determines that activeness of the stations. 
-	Index: counts the number of rows in the raw data. The count starts with 0. 
-	Code: contains the identification number of the docking station. Each code is a unique number.
-	Start_latitude and start_longtitude: the coordinates of the stations in a two-dimensional graph. The coordinates of the stations are unique. 
-	Count of lent trips: counts the number of bikes rented from each station for the operated year 2019. 
-	Count of return trips: counts the number of bikes returned to each station for the operated year 2019.
-	Net_flow: calculates the absolute value of the difference between the Count of lent trips and the Count of return trips.
![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/1.png "Optional title")

### 3.2.	Conditions/ Assumptions 
The original data includes 552 docking stations but only 236 most active stations are kept for this project. Most active station means that there are more activities (of either bike rental and return) occurred at the station in the year 2018, showed in the net_flow column. Because the redistribution takes place only at stations that are either empty or full, which indicates the imbalance of usage at the stations, only ones with the net_flow value of 1000 or higher are chosen as input for the GA code. In addition, this reduction of stations will allow better presentation and visualization of the output. The selection of the docking stations is a part of the data preprocessing and as this is not our main contribution of the project, packages are used to operate this task. 

One important condition of our algorithm is that one station can directly connect to 2 other stations only, which means a station is a destination of the route from previous station and is the departure point to the next station. Plus, the route stops at the last station (236th) without going back to the starting docking station.

## 4.	Application of Genetic Algorithm
### 4.1.	Data preprocessing 
As this project focuses mainly on applying the GA, we used some packages and libraries as complimentary tools to support us with preprocessing the data. These packages and libraries include:
-	OS: we use OS module to create a path to access and read the local data files. 
-	Pandas: we use this library to append data frame within a list and merge data from different tables. 
We also use the provided code for VNS to operate for the purpose of comparing the results of this method and the GA code that we wrote. 
The portions that are not prementioned in this data preprocessing section are our contribution to this project.
### 4.2.	 A general look of our algorithm
![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/2.png "Optional title")
##### Pseudocode #####
![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/3.png "Optional title")

The algorithm first generates a set of initial lives (a set of solutions) randomly, which is the first generation (population), then calculates the score of each individual solution in the set, and directly let the solution with the highest score enter the next solution. If the number of lives in the current generation does not reach the maximum number of lives, then we pick up two lives as parents from the previous generation arbitrarily and make crossover and mutation to get a new child according to a certain probability. We append each child in the current generation until reach the maximum number of lives.

### 4.3.	Class initialization 
#### 4.3.1.	Definition of life 
Initially, we define each solution obtained from the algorithm as “Life”. Each life contains the codes of the 236 stations in order of the route following the condition prementioned. The generation of the route order is defined in our algorithm as “Gene”. From each gene, a population is created with 100 lives and the best solutions (based on the score of each solution) in the population are chosen for the next gene.
![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/4.png "Optional title")

#### 4.3.2.	Prophase preparation
##### Initial population ##### 
The generation of the initial population is done completely random. We choose this option as the randomness ensure solutions in the first generation have more diversity, and therefore reduce than probability of being trapped in the local optima. In order to get this randomness of solutions, we shuffle the sequence of the gene.  
##### Fitness function ##### 
We defined “judge” as our fitness function for the GA. The purpose of this function is to evaluate the quality of the solutions. In order to do this, we first calculate the “score” of each life.  The score is calculated by a lambda function of the accumulation distance between each to stations, which is calculated by : distance += math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2). Then the scores of the lives are compared to each other using a for loop. The loop stops when the highest-score life is found. The average score of the population is calculate as the division of the sum of the lives’ scores over the number of solutions in the population. 
##### Termination condition ##### 
Various termination condition can be used to cancel the loop operation of the GA. For our case, we choose to have a fix number of generations as termination condition. 

In total, 300 generations were run for this project. The total number of generations was decided as the result of the trial and error. We first used 100 as termination condition but the solution obtained from the algorithm under this condition was not satisfying. We then tested different number of generations and decided on 300 as the number of generations since the improve in performance is less significant after 300. More detailed is discussed in the result section.   

#### 4.3.3.	The main algorithm
The next generation is created involve two aspects: Selection and evolution. Evolution mainly generates new solutions by crossover, and further improve solution by using mutation.
##### Selection: ##### 
Selection means we keep the solution from previous population and add them into next one. In this case, firstly we choose the best solution so that the new solution in each iteration will be at least as good as last one. Meanwhile we also choose some solutions when we do crossover to ensure the variety.
##### Crossover: ##### 
The crossover is the most important part in genetic algorithms as well as in this project. It is the main way to get improved solution. The quality of the solution depends heavily on the implementation of the crossover.

First we randomly pick a solution as parent 1 from last generation by turning a wheel.  And we randomly pick a number from zero to 1, if the number is smaller than our crossover rate, we will use the same method to pick a parent 2, then implement crossover based on these selected pair of parents to get a new life. And if the chosen number is equal of larger than crossover rate, we will directly put parent 1 into next generation. So basically, the crossover rate is the percentage of how many new solutions in next population we will get from crossover.

The crossover we implement here is to randomly choose a consecutive piece of gene from parent 2 and put it into the same position of our new gene, and for the rest of the positions we will use the gene in parent 1 to fill it up.

The gene are randomly picked from parent 2 and put it in a temporary gene. Then, pieces in the parent 1 are scanned and compared with the pieces in the temporary gene. Only the pieces in parent 1 that are not in the temporary gene will be added to the new child’s gene. When the numbers of the gene in new child’s gene is equal to the first position of the temporary gene from parent 2, we add the whole temporary gene to new child, and then keep scanning and taking from parent 1 until all pieces in parent 1 have been scanned. After this we will have a new child that has the exact same number of the pieces of gene as the parents. The child will possess partial characteristics of its parents but also obtained variety in the sequence of the gene.

![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/5.png "Optional title")

The quality of the new child is tested to ensure the new gene is better than its parents, which follows the undermentioned conditions: 
-	If the score of new child is > P1 and P2, then this new child we be our new gene.
-	If the score of new child is <= P1 and P2, then we will go back to step 2, use new piece of gene to crossover. 
-	If we try 100 times and still cannot bring an improved solution, we will return what we have as new gene regardless of its quality.
##### Mutation: ##### 
Mutation is a method to further improve the performance of the child after crossover. It is not the main way to improve but only a slightly adjustment on the solution. The mutation happens much less frequently than the crossover and the result will be accepted at a certain probability.

There is many ways to implement mutation and here we only use the most simply way: randomly swap the position of two genes/ stations.  These two positions are swapped with each other then the score of the gene is recalculate. If an improvement is seen in the score of the new gene, the new gene is accepted. Otherwise, either we keep the current solution that we get from the crossover or accept the swapped new solution at a certain probability. The probability is calculated as below:

Possibility = exp(-10 / math.sqrt(self.generation) 
     When generation = 1, x = very small,
     When generation = 100, x = 0.37
     When generation = 300, x = 0.99
     
As generation increase, the change to accept unimproved new gene is increasing. This is because, the more generation we have, the harder it gets to improve a solution. To avoid being stuck in local optima, we are more willingly to accept worse solution just as a shake in VNS. 

## 5.	Result and comparison
This part will discuss the result of the GA algorithm and compare to the one obtained from the Variable neighborhood search (VNS) algorithm.

The figure below shows the shortest path given by genetic algorithm. The blue line is the initial solution that was randomly generated by the algorithm, with distance of 8.234384, crossover rate 0.7 and mutation rate 0.04. These two parameters are chosen after several experiments with consideration of converging speed and quality. Converged at 300th generation, the final solution is 2.580149. 

![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/6.png "Optional title")

To deliver a neater plot and show the improvement of GA on shortest path more clearly, we selected 26 stations, which are as dispersed as possible, and compared the result with VNS algorithm which is popular these days. 

![Alt text](https://raw.githubusercontent.com/chaoyangzhengnash/-Application-of-Genetic-Algorithm-/master/graph/7.png "Optional title")

The results given by both algorithms are quite close, GA only got about 5% better than VNS. But it took twice as much time as it took for the VNS algorithm to give a result (implemented on Python 3.7.0 with 2.2GHz Core I7-8750H). The reason behind this is the mechanism of two different algorithms. VNS uses perturbation to conduct alternate searching in different neighborhood, achieving a good balance between dispersibility and concentricity quickly. In GA, the program needs generate fixed number of lives and killed undesired lives basing on fitness process at each iteration. On one hand, it needs to retain the diversity of lives in order to acquire optimal and avoid the loss of effective gene. On the other hand, in order to speed up convergence, it needs the lives moving to the best performance. However, this will decrease the diversity. That’s a contradiction. So, it has the potential to combine with other algorithms to improve. To Get better performance. Possibility to improve the algorithm. Right now, GA Does not has use the feedback information therefore the converge speed is slow. Still Keep large scale searching throughout the whole time. However, some researches invented GA with ‘step’, which could shorten the searching step when approaching to optimal solution, and that will improve the efficiency a lot [13].
 
## 6.	Challenges, difficulties and takeaways
### 6.1. Algorithm construction
Firstly, the code structure of GA is complex, imitating natural selection and genetical mechanism, involving in many steps (crossover, mutation, etc.,.) all logically linked with one another. But after building it, the applicability of GA is good which means it is easy to deploy in other problems with encoding the gene based on the new problems and changing the fitness function. 

### 6.2. Parameters tuning
The performance of GA highly depends on the quality of crossover and mutation implementation, and it is quite to have poor performance. The parameter chosen for basic GA mostly basing on experience and experiments [14]. For example, the initial population has influence on the dispersity and concentricity. If it is too small, it will not cover as much as possible potential ‘optimal’ solution and will slow down the process to find the optimal. If the population is huge, then will waste time on bad solutions. Each tuning needs Trade-off between solution quality and convergence speed. Some researchers also proposed a self-tuning controller for genetic algorithm [15].  

### 6.3. Result visualization
The visualization is very important for this path-related problem. It shows the improvement of the solutions by maps and it can also check the validation of our algorithm. We expect to draw a path that linked every station in a sequence where we cannot easily find an improvement with only observation of the map. 

We choose Tableau to present to implement the visualization since with all the longitudes and latitude, it marked out the exact position on a geographic map of Montreal. With all the results and improvement on the totally distance after 300 iterations, we are confident that the paths for our optimal solution would be totally different from our initial solution. However, the result is still a mess. First, we thought maybe 236 stations are too many to show a clear change on path. Then we test the result by using only 26 stations. But the path still cannot show any improvement with our algorithm, while the one we draw with VNS is perfect. After many reviews and test on our algorithm, finally we found the mistake was mostly likely made when we draw the map. Actually, instead of directly showing the sequence of each station, the index number in the result is listed in the sequence that we should visit. And if we want to present the sequence we need to add another column in the spreadsheet and linked them on the map. 

This is not a fundamental mistake but did create a huge trouble for us. The reason is that we are not that familiar with tableau and we decided to use it in the last moment. The good thing is that it allowed us to review our code and algorithm for many times and get clearer about the logic behind it. 

### 6.4. Limitation + improvement possibility 
For the purpose of applying GA – an optimization model introduced in class – and due to the time limitation, we skipped various options that could have provided with better result: 

-	The quality of the initial solution: It is true that the GA start with generating a random population and the best solution is chosen to ensure diversity of solutions. However, since the population is randomly chosen, most of the time we receive poor solution to begin with. We acknowledge, for such small number of nodes we use for this project, a possible better start is to calculate the distances among the docking stations and sort stations in pair based on these distances. This method allows us to obtain an already-good solution to begin with so there will be higher chance to obtain the global optima. However, it would take a certain amount of time to just calculate the distances among the nodes and sort them. The complexity of this algorithm is expected to exceed the complexity of the algorithm we used significantly.  

-	Final solution is not global optima: Even though we obtained a better solution with the GA compared to the solution obtained from the VNS algorithm (with the trade-off of processing time), it is obvious and can be seen from the visualized figure that the solution we got is not a global optima. This again, has some relations with the parameters and the different methods we chose at each stage (crossover, and mutation) of this algorithm. We believed that the solution could be improved if we could test different combinations of parameters and methods. 

## 7.	Conclusion
In conclusion, we were able to build the Genetic Algorithm code using Python language and run this code on a practical case - the Bixi bike Montreal. The data structure as well as data processing were described. We also explained in detailed the algorithm that we built based on theoretical knowledge that we learned in class. The major steps of the GA include selection of population, crossover, and mutation. The result of the algorithm was presented and evaluated against the output achieved from the VNS algorithm. Some challenges that we confronted during this project and some limitations were as well discussed.
References

## References
[1]. B. Freisieben and P. Merz, New Genetic Local Search Operator for Travelling salesman Problem, Conference on Parallel Problem Solving From nature, app. 890-899, 1996.

[2]. P. van Laarhoven and E. H. L. Aarts, Simulated Annealing: Theory and Applications, Kluwer Academic, 1987,

[3]. M. Dorigo and L. M. Gambradella, Ant Colony System: A Cooperative Learning Approach to the Travelling Salesman Problem, JEEE Transaction on Evolutionary Computation, Vol. l, pp. 53-66, 1997.

[4]. D.E. Goldberg, Genetic Algorithm in Search, Optimization and Machine Learning. Addison-Wesley, 1989.

[5]. Naef Taher Al Rahedi and Jalal Atoum, Solving TSP problem using New Operator in Genetic Algorithms, American Journal of Applied Sciences 6(8):1586-1590, 2009.

[6] Eugene L. Lawler, E. David Wood. Branch-and-bound methods: a survey. Oper Res, 14 (4), pp. 699-719, 1996.

 [7] Günther R Raidl. A unified view on hybrid metaheuristics. In: Hybrid metaheuristics. Berlin (Heidelberg): Springer; 2006. p. 1–12.
 
 [8] Dowsland Kathryn A, Thompson Jonathan M.  Simulated annealing. In: Handbook of natural computing. Berlin (Heidelberg): Springer; 2012. p. 1623–55.
 
 [9] Fred Glover, Manuel Laguna. Tabu search., Springer, New York (2013)
 
 [10] Thomas Bäck, Hans-Paul Schwefel. An overview of evolutionary algorithms for parameter optimization. Evol Comput, 1 (1), pp. 1-23, 1993. 
 
[11] G. Caporossi, I. Gutman, and P. Hansen. Variable neighborhood search for extremal graphs: IV: Chemical trees with extremal connectivity index.  Journal of Chemical Information and Computer Sciences, Volume 23: 469-477, 1999.

 [12] Pierre Hansen, Nenad Mladenović. Variable neighborhood search. 2005.
 
[13] W. Guohui. Variable Step Size LMS Algorithm Optimized by Using Genetic Algorithm. 2012

[14] H. Dakuo, W. Fuli and Z. Chunmei Establishment of Parameters of Genetic Algorithm Based on Uniform Design. 2002

[15] L. Kegang,Z. Fuxi,Z. Biying andS. Fanchen, Dynamic Parameters Optimization of Genetic Algorithm, 2015



