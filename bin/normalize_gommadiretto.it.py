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

if len(sys.argv) != 3:
    print('Usage: ' + sys.argv[0] + ' <in> <out>')
    sys.exit(1)

# Grab the input and output
input = sys.argv[1]
output = sys.argv[2]

# warehouse_location points to the default location for managed databases and tables
warehouse_location = 'spark-warehouse'

spark = SparkSession \
  .builder \
  .appName(sys.argv[0]) \
  .config("spark.sql.warehouse.dir", warehouse_location) \
  .enableHiveSupport() \
  .getOrCreate()

records = spark.read.json(input) 
records.filter(records.id.isNotNull()) \
  .filter(records.id != '') \
  .filter(regexp_extract('size', '(rinnovati)', 1) == '') \
  .withColumn("chiodabile", regexp_extract("size", "(chiodabile)\s*", 1)) \
  .withColumn("size",       regexp_extract("size", "\s*(\w+/\w+ R\w+ \w+\w+)\s*", 1)) \
  .withColumn("season",     regexp_replace("season", "Pneumatici invernali", "winter")) \
  .withColumn("season",     regexp_replace("season", "Pneumatici estivi",    "summer")) \
  .withColumn("season",     regexp_replace("season", "Pneumatici per tutte le stagioni", "all_seasons")) \
  .withColumn("price",      regexp_replace("price", ",", ".")) \
  .withColumn('country',    lit("IT")) \
  .withColumn('currency',   lit("EUR")) \
  .withColumnRenamed("description", "model") \
  .write.json(output)
