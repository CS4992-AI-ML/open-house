lessThanAgencies = {}
greaterThanAgencies = {}
# Open the file and read lines
with open("../data/lessThanAgencies.txt") as f:
    for line in f:
        # Strip newline characters
        stripped_line = line.strip()
        if stripped_line != "":
            # If the line is already in the dictionary, increment its count
            if stripped_line in lessThanAgencies:
                lessThanAgencies[stripped_line] += 1
            # If the line is not in the dictionary, add it with a count of 1
            else:
                lessThanAgencies[stripped_line] = 1

with open("../data/greaterThanAgencies.txt") as f:
    for line in f:
        # Strip newline characters
        stripped_line = line.strip()
        if stripped_line != "":
            # If the line is already in the dictionary, increment its count
            if stripped_line in greaterThanAgencies:
                greaterThanAgencies[stripped_line] += 1
            # If the line is not in the dictionary, add it with a count of 1
            else:
                greaterThanAgencies[stripped_line] = 1

sorted_lessThanAgencies = sorted(
    lessThanAgencies.items(), key=lambda item: item[1], reverse=True
)
sorted_greaterThanAgencies = sorted(
    greaterThanAgencies.items(), key=lambda item: item[1], reverse=True
)

# Create the absolute_agencies dictionary
absolute_agencies = {}
all_agencies = set(lessThanAgencies.keys()).union(greaterThanAgencies.keys())

for agency in all_agencies:
    less_count = lessThanAgencies.get(agency, 0)
    greater_count = greaterThanAgencies.get(agency, 0)
    absolute_agencies[agency] = less_count - greater_count

sorted_absoluteAgencies = sorted(
    absolute_agencies.items(), key=lambda item: item[1], reverse=True
)

print(sorted_lessThanAgencies)
print("Length: " + str(len(lessThanAgencies)))
print(sorted_greaterThanAgencies)
print("Length: " + str(len(greaterThanAgencies)))

# Print the absolute_agencies dictionary
print("These agencies typically value properties lower than the predicted price:")
print(sorted_absoluteAgencies)
print("These agencies typically value properties higher than the predicted price:")
print(sorted(absolute_agencies.items(), key=lambda item: item[1], reverse=False))
