package root.nrc_workspace.src;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;


public class IpknotPrediction {
	

	public IpknotPrediction() {
	}

	/**
	 * @param sequenceFile - fasta sequence file name
	 * 
	 * @return  BPSEQ representation of secondary structure prediction
	 */
	public String getipknotOutput(String sequenceFile){
		Process proc;
		String ipknot= "/workspace/ipknot-0.0.2-x86_64-linux/ipknot";

		String output="";
		try {
			proc = Runtime.getRuntime().exec(ipknot +" "+ sequenceFile + " -b" );

			// Read the output
			BufferedReader reader =  new BufferedReader(new InputStreamReader(proc.getInputStream()));
			StringBuilder sb = new StringBuilder();

			String line = "";
			while((line = reader.readLine()) != null) {
				sb.append(line + System.getProperty("line.separator"));
			}

			output= sb.toString();
			reader.close();

			proc.waitFor();

		} catch (IOException e) {
			e.printStackTrace();
			System.err.println(e); 
		} catch (InterruptedException e) { 
			e.printStackTrace();
			System.err.println(e); 
		}
		//stampo l'output di ipknot
		//System.out.println(output);
		return output;
	}

	public String getipknotOutput(File sequenceFile) {
		Process proc;
		String ipknot= "/workspace/ipknot-0.0.2-x86_64-linux/ipknot";

		String output="";

		try {	
			
			proc = Runtime.getRuntime().exec(ipknot +" "+ sequenceFile.getAbsolutePath()+ " -b" );

			// Read the output
			BufferedReader reader =  new BufferedReader(new InputStreamReader(proc.getInputStream()));
			StringBuilder sb = new StringBuilder();

			String line = "";
			while((line = reader.readLine()) != null) {
				sb.append(line + System.getProperty("line.separator"));
			}

			output= sb.toString();
			reader.close();

			proc.waitFor();

		} catch (IOException e) {
			e.printStackTrace();
			System.err.println(e); 
		} catch (InterruptedException e) { 
			e.printStackTrace();
			System.err.println(e); 
		}
		//stampo l'output di ipknot
		//System.out.println(output);
		return output;
	}

	
	private void writeOutputFile(String output) {
		
		File outputFile= new File("PKB2.bpseq");
		
		PrintWriter writer=null;
		try {
			writer = new PrintWriter(outputFile);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		writer.println(output);
		writer.close();
		
	}
	
	
	//Test class
	//public static void main(String[] args) throws IOException, InterruptedException{
	//	String output = new IpknotPrediction().getipknotOutput(new File("/workspace/ipknot-0.0.2"));
	//	new IpknotPrediction().writeOutputFile(output);
	//	System.out.println(output);
	//}
	
    
    
}
