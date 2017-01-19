package root.nrc_workspace.src;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.List;


public class FastaReader {
	
	public FastaReader() {
		
	}
	
	
	
	public void createBPSEQFiles(File pathFile, String estensione) {

		File listFile[] = pathFile.listFiles();
		if (listFile != null) {
			for (int i = 0; i < listFile.length; i++) {
				if (listFile[i].getName().endsWith(estensione)) {
					System.out.println("Predicting fasta file: "+ listFile[i]);
					String output = new IpknotPrediction().getipknotOutput( listFile[i]);
					//System.out.println(output);
					String outputName= listFile[i].getAbsolutePath().split("[.]")[0];
					outputName= outputName.concat(".bpseq");
					PrintWriter out=null;
					try {
						out = new PrintWriter(outputName);
					} 
					catch (FileNotFoundException e) {e.printStackTrace();}
					out.print(output);	
					out.close();
				}
			}
		}
	}
	
	
	
	public static void main(String[] args) {
		String path=args[0];
		File myDir= new File(path);
		//File myDir= new File("/home/giacalone/ncRNA/dataset_test");
		FastaReader myFiles= new FastaReader();
		myFiles.createBPSEQFiles(myDir, "fa");
		
	}
	
	
}
