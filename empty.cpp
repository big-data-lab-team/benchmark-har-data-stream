template<class feature_type>
class EmptyClassifier{
	public:
		EmptyClassifier(){
		}
	inline bool train(feature_type const* features, int const label){
		return true;
	}
	inline int predict(feature_type const* features){
		return 0;
	}
};
EmptyClassifier<double>* get_classifier(int argc, char** argv){
	cout << "EmptyClassifier is instanciated." << endl;
	return new EmptyClassifier<double>();
}
