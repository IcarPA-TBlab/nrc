package root.nrc_workspace.src;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.util.HashMap;
import java.util.Map;

/**
 * This Class assign to each vector (representing ncRNA sequence) its proper class, stored in hashIdType file.
 * 
 * @author Fiannaca
 *
 */
public class SeqClassMerge {

	
	public static void main(String[] args) throws IOException, ClassNotFoundException {
			
		String vector_sequence_file= args[0]; //es.: ./data/test/myTestSequence.txt
		String hash_table_file= args[1];      //es.: ./data/test/hashIdType
		
		FileWriter outfile = new FileWriter(vector_sequence_file.split(".temp")[0]+".txt");
		PrintWriter out = new PrintWriter(new BufferedWriter(outfile));
		
		//rebuild hash map from file
		FileInputStream fileHash = new FileInputStream(hash_table_file);
        ObjectInputStream in = new ObjectInputStream(fileHash);
        Map<String, String> hashId2Type = (HashMap) in.readObject();


		//for each row, read the frist element and find its class in HashMap
		try(BufferedReader br = new BufferedReader(new FileReader(vector_sequence_file))) {
		    for(String line; (line = br.readLine()) != null; ) {
		        String seq_label= line.split(",")[0];
		        
		        String ncRNAclass= hashId2Type.get(seq_label);
		        out.println(line+","+ncRNAclass);
		    }
		}
		out.close();
	}
}
