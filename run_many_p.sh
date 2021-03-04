for ((i = 52; i > 13; i=i-4))
do
	sbatch global_script.sh $i;
done
