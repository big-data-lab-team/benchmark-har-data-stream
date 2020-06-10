#include <mondrian.hpp>


MondrianForest<double, functions, TREE_COUNT, FEATURES_COUNT, LABEL_COUNT, SIZE>* get_classifier(int seed, int argc, char** argv){
	if(argc < 3){
		cout << "usage: <lifetime> <base_measure> <discount_factor>" << endl;
		return nullptr;
	}
	double const lifetime = stod(argv[0]);	
	double const base_measure = stod(argv[1]);	
	double const discount_factor = stod(argv[2]);	

	srand(seed);
	return new MondrianForest<double, functions, TREE_COUNT, FEATURES_COUNT, LABEL_COUNT, SIZE>(lifetime, base_measure, discount_factor);
}

