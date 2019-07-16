import time
import datetime
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def parser(input_value, valid_values, indices=2, str_to_ind=False):
    
    """
    Parses the input_value and matches inside the valid_values
    input_value => Taken from outside
    valid_values => List of possible valid values
    indices => How many indexes to verify of input_value to valid_values
    """
    try:
        
        
        # If valid values is not a list, you dont need
        # this parser.
        if type(valid_values) is not list:
            raise Exception
        
        # Converting the first character to uppercase and everything else to lower, so that we 
        # can have a common interface, regardless of values.
        valid_values = [value.title() for value in valid_values]
        input_value = str(input_value).title()
        
        if input_value == 'All' or input_value == '*':
                input_value = 'ALL'
                return input_value
            
        """
        The core of the function. Performs two checks:
        1) When the given input is a number, check if the corresponding index exists
            in the valid list. Or
        2) If the input is a string, check its first two indices. Indices are dynamic. 
            Specify how many indices to check while calling this function.
        This type of loop is called list comprehension.
        
        Return => list 
        
        """
        input_value = [x for i, x in enumerate(valid_values) if ( str(i + 1) == input_value ) or
                           x[:indices] == input_value[:indices] ]
        
        #print(input_value)
        # If we got an input, pop it out of list
        if input_value:
            input_value = input_value.pop()
           
            if str_to_ind:
                input_value = int(valid_values.index(input_value)) + 1
       # print(input_value)    
        
        return input_value
    except Exception as e:
        print(e)

def newlines(num=2):
    """  
    Need some spacing in between? print any number
    of newlines
    num => No of newlines. Default = 2
    """
    i = 0
    while i < num:
        print()
        i=i+1

    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    

    print('-'*50)
    newlines(2)
    cities = ['chicago', 'new york city', 'washington']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    
    
    while(True):
        print('Format: [ c|ch|chicago, n|ne|new york|, w|wa|washington ]')
        city=input("Choose any city: ")
        city = parser(city, cities, indices=1)
        if city:
            break;
        else:
            print("The flight ain't going that way..savvy!!");
            newlines()
    
    newlines(3)
    
    while(True):             
 
        print('Format: [ All|*, Jan|1, Feb|2, ...., Jun|6 ]')
        month=input("Enter the month: ")
        # Bug when 2 indices are used, march and may....
        month = parser(month, months, indices=3, str_to_ind=True)
       
        if month:
            break
        else:
            print("Invalid Input!")
            newlines()
            
    newlines(3)
        
    while(True):
    
        print('Format: [All|*, mo|Mo|monday|1, ... su|Su|Sunday|7 ]')
        day=input("Enter the day: ")
        day = parser(day, days)
        if day:
            break
        else:
             print('Invalid Input')
             newlines()
    
    newlines(3)
    print('-'*40)
    # DEBUG
    print("City: %s  Month: %s (%s) Day: %s" % (city, month, months[month - 1] if str(month).isdigit() else "*", day))
    print('-'*40)
    print("Thinking ->->->->->->->->")
    newlines(3)
    return city, month, day



def filter_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    dateparser = lambda date: pd.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # Dynamically reading csv
    df = pd.read_csv(CITY_DATA[city.lower()], parse_dates=['Start Time'], date_parser=dateparser)
    df1= df
    df['year'] = df['Start Time'].dt.year
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    
   
    if month == 'ALL' or day == 'ALL':
        if month == 'ALL' and day == 'ALL':
            new_df = df
        elif month == 'ALL':
            new_df = df.loc[(df['day'] == day), : ]
        elif day == 'ALL':
            new_df = df.loc[(df['month'] == month), : ]
    else:
        new_df = df.loc[(df['month'] == month) & (df['day'] == day), : ]
    # DEBUG
    
    
    return new_df,df1

   
    

def time_stats(df,df1):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df1['month'] = df1['Start Time'].dt.month
    df1['day'] = df1['Start Time'].dt.weekday_name
    df1['hour'] = df1['Start Time'].dt.hour
   
    
    
    common_month=df1['month'].mode()[0]
    print('\nCalculating The Most common month...\n',common_month)
    newlines(1)

   
    common_week=df1['day'].mode()[0]
    print('\nCalculating The Most common week...\n',common_week)
    newlines(1)


   
    common_hour=df1['hour'].mode()[0]
    print('\nCalculating The Most common hour...\n',common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    newlines(2)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

  
    popular_start_station=df['Start Station'].mode()[0]
    print("The most commonly used start station is:",popular_start_station)
    newlines(1)

   
    popular_end_station=df['End Station'].mode()[0]
    print("The most commonly used end station is:",popular_end_station)
    newlines(1)


    
    counts = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print("The most frequent combination of start station and end station trip is:",counts.index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    newlines(2)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

  
    print("Trip Duration:",df['Trip Duration'].sum(),'sec')
    newlines(1)


    print("Mean Travel Time:",df['Trip Duration'].mean(),'sec')
    newlines(1)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    newlines(2)


def user_stats(df,df1):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    

    user_types=df['User Type'].value_counts()
    print("No of user types:\n",user_types)
    newlines(1)

    
    column_list=np.array([df.columns])
   
    if 'Gender' not in column_list:
        print("Gender: Oops!!Sorry...No data found")
    else:
        gender_types=df['Gender'].value_counts()
        print("No of males and females:\n",gender_types)                                                                                                                            
    newlines(1)                                                                                      

   
    if 'Birth Year' not in column_list:
        print("Birth Year:Oops!!Sorry...No data found")
    else:
        print("Most common earliest year of birth is:",df['Birth Year'].min())
        newlines(1)
        print("Most common recent year of birth is:",df['Birth Year'].max())
        newlines(1)
        print("Most common year of birth is:",df['Birth Year'].mode()[0])
     


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    print("Done!!!")
    newlines(2)
    i=0
    j=5
    where = 1
    while(True):
        if where > 5:
            data = input("Continue [y/n]: ")
        else:    
            data=input("\nWould you like to see individual trip data? Enter yes or no [y/n]: ")
        
        if data.lower()[:1]=='y':     
            print(df.iloc[i:j,0:])
            i=i+5
            j=j+5
            where = where + 5
        else:
           break
        

def main():
    while True:
        city, month, day = get_filters()
        df,df1 = filter_data(city, month, day)

        time_stats(df,df1)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,df1)


        restart = input('\nWould you like to restart? Enter yes or no [y/n] .\n')
        if restart.lower()[:1] != 'y':
            break

if __name__ == "__main__":
    main()
