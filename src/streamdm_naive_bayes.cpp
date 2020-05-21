#include "src/learners/Learner.h"
#include "src/learners/Classifiers/Bayes/Naivebayes.h"
#include <src/core/Attribute.h>
#include <src/core/DenseInstance.h>
#include <src/core/InstanceInformation.h>

template<class feature_type, int label_count, int feature_count>
class NaiveBayesClassifier{
	Learner* learner = nullptr;
	InstanceInformation* ii = nullptr;
	Instance* instance = nullptr;
	vector<double> labels, values;
	public:
	NaiveBayesClassifier(): labels(1), values(feature_count){
		learner = new NaiveBayes();
		ii = new InstanceInformation();
		for(int i = 0; i < feature_count; ++i)
			ii->addAttribute(new Attribute(), i);
		vector<string> vec(label_count);
		for(int i = 0; i < label_count; ++i){
			vec[i] = to_string(i);
		}
		ii->addClass(new Attribute(vec), 0);
		instance = new DenseInstance();
		instance->setInstanceInformation(ii);
	}
	inline bool train(feature_type const* features, int const label){
		for(int i = 0; i < feature_count; ++i)
			values[i] = features[i];
		labels[0] = label;
		instance->addLabels(labels);
		instance->addValues(values);
		learner->train(*instance);
		return true;
	}
	inline int predict(feature_type const* features){
		for(int i = 0; i < feature_count; ++i)
			values[i] = features[i];
		instance->addValues(values);
		double* predictions = learner->getPrediction(*instance);
		int hightest = 0;
		for(int i = 0; i < label_count; ++i)
			if(predictions[i] > predictions[hightest])
				hightest = i;
		delete predictions;
		return hightest;
	}
	~NaiveBayesClassifier(){
		delete learner;
		delete ii;
		delete instance;
	}
};
NaiveBayesClassifier<double, LABEL_COUNT, FEATURES_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	return new NaiveBayesClassifier<double, LABEL_COUNT, FEATURES_COUNT>();
}


