# traffic_management_grab
Grab's Traffic Management Challenge: https://www.aiforsea.com/traffic-management.


			README
			------

1. Data & Characteristics:

   + Geohash6:    1329 unique values
   + Days         with range [1..61]
   + Time:
       ++ Hours   with range [0..23]
       ++ Minutes with values [0, 15, 30, 45]
   + Demand:      normalized between [0..1]


   Observations and Assumptions about the Data:

   + This Spatio-Temporal time series very clearly have a distinctive:
     ++ HEAD for geohashes with data-points above the 1000('s),
     ++ a clear TORSO for those geohashes having more than 21 datapoints but less than a 1,000.
     ++ and a TAIL of geohashes with less than 21 datapoints; some with a SINGLE value.

     In such situations the TAIL part of this data would provide some issues but
        in this case the solution is to augment this data with
	++ values from adjacent time intervals,  and
	++ values from adjacent geohash(es),     and
	++ values from the combination of adjacent time intervals & geohashes.

   + Missing values for Demand -- that is, we do not have value for
         ++ each and every 15 minute interval
	    ++ of each and every hour
	       ++ for each 61 days
	          ++ for each geo6

     My assumption is that these MISSING values are ZERO.
     This is a convenient assumption, the data suggests otherwise; that is,
        these are mostly ZEROs but at times the value of Demand is non-zero yet
	still is missing. (Example for this scenario is attached 'IMG_0338_Missing_Data.jpg').

     Clearly Missing: the 3rd Peak in the file 'IMG_0338_Missing_Data.jpg'. The data is an aggregated 20-geo6's
        for 14 days. There must have been some data outage -- that could be the reason the data is missing.
	This, however is not the objective of this Challenge. 
     
     The focus for this execrcise is NOT to fill in missing data -- although
        the same prediction process could also be used for that --
	hence is the assumption that if data is MISSING then it's value is ZERO.

   + Further Assumed that the values of the normalized Demand field behave LINEARLY:
     ++ a LARGER VALUE of the Demand field represents a HIGHER DEMAND,   and
     ++ twice larger value represents twice larger demand, etc.


2. Judging the contest:
   + Code quality: both functional and structural,
   + Feature Engineering,
   + Creativity in problem solving,
   + Model performance:
     ++ Sliding-Window of training set to use a 14 consecutive way of time-window,
     ++ geohash and neighboring/adjacent geohashes,
     ++ RMSE -- to evaluate the performance of the model.


3. Features Aiding the Model:
   Spatio-Temporal problems have been quite a challenge for Neural Networks and
   for traditional Machine Learning. In most cases the Spatial features are assumed
   independent from the Temporal features
      ==> which provides a nice but in-accurate model.
   I have yet to see a model that combinez of Spatial and Temporal features together.

   Features:
   + geohash6
     ++ adjacent geohash6's (libs), especially helpful with similar Demand time series patterns
   + day
     ++ the day itself,    and
     ++ same day a week ago (day -7),   and
     ++ same day two weeks ago (day -14),   and
     ++ the day before (day -1) -- maybe weekend/weekday --
        adjust weight of usage to the similarity of Demand time series characteristics --
	COS similarity works well here.
   + hour (of the day)
     ++ same hour of different days:
        +++ of same geohash6,
	+++ and with a lesser extent      -- of adjacent geohash6,
	+++ and with an even lesser extent -- of any geohash6.
     ++ adjacent hours:
        ++ of same day,
	++ and with a lesser extent -- 7 and 14 days earlier -- of same geo6,
	++ and with yet a lesser extent -- adjacent days -- of same geo6,
	++ and with yet a lesser extent -- 7 and 14 days earlier -- of adjacent geo6's,
	++ and with yet an even lesser extent -- adjacent days -- of adjacent geo6's,
	

4. Data Preparation:
   Data is prepared using a Perl script named 'prepare_data_for_DL_TRAIN.pl' in the data directory.
   This script reads the provided traffic.csv file and prepares it as input for DL_regression.py .
   It prepares 4 files (submitted) for the various stages of the Training process.

   Training is done by 'python DL_regression.py' command.

   Testing then done by:
   + prepare Test data using 'data/prepare_data_for_DL_TEST.pl'
   + load latest model in to DL
   + input the file to 'src/DL_regression_TEST_only.py'


5. Running the model & Tranfer Learning:
   Due to the limited capacity of my Desktop I could not fit the entire dataset
   into my RAM and Swap space of my machine. Transfer Learning came to the rescue.

   The biggest memory hug was the one-hot encoding of the 1329 Geohash codes.
   That was very taxing on my Desktop's memory. 

   As a solution: my Model is trained in pieces utilizing the concept of Transfer Learning:
      trained for the HEAD data first,
      then in 2 segments I trained it for the TORSO and
      then for the TAIL part of the time series data.
      
   Between trainings, the model was comitted to disk, then read back for the next training.


6. Results:
   First and foremost, one more comment about the data before we proceed.
   I tried to separate week days from weekend days based upon the time of demand differences.
   For example,
      + weekend day: peak demand for the day at 2:00 am is more likely to show up on a weekend day,
      + week day: an 8:00 am hour peak is more likely indicate week days.
   I found the exact patterns I was looking for using both the highest and lowest demand hours.
   I also found that these days are not apart by the usual of 6 to 7 days. Granted, there may be holidays.
   But still, the 'weekend' days occured between 4 to 15 days of each other.
   This makes me wonder if 'weekend' days may have been spread around weekdays in the data set by using
   '4 + rand() * (15 -4)'. 

   Although large dataset for a 16Gb home desktop PC, my CNN model performs amazingly
   well even with little training.  It has an impressive RMSE of '0.0078739293461' --
   naturally, this RMSE may vary a little due to the Stochastic nature of the model. 

   It is important to note that adding the RATE-OF-CHANGE to the model did not
   improve accuracy. RATE-OF_CHANGE is defined as

   First Order of Rate of Change -- denoted by '_1':

       RATE-OF-CHANGE_1_15 ( geohash6, day, hour, minute) =
          = Demand( geohash6, day, hour, minute) 
                    - Demand( geohash6, day, hour, minute -15);

       RATE-OF-CHANGE_1_30 ( geohash6, day, hour, minute) =
          = Demand( geohash6, day, hour, minute)
	            - Demand( geohash6, day, hour, minute -30);

       where '_15', and '_30' (and unwritten: '_45', '_60', '_75') are the rate of changes for the predictions of T+1, T+2, T+3, T+4, T+5, respectiively.


    The Second Order of Rate of Change: is the Rate-of-change of the First Order of rate of change:

       RATE-OF-CHANGE_2_15 ( geohash6, day, hour, minute) =
          = RATE-OF-CHANGE_1_15( geohash6, day, hour, minute) 
                    - RATE-OF-CHANGE_1_15( geohash6, day, hour, minute -15);

       Similarly:
       RATE-OF-CHANGE_2_30 ( geohash6, day, hour, minute) =
          = RATE-OF-CHANGE_1_15( geohash6, day, hour, minute) 
                    - RATE-OF-CHANGE_1_15( geohash6, day, hour, minute -30);

   Unfortunately, neither adding the First Order Rate of Change,
   nor adding the Second Order of Rate of Change, or their combination -->
   -->  Did NOT improve the results of Neural Nets.
   Note, these FEATURES may have improved results for traditional ML algorithms.
   

7. Next Step:
   Here I implemented a Deep Learning model for this Spateo-Temporal problem.
   Historically, ARIMA provides good results. It has been around for some time,
      and I assumed Grab has implemented and tested that solution already. 
   

8. Summary:
   This has been a fantastic exercise because it gave me a good opportunity 
      to implement and examine Deep Learning solutions for Spatio-Temporal Data.

Thank you,
Dr. Michael Moricz
