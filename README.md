# artist_classifier

All data is stored in lyrics directory.
Inside of the src directory, billboard_classifier.py and util.py are stored which contain the functions for the classifiers.
The directory, scripts, contains code used to getting lyrics, themes, and removing duplicates.

To Run do following command in src directory: `python3 billboard_classifier.py`. Accuracy, recall, and precision are printed at the end of the log.

Optional flags:
1. `--c`: Types of classifiers ['regular', 'svm', 'bayes', 'logistic'] (defaults to regular) (regular refers to hinge loss)
2. `--i`: Number of iterations (defaults to 50)
3. `--e`: Eta value (defaults to .01)
4. `--d`: Dataset to use ['dataset_1', 'dataset_2'] (defaults to dataset_1)


