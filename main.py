import subprocess
from Bio import SeqIO
def create_blast_db(fasta_path, db_name="mouse_db"):
    makeblastdb_cmd = ["makeblastdb", "-in", fasta_path, "-dbtype", "prot", "-out", db_name]
    subprocess.run(makeblastdb_cmd, check=True)
    print(f"Database {db_name} created.")



def run_blast(human_sequences, db_name="mouse_db", output_file="results.txt"):
    with open(output_file, "w") as out_file:
        for human_id, sequence in human_sequences.items():
            print(f"Running BLAST for {human_id}...")
            blastp_cmd = [
                "blastp",
                "-query", "-",
                "-db", db_name,
                "-evalue", "0.001",
                "-outfmt", "6",
                "-max_target_seqs", "1"
            ]
            result = subprocess.run(blastp_cmd, input=sequence, text=True, capture_output=True, check=True)
            out_file.write(f"Human ID: {human_id}\n")
            out_file.write(result.stdout + "\n")
            print(f"Completed BLAST for {human_id}")


mouse_fasta_path = "./mouse.fa"
human_fasta_path = "./human.fa"

create_blast_db(mouse_fasta_path)

human_sequences = {}
with open(human_fasta_path, "r") as handle:
    for record in SeqIO.parse(handle, "fasta"):
        human_sequences[record.id] = str(record.seq)

run_blast(human_sequences)


