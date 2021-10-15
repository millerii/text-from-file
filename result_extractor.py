#!usr/bin/env/ python3

import os
import sys

folder = "C:\\TestReports\\" # Where to search
f_start_with = "[BC30" # *Files start with...
f_end_with = ".xml" # ...Files end with*
line_number = 668 # Line no. to search (target line minus one)
mark_start = '= "' # *Desired string is between...
mark_end = '" x' # ...Desired string is between*
run_dir = os.path.dirname(__file__) # .py file run location, used as save location for results


def Get_File_List(path: str) -> list: # Absolute folder path
	files=[]
	
	# Get list of files in [folder] filtered with [f_start_with] & [f_end_with]
	try:
		print("Scanning path: " + path)
		for entry in os.scandir(path):
			if entry.name.startswith(f_start_with) and entry.name.endswith(f_end_with) and entry.is_file():
				files.append(entry.name)
	except Exception as e:
		print("\n*** Invalid folder path ***\n")
		raise SystemExit(e)

	return files # List of files found ['filename']

def Get_Line_Data(files: list, path: str, line_no: int) -> dict:
	# Go through files and pick desired line
	data= {}
	
	print("")
	try: # Open files and save desired line
		for file in files:
			print("Reading files in Get_Line_Data..." + file + "        ", end = "\r")
			with open(path + file, "r") as f:
				lines = f.readlines()
				try: # Case if file has no enought lines to proceed
					data[file] = lines[line_no]
				except Exception as e:
					print(e)
	except Exception as e:
		print(type(e))
		print(e)
		raise SystemExit(e)
	
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
		with open(dir + '\\Result_' + f_start_with + '.txt', 'w') as f:
			for key, value in result.items():
				f.write(key + "\t" + value + "\n")
	except Exception as e:
		print(e)
		
	return()


files = Get_File_List(folder)
print("Found files from Get_File_List:")
print(files[0] + " ... " + files[-1])

data = Get_Line_Data(files, folder, line_number)
print("\n\nFirst 5 lines in files from Get_Line_Data: ")
for key in list(data.items())[0:5]:
	print(key)

result = Extract_Line_Data(data, mark_start, mark_end)
print("\nFirst 10 result from Extract_Line_Data:")
for key, value in list(result.items())[0:10]:
	print("File: " + key + "\tValue: " + value)

Save_To_File(result, run_dir)
print("\nSaving results to " + run_dir + '\\Result_' + f_start_with + '.txt')
