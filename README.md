# artist_classifier

This project's main objective is to predict whether a rap song will make the Billboard Hot Rap Songs chart using only the songs lyrics. We first found thousands of rap song titles that both made the Billboard Hot Rap Songs chart and that didn't. We then scraped those songs lyrics from songlyrics.com. We then created a test set, validation set, and training set for the lyrics. Finally, we trained a support vector machine model, a naive bayes model, and a logistical regression model using the lyrics and features which we thought were important. The naive bayes model gave us the best results with accuracy of 70% of prediction whether a rap song made it to the Billboard Hot Rap Songs chart.

All data is stored in lyrics directory.
Inside of the src directory, billboard_classifier.py and util.py are stored which contain the functions for the classifiers.
The directory, scripts, contains code used to getting lyrics, themes, and removing duplicates.

To Run do following command in src directory: `python3 billboard_classifier.py`. Accuracy, recall, and precision are printed at the end of the log.

Optional flags:
1. `--c`: Types of classifiers ['regular', 'svm', 'bayes', 'logistic'] (defaults to regular) (regular refers to hinge loss)
2. `--i`: Number of iterations (defaults to 50)
3. `--e`: Eta value (defaults to .01)
4. `--d`: Dataset to use ['dataset_1', 'dataset_2'] (defaults to dataset_1)


