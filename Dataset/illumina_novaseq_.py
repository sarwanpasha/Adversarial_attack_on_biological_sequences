from Bio import SeqIO
from Bio.Seq import Seq
import os

i=1
for seq_record in SeqIO.parse("gisaid_hcov-19.fasta","fasta"):
	my_seq = seq_record.seq
	my_id = seq_record.id
	
	seq = ">"+"seq_"+str(i)+"\n"+my_seq
	seq_ = "seq_"+str(i)+".fasta"
	f = open(seq_,"w")
	f.write(str(seq))

	cmd = 'iss generate --genomes seq_'+str(i)+'.fasta -n 5000 --model novaseq --output seq_'+str(i)
	os.system(cmd)

	cmd1 = 'bowtie2 -x /alina-data1/Bikram/statitics/Raw_data_20200801/Preprocessed/Bowtie2/NC_0455122/NC_0455122_covid19 -1 seq_'+str(i)+'_R1.fastq -2 seq_'+str(i)+'_R2.fastq | samtools view -bS | samtools sort -o aln_'+str(i)+'.bam'
	os.system(cmd1)

	cmd2 = 'samtools index aln_'+str(i)+'.bam'
	os.system(cmd2)

	cmd3 = 'rm seq_'+str(i)+'_R1.fastq'
	os.system(cmd3)

	cmd4 = 'rm seq_'+str(i)+'_R2.fastq' 
	os.system(cmd4)

	cmd7 = 'bcftools mpileup -Ou -f /alina-data2/Bikram/GISAID/NC_0455122.fa aln_'+str(i)+'.bam | bcftools call -Ou -mv | bcftools norm -f /alina-data2/Bikram/GISAID/NC_0455122.fa -Oz -o output_'+str(i)+'.vcf.gz'
	os.system(cmd7)

	cmd8 = 'rm aln_'+str(i)+'.bam'
	os.system(cmd8)


	cmd9 = 'tabix output_'+str(i)+'.vcf.gz'
	os.system(cmd9)

	cmd10 = 'bcftools consensus -f /alina-data2/Bikram/GISAID/NC_0455122.fa output_'+str(i)+'.vcf.gz > out_'+str(i)+'.fa'
	os.system(cmd10)

	cmd11 = 'rm output_'+str(i)+'.vcf.gz'
	os.system(cmd11)

	cmd12 = 'cat out_'+str(i)+'.fa >> illumina_5000_novaseq_simulated_error.fasta'
	os.system(cmd12)

	cmd13 = 'rm out_'+str(i)+'.fa'
	os.system(cmd13)

	cmd14 = 'rm output_'+str(i)+'.vcf.gz.tbi'
	os.system(cmd14)

	cmd15 = 'rm seq_'+str(i)+'.fasta'
	os.system(cmd15)

	cmd16 = 'rm aln_'+str(i)+'.bam.bai'
	os.system(cmd16)

	cmd17 = 'rm seq_'+str(i)+'_abundance.txt'
	os.system(cmd17)
	i = i+1
