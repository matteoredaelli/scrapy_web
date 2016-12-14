# -*- coding: utf-8 -*-

#    Copyright (C) 2016-2017 Matteo.Redaelli@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import *
import re, sys

if len(sys.argv) != 4:
    print('Usage: ' + sys.argv[0] + ' <in> <out> <date>')
    sys.exit(1)

# Grab the input and output
input = sys.argv[1]
output = sys.argv[2]
date = sys.argv[3]
# warehouse_location points to the default location for managed databases and tables
warehouse_location = 'spark-warehouse'

spark = SparkSession \
  .builder \
  .appName(sys.argv[0]) \
  .config("spark.sql.warehouse.dir", warehouse_location) \
  .enableHiveSupport() \
  .getOrCreate()

r = spark.read.json(input)

r = r.withColumn("ts", lit(date)) \
  .distinct() \
  .dropDuplicates(["id"]) \
  .write.json(output)

  

  
