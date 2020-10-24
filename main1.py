import os
import pyspark
os.environ["PYSPARK_PYTHON"]="python3.6"
sc = pyspark.SparkContext('local[8]')
from pyspark.sql import SparkSession
spark = SparkSession(sc)
import numpy as np
from pyspark.sql import functions as F

test_data = np.loadtxt('DTest')
distance_final = []
for test_node in test_data:
    data = sc.textFile('direct.graph').map(
        lambda x:(int(x.split(' ')[0]),int(x.split(' ')[1]))).toDF(['node','neighbor'])
    data = data.groupby('node').agg(F.collect_list('neighbor'))
    
    start_node = sc.broadcast(test_node[0])
    end_node = sc.broadcast(test_node[1])
    update_func = (F.when(F.col('node') == start_node.value, 0)
                    .otherwise(100000000))
    data = data.withColumn('dist', update_func)
    
    k=0
    while True:
        first_temp = data.filter(F.col('dist')==k).rdd.map(tuple).flatMap(
            lambda x:[(a,[1]) for a in x[1]]).reduceByKey(lambda a,b:a+b).map(lambda x:(x[0],list(set(x[1]))))      
        
        accumulator_val1 = sc.accumulator(0)
        accumulator_val2 = sc.accumulator(0)
        
        def map_acm(x):
            global accumulator_val1
            global accumulator_val2
            accumulator_val2+=1
            if x[0]==end_node.value:
                accumulator_val1+=1
            return 1
        second_temp = first_temp.foreach(map_acm)
        if accumulator_val1.value>0:
            k+=1
            break 
        
        if accumulator_val2.value==0:
            k=-1
            break 
        data = data.filter(F.col('dist')!=k)
        third_temp = first_temp.toDF(['node','dist1'])
        data = data.join(third_temp,on='node',how='left')
        update_func = (F.when(F.isnull(F.col('dist1')),100000000)
                        .otherwise(k+1))
        data = data.withColumn('dist', update_func).drop('dist1')
        k+=1
    del data
    print(test_node[0],'to',test_node[1],'distance=',k)
    distance_final.append(str(k))
    output_sentence = '\n'.join(distance_final)     
    with open('DRes','w') as f:
        f.write(output_sentence)
        f.close()
    start_node.destroy()
    end_node.destroy()