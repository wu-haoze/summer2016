i=1
while [ $i -lt 101 ]
do
python python/format_test.py testFeatures2/test2_ksat-$i.txt $i
i=$((i+1))
done