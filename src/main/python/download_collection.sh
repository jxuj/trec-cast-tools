echo "Creating collection and duplicates directory..."
#mkdir -p /exports/eddie/scratch/s1717425/files/raw_collection
#mkdir -p files/duplicates_file

echo "Begin downloading raw collections.."

#echo "Downloading WaPo...," 
#echo "Enter the password (if you don't have it, please visit https://trec.nist.gov/data/wapost/)"
#wget -c --user TRECWaPoSt --ask-password https://ir.nist.gov/wapo/WashingtonPost.v4.tar.gz -P files/raw_collection

echo "Downloading KILT..."
wget -c http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json -P /exports/eddie/scratch/s1717425/files/raw_collection

#echo "Downloading MARCO V2..."
#wget --header "X-Ms-Version: 2019-12-12" https://msmarco.blob.core.windows.net/msmarcoranking/msmarco_v2_doc.tar -P /exports/eddie/scratch/s1717425/files/raw_collection

#echo "Downloading duplicates file..."
#wget -c https://raw.githubusercontent.com/daltonj/treccastweb/master/2022/duplicate_files/all_duplicates.txt -P /exports/eddie/scratch/s1717425/files/duplicates_file

echo "Collection Downloaded"