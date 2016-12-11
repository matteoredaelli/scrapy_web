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

r = spark.read.json(input)

r = r.dropDuplicates() \
  .dropDuplicates(["id"]) \
  .select(*(upper(col(c)).alias(c) for c in r.columns))

r.select("brand", "model").distinct().write.json(output + "/fact_brand_model")
for c in ["brand", "size", "season"]:
    r.select(c).distinct().write.json(output + "/fact_%s" % c)


price_cols = ['country', 'currency', 'id', 'price', 'source', 'ts']
product_cols = list(set(r.columns) - set(price_cols)) + ['id', 'source', 'ts']

source = r.first().source
ts = r.first().ts

regexp_ts = "^(\d\d\d\\d)-(\d\d)-(\d\d)"
year  = re.search(regexp_ts, ts).group(1)
month = re.search(regexp_ts, ts).group(2)
day   = re.search(regexp_ts, ts).group(3)

r.select(price_cols).coalesce(1).write.parquet(output + "/prices/year=%s/month=%s/day=%s/source=%s" % (year, month, day, source))
                                       

r.select(product_cols) \
  .dropDuplicates(["ean"]) \
  .write.json(output + "/product")

  

  
