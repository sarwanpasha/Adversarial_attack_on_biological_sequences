from Bio import SeqIO
from Bio.Seq import Seq
import os

i=1
for seq_record in SeqIO.parse("gisaid_hcov-19.fasta","fasta"):
	my_seq = seq_record.seq
	my_id = seq_record.id
	
	seq = ">"+my_id+"\n"+my_seq
	seq_ = "seq_"+str(i)+".fasta"
	f = open(seq_,"w")
	f.write(str(seq))

	cmd = 'pbsim --data-type CLR --depth 5 --model_qc /alina-data2/Bikram/GISAID/data/PBSIM-PacBio-Simulator-master/data/model_qc_clr seq_'+str(i)+'.fasta'
	os.system(cmd)

	cmd1 = 'mv sd_0001.fastq sd_'+str(i)+'.fastq'
	os.system(cmd1)

	cmd2 = 'rm seq_'+str(i)+'.fasta'
	os.system(cmd2)

	cmd3 = './minimap2-2.24_x64-linux/minimap2 -a /alina-data2/Bikram/GISAID/NC_0455122.fa sd_'+str(i)+'.fastq'+'>'+'aln_'+str(i)+'.sam'
	os.system(cmd3)

	cmd4 = 'rm sd_'+str(i)+'.fastq' 
	os.system(cmd4)

	cmd5 = 'samtools view -bS aln_'+str(i)+'.sam > aln_'+str(i)+'.bam'
	os.system(cmd5)

	cmd6 = 'rm aln_'+str(i)+'.sam'
	os.system(cmd6)

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

	cmd12 = 'cat out_'+str(i)+'.fa >> pacbio_depth_5_simulated_error.fasta'
	os.system(cmd12)

	cmd13 = 'rm out_'+str(i)+'.fa'
	os.system(cmd13)

	cmd14 = 'rm output_'+str(i)+'.vcf.gz.tbi'
	os.system(cmd14)

		
			
	i = i+1
