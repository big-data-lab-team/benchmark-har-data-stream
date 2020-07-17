#include <perceptron.hpp>
#include <cmath>

template<class feature_type, int label_count, int feature_count, int layer_count>
class MLPClassifier{
	MultiLayerPerceptron<layer_count, 600000, functions>* mlp = nullptr;
	int last_layer_size;
	int total_weight_count;
	double min_err = 1000;
	int counter = 0;
	public:
	MLPClassifier(int* layer_size, string weight_file, double learning_rate=0.1){
		mlp = new MultiLayerPerceptron<layer_count, 600000, functions>(layer_size, learning_rate);
		last_layer_size = layer_size[layer_count-1];
		total_weight_count = 0;
		for(int i = 1; i < layer_count; ++i)
			total_weight_count += layer_size[i]*(layer_size[i-1]+1); //+1 for the bias
		if(weight_file != ""){
			read_weights(weight_file);
		}
	}
	inline bool train(feature_type const* features, int const label){
		double output[last_layer_size];
		mlp->feed_forward(features, output);
		double real_output[last_layer_size] = {0};
		real_output[label] = 1;
		double err = mlp->backpropagate(real_output);
		if(err < min_err)
			min_err = err;


#ifdef NN_TRAINING
		if(counter%5000 == 0)
			cout << "Error: " << err << " ---- " << min_err << " (" << (min_err > 0.00001) << ") " << 0.00001 << endl;
#endif

		counter += 1;
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
	void write_weights(string const& filename) const{
		double* weights = mlp->get_weights();
		std::fstream fs;
		fs.open (filename, std::fstream::in | std::fstream::out | std::fstream::app);
		for(int i = 0; i < total_weight_count; ++i)
			fs << weights[i] << ",";
		fs.close();
	}
	void read_weights(string const& filename){
		ifstream fs;
		fs.open (filename, std::fstream::in | std::fstream::out | std::fstream::app);
		int i = 0;
		double weights[total_weight_count];
		while(fs){
			string weight_str;
			if(!getline(fs, weight_str, ',')){
				if(i < total_weight_count)
					cout << "Error while loading the weights" << endl;
				break;
			}
			weights[i] = stod(weight_str);
			i++;
		}
		mlp->set_weights(weights);
	}
	double err(void) const{
		return min_err;
	}
	~MLPClassifier(){
		write_weights("weights");
	}
};
MLPClassifier<double, LABEL_COUNT, FEATURES_COUNT, LAYER_COUNT>* get_classifier(int seed, int argc, char** argv){
	srand(seed);
	if(argc < (2+LAYER_COUNT-2)){
		cout << "Need " << (1+LAYER_COUNT-2) << " parameters." << endl;
		cout << "usage: <learning_rate> <weight file>";
		for(int i = 1; i < LAYER_COUNT-1; ++i)
			cout << "<size hidden layer " << i << "> ";
		cout << endl;
		return nullptr;
	}

	double learning_rate = stod(argv[0]);
	string weight_file(argv[1]);
	int layer_size[LAYER_COUNT];
	layer_size[0] = FEATURES_COUNT;
	layer_size[LAYER_COUNT-1] = LABEL_COUNT;
	for(int i = 1; i < LAYER_COUNT-1; ++i){
		cout << argv[i] << endl;
		layer_size[i] = stoi(argv[i+1]);	
	}
	return new MLPClassifier<double, LABEL_COUNT, FEATURES_COUNT, LAYER_COUNT>(layer_size, weight_file, learning_rate);
}

