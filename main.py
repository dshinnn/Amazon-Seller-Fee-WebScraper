import requests
from bs4 import BeautifulSoup

# Make a GET request to the URL you want to scrape
url = 'https://sell.amazon.com/pricing#referral-fees'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find_all('div', class_='text align-start color-storm font-size-small ember font-normal')

def Referral_Fees():
    referral_fees_contents = soup.find_all('div', class_='content')
    data = []
    row_data = []
    count = 0

    # Grabs the div with the Referral Fees Content
    referral_fees_main_content = referral_fees_contents[4] 
    referral_fees = referral_fees_main_content.find_all('div', class_='text align-start color-storm font-size-small ember font-normal')

    # Parses div text into string and formats data into rows 
    for row in referral_fees:
        # Resets count once the value is no longer in the same row
        if count > 2:
            data.append(row_data)
            count = 0
            row_data = []    
        row_data.append(row.get_text())
        count += 1
    
    # Appends last row manually
    data.append([row.get_text() for row in referral_fees[-3:]])

    return data

def FBA_Fulfillment_Fees(type=3):
    data = []
    size_and_dimension = []
    shipping_weight = []
    non_apparel_fees = []
    apparel_fees = []
    small_and_light_fees = []
    is_first_set = True

    for index in range(len(table)):
        INDEX_TEXT = table[index].get_text()
        # Gets fulfillments fees for apparel items 
        if index in range(195, 199) or index in range(210, 218) and type == 1:
            apparel_fees.append(INDEX_TEXT)
        # Gets fulfillments fees for non-apparel items 
        if index >= 149 and index <= 152 or index >= 164 and index <= 172 and type == 2:
            non_apparel_fees.append(INDEX_TEXT)
        # Gets fulfillments fees for Small and Light items
        if index in range(241, 245) or index in range(255, 262) or index in [152, 168] and type == 3:
            small_and_light_fees.append(INDEX_TEXT)

    # Gets common data for the fulfillment fees
    for row in table:
        ROW_TEXT = row.get_text()
        ROW_INDEX = table.index(row)

        if not is_first_set and ROW_INDEX == 143 and type != 3:
            break
        
        # Gets only the non-apparel fulfillment fees
        if ROW_INDEX >= 143 and ROW_INDEX <= 188:
            if ROW_INDEX == 143:
                is_first_set = False

            # Gets Size Tier and Max Dimension column values as well as full rows for Small to Special Oversizes
            if ROW_INDEX in [143, 144, 153, 154] or ROW_INDEX in range(173, 189):
                size_and_dimension.append(ROW_TEXT)
            
            # Gets Shipping Weight column values
            if ROW_INDEX >= 145 and ROW_INDEX <= 148 or ROW_INDEX > 154 and ROW_INDEX <= 163:
                shipping_weight.append(ROW_TEXT)
            
    # Removes duplicates in the shipping_weight list
    del shipping_weight[0:4]
    del small_and_light_fees[0:2]

    # Gets fees for non-apparel items
    if type == 1:
        # Manually formats rows for print
        data.append([size_and_dimension[0], size_and_dimension[1], list(zip(shipping_weight[0:4], non_apparel_fees[0:4]))])     # Small Standard
        data.append([size_and_dimension[2], size_and_dimension[3], list(zip(shipping_weight[0:9], non_apparel_fees[4:13]))])    # Large Standard
    
    # Gets fees for apparel items
    if type == 2:
        data.append([size_and_dimension[0], size_and_dimension[1], list(zip(shipping_weight[0:4], apparel_fees[0:4]))])     # Small Standard
        data.append([size_and_dimension[2], size_and_dimension[3], list(zip(shipping_weight[0:9], apparel_fees[4:13]))])    # Large Standard

    # Gets fees for small and light items
    if type == 3:
        data.append([table[235].get_text(), size_and_dimension[1], list(zip(shipping_weight[0:4], small_and_light_fees[0:4]))])     # Small Standard
        data.append([table[245].get_text(), size_and_dimension[3], list(zip(shipping_weight[0:8], small_and_light_fees[4:12]))])    # Large Standard        
    
    # Appends to data only if apparel or non-apparel fees are requested
    if type == 1 or type == 2:    
        # Identical for both apparel and non-apparel fees
        data.append(size_and_dimension[4:7])      # Small Oversize
        data.append(size_and_dimension[8:11])     # Medium Oversize
        data.append(size_and_dimension[12:15])    # Large Oversize
        data.append(size_and_dimension[16:19])    # Special Oversize

    return data

def Storage_Fees():
    data = []
    data.append([row.get_text() for row in table[263:266]])     # Standard
    data.append([row.get_text() for row in table[266:269]])     # Oversize
    return data

if __name__ == '__main__':
    # FBA_Fulfillment_Fees()
    # Referral_Fees()
    Storage_Fees()