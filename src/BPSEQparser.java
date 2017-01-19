package root.nrc_workspace.src;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class BPSEQparser {
	
	File input;
	File output;
	BufferedReader inputReader = null;
	
	
	
	
	/**
	 * 
	 * @param pathFile - directory che contiene i file bpseq
	 */
	private void parseFiles(String pathFile) {
		File listFile[] = (new File(pathFile)).listFiles();
		if (listFile != null) {
			for (int i = 0; i < listFile.length; i++) {
				if (listFile[i].getName().endsWith(".bpseq")) {
					parse(listFile[i].getAbsolutePath());
				}
			}
		}
	}
	
	
	
	/**
	 * 
	 * @param inputFile - file bpseq da convertire in nel
	 * @param outputFile
	 */
	private void parse(String inputFile) {

		String inputRow = null;
		String graphName= "";
		int nodes=0;
		ArrayList<String> rowLines= new ArrayList<String>();

		input = new File(inputFile);
		String outputName= input.getAbsolutePath().split("[.]")[0];
		outputName= outputName.concat(".nel");
		
		//output = new File(outputName.concat(".nel"));

		graphName= input.getName().split("[.]")[0];

		try {
			//(STEP 1) Save vertices  /////////////////////////////////////
			inputReader = new BufferedReader(new FileReader(input));


			while( (inputRow = inputReader.readLine())!=null ){
				if ( !inputRow.startsWith("#") && (!inputRow.equals("")) ){
					nodes++;
					String[] currentRow= inputRow.split("\\W+");

					rowLines.add("v "+ currentRow[0] + " " + currentRow[1]);
					//System.out.println("v "+ currentRow[0] + " " + currentRow[1]);
				}
			}				

			//(STEP 2) Save consecutive edges  ////////////////////////////
			String node1="";
			String node2="";
			inputReader = new BufferedReader(new FileReader(input));
			inputReader.readLine(); //salto la prima riga
			
			node1 = inputReader.readLine().split("\\W+")[0];

			while( (inputRow = inputReader.readLine())!=null ){
				if ( !inputRow.startsWith("#") && (!inputRow.equals("")) ){
					String[] currentRow= inputRow.split("\\W+");
					node2= currentRow[0];
					rowLines.add("e " + node1 + " " + node2 + " -");
					//System.out.println("e " + node1 + " " + node2 + " -");
					node1= node2;
				}
			}	


			//(STEP 3) Save other edges	///////////////////////////////////
			inputReader = new BufferedReader(new FileReader(input));
			// set used to delete duplicates
			Set<String> hs = new HashSet<String>();
			while( (inputRow = inputReader.readLine())!=null ){
				if ( !inputRow.startsWith("#") && (!inputRow.equals("")) ){
					String[] currentRow= inputRow.split("\\W+");
					if ( !(currentRow[2].equals("0")) ){	
						//print edge with ordered nodes
						if ( Integer.valueOf(currentRow[0]) < Integer.valueOf(currentRow[2]) ){
							hs.add("e " + currentRow[0] + " " + currentRow[2] + " -");
							//System.out.println("e " + currentRow[0] + " " + currentRow[2] + " -");
						}
						else {
							hs.add("e " + currentRow[2] + " " + currentRow[0] + " -");
							//System.out.println("e " + currentRow[2] + " " + currentRow[0] + " -");
						}
					}
				}
			}
			rowLines.addAll(hs);

			//(STEP 4) Save end lines ////////////////////////////////////
			rowLines.add("g "+graphName);
			rowLines.add("x 0");
			//System.out.println("g g");
			//System.out.println("x 0");

			//(STEP 5) Write output file	//////////////////////////////////
			PrintWriter writer = new PrintWriter(outputName);
			for (int i=0; i <rowLines.size(); i++){
				writer.println(rowLines.get(i));
			}
			writer.close();
			inputReader.close();
			


		} catch (FileNotFoundException e) {	e.printStackTrace();
		} catch (IOException e) { e.printStackTrace();
		}

	}
	
	
	/**
	 * 
	 * @param pathFile - percorso che contiene i file da unire
	 * @param estensione - estensione dei file da unire (i.e., "nel")
	 * @throws IOException
	 * 
	 */
	public void mergeFiles(File pathFile, String estensione) throws IOException {

		String outputFile= (pathFile.getAbsolutePath()).concat("/merged."+estensione); 
		
		
		Path outPath= Paths.get(outputFile);
		
		File listFile[] = pathFile.listFiles();
		if (listFile != null) {
			for (int i = 0; i < listFile.length; i++) {
				if (listFile[i].getName().endsWith(estensione)) {
					System.out.println("Merge NELlist file: "+ listFile[i]);
					List<String> lines= Files.readAllLines(Paths.get(listFile[i].getAbsolutePath()),StandardCharsets.UTF_8);
					Files.write(outPath, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
					lines.removeAll(lines);
					lines.add("");
					Files.write(outPath, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
					
					
				}
			}
		}
	}
	
	
	
	
	
	
	
	
	public static void main(String[] args) {
	
		//args[0] = input BPSEQ file
		//new BPSEQparser().parseFiles("/home/giacalone/ncRNA/dataset_test");
	    String path=args[0];
		
		System.out.println(path);
		//new BPSEQparser().parseFiles("/home/giacalone/ncRNA/dataset_test/sostituzioneACGT");
		new BPSEQparser().parseFiles(path);
	try {
			
		//new BPSEQparser().mergeFiles("/home/giacalone/ncRNA/dataset_test/");
		
		new BPSEQparser().mergeFiles(new File(path),"nel");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}


	
	
	

}
