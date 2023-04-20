from datetime import datetime
import os
import re
import requests
from bs4 import BeautifulSoup

def main():
    # define the base URL for the search results to be Psychology Today. This is the URL that will be scraped
    base_url = 'https://www.psychologytoday.com'

    clear('win')
    # get the search query parameters from the user
    state = input("Enter the state you want to search (ENTER STATE ABRV): ").upper()
    city = input("Enter the city you want to search: ").lower()
    city.replace(" ", "-")

    # define the search query parameters
    search_params = {
        'search': city,
        'state': state,
        'therapy_select': 'Yes',
        'page': 1
    }

    #headers
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    # send a get request to the search results page with the query parameters
    response = requests.get(base_url + '/us/therapists', params=search_params, headers=headers)
    print("Response status code: ", response.status_code)

    # parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    #print("Soup: ", soup)

    # define a dictionary to store the profile locations and their corresponding counts
    profile_locations = {}
    date = datetime.now()
    dt_string = date.strftime("%d/%m/%Y %H:%M:%S")
    
    clear('win')

    # iterate through all the search result pages
    page = 1
    print("Loading...")
    while(True):
        try:
            loadingBar(page)

            # update the page parameter in the search query
            search_params.update({'page': page})
            # send a GET request to the search results page with the updated query parameters
            response = requests.get(base_url + '/us/therapists', params=search_params, headers=headers, allow_redirects=False)
            if(response.status_code != 200):
                break
            
            # parse the HTML content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # find all the profile cards on the page
            profile_cards = soup.find_all('div', {'class': 'results-row top-divider'})

            # iterate through all the profile cards on the page
            for card in profile_cards:
                # extract the profile location from the card
                location = card.find_all('div', {'class': 'profile-location'})
                for loc in location:
                    # get the zip code from the location card
                    zip_code = re.search(r'\d+', loc.text).group()

                    #add the location to the dictionary if it doesn't exist yet
                    if zip_code not in profile_locations:
                        profile_locations[zip_code] = 1
                    #increment the count for the location if it already exists in the dictionary
                    else:
                        profile_locations[zip_code] += 1
            page += 1
        except:
            break
    
    clear('win')
    print("\nDone!")

    # format the city name
    city = search_params.get("search")
    first_letter = city[0].upper()
    rest_of_city = city[1:].lower()
    city = first_letter + rest_of_city

    # print the total results per location
    print("\nAccording to Psychology Today, as of " + dt_string + ":\n")
    print("\nThe total results of therapists per zip code in " + city + ", " + search_params.get("state") + ":\n")
    for location, count in profile_locations.items():
        print(f'{location}: {count}')

    # print the total number of therapists found
    print("\nTotal number of therapists found in " + city + ", " + search_params.get("state") + ": " + str(sum(profile_locations.values())))

# clear the console
def clear(name):
    # for windows
    if name == 'win':
        _ = os.system('cls')
    # for mac and linux
    else:
        _ = os.system('clear')

# animates the loading bar
def loadingBar(pageNum, enable=False):
    if enable:
        pageNum = pageNum % 10
        match pageNum:
            case 3:
                clear('win')
                print("Loading.  ")
            case 6:
                clear('win')
                print("Loading.. ")
            case 9:
                clear('win')
                print("Loading...")
    

# run the main function
if __name__ == '__main__':
    main()