from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_timestamp, unix_timestamp, countDistinct, avg, date_trunc,
    sequence, explode, expr, round as spark_round, date_format
)

# Create Spark Session
spark = SparkSession.builder \
    .appName("CS328_A3_Parking") \
    .getOrCreate()

# Load CSV
df = spark.read.csv("parking_data_sz.csv", header=True, inferSchema=True)

# Convert time columns to timestamp
df = df.withColumn("in_time_ts",  to_timestamp("in_time",  "yyyy-MM-dd HH:mm:ss")) \
       .withColumn("out_time_ts", to_timestamp("out_time", "yyyy-MM-dd HH:mm:ss"))

# Filter invalid rows (out_time ≤ in_time)
df = df.filter(col("out_time_ts") > col("in_time_ts"))

# Pre-compute parking time in seconds
df = df.withColumn(
    "parking_time_sec",
    unix_timestamp("out_time_ts") - unix_timestamp("in_time_ts")
)

# TASK 1 — Total number of berthages for each section
r1 = df.groupBy("section").agg(countDistinct("berthage").alias("count"))

r1.coalesce(1).write.csv("d-r1.csv", mode="overwrite", header=True)


# TASK 2 — All unique berthages per section
r2 = df.select("berthage", "section").dropDuplicates()
r2.coalesce(1).write.csv("d-r2.csv", mode="overwrite", header=True)


# TASK 3 — Average parking time per section (seconds)
r3 = df.groupBy("section") \
       .agg(avg("parking_time_sec").cast("int").alias("avg_parking_time"))

r3.coalesce(1).write.csv("d-r3.csv", mode="overwrite", header=True)


# TASK 4 — Average parking time per berthage, sorted DESC
r4 = df.groupBy("berthage") \
       .agg(avg("parking_time_sec").cast("int").alias("avg_parking_time")) \
       .orderBy(col("avg_parking_time").desc())

r4.coalesce(1).write.csv("d-r4.csv", mode="overwrite", header=True)


# TASK 5 — Hourly in-use berthage count & percentage

# Step 1: total berthage per section (denominator)
section_total = df.groupBy("section") \
                  .agg(countDistinct("berthage").alias("total_berthage"))

# Step 2: create hourly intervals for each parking record
df_interval = df.withColumn(
    "start_hour",
    date_trunc("hour", col("in_time_ts"))
).withColumn(
    "end_hour",
    date_trunc("hour", col("out_time_ts"))
).withColumn(
    "hour_range",
    sequence("start_hour", "end_hour", expr("INTERVAL 1 HOUR"))
).withColumn(
    "interval_start", explode(col("hour_range"))
).withColumn(
    "interval_end", expr("interval_start + INTERVAL 1 HOUR")
)

# Step 3: for each hour/section, count distinct used berthages
hourly_berthage = df_interval.select(
    "section", "berthage", "interval_start", "interval_end"
).dropDuplicates(["section", "berthage", "interval_start", "interval_end"])

from pyspark.sql.functions import countDistinct
hourly_usage = hourly_berthage.groupBy(
    "section", "interval_start", "interval_end"
).agg(countDistinct("berthage").alias("count"))

# Step 4: compute percentage
joined = hourly_usage.join(section_total, on="section", how="left")

result_5 = joined.withColumn(
    "percentage_value",
    spark_round(col("count") / col("total_berthage") * 100, 1)
).withColumn(
    "percentage",
    expr("concat(percentage_value, '%')")
)

# Step 5: format time and output
result_5 = result_5.select(
    date_format("interval_start", "yyyy-MM-dd HH:mm:ss").alias("start_time"),
    date_format("interval_end",   "yyyy-MM-dd HH:mm:ss").alias("end_time"),
    "section",
    "count",
    "percentage"
).orderBy("start_time", "section")

result_5.coalesce(1).write.csv("d-r5.csv", mode="overwrite", header=True)


print("All tasks completed. Results saved as r1.csv–r5.csv")
spark.stop()
