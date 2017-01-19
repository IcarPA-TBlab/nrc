package root.nrc_workspace.src;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream.GetField;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import moss.Miner;


/**
 * Questa classe confronta il .nel ottenuto dal MoSS della sequenza di test 
 * con il .nel del modello MoSS addestrato.
 * Il risultato sara' il vettore di feature della sequenza di test.
 * 
 * 
 * @author Fiannaca
 *
 */
public class CreateVectorFromNELfile {

	ArrayList<ArrayList<String>> adjListSet= new ArrayList<ArrayList<String>>();



	private void getAdjListFromGraph(String filename) throws FileNotFoundException {

		FileReader mytest= new FileReader(filename);
		ArrayList<String> nt= new ArrayList<String>(); 
		int[][] adjMatrix = null; 
		ArrayList<String> adjList= new ArrayList<String>();
		adjListSet= new ArrayList<ArrayList<String>>();
		boolean isEdgeReading= false;

		BufferedReader filebuf = new BufferedReader(mytest);


		try{
			String nextStr;
			nextStr = filebuf.readLine(); 
			while (nextStr != null){
				String[] strArray = nextStr.split(" ");
				if(strArray[0].equals("n") ){
					//conserva la lettera nel'array nt
					nt.add(strArray[2]);
					//System.out.println(strArray[2]);
				}
				else if( strArray[0].equals("e") ){
					if (isEdgeReading== false){  //se leggo il primo edge, creo la matrice di adiacenza
						adjMatrix = new int[nt.size()][nt.size()];
						for (int i=0; i < nt.size(); i++){
							for (int j=0; j < nt.size(); j++){
								adjMatrix[i][j]=0;
							}
						}
						isEdgeReading= true;
					}
					adjMatrix[Integer.valueOf(strArray[1])-1][Integer.valueOf(strArray[2])-1]= 1;
					adjMatrix[Integer.valueOf(strArray[2])-1][Integer.valueOf(strArray[1])-1]= 1;	
				}
				else if( strArray[0].equals("g") ){ //memorizza l'adjList e reset parameters
					String mainNode="";  //contiene il vertice di riferimento della lista di nucleotidi che formeranno la stringa
					String temp="";
					for (int i=0; i < nt.size(); i++){
						mainNode= nt.get(i);
						temp="";
						//System.out.println(nt.get(i)); 
						for (int j=0; j < adjMatrix[0].length; j++){
							if (adjMatrix[i][j] == 1){
								temp= temp + "" + nt.get(j);
							}
						}
						char[] sortString= temp.toCharArray();
						Arrays.sort(sortString); //ordino la lista di nodi che sono adiacenti al main node
						adjList.add( mainNode + String.valueOf(sortString) );
					}
					Collections.sort(adjList);  //ordina gli elementi nell'arraylist
					adjListSet.add(adjList);
					//System.out.println(adjList.toString());      /////////stampa di controllo
					isEdgeReading= false;   /////////reset dei parametri
					nt.clear();
					adjList= new ArrayList<String>();
					adjMatrix = null;
				}		
				nextStr = filebuf.readLine();	
			}

			//////////////// STAMPE DI TEST //////////////////////////
			//			for (int i=0; i < adjMatrix.length; i++){
			//				System.out.print(nt.get(i)+"\t");
			//			}
			//			System.out.println();
			//			printAdjMatrix(adjMatrix);
			/////////////////////////////////////////////////////////

			//			for (int i=0; i < nt.size(); i++){
			//				System.out.print(nt.get(i)+"->");
			//				for (int j=0; j < adjMatrix[0].length; j++){
			//					if (adjMatrix[i][j] == 1){
			//						System.out.print(nt.get(j)+"\t");
			//					}
			//				}
			//				System.out.println();
			//			}
			////////////////////////////////////////////////////////
			//System.out.println( adjListSet.get(1).equals(adjListSet.get(2)) );	
			//System.out.println( adjListSet.toString() );
		}
		catch (IOException e) {
			e.printStackTrace();
		}

	}



//
//
//	private void printAdjMatrix(int[][] adjMatrix) {
//		for (int i=0; i < adjMatrix.length; i++){
//			for (int j=0; j < adjMatrix[0].length; j++){
//				System.out.print( adjMatrix[i][j] + "\t");
//			}
//			System.out.println();
//		}
//
//	}


	public ArrayList<ArrayList<String>> getAdjListSet() {
		return adjListSet;
	}


