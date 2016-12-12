"""
A pseudocode map-reduce style algorithm for computing co-views is something like:

x 1. Read data in as pairs of (user_id, item_id clicked on by the user)
x 2. Group data into (user_id, list of item ids they clicked on)
x 3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
x 4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
x 5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
x 6. Filter out any results where less than 3 users co-clicked the same pair of items
"""

from pyspark import SparkContext

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/clicks.log", 2)     # each worker loads a piece of the data file
data = data.distinct() # Make distinct rows

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition

pages = pairs.map(lambda pair: (pair[0], pair[1]))   # Map to (user_id, item_id) (#1)

users_with_list = pages.groupByKey() # Group item_ids to user_id: (user_id, list of item ids they clicked on) (#2)

def return_pairs(user_id, list_of_ids):
    resulting_list = []
    # Sort ids
    list_of_ids = sorted(list_of_ids)
    for i in range(0, len(list_of_ids) - 1):
        for j in range(i + 1, len(list_of_ids)):
            resulting_list.append((user_id, (list_of_ids[i], list_of_ids[j])))

    return resulting_list

# (#3) Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
users_with_pairs = users_with_list.flatMap(lambda data: return_pairs(data[0], data[1]))

# Switch pairs
pairs_with_users = users_with_pairs.map(lambda pair: (pair[1], pair[0]))

# (#4) Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
pairs_with_users = pairs_with_users.groupByKey()

# (#5) Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
pairs_with_users_count = pairs_with_users.map(lambda pair: (pair[0], len(pair[1])))

# (#6) Filter out any results where less than 3 users co-clicked the same pair of items
filtered_pairs_with_users_count = pairs_with_users_count.filter(lambda pair: pair[1] >= 3)

output = filtered_pairs_with_users_count.collect()
for key,value in output:
    print("Co-clicks: %s and %s with count: %d" % (key[0], key[1], value))
print("Co-clicks done")

sc.stop()
