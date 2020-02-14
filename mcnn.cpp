#include <mc_nn.hpp>


MCNN<double, FEATURES_COUNT, MAX_CLUSTERS, ERROR_THRESHOLD, PERFORMANCE_THRESHOLD> * get_classifier(int seed, int argc, char** argv){
	srand(seed);
		
	return new MCNN<double, FEATURES_COUNT, MAX_CLUSTERS, ERROR_THRESHOLD, PERFORMANCE_THRESHOLD>();
}

