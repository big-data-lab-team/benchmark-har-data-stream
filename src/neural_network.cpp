#include <perceptron.hpp>
#include <cmath>

template<class feature_type, int label_count, int feature_count, int layer_count>
class MLPClassifier{
	MultiLayerPerceptron<layer_count, 600000, functions>* mlp = nullptr;
	int last_layer_size;
	public:
	MLPClassifier(int* layer_size, double learning_rate=0.1){
		mlp = new MultiLayerPerceptron<layer_count, 600000, functions>(layer_size, learning_rate);
		last_layer_size = layer_size[layer_count-1];
	}
	inline bool train(feature_type const* features, int const label){
		double output[last_layer_size];
		mlp->feed_forward(features, output);
		double real_output[last_layer_size] = {0};
		real_output[label] = 1;
		mlp->backpropagate(real_output);
		return true;
	}
	inline int predict(feature_type const* features){
		double output[last_layer_size];
		mlp->feed_forward(features, output);

		//From the output find the highest
		int hightest = 0;
		for(int i = 1; i < label_count; ++i)
			if(output[i] > output[hightest])
				hightest = i;
		return hightest;
	}
};
MLPClassifier<double, LABEL_COUNT, FEATURES_COUNT, LAYER_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	if(argc < (1+LAYER_COUNT-2)){
		cout << "Need " << (1+LAYER_COUNT-2) << " parameters." << endl;
		cout << "usage: <learning_rate> ";
		for(int i = 1; i < LAYER_COUNT-1; ++i)
			cout << "<size hidden layer " << i << "> ";
		cout << endl;
		return nullptr;
	}

	double learning_rate = stod(argv[0]);
	int layer_size[LAYER_COUNT];
	layer_size[0] = FEATURES_COUNT;
	layer_size[LAYER_COUNT-1] = LABEL_COUNT;
	for(int i = 1; i < LAYER_COUNT-1; ++i){
		layer_size[i] = stoi(argv[i]);	
	}
	return new MLPClassifier<double, LABEL_COUNT, FEATURES_COUNT, LAYER_COUNT>(layer_size, learning_rate);
}

