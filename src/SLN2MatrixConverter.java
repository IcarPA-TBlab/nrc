package root.nrc_workspace.src;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;


public class SLN2MatrixConverter {
	
	
	public SLN2MatrixConverter() {
		// TODO Auto-generated constructor stub
	}	

	private void createMatrix(String matrix_name,String path) throws IOException, ClassNotFoundException {
		
		String[] codesPosix;
		double[][] vals;
		
		ArrayList<SubGraphsContenuti> sequenceID = new ArrayList<SubGraphsContenuti>();	
		int dimSubGraph= 0;	
		FileWriter fileout = new FileWriter(path+"/"+matrix_name+".txt");
		PrintWriter out = new PrintWriter(new BufferedWriter(fileout));
		
		FileWriter fileout1 = new FileWriter(path+"/"+matrix_name+"_weka.csv");
		PrintWriter out1 = new PrintWriter(new BufferedWriter(fileout1));
		try{ 
			
			FileReader filein = new FileReader(path+"/out.sln");
          
			BufferedReader filebuf = new BufferedReader(filein);
       
			String nextStr;
			String[] tempStr;
			nextStr = filebuf.readLine();     // legge la prima riga del file, che scartiamo perche' contiene solo la stringa "ids:list"
			nextStr = filebuf.readLine();	
			while (nextStr != null){
				String[] row=nextStr.split(":");
				String subgraphID= row[0];
				tempStr = row[1].split(",");
				//prendo i sequenceID e creo un oggetto SubGraphsContenuti ed inserisco il subGraphs che sto guardando
				for(int i = 0; i < tempStr.length; i++){            	
					int elem = isConteinedIn(tempStr[i], sequenceID);
					if ( elem >= 0 ){		//se la sequenceID gia' figura nella lista, il subGraphs viene inserito in coda
						//TODO sicuramente puo essere alleggerito
						SubGraphsContenuti sequence = (SubGraphsContenuti)sequenceID.get(elem);
						sequence.addSubGraph( subgraphID);
						sequenceID.set(elem, sequence);
						//controlla se ha inserito il valore nell'ArrayList di subGraphs
						//System.out.println("il nuovo vettore comp e': ");
					}
					else{
						SubGraphsContenuti sequence = new SubGraphsContenuti(tempStr[i]);
						sequence.addSubGraph( subgraphID );   // aggiunge questo alla lista dei subGraphs 
						sequenceID.add(sequence);
//						System.out.println("Ho aggiunto a: "+tempStr[i] +", il subGraphs: "+tempStr[0]); 
					}            	
				}
            
				nextStr = filebuf.readLine(); // legge la prossima riga       
				dimSubGraph++;    //tengo il conto del numero dei composti, ovvero delle righe del file
			}
			filebuf.close();  // chiude il file 
			//out.close();      // chiude il file di scrittura  
		}
		catch (FileNotFoundException e) {
			System.out.println("FileNotFound :"+e);
		}
		
		     
		//ora deve prelevare la dimesione dell'array di double che diventera' la matrice trasposta.
		//Innanzitutto misuro la lunghezza dell'ArrayList di composti x sapere quanti sono. 
		//I frammenti erano il numero delle righe del file
		int dimSequenceID = sequenceID.size(); // --- OK
		//System.out.println( "Il numero delle sequenze e': " + dimSequenceID );
		System.out.println( "INFO: Feature model is composed of "+dimSubGraph+" sub-graphs." );

//		ordina la lista dei composti in ordine crescente
		Collections.sort(sequenceID);
		
		
		
		
		vals= new double[dimSequenceID][dimSubGraph];
		codesPosix = new String[dimSequenceID]; //lista ordinata dei codici dei composti
		
		for (int i = 0; i < dimSequenceID; i++){
    	
//    		double compDouble;
			SubGraphsContenuti unSubGraph = (SubGraphsContenuti) sequenceID.get(i);
//    		compDouble = Double.valueOf(unFram.getComp()).doubleValue();
			ArrayList<String> unVett = unSubGraph.getSubGraph();
//			System.out.println("sequenza= "+unSubGraph.getSequenceID());
			codesPosix[i] = unSubGraph.getSequenceID();
			String[] strVect = (String[])unVett.toArray( new String[ unVett.size() ] );
//			System.out.println("la lunghezza del vettore corrente e': " + strVect.length);
			for (int s=0; s < strVect.length; s++)
				//System.out.println("strVect["+s+"]= "+strVect[s] );
//			System.out.println("Il codice corrente e': " + codesPosix[i]+", nella posizione "+i);
			for (int j = 0; j < strVect.length; j++){
				String tempSubGraph = strVect[j];
//				System.out.println("Il sottografo e' :"+tempSubGraph);
				int posSubGraph = Integer.valueOf(tempSubGraph);
//				System.out.println(posFragm);
				
				vals[i][posSubGraph - 1]= 1;    		
			}
    	   	
		}
		
		FileInputStream fileIn = new FileInputStream(path+"/dataset_test/hashIdType");
		
        ObjectInputStream in = new ObjectInputStream(fileIn);
        Map<String, String> hashId2Type = (HashMap) in.readObject();
        
       	for (int i=0;i<=dimSubGraph;i++){
       		if(i==dimSubGraph) out1.print("F"+i);
       		else out1.print("F"+i+",");
       	}
       	
       	out1.println();
        
		//print matrix
		for (int i=0; i < vals.length; i++){
			out.print(codesPosix[i]+",");
			for (int j=0; j < vals[0].length; j++){
				out.print(vals[i][j] + ",");
				out1.print(vals[i][j] + ",");
			}
			
			out.println(hashId2Type.get(codesPosix[i]));
			out1.println(hashId2Type.get(codesPosix[i]));
			//out.println();
		}

		out.close();      // chiude il file di scrittura
		out1.close();

	}
	
	
	
	
	// It compares if the fragment is contained in the compounds' list
	private int isConteinedIn(String str, ArrayList comps) { 
		
		for (int i = 0; i < comps.size(); i++){
			SubGraphsContenuti temp = (SubGraphsContenuti)comps.get(i);
			if ( temp.getSequenceID().compareTo(str) == 0 ) 
				return (i);
		}
		return(-1);
	}
	
	
	
	
	public static void main(String[] args) throws IOException {
	
		String matrix_name=args[0];
		String path =args[1];
		try {
			new SLN2MatrixConverter().createMatrix(matrix_name,path);
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	
	
	
}
