
ARG3=${3:-0.0001}
ARG4=${4:-.}
JAR="$ARG4/target/AutoYara-1.0-SNAPSHOT.jar"
echo $JAR
for ngram in 8 16 32 64 128 256 512 1024
do
echo "java -Xmx10G -cp $JAR edu.lps.acs.ml.autoyara.Bytes2Bloom -i $1 -n $ngram -o $2 -k $ngram -fp $ARG3"
java -Xmx10G -cp $JAR edu.lps.acs.ml.autoyara.Bytes2Bloom -i "$1" -n $ngram -o "$2" -k $ngram -fp $ARG3
done