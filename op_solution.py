import time
import pandas as pd
import numpy as np
import random

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_city():
    # these lists are the available options the user can type into the various filters
    city_options = ['chicago', 'new york city','washington']

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington), this loop will return statements if the selection is not what is expected.
    while True:
        try:
            city_input = str(input('\nSo, what city would you like to explore?! Chicago, New York City, or Washington:\n'))
        # if there is a value error it will print this
        except ValueError:
            print("{} was sadly not understood".format(city_input))
            continue
        # if it is not part of the pre-defined list above it will print this
        if city_input.lower() not in city_options:
            print("{}, was sadly not an option".format(city_input))
            continue
        else:
#           if the input is accepted it will assign the input to 'city'
            city = city_input.lower()
            break
    return city

def get_time_period():
    # these are the available options which are used in the loops below
    period_options = ['month', 'day', 'none']
    month_options = ['january', 'february', 'march', 'april', 'may', 'june']
    day_options = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    confirm_options = ['y', 'yes', 'n', 'no']

    print("\nHow would you like to filter this data?")

    # get user input, this loop will return statements if the selection is not what is expected.

    while True:
        try:
            period_input = str(input('\nYou can filter by month, day or not at all. If you want no filter, type "none":\n'))
        # if there is a value error it will print this
        except ValueError:
            print("{} was sadly not understood".format(period_input))
            continue
        # if it is not part of the pre-defined list above it will print this
        if period_input.lower() not in period_options:
            print("{}, was sadly not an option".format(period_input))
            continue
        else:
            #if the input is accepted it will assign the input to 'period'
            period = period_input.lower()
            break
    # if youn have selected to look for a month, this will ask which month you look for, the loop will reject invalid answers
    if period.lower() == 'month':
        print('\nOkay, now we need some more infomation to help us get your data.')
        while True:
            try:
                # if there is a value error it will print this
                month_input = str(input('\nNow lets find out what month you want, between Jan & June! Please enter full name e.g. January:\n'))
            except ValueError:
                print("That was sadly not understood, enter a full month name please.")
                continue
            # if it is not part of the pre-defined list above it will print this
            if month_input.lower() not in month_options:
                print("{}, was sadly not an option".format(month_input))
                continue
            #if the input is accepted it will assign the input to 'month'
            else:
                month = month_input.lower()
                # if month is chosen it will assign day to show all days
                day = 'all'
                break
        # confirmation of the month you are looking at
        print("\nYou selected to look at data based on the month of {}\n".format(month.title()))
    # if you have selected to look at a day, this will ask you what day, the loop will reject invalid answers
    elif period.lower() == 'day':
        print('\nOkay, now we need some more infomation to help us get your data.')
        while True:
            try:
                day_input = str(input('\nPlease enter the day you want to search on e.g.Monday:\n'))
            # if there is a value error it will print this
            except ValueError:
                print("That was sadly not understood, enter the full day name please.")
                continue
            # if it is not part of the pre-defined list above it will print this
            if day_input.lower() not in day_options:
                print("{}, was sadly not an option".format(day_input))
                continue
            #if the input is accepted it will assign the input to 'day'
            else:
                day = day_input.lower()
                # if day is chosen it will assign month to show all months
                month = 'all'
                break
        # confirmation of the day you are looking at
        print("\nYou selected to look at data based on {}\n".format(day.title()))
    # if you are looking for no filters (all data) this will tell you that
    else:
        print('\nAs you are selecting no filter, we will go ahead and show you information based on all the data')
        # if no filters it will show all days and months
        day = 'all'
        month = 'all'
    # this is used to confirm that the user is happy with their inputs
    while True:
        try:
            # this prints what has been currently selected
            print('\n\nFilter: {}, Month: {}, Day: {}'.format(period.title(),month.title(),day.title()))
            confirm_input = str(input('\nOkay, you have now chosen your selection (shown above), are you happy with this? (y/n)\n'))
        # if there is a value error it will print this
        except ValueError:
            print("{} was sadly not understood".format(period_input))
        # if it is not part of the pre-defined list above it will print this
        if confirm_input.lower() not in confirm_options:
            print("{}, was sadly not an option".format(period_input))
            continue
        # if it is not part of the pre-defined list above it will print this
        elif confirm_input.lower() == 'y' or confirm_input.lower() == 'yes':
            print('\nOkay perfect, lets get started\n')
            break
        else:
            # this will close the script if the user is not happy with their selections
            print('\nOkay then, this will now close, please run again and input your desired parameters')
            raise SystemExit
            break

    return  period, month, day

