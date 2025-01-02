# police-fine-records

## Overview
This project is designed to manage data related to fines issued by the municipal police. The system handles the storage, manipulation, and processing of fine-related data, including the types of fines, users, and relevant details. The system works with binary sequential files for data storage, with a specific focus on blocking factor management and sequential processing during updates.

## Key Features
1. **File Creation**  
   Create an empty file where the user specifies the file name.

2. **Activate File**  
   Choose an active file by specifying its name.

3. **File Display**  
   Display the name of the active file along with the first three menu options.

4. **Leading Serial File Formation**  
   Generate a leading serial file in real-time, containing records for adding, modifying, and deleting entries in the active file.

5. **Sequential Change File Formation**  
   - Load records from the serial change file into a dynamic data structure.  
   - Sort records based on ascending values of identifiers.  
   - Write records from the data structure into a sequential change file.

6. **Output Sequential File Formation**  
   Form an output sequential file based on the contents of both the sequential change file and the active file. Additionally, create an error log file detailing any errors encountered.

7. **Display All Active File Records**  
   Show all records from the active file, including block addresses and the serial number of records in each block.

## Requirements
- **Blocking Factor (f):** The blocking factor is set to 5.
- **File Operations:** The system supports reading and writing complete blocks only.
- **Change File Status Field:** The change file contains a status field for each record.
- **Error Description Field:** The error log file includes a field for error descriptions.
- **End-of-File Record:** The system uses a special record to indicate the end of the file.
- **Character Encoding:** The system uses only ASCII characters for textual content.

## Test Data
Prepare a test data file with at least 10 records to validate the functionality of the system.

## How to Use
1. **Create a New File:** Choose option 1 from the menu to create an empty file.
2. **Activate a File:** Select option 2 to specify and activate a file.
3. **Generate Files and Process Changes:** Use options 4 to 6 to form and process serial and sequential change files.
4. **View Active File Records:** Use option 7 to display all records in the active file.

## Technology Stack
- **Programming Language:** [Python]
- **File Format:** Binary Sequential File
- **Encoding:** ASCII

