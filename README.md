# P1-bigdata
Shortest Path Computation

**Configuration**

We used apache spark prebuilt version from pip.  

Please run `pip install -r requirements.txt` to install the dependencies

The spark context that we used had the following properties

[('spark.rdd.compress', 'True'),
 ('spark.serializer.objectStreamReset', '100'),
 ('spark.ui.showConsoleProgress', 'true'),
 ('spark.submit.deployMode', 'client'),
 ('spark.driver.memory','5g'),
 ('spark.num.executor','10'),
 ('spark.executor.cores','1'),
 ('spark.worker.memory','32g')]

**Note**

Please note that you need to change the environment variable with the version of python you are using
 
` import os
 os.environ["PYSPARK_PYTHON"]="python3.6"` (assuming python3.6 is your version)

Change these two lines of code accordingly

**Exceution**

Main code is in "main1.py" file

Please run the code in terminal with the filepaths as input arguments

Run one of the following lines in terminal 

`python3.6 main1.py

or 

spark-submit main1.py
`
Inside the code you will find the directory of the input graph which needs to be changed if you are not pasting the graph in the directory


**Results**

The code runs for the smaller dataset.(P1small - takes around 5 minutes for all queries)

For bigger dataset it runs too but you have to spend some time with the configuration so that outOfMemory error is not reached



**Algorithm Description**

No help from any library is taken here. It is BFS implemented parallely but with each iteration I am truncating the input graph.

The pseudocode is given below


**PseudoCode:**

    1. For each edge produce one key-value pair (since directed graph)
    
    2. Reduce the mapped pairs to generate the (nodeID,neighborList) 
	
	3  Initiate distance = 0 for source node but distance=Infinity for every other node
	
	start_distance = 0
	
	In a loop start doing the following unless it converges:
		
		1. Take the neighbors of the nodes whose distance == start_distance
		
		2. In the original graph find these nodes and change their distances to start_distance+1
		
		3. Remove from the original graph whose distance == start_distance
		
		4. start_distance+=1
		
		(In step 1 within the loop if our destination is one of the neighbors then stop the code and output start_distance+1 as the distance)
		
		(In step 1 if we do not have any neighbors then there is no path from source to destination)
		
		
