
for ngram in 8 16 32 64 128 256 512 1024
do
java -Xmx10G -cp target/AutoYara-1.0-SNAPSHOT.jar edu.lps.acs.ml.autoyara.Bytes2Bloom -i "$1" -n $ngram -o "$2" -k $ngram -pl
done