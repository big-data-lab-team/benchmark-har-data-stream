#include <naive_bayes.hpp>


NaiveBayes<double, LABEL_COUNT, FEATURES_COUNT, functions>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	return new NaiveBayes<double, LABEL_COUNT, FEATURES_COUNT, functions>();
}


