#include <mc_nn.hpp>


MCNN<double, FEATURES_COUNT, MAX_CLUSTERS> * get_classifier(int seed, int argc, char** argv){
	if(argc < 3){
		cout << "usage: <error_thr> <cleaning_method> <performance_thr>" << endl;
		return nullptr;
	}
	unsigned int const error_thr = stoi(argv[0]);	
	unsigned int const cleaning_method = stoi(argv[1]);	
	double const performance_thr = stod(argv[2]);	

	srand(seed);
	return new MCNN<double, FEATURES_COUNT, MAX_CLUSTERS>(error_thr, cleaning_method, performance_thr);
}

