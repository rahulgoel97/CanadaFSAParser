'''
- Canadian FSA (Forward Sortation Area) parser
- Use Canada Post's listing to parse FSAs and Areas into a pandas dataframe and JSON format
- Example: https://www.canadapost.ca/assets/pdf/KB/nps/nps_nonlettermail_fsalist_jan2019.pdf (Jan 2019)
- Download the PDF on your computer, and use directory as input
'''

# Import dependencies
import PyPDF2
import re
import pandas as pd
import json

# Get the directory
file_location=input("Please enter the directory: ")

# Parse the file
def parse_pages(pdfReader):
    """
    Loops over all the pages from the Canada Post document, and returns parsed data    
    
    """
    
    fullList = []
    
    ### Get number of paged
    numPages = pdfReader.numPages
    
    ### Loop over pages
    for page in range(0, numPages):
        
        # Create page object
        pageObj = pdfReader.getPage(page)  
       
        
        # Extract text 
        text = pageObj.extractText()
            
        # Parse data
        parsedData = parse_page(text)
        
        # Build data
        fullList.append(parsedData)
        
    # Initialize the lists
    fsa_name_list = []
    fsa_desc_list = []

    # To count FSAs and ensure totals are 1.6K, initialize to 1
    counter = 1

    # Iterate over the fullList
    for value in fullList:
        for idx, subvalue in enumerate(value):

            # Extract the tokens
            fsa = subvalue[0]
            fsa_desc = subvalue[1:len(subvalue)]

            # Join tokens into a sentence
            fsa_desc_clean = ' '.join(fsa_desc)

            # Build the lists
            fsa_name_list.append(fsa)
            fsa_desc_list.append(fsa_desc_clean)

            # Incremenet
            counter+=1
    
    ### Build the table
    df = pd.DataFrame()
    df['FSA'] = fsa_name_list
    df['Area'] = fsa_desc_list
    
    ### Return dataframe
    return df
        
def parse_page(strings):
    """
    Input: Takes in a string of Canada Post's listing of Forward Sortation Areas
    Output: Parsed FSA name and location in a large list
    
    """
    ### Use RegEx to identify the FSAs
    fsa_vals = re.findall(r'([A-Z][0-9][A-Z$])', strings)
    
    
    ### Split up the input into tokens, separated by a space
    tokens = strings.split()
    
    # List to capture the indices of identified FSAs in fsa_vals
    location_list = []
    
    # Loop over all the FSA-values & append to list
    for fsa in fsa_vals:
        for idx, token in enumerate(tokens):
            if(token==fsa):
                location_list.append(idx)
                
    
    ### Construct the FSA list
    
    #List of lists for FSAs
    fsa_full_list=[]
    
    # Loop over the indices of identified FSAs
    for idx_value in range(len(location_list)):
        
        # Temporary list to capture data for each individual FSA
        fsa_temp_list=[]
        
        # For all FSAs...
        try:
            for i in range(location_list[idx_value], location_list[idx_value+1]):
                
                # Add the data to the temporary list
                fsa_temp_list.append(tokens[i])
            
        # Except the last FSA...
        except:
            
            # Create variable to capture the "last index" to capture 
            last_index = 0
            
            # The last index occurs before the "(+) ADDITION" descriptor in tokens
            for idx, token in enumerate(tokens):
                if(token=='(+)' and tokens[idx+1]=='ADDITION'):
                    last_index=idx # This is the last index
            
            # Now, use the last index to capture the last FSA's data
            for i in range(location_list[len(location_list)-1], last_index):
                fsa_temp_list.append(tokens[i])
                
        # Finally, append to the large list, to create a list of lists
        fsa_full_list.append(fsa_temp_list)
        
    ### Return the list of lists
    return fsa_full_list

def getFSAValues(file_location):
    
    # Open File
    pdfFileObj = open(file_location, 'rb')  
    
    # creating a pdf reader object  
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    
    # Parse the pdf 
    df = parse_pages(pdfReader)
    
    # Convert to JSON
    fsa_json = json.loads(df.to_json())
    
    # Return dataframe and json file
    return df, fsa_json

print("...Parsing the data")

try:
	dfvals, jsonvals = getFSAValues(file_location)
	print("...Success!")

	while(True):
		response = input("Do you want to save into Excel? (Y/n)")
		if(response=='Y' or response=='y'):
			dfvals.to_excel('FSA_Values.xlsx')
			print("...Saved into Excel file")
			break
		elif(response=='N' or response=='n'):
			break
		else:
			print("Please enter a valid response")
			pass

	while(True):
		response = input("Do you want to save into JSON format? (Y/n)")
		if(response=='Y' or response=='y'):
			with open('FSA_vals.txt', 'w') as outfile:
				json.dump(jsonvals, outfile)
			print("...Saved into TXT file")
			break
		elif(response=='N' or response=='n'):
			break
		else:
			print("Please enter a valid response")
			pass

except:
	print(f"Unknown error...")


