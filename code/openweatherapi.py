'''
  File:  openweatherapi.py
  Name:  Sam Loyd
  Date:  May 26, 2019
  Desc:  This program uses an api call to open weather at http://api.openweathermap.org.
 Usage:  You can run this program by calling its name and answering prompts as instructed.
      :  Requires os, requests, iso3166, textwrap and zipcodes, and datetime packages be installed
'''


print("Please wait. Modules Loading ...")

# Verify needed modules are installed.
try:
    import requests
except:
    print("Please add requests package and restart.")
    exit()
try:
    import textwrap
except:
    print("Please add textwrap package and restart.")
    exit()
try:
    from iso3166 import countries
except:
    print("Please add countries package and restart.")
    exit()
try:
    import os
except:
    print("Please add os package and restart.")
    exit()
try:
    import zipcodes
except:
    print("Please add zipcodes package and restart.")
    exit()
try:
    from datetime import datetime
except:
    print("Please add datetime package and restart.")
    exit()

# Object used to count successful and unsuccessful attempts
class forecastCounter():

    #clean
    def __init__(self):
        self.countCalls = 0
        self.countFails = 0

    #setter for successes
    def addCall(self):
        self.countCalls += 1

    #setter for failures
    def addFail(self):
        self.countFails += 1

    #getter for successes
    def getCall(self):
        return self.countCalls

    #getter for failures
    def getFail(self):
        return self.countFails


# Acts as pause while the user reviews the answer returned if outside Pycharm.
def returnKey():
    isRunningInPyCharm = "PYCHARM_HOSTED" in os.environ
    if (not isRunningInPyCharm):
        promptValue = "\nPress enter to exit. Losing focus might require you to press enter a second time.\n"
        input(promptValue)