def load_data(city, period, month, day):
    #load the data from relevant file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # this will turn the trip duration (currently in seconds) into minutes
    df['Trip_Dur_Mins'] = df['Trip Duration'] / 60

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def user_type_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    user_types = df['User Type'].value_counts()
    #prints out some information regarding what we will show
    print("\n\nThe data below shows the amount of subscribers and the amount of customer")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(user_types)

def start_station_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    start_station = df['Start Station'].value_counts().head(5)
    #prints out some information regarding what we will show
    print("\n\nThe data below shows the most used start stations")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(start_station)

def end_station_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    end_station = df['End Station'].value_counts().head(5)
    #prints out some information regarding what we will show
    print("\n\nThe data below shows the most used end stations")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(end_station)

def gender_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    gender_count = df['Gender'].value_counts()
    #prints out some information regarding what we will show
    print("\n\nThe data below shows the usage by gender")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(gender_count)

def birth_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    birth_stats = df['Birth Year'].describe()
    #prints out some information regarding what we will show
    print("\n\nThe data below gives us some statistics related to the birth dates of the people using the service")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(birth_stats)

def dur_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    dur_stats = df['Trip_Dur_Mins'].describe()
    #prints out some information regarding what we will show
    print("\n\nThe data below gives us some statistics based on the duration of journeys (minutes)")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(dur_stats)

def weekday_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    weekday_count = df['day_of_week'].value_counts()
    #prints out some information regarding what we will show
    print("\n\nThe data below gives us some statistics based on the day used")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(weekday_count)

def month_breakdown(df):
    #starts a timer to see how long this takes to execute
    start_time = time.time()
    #selects the column of the dataframe we will analyse
    month_count = df['month'].value_counts()
    #prints out some information regarding what we will show
    print("\n\nThe data below gives us some statistics based on the month's used")
    #stops the timer and prints out how long it took to execute
    print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)

    print(month_count)


def random_line(df):
    # this is used to select a random line of data to look at
    df_1 = df.sample(n=1)
    print(df_1)

def main():
    # this is the main function that we will run, below are the acceptable inputs for a variable below
    random_options = ['y','n','yes','no']
    #this assigns the relevant city and periods to the functions called below
    city = get_city()
    period, month, day = get_time_period()
    df = load_data(city, period, month, day)
    #this calls the functions to analyse data
    user_type_breakdown(df)
    start_station_breakdown(df)
    end_station_breakdown(df)
    dur_breakdown(df)
    #as washington does not have this data, this only runs on other cities
    if city != 'washington':
        birth_breakdown(df)
        gender_breakdown(df)
    # this would not be relevant if you looked at months, so wont run if that was chosen
    if period != 'month':
        month_breakdown(df)
    # this would not be relevant if you looked at days, so wont run if that was chosen
    if period != 'day':
        weekday_breakdown(df)

    # this loop will show random individual trip data until 'n' is chosen, if incorrect inputs are given it will loop until they are
    while True:
        try:
            rand_input = str(input('\nWould you like to see a random trip? (y/n) \n'))
        # if there is a value error it will print this
        except ValueError:
            print("{} was sadly not understood".format(rand_input))
        # if it is not part of the pre-defined list above it will print this
        if rand_input.lower() not in random_options:
            print("{}, was sadly not an option".format(rand_input))
            continue
        # if some determined variables are selected it will run the function to show random trips
        # this will loop until 'n' is entered
        elif rand_input.lower() == 'y' or rand_input.lower() == 'yes':
            random_line(df)
            continue
        # if 'n' is chosen the script will shut down
        else:
            print("Okay, thanks for analysing some data! We will now exit. Run the script again if you want more insights.")
            raise SystemExit
            break

if __name__ == "__main__":
	main()
