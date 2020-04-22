template<class feature_type, int first_prediction=0>
class PreviousClassifier{
	int previous = first_prediction;
	public:
		PreviousClassifier(){
		}
	inline bool train(feature_type const* features, int const label){
		previous = label;
		return true;
	}
	inline int predict(feature_type const* features){
		return previous;
	}
};
PreviousClassifier<double>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	return new PreviousClassifier<double>();
}

