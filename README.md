# CanadaFSAParser
Parse Canadian FSA information from Canada Post's Official Listing of Forward Sortation Areas

# Reqiurements

Python packages used:
* PyPDF2 - To parse information from the PDF
* re - To use regular expressions to focus on the FSAs
* pandas - To store in a dataframe, then excel
* json - To store as a JSON

# Example link
Here is an example document, for which this script works well: https://www.canadapost.ca/assets/pdf/KB/nps/nps_nonlettermail_fsalist_jan2019.pdf

# Usage
1. Place the script in your preferred location
2. Download the latest Canada Post listing of Forward Sortation Areas (FSAs)
3. Run the python script, by navigating to the location and using 'python canada_fsa_parser.py' on your shell
4. Provide the location when prompted. For ease of use, place the PDF in the same directory/folder and supply the full file name. Eg: 'nps_nonlettermail_fsalist_jan2019.pdf'
5. The script will prompt you to save as an Excel or JSON, and make your selections
6. The files should appear in the same directory as your script
7. Voila!

# Output
Example of the Excel file <br/>
<img width="400" alt="ExcelExample" src="https://user-images.githubusercontent.com/66018030/105915081-e72bd300-5ff4-11eb-9a75-229e0a638919.PNG">


# Other
Feel free to use the JSON text file or Excel file included in the files above 

