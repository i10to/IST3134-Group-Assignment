from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum
import time

spark = SparkSession.builder.appName("Ecommerce Analysis").getOrCreate()

# Start the timer for the whole process
total_start = time.time()

# Step 1: Read the dataset from S3 (this is for Rameen's bucket)
df = spark.read.csv(
    "s3://ist3134-rameen-ecommerce-2026/2019-Nov.csv",
    header=True,
    inferSchema=True
)

# Step 2: Remove duplicate records
df = df.dropDuplicates()

# Step 3: Check the missing values
df.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in df.columns
]).show()

# Step 4: Remove rows with missing category_code
df = df.dropna(subset=["category_code"])

# Step 5: Count the unique categories
print("Number of unique categories:")
print(df.select("category_code").distinct().count())

# Step 6: Rank the categories by frequency
df.groupBy("category_code") \
    .count() \
    .orderBy("count", ascending=False) \
    .show(129, truncate=False)

# End the timer for the whole process
total_end = time.time()
print(
    f"Total PySpark execution time: "
    f"{total_end - total_start:.3f} seconds"
)
spark.stop()
