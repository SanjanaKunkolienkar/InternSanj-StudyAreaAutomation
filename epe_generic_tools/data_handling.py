def kwarg_or_def(kwargs, kw, default_val):
    """
    Return lookup-value in a dictionary if it exists, or a default value if it doesn't exist.
    
    INPUTS:
    kwargs - Input dictionary
    kw - Keyword to find in dictionary
    default_val - Default value if keyword does not exist
    
    OUTPUTS:
    output_1 - Value from dictionary if exists, else default_val
    """
    if kwargs == None:
        return default_val
    return kwargs[kw] if kwargs.has_key(kw) else default_val
    
    
def csv_data_to_dictionary(in_data):
    """
    Function that takes csv formated list of lists (matrix) and creates a dictionary with the first element in the list being
    the key and all following values being the values. If there are duplicates seen in the first 'column' then an exception is raised,
    it should be unique.
    
    INPUTS:
    in_data - Csv formated list of lists (matrix) 
    
    OUTPUTS:
    data_dict - Dictionary with keys made up of all first column values, remaining columns making up values.
    """

    data_dict = {}
    for x in range(len(in_data)):
        entry_header = in_data[x][0]
        entry_data = in_data[x][1:]

        if entry_header in data_dict:
            raise ValueError('The provided data already has an instance ' + str(entry_header) + ' in the first column. Please rename one.' )
        data_dict[entry_header] = entry_data

    
    return data_dict
    

def transpose_list(in_list):
    """
    Transposes an input list. If length of lists on a given access are not the same, values of 'N/A' are filled in.
    
    INPUTS:
    in_list - Input list of lists (matrix represnted as list of lists)
    
    OUTPUTS:
    output_1 - Transposed list with 'N/A' filling locations caused by uneven length lists
    """
    return [list(row) for row in six.moves.zip_longest(*in_list, fillvalue='N/A')]
    
    
def search_list(inList,search_term):
    """
    Search list for entry and find index 
    
    INPUTS:
    in_list - Input list of lists (matrix represnted as list of lists)
    search_term - Value to search list for 
    
    OUTPUTS:
    output_1 - Index of first found instance of searched term or None if not found
    """
    try:
        return inList.index(search_term)
    except ValueError:
        return None

        
def enumerate_list_indeces(list_to_search):
    """
    Find the location of each kw in the list, duplicates may exist
    thus duplicate kws in the list will have multiple element locations.
    EX: ['this','that','this'] will return a dict: {'this':[0,2],'that':[1]}
    
    INPUTS:
    list_to_search - Input list to find indeces of each unique entry
    
    OUTPUTS:
    output_1 - Dictionary with each unique entry in list_to_search being a key and values being the indeces where the entry exists in list_to_search
    """  
    kwDict = {}
    for element in list_to_search:       
        if element not in kwDict: 
            kwDict[element] = [i for i, e in enumerate(list_to_search) if e == element]

    return kwDict 
    
    
def type_cast_lists(in_list,in_type):
    """
    Typecasts all elements of a list to a specific type, or returns None if it fails.
    
    INPUTS:
    in_list - Input list
    in_type - Type to typecast all values in in_list
    
    OUTPUTS:
    output_1 - Original list with all values of type in_type or None if function fails
    """  
    try:
        return [in_type(x) for x in in_list]
    except:
        print("could not type cast elements in list to type " + str(in_type))
        return None
        
        
        
def condense_csv_readable(in_data):
    """
    Takes in csv data and re-organizes into readable data. 
    
    INPUTS:
    in_data - Input CSV data
    
    OUTPUTS:
    out_data - Reorganized data with enhanced readability
    
    This function will attempt to reorganize data assuming the data is presented in a format as follows:
    A,1
    B,2
    A,2
    B,3
    C,1
    C,4
    
    The function will group the first column as a key and append values as extended columns. The organization will
    attempt to capture similarities between data and thus above would come out to be:
    A,1,2, ,
    B, ,2,3,
    C,1, , ,4
    
    Note that the values will be lined up on SAME VALUES. As a result, this function will be able to find similarities
    between Column A and Column B pairings by reducing Column A to unique keys and Column B - Column n being the values
    for the unique key.
    """  
    
    dict_data = {}
    vals = []
    dump_format = []
    for entry in in_data:
        key = entry[0]
        val = entry[1]
        if key not in dict_data:
            dict_data[key] = []
        dict_data[key].append(val)
        vals.append(val)
        
    unique_vals = list(set(vals))
    unique_vals_count = [vals.count(v) for v in unique_vals]
    unique_vals_sorted = [x for _,x in sorted(zip(unique_vals_count,unique_vals), reverse=True)]
    print(unique_vals)

    
    for key in dict_data:
        temp = [key]
        for val in unique_vals_sorted:
            if val in dict_data[key]:
                temp.append(val)
            else:
                temp.append('')

        dump_format.append(temp)
    
    
    return dict_data, dump_format
    
    
    