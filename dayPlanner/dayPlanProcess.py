import math
# takes the day plan from the file and shifts the numbers within the day plan
# every day plan should look like this: "hh:mm-hh:mm activity"
with open("dayPlan.txt", "r") as file:
	day_plan = file.readlines()

# number of minutes to shift day plan up by. can be negative
shiftMinutes = 40
shiftHours = 0

# lists to put items to update
start_times = []
end_times = []
activities = []

final_plan = ""

for line in day_plan:
	# extract first hh:mm, ending at a -
	start_time = line[:line.index("-")]
	# extract second hh:mm after the -
	end_time = line[line.index("-")+1:line.index(" ")]
	# add the activity list to a separate bucket after a space
	activity = line[line.index(" ")+1:].strip("\n")

	start_hour, start_minute = start_time.split(":")
	end_hour, end_minute = end_time.split(":")

	start_hour = int(start_hour)
	end_hour = int(end_hour)
	start_minute = int(start_minute)
	end_minute = int(end_minute)

	# carry minutes past 60 to the hours column to avoid overflow
	start_minute += shiftMinutes
	start_rounded = math.floor(start_minute / 60)
	start_minute %= 60
	end_minute += shiftMinutes
	end_rounded = math.floor(end_minute / 60)
	end_minute %= 60

	# add carried digits to the hours column, then modulo to prevent overflow
	start_hour += shiftHours + start_rounded
	end_hour += shiftHours + end_rounded
	start_hour %= 12
	end_hour %= 12

	print(start_hour, start_minute, end_hour, end_minute)

	final_plan += f"{start_hour}:{start_minute:02}-{end_hour}:{end_minute:02} {activity}\n"

print(start_times)
print()
print(end_times)
print()
print(activities)

print(final_plan)
