import math
# takes the day plan from the file and shifts the numbers within the day plan
# every day plan should look like this: "hh:mm-hh:mm activity"
with open("dayPlan.txt", "r") as file:
	day_plan = file.readlines()

# lists to put items to update
start_times = []
end_times = []
activities = []

# process the lines in the day plan into lists to update
for line in day_plan:
	# extract first hh:mm, ending at a -
	start_time = line[:line.index("-")]
	# extract second hh:mm after the -
	end_time = line[line.index("-")+1:line.index(" ")]
	# add the activity list to a separate bucket after a space
	activity = line[line.index(" ")+1:].strip("\n")

	start_times.append(start_time)
	end_times.append(end_time)
	activities.append(activity)


def shiftPlan(shift_hours, shift_minutes):
	final_plan = ""

	for i in range(len(activities)):
		start_time = start_times[i]
		end_time = end_times[i]
		activity = activities[i]

		start_hour, start_minute = start_time.split(":")
		end_hour, end_minute = end_time.split(":")

		start_hour = int(start_hour)
		end_hour = int(end_hour)
		start_minute = int(start_minute)
		end_minute = int(end_minute)

		# carry minutes past 60 to the hours column to avoid overflow
		start_minute += shift_minutes
		start_rounded = math.floor(start_minute / 60)
		start_minute %= 60
		end_minute += shift_minutes
		end_rounded = math.floor(end_minute / 60)
		end_minute %= 60

		# add carried digits to the hours column, then modulo to prevent overflow
		start_hour += shift_hours + start_rounded
		end_hour += shift_hours + end_rounded
		start_hour %= 12
		end_hour %= 12

		print(start_hour, start_minute, end_hour, end_minute)

		final_plan += f"{start_hour}:{start_minute:02}-{end_hour}:{end_minute:02} {activity}\n"

	return final_plan


def createPlan(begin_hour, begin_minute):
	created_plan = ""
	created_plan_list = []
	current_minute = begin_minute
	current_hour = begin_hour

	while True:
		# ask the user for duration and activity
		plan_line = input("Add activity (duration, activity): ")

		if plan_line == "del":
			# avoid deleting from an empty list
			if len(created_plan_list) == 0:
				continue

			# get rid of the current element and reset the current time
			del_element = created_plan_list.pop()
			deleted_start = del_element[:del_element.index("-")]
			deleted_hour, deleted_minute = deleted_start.split(":")

			current_hour = int(deleted_hour)
			current_minute = int(deleted_minute)

			for i in range(len(created_plan_list)):
				print(created_plan_list[i])

			continue

		# when finished the user just has to enter q
		if plan_line == "q":
			break

		if plan_line == "":
			continue

		input_duration, input_activity = plan_line.split(", ")
		input_duration = int(input_duration)

		# assemble the start time, then calculate the end time
		start_time = f"{current_hour}:{current_minute:02}"

		end_minute = current_minute + input_duration
		end_carry = math.floor(end_minute / 60)
		end_minute %= 60
		end_hour = (current_hour + end_carry) % 12

		end_time = f"{end_hour}:{end_minute:02}"

		# add the formatted line to the end result
		created_plan_list.append(f"{start_time}-{end_time} {input_activity}")
		for i in range(len(created_plan_list)):
			print(created_plan_list[i])

		current_minute = end_minute
		current_hour = end_hour

	# format the created plan before returning it
	for i in range(len(created_plan_list)):
		created_plan += f"{created_plan_list[i]}\n"

	return created_plan



# print(start_times)
# print()
# print(end_times)
# print()
# print(activities)
#
# print(shiftPlan(0, 40))

print(createPlan(2, 40))