# Format and print forecast data
def pretty_print(dataReturned, mainKey, weatherKey, windKey, sysKey):
    longLine = "     {:_^78}".format("")
    print("{}\n\n         {}, {} current weather forecast: {}".format(longLine,dataReturned["name"],
        sysKey["country"],datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print("         Weather Description: {}".format(weatherKey[0]["description"]))
    print("         Current Temp: {} degrees".format(mainKey["temp"]))
    print("         Humidity: {} percent".format(mainKey["humidity"]))
    print("         Wind Speed: {} miles per hour\n{}\n".format(windKey["speed"],longLine))


# Parse and validate JSON data returned in a dictionary format
def parse_json(dataReturned, instance):
    if type(dataReturned) == type(dict()):
        try:
            mainKey = dataReturned["main"]
        except:
            instance.addFail()
            invalid_response("Main dictionary key unmatched")
            return
        try:
            weatherKey = dataReturned["weather"]
        except:
            instance.addFail()
            invalid_response("Weather key unmatched")
            return
        try:
            windKey = dataReturned["wind"]
        except:
            instance.addFail()
            invalid_response("Wind key unmatched")
            return
        try:
            sysKey = dataReturned["sys"]
        except:
            instance.addFail()
            invalid_response("Sys key unmatched")
            return
        instance.addCall()
        pretty_print(dataReturned,mainKey, weatherKey, windKey, sysKey)
    else:
        instance.addFail()
        invalid_response("Not a valid dictionary type")

# Error Call functions
def data_error(text):
    longLine = "{:.^118}".format(" (Error) ")
    longBottom = "{:.^118}".format("")
    print("{}\n{}\n{}".format(longLine,text,longBottom))

def invalid_response(reasonCode):
    longLine = "{:.^118}".format(" (Error) ")
    longBottom = "{:.^118}".format("")
    notValResp = "{}\nServer did not return response in expected format. Reason: {}.\n{}"\
        .format(longLine,reasonCode,longBottom)
    print(notValResp)

def error_call(err):
    longLine = "{:.^118}".format(" (Error) ")
    longBottom = "{:.^118}".format("")
    failureResp = "{}\nCall failed. Check your zip or city provided and internet connection."\
        .format(longLine)
    print(failureResp)
    wrapper = textwrap.TextWrapper(width=100)
    word_list = wrapper.wrap(text=str(err))
    for line in word_list:
        print("      {}".format(line))
    print("{}".format(longBottom))

# function to attempt URL call and provide error codes on failure
def call_url(completeUrl, instance):
    successResp = "Server response was successful."
    try:
        response = requests.get(completeUrl)
        response.raise_for_status()
    except Exception as err:
        instance.addFail()
        error_call(err)
        return
    else:
        print(successResp)
    try:
        dataReturned = response.json()
    except:
        instance.addFail()
        invalid_response("JSON load failed.")
        return
    parse_json(dataReturned, instance)

# function that builds URL based on type of data provided by user
def createUrl(userInput):
    apiKey = "fc97a039291d092e50e1ec694e3b206b"
    weatherUrl = "http://api.openweathermap.org/data/2.5/weather"
    tryResp = "Trying call to {}. Please wait ...".format(weatherUrl)
    print(tryResp)

    try:
        float(userInput)
    except:
        queryType = "&q="
    else:
        queryType = "&zip="
    completeUrl = weatherUrl + "?appid=" + apiKey + queryType + userInput + "&units=imperial"
    return completeUrl

# function to display examples
def exampleMessage():
    exampleLine = "{:*^118}".format(" USER EXAMPLES ")
    exampleBottom = "{:*^118}".format("")
    exampleLine =\
    "{}\nValidated domestic examples: 10001 or New York or honolulu\n"\
    "Non-validated examples: paris,fr or 75000,fr or paris,france or e1,gb or 10001,us or honolulu,us\n{}"\
    .format(exampleLine, exampleBottom)
    print(exampleLine)


# function creating help message with important links.
def helpMessage():
    helpLine = "{:*^118}".format(" USER HELP ")
    helpBottom = "{:*^118}".format("")
    helpMessage =\
    "{}\nDomestic zip codes must be entered with five digits for validation.  "\
    "Some valid zip codes do not work with the API.\n    Domestic zip example: 10001\n"\
    "US City names should not include a comma or two character country code to be validated.\n"\
    "    Validated US city example: New York\n"\
    "Cities outside the US like Paris, France require a comma and two character country code"\
    " which turns off validation.\n"\
    "The links below can help you with API specifics.  Full country name can work with city in some cases.\n"\
    "    Non-validated examples: paris,fr or 75000,fr or paris,france or 10001,us or honolulu,us\n"\
    "Entering a z provides a zip code lookup for a city name and entering a c provides a country code lookup.\n"\
    "See https://pypi.org/project/zipcodes/ for domestic zipcode and city validation information.\n"\
    "See https://openweathermap.org/api and https://openweathermap.org/current for API information.\n"\
    "{}".format(helpLine, helpBottom)
    print(helpMessage)

# function to run through a list of valid zips while conserving screen real estate where possible
# by joining zips for a city in the same state
def printZips(validZip):
    oldState = ""
    counter = 0
    innercount = 0
    linVal = ""
    for loop in validZip:
        if oldState != validZip[counter]["state"]:
            innercount = 0
            if counter != 0:
                linVal += "\n"
            linVal += "     {}, {} ".format(validZip[counter]["city"], validZip[counter]["state"])
        else:
            if innercount == 14:
                innercount = 0
                linVal += "\n     {}, {} ".format(validZip[counter]["city"], validZip[counter]["state"])

        innercount += 1
        linVal = "{} {}".format(linVal, validZip[counter]["zip_code"])
        oldState = validZip[counter]["state"]
        counter += 1
    print(linVal)

# Lookup Zips by US City
def zipLookup():
    inputLine = "{:-^118}".format(" (Zip Lookup) ")
    inputBottom = "{:-^118}".format("")
    numericMessage = "Numeric values are not accepted. Did you mean to back up a level to the main menu?"
    inputMessage = "{}\nEnter a US city name for zip code lookup or x to exit to the main menu and "\
                   "press enter.\n{}\n>".format(inputLine,inputBottom)
    while True:
        userInput = input(inputMessage)
        if (userInput in ["X", "x"]):
            break
        else:
            try:
                float(userInput)
            except:
                pass
            else:
                print(numericMessage)
                continue
            validZip = zipcodes.filter_by(city=userInput.upper())
            if validZip == []:
                print("City not found.")
                continue
            else:
                validZip = sorted(validZip, key=lambda i: i['state'])
                printZips(validZip)
                print("Note: Not all valid zip codes work with the API.")

# Lookup country code by name
def countryLookup():
    inputLine = "{:-^118}".format(" (Country Lookup) ")
    inputBottom = "{:-^118}".format("")
    inputMessage = "{}\nEnter all or part of a country name or x to exit back to the main menu and press "\
                   "enter.\n{}\n>".format(inputLine, inputBottom)
    while True:
        userInput = input(inputMessage)
        if (userInput in ["X", "x"]):
            break
        else:
            for country in countries:
                if userInput.upper() in country.name.upper():
                    print("    {} {}".format(country.alpha2, country.name))

# Verify City with zipcodes module
def byCity(userInput):
    cityNotUnique = "City is not unique by state. Please retry using a valid zipcode from above. "\
                  "City comma US can disable validation.\nExample: 10001 or jackson,us"
    cityNotFound = "City not found. Outside the US or to disable module validation, use city and comma with "\
                   "two character country code.\nExample:paris,fr or juno,us"
    validZip = zipcodes.filter_by(city=userInput.upper())
    if validZip == []:
        data_error(cityNotFound)
        return 0
    else:
        counter = 0
        oldState = ""
        stateCounter = 0
        # Sort By State
        validZip = sorted(validZip, key=lambda i: i['state'])
        # More than 1 state returned?
        for loop in validZip:
            if validZip[counter]["state"] != oldState:
                stateCounter += 1
                oldState = validZip[counter]["state"]
                # Performance aide
                if stateCounter > 1:
                    break
            counter += 1
        if stateCounter > 1:
            # Print list of zips to choose from when not unique by state
            printZips(validZip)
            data_error(cityNotUnique)
            # print(zipList)
            return 0
        else:
            print("Location validated for {}, {}.".format(validZip[0]["city"], validZip[0]["state"]))
            return 1

# Verify Zip with zipcodes module.
def byZip(userInput):
    zipErrorMessage = "Zip not found. Outside the US or to disable validation, use zip code and comma with two "\
                      "character country code.\nExample:75000,fr or 10001,us"
    validZip = zipcodes.matching(userInput)
    if validZip == []:
        data_error(zipErrorMessage)
        return 0
    else:
        print("Location validated for {}, {} {}."
              .format(validZip[0]["city"], validZip[0]["state"],validZip[0]["country"]))
        return 1

# Attempts to open the file for writing until a successful file name is given.
def checkFileName():
    inputLine = "{:-^118}".format(" (Log Writer) ")
    inputBottom = "{:-^118}".format("")
    filePrompt = "{}\nEnter a file name for logging attempts, l to list files in current directory or x to exit"\
            " and press enter.\n"\
            "Selecting an existing file name will append data to the file.\n{}\n>".format(inputLine,inputBottom)
    while True:
        fileName = input(filePrompt)
        if fileName in ["X","x"]:
            print("Log writer skipped.")
            return 0
            break
        if fileName in ["L","l"]:
            for files in os.listdir("."):
                    print("    {}".format(files))
            continue
        try:
            with open(fileName, 'a') as checkHandle:
                pass
        except:
            errorLine = "{:.^118}".format(" (Error) ")
            errorBottom = "{:.^118}".format("")
            print("{}\nFailed to open file:{} for writing."\
                      "    Check file name, file and folder permissions and retry.\n{}\n"\
                      .format(errorLine,fileName,errorBottom))
            continue
        else:
            checkHandle.close()
            return fileName
            break

# Create log file if requested
def process_file(successCalls,failCalls,fileName):
    try:
        with open(fileName, 'a') as fileHandlePretty:
            logDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            linePrint = "Date Time:{}, Successes:{}, Failures:{}\n".format(logDate,successCalls,failCalls)
            fileHandlePretty.write(linePrint)
            fileHandlePretty.close()
    except:
        print("Log writer failed.\n")
    else:
        print("Log writer successful.\n")

def main():
    inputLine = "{:-^118}".format(" (Main Menu) ")
    inputBottom = "{:-^118}".format("")
    welcomMessage = "Hello and welcome to Current Weather Forecast provided by openweathermap.org's API."
    inputMessage = "{}\nEnter zip code or city name, h for help, e for examples, z for zip code lookup,"\
                   " c for country lookup or x to exit \nand press enter.  Outside the US"\
            " and to turn off local validation add comma and provide country code.\n{}\n>".format(inputLine, inputBottom)
    fiveError =  "Provide a 5 digit zip code. Outside the US, use zip code and comma with two "\
                 "character country code.\nExample: 10001 for New York or 75000,FR for Paris, France."
    tooShortError = "That is too short. Outside the US, use city and comma with two character country code."\
                    "\nExample: y,fr for Y in France"
    print(welcomMessage)
    instance=forecastCounter()
    while True:
        userInput = input(inputMessage)
        if (userInput in ["X","x"]):
            successCalls = instance.getCall()
            failCalls = instance.getFail()
            print("    Summary count of forecast attempts:\n    Date Time: {}\n    Successes: {}\n    Failures: {}"
                  .format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),successCalls, failCalls))
            fileName=checkFileName()
            if fileName:
                process_file(successCalls,failCalls,fileName)
            returnKey()
            break
        elif (userInput in ["H","h"]):
            helpMessage()
            continue
        elif (userInput in ["E","e"]):
            exampleMessage()
            continue
        elif (userInput in ["Z","z"]):
            zipLookup()
            continue
        elif (userInput in ["C","c"]):
            countryLookup()
            continue
        else:
            try:
                float(userInput)
            except:
                if len(userInput) < 3:
                    instance.addFail()
                    data_error(tooShortError)
                    continue
                else:
                    if "," not in userInput:
                        checkByCity = byCity(userInput)
                        if not checkByCity:
                            instance.addFail()
                            continue
            else:
                if len(userInput) != 5:
                    instance.addFail()
                    data_error(fiveError)
                    continue
                else:
                    checkByZip = byZip(userInput)
                    if not checkByZip:
                        instance.addFail()
                        continue
            completeUrl = createUrl(userInput)
            call_url(completeUrl, instance)
main()
