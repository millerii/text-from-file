#!/usr/bin/env python3

import os

folder = r'C:\TestReports' # Where to search
folder = os.path.join(folder, "")
f_start_with = "[BC30" # Files start with... (no * wildcard support)
f_end_with = ".xml" # ...Files end with
line_number = 669 # Line no. to search
mark_start = '= "' # Desired string is between...
mark_end = '" x' # ...Desired string is between
run_dir = os.path.dirname(os.path.abspath(__file__)) # .py file run location, used as save location for results
run_dir = os.path.join(run_dir, "")


def Progress_Bar(progress, total):
	percent = int(90 * (progress / float(total)))
	bar = '█' * percent + '-' * (90 - percent)
	print(f"|{bar}| {percent:.0f}%", end="\r")


def Get_File_List(path: str) -> list: # Absolute folder path
	files=[]

	# Get list of files in [folder] filtered with [f_start_with] & [f_end_with]
	try:
		print("Scanning path: " + path)
		for entry in os.scandir(path):
			if entry.name.startswith(f_start_with) and \
			 entry.name.endswith(f_end_with) and \
			 entry.is_file():
				files.append(entry.name)
	except FileNotFoundError:
		print("\n*** Invalid folder path ***\n")
		raise SystemExit(1)
	except Exception as e:
		print(type(e))
		print(e)

	return files # List of files found ['filename']


def Get_Line_Data(files: list, path: str, line_no: int) -> dict:
	# Go through files and pick desired line
	data= {}

	print("")
	try: # Open files and save desired line
		for i, file in enumerate(files):
			Progress_Bar(i + 1, len(files)) # Write progress bar on background
			print(f'{"Reading files in Get_Line_Data":.<33}' + file, end = "\r") # Write over the same line
			with open(path + file, "r") as f:
				lines = f.readlines()
				try: # Case if file has no enought lines to proceed
					data[file] = lines[line_no]
				except IndexError:
					print(f'{"File has no enought lines":.<33}')
				except Exception as e:
					print(type(e))
					print(e)
	except Exception as e:
		print(type(e))
		print(e)

	return data # Dict format {'filename' & 'line of text'}


def Extract_Line_Data(data: dict, mark_start: str, mark_end: str) -> dict:
	# Find desired position from line in middle of [mark_start] & [mark_end]
	for key, value in data.items():
		if mark_start in value and mark_end in value:
			start = value.find(mark_start) + len(mark_start)
			end = value.find(mark_end)
			value = value[start:end]
			data[key] = value
		else:
			# Remove incorrect value & key data
			data[key] = ""
			data = dict([(vkey, vdata) for vkey, vdata in data.items() if(vdata) ])

	return data # Dict format {'filename' 'value-str'}


def Save_To_File(result: dict, dir: str): # Dict format {'filename' 'value-str'}
	try:
		with open(dir + "Result_" + f_start_with + ".txt", "w") as f:
			for key, value in result.items():
				# Replace unwanted characters
				value = value.replace(".", ",")
				key = key.replace("[", "")
				key = key.replace("]", "")
				key = key.replace(".xml", "")
				f.write(key + "\t" + value + "\n")
	except Exception as e:
		print(e)

	return()


def main():
	files = Get_File_List(folder)
	if not files:
		print("\n*** No files matching the search pattern ***\n")
		raise SystemExit()
	else:
		print("\n*** Found files from Get_File_List:")
		print(files[0] + " ... " + files[-1])

	data = Get_Line_Data(files, folder, (line_number - 1)) # @line_number = target line minus one
	if not data:
		print("\n*** No matching line in any file ***\n")
		raise SystemExit()
	else:
		print("\n\n*** First 5 lines in files from Get_Line_Data: ") # For inspection purpose
		for key in list(data.items())[0:5]:
			print(key)

	result = Extract_Line_Data(data, mark_start, mark_end)
	if not result:
		print("\n*** No results matching the search pattern in any file ***\n")
		raise SystemExit()
	else:
		print("\n*** First 10 result from Extract_Line_Data:") # For inspection purpose
		for key, value in list(result.items())[0:10]:
			print("File:", key, "\tValue:", value)

	Save_To_File(result, run_dir)
	print("\nSaving results to " + run_dir + "Result_" + f_start_with + ".txt")


if __name__ == "__main__":
	main()
