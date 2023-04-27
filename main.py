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

def FBA_Fulfillment_Fees(type=1):
    data = {}
    size_and_dimension = []
    shipping_weight = []
    non_apparel_fees = []
    apparel_fees = []
    small_and_light_fees = []
    oversize_fees = []
    is_first_set = True

    # Creates prices for FBA categories if requested
    for INDEX in range(len(table)):
        INDEX_TEXT = table[INDEX].get_text()
        # Gets fulfillments fees for non-apparel items 
        if INDEX >= 149 and INDEX <= 152 or INDEX >= 164 and INDEX < 172 and type == 1:
            non_apparel_fees.append(INDEX_TEXT)
        # Gets fulfillments fees for apparel items 
        if INDEX in range(195, 199) or INDEX in range(210, 218) and type == 2:
            apparel_fees.append(INDEX_TEXT)
        # Gets fulfillments fees for Small and Light items
        if INDEX in range(241, 245) or INDEX in range(255, 262) or INDEX == 152 and type == 3:
            small_and_light_fees.append(INDEX_TEXT)
        # Gets oversize fees for non-apparel and apparel items
        if INDEX in [176, 180, 184, 188] and INDEX_TEXT not in oversize_fees:
            oversize_fees.append(INDEX_TEXT)

    # Manually appends last fee to lists below (indices being reused mixes the order from the scrape)
    # Note: In this case, order is important due to the zip function for the final print out
    if type == 1:
        non_apparel_fees.append(table[172].get_text())
    if type == 2:
        apparel_fees.append(table[172].get_text())
    if type == 3:
        small_and_light_fees.append(table[168].get_text())

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
                if ROW_TEXT not in shipping_weight:
                    shipping_weight.append(ROW_TEXT)

    # Removes duplicates in the shipping_weight list
    del small_and_light_fees[0]

    # Gets fees for non-apparel items
    if type == 1 or type == 4:
        # Manually formats rows for print
        data['non_apparel_small'] = [size_and_dimension[0], size_and_dimension[1], list(zip(shipping_weight[0:4], non_apparel_fees[0:4]))]     # Small Standard
        data['non_apparel_large'] = [size_and_dimension[2], size_and_dimension[3], list(zip(shipping_weight[0:9], non_apparel_fees[4:13]))]    # Large Standard
    
    # Gets fees for apparel items
    if type == 2 or type == 4:
        data['apparel_small'] = [size_and_dimension[0], size_and_dimension[1], list(zip(shipping_weight[0:4], non_apparel_fees[0:4]))]     # Small Standard
        data['apparel_large'] = [size_and_dimension[2], size_and_dimension[3], list(zip(shipping_weight[0:9], non_apparel_fees[4:13]))]    # Large Standard

    # Appends to data only if apparel or non-apparel fees are requested
    if type == 1 or type == 2 or type == 4:    
        # Identical for both apparel and non-apparel fees
        data['small_oversize'] = [size_and_dimension[4:7], oversize_fees[0]]       # Small Oversize
        data['medium_oversize'] = [size_and_dimension[8:11], oversize_fees[1]]     # Medium Oversize
        data['large_oversize'] = [size_and_dimension[12:15], oversize_fees[2]]     # Large Oversize
        data['special_oversize'] = [size_and_dimension[16:19], oversize_fees[3]]   # Special Oversize
        
    # Gets fees for small and light items
    if type == 3 or type == 4:
        data['small_and_light_small'] = [table[235].get_text(), size_and_dimension[1], list(zip(shipping_weight[0:4], small_and_light_fees[0:4]))]      # Small Standard
        data['small_and_light_large'] = [table[245].get_text(), size_and_dimension[3], list(zip(shipping_weight[0:8], small_and_light_fees[4:12]))]     # Large Standard       
    
    return data

def Storage_Fees():
    data = {}
    data['first'] = [row.get_text() for row in table[263:266]]      # Standard
    data['second'] = [row.get_text() for row in table[266:269]]     # Oversize
    return data

if __name__ == '__main__':
    # print(FBA_Fulfillment_Fees(3))
    print(Referral_Fees())
    # Storage_Fees()