import time
import pandas as pd
import numpy as np
import calendar as cal

# information about the bikeshare data we have available
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for Chicago, New York City, or Washington?\n')
            if city.lower() not in ('chicago', 'new york city', 'washington'):
                print('I don\'t have data for that city\n')
                continue
        except ValueError:
            print('I need a valid city name')
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            next = input('Would you like to filter by month, day, or none?\n')
            if next.lower() not in ('month','day','none'):
                print('Please specify a valid option\n')
                continue
        except ValueError:
            print('I need a valid option')
        else:
            if next == 'none':
                month = 'all'
                day = 'all'
            elif next == 'month':
                while True:
                    try:
                        month = input('Enter the month you\'d like to filter by (options include all, Jan, Feb, Mar, Apr, May, Jun)\n')
                        if month.lower() not in ('all', 'jan','feb','mar','apr','may','jun'):
                            print('Please specify a valid month\n')
                            continue
                    except ValueError:
                        print('I need a valid month')
                    else:
                        day = 'all'
                        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
            elif next == 'day':
                while True:
                    try:
                        day = input('Enter the day you\'d like to filter by (options include all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)\n')
                        if day.lower() not in ('all', 'monday','tuesday','wednesday','thursday','friday','saturday','sunday'):
                            print('Please specify a valid day\n')
                            continue
                    except ValueError:
                        print('I need a valid day')
                    else:
                        month = 'all'
                        break
        break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.lower()])

    # converts Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month_index = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month_index]

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_index = df['Month'].mode()[0]
    common_month = cal.month_name[month_index]
    print('The most common month to travel is {}'.format(common_month))

    # display the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print('The most common day of the week to travel is {}'.format(common_day))

    # display the most common start hour
    hours = df['Start Time'].dt.hour.mode()[0]
    print('The most common hour to start travelling is {}'.format(hours))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most common station to start travelling from is {}'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most common station to finish your travels is {}'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['Start End'] = df['Start Station'] + ' / ' + df['End Station']
    common_start_end = df['Start End'].mode()[0]
    print('The most common start / end combination for travel is {}'.format(common_start_end))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Diff'] = df['End Time'].sub(df['Start Time'], axis = 0)
    diff_sum = df['Diff'].sum()
    diff_days, diff_hours, diff_minutes, diff_seconds = time_parts(diff_sum)
    print('The total travel time is {} days, {} hours, {} minutes, and {} seconds'.format(diff_days, diff_hours, diff_minutes, diff_seconds))

    # display mean travel time
    mean_time = df['Diff'].mean()
    mean_days, mean_hours, mean_minutes, mean_seconds = time_parts(mean_time)
    print('The average travel time is {} days, {} hours, {} minutes, and {} seconds'.format(mean_days, mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_parts(time):
    """ Breaks down a datetime object into its individual parts of
    days, hours, minutes, and seconds. """

    days = time.days
    hours = time.seconds//3600
    minutes = (time.seconds%3600)//60
    seconds = time.seconds%60

    return days, hours, minutes, seconds


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The different types of users are:')
    print(user_types)
    print('\n')

    # Display counts of gender
    if city.lower() == 'washington':
        print('There is no gender data for this city.')
    else:
        gender_count = df['Gender'].value_counts()
        print('The breakdown of the genders of users are')
        print(gender_count)
        print('\n')

    # Display earliest, most recent, and most common year of birth
    if city.lower() == 'washington':
        print('There is no birth year data for this city.')
    else:
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])
        print('The oldest user was born in {}'.format(oldest))
        print('The youngest user was born in {}'.format(youngest))
        print('The most common birth year among users is {}'.format(common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        first_index = 0
        second_index = 5
        increment = 5

        # Determines if user wants to see raw data from potentially filtered file.
        while True:
            try:
                show_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
                if show_raw_data.lower() == 'yes':
                    print(df.iloc[first_index:second_index, :])
                    first_index = second_index
                    second_index = second_index + increment
                    continue
                else:
                    break
            except ValueError:
                print('Please enter a valid option.\n')
                continue
            else:
                break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