	/**
	 * Esegue tanti MoSS quanto e' il range dei substructure size
	 * @param string - filename
	 * @param i - min substructure size
	 * @param j - max substructure size
	 * @return
	 * @throws IOException 
	 */
	private String getMOSSfragments(String filename, int min, int max) throws IOException {
		
		Path p = Paths.get(filename);
		String myInputName = p.getFileName().toString(); //elimino il percorso
		myInputName = filename.split(".nel")[0];  //Elimino l'estensione
		//String myInputPath= new File(filename).getAbsolutePath();		

		String myOut= myInputName+"_out.nel";
		Path outPath= Paths.get(myOut);
		
		//svuota il file
		PrintWriter writer = new PrintWriter( new File(myOut) );
		writer.print("");
		writer.close();
		
		for (int i = min ; i <= max; i++){
			runMoss(filename, i, i);
		}
		for (int i = min ; i <= max; i++){
			File filein = new File(myInputName+"_out_part"+i+".nel");
			List<String> lines= Files.readAllLines(Paths.get(filein.getAbsolutePath()),StandardCharsets.UTF_8);
			Files.write(outPath, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
			lines.removeAll(lines);
			lines.add("");
			Files.write(outPath, lines, StandardCharsets.UTF_8, StandardOpenOption.CREATE, StandardOpenOption.APPEND);
			
		}
		return myOut;
	}


	/**
	 * run MOSS algorithm. Output is not restricted to closed substructures.
	 * 
	 * @param inputFile
	 * @param maxSupport
	 * @param minSupport
	 */
	private void runMoss(String inputFile, int maxSupport, int minSupport) {

		//Path p = Paths.get(inputFile);
		String myInputName = inputFile.split(".nel")[0];  //Elimino l'estensione
		//String myInputPath= new File(inputFile).getAbsolutePath();		
	
		String[] boo= new String[]{"-m"+minSupport,"-n"+maxSupport,"-C","-inel",inputFile,"-onel",myInputName+"_out_part"+minSupport+".nel","-fsln",myInputName+"_out_part"+minSupport+".sln"};
		
		Miner moss= new Miner();
		try {
			moss.init(boo);
			
			moss.run();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	
	

	public static void main(String[] args) throws FileNotFoundException {

		String nel_input_file= args[0];
		String feature_model_file= args[1];
		int max_moss= Integer.parseInt(args[2]);
		int min_moss= Integer.parseInt(args[3]);

		Path p = Paths.get(nel_input_file);
		String myInputName = p.getFileName().toString(); //elimino il percorso
		String myInputPath= nel_input_file.split(".nel")[0];  //Elimino l'estensione
	
		String ncRNA_sequence_output= myInputPath+"_out_matrix.part";
	    File outfile = new File(ncRNA_sequence_output);
	    FileWriter writer;
		
		CreateVectorFromNELfile adjReferenceSet= new CreateVectorFromNELfile();
		CreateVectorFromNELfile adjTestSet= new CreateVectorFromNELfile();
		
		ArrayList<Integer> features= new ArrayList<Integer>();
		String subgraphsTestSet= "";
		try {
			subgraphsTestSet = adjTestSet.getMOSSfragments(nel_input_file,min_moss,max_moss);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		adjReferenceSet.getAdjListFromGraph(feature_model_file);
		ArrayList<ArrayList<String>> referenceSet = adjReferenceSet.getAdjListSet();
		
		adjTestSet.getAdjListFromGraph(subgraphsTestSet);
		ArrayList<ArrayList<String>> mySet = adjTestSet.getAdjListSet();
		
		
		
		//System.out.println("mySet.size()= "+ mySet.size());
		//System.out.println("referenceSet.size()= "+ referenceSet.size());
		
		int count=0;
		for (int i=0; i< mySet.size(); i++){
			for (int j=0; j < referenceSet.size(); j++){
				if ( mySet.get(i).equals(referenceSet.get(j)) ){
					//System.out.println("sottografi uguali= "+ (i+1) + "," + (j+1));
					features.add( j );
					j=  referenceSet.size();
					count++;
					
				}
			}
		}
		//System.out.println(features.size());
		//for (int i=0; i < features.size(); i++){
		//	System.out.print(features.get(i));		
		//}
		
		int[] inputValues= new int[referenceSet.size()];
		for (int i=0; i < inputValues.length; i++){
			inputValues[i]=0;
		}
		
		for (int i=0; i < features.size(); i++){
			inputValues[features.get(i)]=1;
		}
	    
	    
	    try {
	        writer = new FileWriter(outfile, false);
	        PrintWriter printer = new PrintWriter(writer);
			String seq_name= myInputName.split(".nel")[0];
	        printer.append(seq_name); //etichetta del vettore
	        for (int i=0; i < inputValues.length; i++){
	        	printer.append(","+inputValues[i]);	
			}
	        //printer.append("10"); //test_class
			printer.append("\n");
	        printer.close();
	        
	    } catch (IOException e) {
	        e.printStackTrace();
	    }


	}



}
