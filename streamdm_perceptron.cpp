#include "src/learners/Classifiers/Functions/Perceptron.h"
#include <src/core/Attribute.h>
#include <src/core/DenseInstance.h>
#include <src/core/InstanceInformation.h>

template<class feature_type, int label_count, int feature_count>
class PerceptronClassifier{
	Perceptron* perceptron = nullptr;
	InstanceInformation* ii = nullptr;

	public:
	PerceptronClassifier(){
		perceptron = new Perceptron();
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
		perceptron->train(*instance);
		return true;
	}
	inline int predict(feature_type const* features){
		vector<feature_type> values(features, features+feature_count);
		Instance* instance = new DenseInstance();
		instance->setInstanceInformation(ii);
		instance->addValues(values);
		double* predictions = perceptron->getPrediction(*instance);
		int hightest = 0;
		for(int i = 0; i < label_count; ++i)
			if(predictions[i] > predictions[hightest])
				hightest = i;
		return hightest;
	}
};
PerceptronClassifier<double, LABEL_COUNT, FEATURES_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	return new PerceptronClassifier<double, LABEL_COUNT, FEATURES_COUNT>();
}


