# Most global file. Modify loops as desired to run the intented 
for ((i = 1; i <= 52; i=i+1)) # Precisions (mantissa length) tested
do
	for ((j = 2; j <= 11; j=j+1)) # Exponent size tested
	do
		sbatch task.sh $i $j;
	done
done
