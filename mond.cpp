#include <mondrian.hpp>


MondrianForest<double, functions, TREE_COUNT, LABEL_COUNT, FEATURES_COUNT, 60000>* get_classifier(int argc, char** argv){
	if(argc < 3){
		cout << "usage: <lifetime> <base_measure> <discount_factor>" << endl;
		return nullptr;
	}
	double const lifetime = stod(argv[0]);	
	double const base_measure = stod(argv[1]);	
	double const discount_factor = stod(argv[2]);	

	cout << "Lifetime: " << lifetime << " Base measure: " << base_measure << " Discount factor: " << discount_factor << " Tree count: " << TREE_COUNT << endl;
	return new MondrianForest<double, functions, TREE_COUNT, LABEL_COUNT, FEATURES_COUNT, 60000>(lifetime, base_measure, discount_factor);
}

