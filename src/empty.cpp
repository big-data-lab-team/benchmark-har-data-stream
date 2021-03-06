template<class feature_type, int default_prediction=0>
class EmptyClassifier{
	public:
	inline bool train(feature_type const* features, int const label){
		return true;
	}
	inline void memory_leak(void){
		int const hehe = 1024;
		int* c = new int[hehe];
		for(int i = 0; i < hehe; ++i)
			c[i] = 1;
	}
	inline int predict(feature_type const* features){
		//memory_leak();
		return default_prediction; //1 because 0 is when there is no activity therefore 0 is more dominant
	}
};
EmptyClassifier<double, 0>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	return new EmptyClassifier<double, 0>();
}
