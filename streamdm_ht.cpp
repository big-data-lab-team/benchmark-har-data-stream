#include "src/learners/Classifiers/Trees/HoeffdingTree.h"
#include <src/core/Attribute.h>
#include <src/core/DenseInstance.h>
#include <src/core/InstanceInformation.h>

template<class feature_type, int label_count, int feature_count>
class HoeffdingTreeClassifier{
	HT::HoeffdingTree* ht = nullptr;
	InstanceInformation* ii = nullptr;

	public:
	HoeffdingTreeClassifier(double const confidence, int const grace_period){
		ht = new HT::HoeffdingTree();
		ht->params.gracePeriod = grace_period;
		ht->params.splitConfidence = confidence;
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
		vector<feature_type> values(features, features+FEATURES_COUNT);
		vector<double> labels(1, label);
		Instance* instance = new DenseInstance();
		instance->setInstanceInformation(ii);
		instance->addLabels(labels);
		instance->addValues(values);
		ht->train(*instance);

		return true;
	}
	inline int predict(feature_type const* features){
		vector<feature_type> values(features, features+FEATURES_COUNT);
		Instance* instance = new DenseInstance();
		instance->setInstanceInformation(ii);
		instance->addValues(values);
		double* predictions = ht->getPrediction(*instance);
		int hightest = 0;
		for(int i = 0; i < label_count; ++i)
			if(predictions[i] > predictions[hightest])
				hightest = i;
		return hightest;
	}
};
HoeffdingTreeClassifier<double, LABEL_COUNT, FEATURES_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	if(argc < 2){
		cout << "usage: <split confidence> <grace period>" << endl;
		return nullptr;
	}
	double const confidence = stod(argv[0]);	
	int const grace_period = stod(argv[1]);	
	return new HoeffdingTreeClassifier<double, LABEL_COUNT, FEATURES_COUNT>(confidence, grace_period);
}

