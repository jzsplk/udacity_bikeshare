import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    citys = ['chicago', 'new york city', 'washington']
    city = input('Enter the city: ').lower()
    while (city not in citys):
      print('city not supported, we have data for chicago, new york city and washington')
      city = input('Enter the city: ').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = input('Enter the month: january, february, march, april, may, june. all for all the months : ').lower()
    while (month not in months):
      print('please input valid month name: january, february, march, april, may, june. ')
      month = input('Enter the month: ').lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weeks = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = input('Enter the day of week: all for no filter: ').lower()
    while (day not in weeks):
      print('please input valid day of week')
      day = input('Enter the day of week: ').lower() 

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
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # print(df.head())
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
    # print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = df['month'].mode()[0]
    print('The most common month is : {}'.format(months[month - 1]))

    # TO DO: display the most common day of week
    week = df['day_of_week'].mode()[0]
    print('The most common day of week is : {}'.format(week))
    # TO DO: display the most common start hour
    hour = df['hour'].mode()[0]
    print('The most common start hour is : {}:00'.format(hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station ==> {}'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('Most commonly used end station ==> {}'.format(end_station))

    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start and end trip: ')
    print(df.groupby(['Start Station', 'End Station']).size().nlargest(1))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time: ')
    # print(df['Trip Duration'].sum())
    total_trip = df['Trip Duration'].sum()
    days = int(total_trip / (24*60*60))
    seconds = total_trip % (24*60*60)
    print('{0} days {1} seconds'.format(days, seconds))

    # TO DO: display mean travel time
    mean_trip = df['Trip Duration'].mean()
    # print(df['Trip Duration'].mean())
    print('Mean travel time: ')
    print(time.strftime("%H:%M:%S", time.gmtime(mean_trip)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User types: ')
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
      print('counts of gender')
      print(df['Gender'].value_counts())
    except:
      print('no Gender data for this city')
    # TO DO: Display earliest, most recent, and most common year of birth
    try:
      print('earliest birth year: ')
      print(df['Birth Year'].min())

      print('most recent year of birth: ')
      print(df['Birth Year'].max())

      print('most common year: ')
      print(df.groupby('Birth Year')['Birth Year'].size().nlargest(1))
    except:
      print('no birth data for this city!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
