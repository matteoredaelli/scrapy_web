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

regexp_model = "^(\w+) (.+) (\w+/\w+ R\w+)"
regexp_size = "(\w+/\w+ R\w+ \w+\w+)\s*"

records = spark.read.json(input)

records.filter(records.id.isNotNull()) \
  .filter(records.id != '') \
  .filter(regexp_extract('description', '(rinnovati)', 1) == '') \
  .withColumn("size",        regexp_extract("description", regexp_size, 1)) \
  .withColumn("brand",       regexp_extract("model", regexp_model, 1)) \
  .withColumn("season",      trim(regexp_replace("season", "tires_season",""))) \
  .withColumn("id",          trim(regexp_replace("id", "MPN: ",""))) \
  .withColumn("ean",         trim(regexp_replace("ean", "EAN: ",""))) \
  .withColumn("runflat",     regexp_extract("description", "(runflat)", 1)) \
  .withColumn("mfs",         regexp_extract("description", "(MFS|FSL|bordo di protezione|bordino di protezione)", 1)) \
  .withColumn("xl",          regexp_extract("description", " (XL|RF)\s*", 1)) \
  .withColumn("chiodabile",  regexp_extract("description", "(chiodabile)\s*", 1)) \
  .withColumn("price",       regexp_replace("price", "\u00a0\u20ac", "")) \
  .withColumn("price",       regexp_replace("price", ",", ".")) \
  .withColumn("model",       regexp_extract("model", regexp_model, 2)) \
  .withColumn('country',     lit("IT")) \
  .withColumn('currency',    lit("EUR")) \
  .write.json(output)
