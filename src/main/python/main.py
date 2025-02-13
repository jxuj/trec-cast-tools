import argparse
from hashlib import md5
from pathlib import Path
import multiprocessing
#import shutil

from generators import WaPoGenerator, KILTGenerator, MARCOGenerator
from passage_chunkers import PassageChunker
from utils import write_to_jsonlines, write_to_trecweb, write_md5_hashes

parser = argparse.ArgumentParser(
    description='Collection Processing Parameters')

# KILT collection path
parser.add_argument(
    '--kilt_collection',
    type=str,
    # if collection dowloaded with bash script
    default="/exports/eddie/scratch/s1717425/files/raw_collection/kilt_knowledgesource.json",
    help="Path to the raw KILT collection"
)

# MARCO collection path
parser.add_argument(
    '--marco_v2_collection',
    type=str,
    default="/exports/eddie/scratch/s1717425/files/raw_collection/msmarco_v2_doc.tar",
    help="Path to compressed MARCO V2 collection"
)

# WaPo collection path
parser.add_argument(
    '--wapo_collection',
    type=str,
    default="/exports/eddie/scratch/s1717425/files/raw_collection/WashingtonPost.v4.tar.gz",
    help="Path to compressed WaPo collection"
)

# Duplicates file path
parser.add_argument(
    '--duplicates_file',
    type=str,
    default="/exports/eddie/scratch/s1717425/files/duplicates_file/all_duplicates.txt",
    help="Path to duplicates file"
)

parser.add_argument('--batch_size', type=int, default=10000,
                    help="Number of documents per batch")
parser.add_argument('--skip_process_kilt', default=True, action='store_true')
parser.add_argument('--skip_process_marco', default=True, action='store_true')
parser.add_argument('--skip_process_wapo', default=False, action='store_true')
parser.add_argument('--output_dir', type=str, default="/exports/eddie/scratch/s1717425/files",
                    help="Directory to write files to")
parser.add_argument('--output_type', type=str, default="jsonlines",
                    help="Output file type: trecweb or jsonlines")


if __name__ == '__main__':

    args = parser.parse_args()
    passage_chunker = PassageChunker()
    output_path = f"{args.output_dir}/{args.output_type}"
    md5_dir_path = f"{args.output_dir}/md5_hashes"
    Path(output_path).mkdir(parents=True, exist_ok=True)
    Path(md5_dir_path).mkdir(parents=True, exist_ok=True)

    if not args.skip_process_kilt:
        print("--- Processing KILT ---")

        kilt_generator: KILTGenerator = KILTGenerator(
            args.kilt_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        with multiprocessing.Pool() as pool:
            for batch_id, document_batch in enumerate(pool.imap_unordered(passage_chunker.process_batch, kilt_generator)):

                print(
                    f"--- Passages generated for KILT documents in batch number {batch_id} ---")
                write_md5_hashes(
                    f"{md5_dir_path}/KILT_md5hashes_{batch_id}.csv", document_batch)
                if args.output_type == 'jsonlines':
                    write_to_jsonlines(
                        f"{output_path}/KILT_{batch_id}.jsonl", document_batch)
                elif args.output_type == 'trecweb':
                    write_to_trecweb(
                        f"{output_path}/KILT_{batch_id}.trecweb", document_batch)
                else:
                    raise ValueError(
                        "--output type must be 'jsonlines' or 'trecweb'")
                print(
                    f"--- Done processing KILT documents in batch number {batch_id} ---")

    if not args.skip_process_marco:
        print("Processing MARCO")

        marco_generator: MARCOGenerator = MARCOGenerator(
            args.marco_v2_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        with multiprocessing.Pool() as pool:
            for batch_id, document_batch in enumerate(pool.imap_unordered(passage_chunker.process_batch, marco_generator)):

                print(
                    f"--- Passages generated for MARCO documents in batch number {batch_id} ---")
                write_md5_hashes(
                    f"{md5_dir_path}/MARCO_md5hashes_{batch_id}.csv", document_batch)
                if args.output_type == 'jsonlines':
                    write_to_jsonlines(
                        f"{output_path}/MARCO_{batch_id}.jsonl", document_batch)
                elif args.output_type == 'trecweb':
                    write_to_trecweb(
                        f"{output_path}/MARCO_{batch_id}.trecweb", document_batch)
                else:
                    raise ValueError(
                        "--output type must be 'jsonlines' or 'trecweb'")
                print(
                    f"--- Done processing MARCO documents in batch number {batch_id} ---")
                #shutil.copy(f"{output_path}/MARCO_{batch_id}.jsonl", "/content/drive/MyDrive/UoE/Data/MARCO")

    if not args.skip_process_wapo:
        print("Processing WaPo")

        wapo_generator: WaPoGenerator = WaPoGenerator(
            args.wapo_collection, args.duplicates_file, args.batch_size
        ).generate_documents()

        with multiprocessing.Pool() as pool:
            for batch_id, document_batch in enumerate(pool.imap_unordered(passage_chunker.process_batch, wapo_generator)):

                print(
                    f"--- Passages generated for WaPo documents in batch number {batch_id} ---")
                write_md5_hashes(
                    f"{md5_dir_path}/WaPo_md5hashes_{batch_id}.csv", document_batch)
                if args.output_type == 'jsonlines':
                    write_to_jsonlines(
                        f"{output_path}/WaPo_{batch_id}.jsonl", document_batch)
                elif args.output_type == 'trecweb':
                    write_to_trecweb(
                        f"{output_path}/WaPo_{batch_id}.trecweb", document_batch)
                else:
                    raise ValueError(
                        "--output type must be 'jsonlines' or 'trecweb'")
                print(
                    f"--- Done processing WaPo documents in batch number {batch_id} ---")
