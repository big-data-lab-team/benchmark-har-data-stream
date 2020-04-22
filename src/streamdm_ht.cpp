#include "src/learners/Classifiers/Trees/HoeffdingAdaptiveTree.h"
#include "src/learners/Classifiers/Trees/HoeffdingTree.h"
#include <src/core/Attribute.h>
#include <src/core/DenseInstance.h>
#include <src/core/InstanceInformation.h>

template<class feature_type, int label_count, int feature_count>
class HoeffdingTreeClassifier{
	HT::HoeffdingTree* ht = nullptr;
	InstanceInformation* ii = nullptr;

	public:
	HoeffdingTreeClassifier(bool const adaptive, double const confidence, int const grace_period){
		if(adaptive)
			ht = new HT::HoeffdingAdaptiveTree();
		else
			ht = new HT::HoeffdingTree();
		ht->params.gracePeriod = grace_period;
		ht->params.splitConfidence = confidence;
		ht->params.leafPrediction = 2;
		ii = new InstanceInformation();
		for(int i = 0; i < feature_count; ++i)
			ii->addAttribute(new Attribute(), i);
		vector<string> vec(label_count);
		for(int i = 0; i < label_count; ++i){
			vec[i] = to_string(i);
		}
		ii->addClass(new Attribute(vec), 0);

	}
	inline bool train(feature_type const* features, int const label){
		vector<feature_type> values(features, features+feature_count);
		vector<double> labels(1, static_cast<double>(label));
		Instance* instance = new DenseInstance();
		instance->setInstanceInformation(ii);
		instance->addLabels(labels);
		instance->addValues(values);
		ht->train(*instance);

		delete instance;
		return true;
	}
	inline int predict(feature_type const* features){
		vector<feature_type> values(features, features+feature_count);
		Instance* instance = new DenseInstance();
		instance->setInstanceInformation(ii);
		instance->addValues(values);
		double* predictions = ht->getPrediction(*instance);
		int hightest = 0;
		for(int i = 0; i < label_count; ++i)
			if(predictions[i] > predictions[hightest])
				hightest = i;
		delete instance;
		return hightest;
	}
};
HoeffdingTreeClassifier<double, LABEL_COUNT, FEATURES_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	if(argc < 3){
		cout << "usage: <adaptive> <split confidence> <grace period>" << endl;
		return nullptr;
	}
	int const adaptive = stod(argv[0]);	
	double const confidence = stod(argv[1]);	
	int const grace_period = stod(argv[2]);	
	return new HoeffdingTreeClassifier<double, LABEL_COUNT, FEATURES_COUNT>(adaptive == 1, confidence, grace_period);
}

