import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def filters():

    while True:
        print('\nHello! Let\'s explore some US bikeshare data!\n')

        while True:
            city = input('Which city are you interested in analyzing data for? (Chicago, New York City, Washington): ').lower().strip()
            if city in cities:
                break
            else:
                print('This is not a valid city. Please try again.\n')

        while True:
            month = input('Which month are you interested in analyzing data for? (All, January, February, March, April, May, June): ').lower().strip()
            if month in months:
                break
            else:
                print('This is not a valid month. Please try again.\n')

        while True:
            day = input('Which day are you interested in analyzing data for? (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ').lower().strip()
            if day in days:
                break
            else:
                print('This is not a valid day. Please try again.\n')

        print('\nIt seems like you wish to filter Bikeshare data based on the following criteria:')
        print('City: ', city.title())
        print('Month: ', month.title())
        print('Day of week: ', day.title())
        answer = input('Do you wish to continue analyzing Bikeshare data with the above criteria? (yes or no): ').lower().strip()
        if answer == 'yes':
            break

    print('-'*100)
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

    # Load data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    # Extract hour of day from Start Time to create new column.
    df['hour'] = df['Start Time'].dt.hour
    # Filter by month if applicable.
    if month != 'all':
        # Use the index of the months list to get the corresponding int.
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # Filter by month to create the new dataframe.
        df = df.loc[df['month'] == month]
    # Filter by day of week if applicable.
    if day != 'all':
        # Use the index of the days list to get the corresponding int.
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day)
        # Filter by day of week to create the new dataframe.
        df = df.loc[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    print('\nMost common month is: ', months[df['month'].value_counts(dropna = False).idxmax()].title())

    # Display the most common day of week.
    print('\nMost common day of week is: ', days[df['day_of_week'].value_counts(dropna = False).idxmax() + 1].title())

    # Display the most common start hour.
    print('\nMost common hour is: ', df['hour'].value_counts(dropna = False).idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    print('\nMost commonly used start station is: ', df['Start Station'].value_counts(dropna = False).idxmax())

    # Display most commonly used end station.
    print('\nMost commonly used end station is: ', df['End Station'].value_counts(dropna = False).idxmax())


    # Display most frequent combination of start station and end station trip.
    trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print('\nMost frequent combination of start station and end station trip: ', 'From: ', trip[0], 'To: ' , trip[1])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def convert_seconds(seconds):
        # Get min and seconds first.
        mm, ss = divmod(seconds, 60)
        # Get hours.
        hh, mm = divmod(mm, 60)

        return hh, mm, ss

    # Display total travel time.
    print('\nTotal travel time in seconds: ', (df['Trip Duration'].sum()), 'seconds')
    print('\nTotal travel time in hours, minutes & seconds: ', convert_seconds(df['Trip Duration'].sum())[0], 'hours', convert_seconds(df['Trip Duration'].sum())[1], 'minutes', convert_seconds(df['Trip Duration'].sum())[2], 'seconds')

    # Display mean travel time.
    print('\nMean travel time in seconds: ', df['Trip Duration'].mean(), 'seconds')
    print('\nMean travel time in hours, minutes & seconds: ', int(convert_seconds(df['Trip Duration'].mean())[0]), 'hours', int(convert_seconds(df['Trip Duration'].mean())[1]), 'minutes', convert_seconds(df['Trip Duration'].mean())[2], 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    print('\nCounts of User Types: ')
    print(df['User Type'].value_counts(dropna = False))

    # Display counts of gender.
    if 'Gender' in df.columns:
        print('\nCounts of Gender: ')
        print(df['Gender'].value_counts(dropna = False))


    # Display earliest, most recent, and most common year of birth.
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth is: ', int(df['Birth Year'].min()))
        print('\nMost recent year of birth is: ', int(df['Birth Year'].max()))
        print('\nMost common year of birth is: ', int(df['Birth Year'].value_counts().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


# Display raw data upon request.
def display(df):
    answer_1 = 'yes'
    while answer_1 == 'yes':
        answer_1 = input('\nWould you like to see the first 5 lines of raw data based on the filters you provided?. Enter yes or no: ').lower().strip()
        if answer_1.lower() != 'yes':
            break
        else:
            print(df.head())
            print('-'*100)
            answer_2 = input('\nWould you like to see the next 5 lines of raw data based on the filters you provided?. Enter yes or no: ').lower().strip()
            n = 5
            answer_1 = 'no'
            while (answer_2 == 'yes'):
                if answer_2.lower() != 'yes':
                    break
                else:
                    print(df.iloc[n:(n+5)])
                    print('-'*100)
                    n = n + 5
                    if n <= len(df.index):
                        answer_2 = input('\nWould you like to see the next 5 lines of raw data based on the filters you provided?. Enter yes or no: ').lower().strip()
                    else:
                        print('Please note that there are no other data to display.')
                        break


    return df


# The provided code snippet will execute regardless of the circumstances.
def main():
    while True:
        city, month, day = filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower().strip()
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
