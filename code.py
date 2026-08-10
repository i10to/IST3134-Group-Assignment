# Step 1:
# Read the dataset from the S3 bucket as a dataframe 
# name the dataframe it as df
df = spark.read.csv(
    "s3://ist3134-group-assignment-2026/2019-Nov.csv",
    header=True,
    inferSchema=True
)

# Step 2:
# Drop the duplicate records in the dataset
df = df.dropDuplicates()

# Step 3:
# Check the missing values of variables
from pyspark.sql.functions import col, sum
df.select([
    sum(col(c).isNull().cast("int")).alias(c)
    for c in df.columns
]).show()

# Step 4:
# Drop the missing values in category_code
df = df.dropna(subset=["category_code"])

# Step 5:
# Count all the unique values in 'category_code' excluding the blanks
df.select("category_code").distinct().count()

# Step 6:
# Rank the most frquent appearing category in ascending order
df.groupBy("category_code") \
  .count() \
  .orderBy("count", ascending=False) \
  .show(129, truncate=False)

# Step 7:
# Check the executing time when executing when grouping the category
import time
start = time.time()
df.groupBy("category_code") \
    .count() \
    .orderBy("count", ascending=False) \
    .show(truncate=False)
end = time.time()
print(f"Execution time: {end - start:.3f} seconds")
